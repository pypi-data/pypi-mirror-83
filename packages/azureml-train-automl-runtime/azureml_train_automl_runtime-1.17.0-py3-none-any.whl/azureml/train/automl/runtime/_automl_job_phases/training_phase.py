# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Any, cast, Dict, Optional

from azureml.automl.core.shared import log_server
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.core import Run
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.run import AutoMLRun
from azureml.train.automl.runtime._automl_job_phases import TrainingIteration
from azureml.train.automl.runtime._azureautomlruncontext import AzureAutoMLRunContext
from azureml.train.automl.runtime._task_queue import QueueClient

logger = logging.getLogger(__name__)


class TrainingPhase:
    """Iteration that outputs a fully trained ML model."""

    @staticmethod
    def run(
        automl_parent_run: Run,
        automl_settings: AzureAutoMLSettings,
        dataset: DatasetBase,
        feature_configs: Optional[Dict[str, Any]],
        onnx_cvt: Optional[OnnxConverter],
        remote: bool,
        task_queue: QueueClient
    ) -> None:
        """
        TrainPhase
        Run training iterations until the experiment exit status is reached
        :param automl_parent_run: Parent run context
        :param automl_settings: AutoMl settings for current run
        :param dataset: Dataset used for the run
        :param feature_configs: Feature configuration dictionary for AutoML features.
        :param onnx_cvt: ONNX converter if run requires ONNX compatible model
        :param remote: Whether run is remote run or not
        :param task_queue: Azure Queue client storing task info
        :return:
        """

        task_from_queue = task_queue.get_next_task()

        while task_from_queue is not None and not task_from_queue.task.is_experiment_over:
            try:
                child_run = automl_parent_run.child_run(run_id=task_from_queue.task.childrun_id)
                log_server.update_custom_dimension(run_id=child_run.id)
                training_percent = float(task_from_queue.task.training_percent or 100)

                fit_output = TrainingIteration.run(
                    automl_parent_run=automl_parent_run,
                    automl_run_context=AzureAutoMLRunContext(child_run),
                    automl_settings=automl_settings,
                    dataset=dataset,
                    feature_configs=feature_configs,
                    onnx_cvt=onnx_cvt,
                    pipeline_id=task_from_queue.task.pipeline_id,
                    pipeline_spec=task_from_queue.task.pipeline_spec,
                    remote=remote,
                    training_percent=training_percent
                )

                if fit_output.errors:
                    for fit_exception in fit_output.errors.values():
                        if fit_exception.get("is_critical"):
                            exception = cast(BaseException, fit_exception.get("exception"))
                            raise exception.with_traceback(exception.__traceback__)

            except Exception as e:
                logger.info("Error while running child iteration {}.".format(child_run.id))
                child_run.fail(e)

            # Get next pipeline from queue
            task_from_queue = task_queue.get_next_task()
