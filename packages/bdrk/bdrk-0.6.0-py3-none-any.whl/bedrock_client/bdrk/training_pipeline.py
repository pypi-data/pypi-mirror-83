import logging
from contextlib import AbstractContextManager
from typing import Mapping, Optional

from bedrock_client.exceptions import BedrockClientNotFound
from bedrock_client.utils import check_param
from bedrock_client.vars import Constants
from spanlib.infrastructure.kubernetes.env_var import BEDROCK_ENVIRONMENT_ID, BEDROCK_PIPELINE_ID
from spanlib.types import PipelineRunStatus

from .. import bdrk

_logger = logging.getLogger(Constants.MAIN_LOG)


class RunContext(AbstractContextManager):
    def __init__(
        self, pipeline_id: str, environment_id: str, model_id: Optional[str] = None,
    ):
        """Initialize the run context, register the necessary variables
        """
        self.pipeline_id = pipeline_id
        self.environment_id = environment_id
        self.model_id = model_id
        self.run_id = None

    def __enter__(self):
        """Enter the run context, register it with the bedrock_client
        """
        if bdrk.bedrock_client is None:
            raise BedrockClientNotFound
        # First, need to register the run context to block other runs
        bdrk.bedrock_client.init_run_context(self)
        try:
            # Try to get/create pipeline and start the run
            pipeline = bdrk.bedrock_client.get_or_create_training_pipeline(
                pipeline_id=self.pipeline_id, model_id=self.model_id,
            )
            run = bdrk.bedrock_client.create_training_run(
                pipeline_id=self.pipeline_id, environment_id=self.environment_id,
            )

            # Update run_id and model_id
            self.model_id = pipeline.model_id
            self.run_id = run.run.entity_number
            _logger.info(f"Run started: {self.pipeline_id}-run{self.run_id}")
        except Exception as e:
            # Clean up the run context if the run cannot start
            bdrk.bedrock_client.exit_run_context()
            raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the run context, unregister it with the bedrock_client
        """
        try:
            if exc_type is None:
                # Succeeded, creating model version
                status = PipelineRunStatus.SUCCEEDED
                model_version = bdrk.bedrock_client.create_model_version(
                    model_id=self.model_id, pipeline_id=self.pipeline_id, run_id=self.run_id
                )
                if model_version:
                    _logger.info(
                        f"Model version created: {self.model_id}-v{model_version.model_version_id}"
                    )
            elif exc_type == KeyboardInterrupt:
                status = PipelineRunStatus.STOPPED
            else:
                status = PipelineRunStatus.FAILED

            bdrk.bedrock_client.update_training_run_status(
                pipeline_id=self.pipeline_id, run_id=self.run_id, status=status,
            )
            _logger.info(f"Run {status}: {self.pipeline_id}-run{self.run_id}")
        finally:
            # Always exit the context
            bdrk.bedrock_client.exit_run_context()

        _logger.info("Run exitted")
        return True if exc_type is None else False


def start_run(
    pipeline_id: Optional[str] = None,
    environment_id: Optional[str] = None,
    model_id: Optional[str] = None,
) -> RunContext:
    """Start a run. This will return a RunContext that's to be used in a `with` statement.
    Without a `with` statement, the run_context will not start.

    Args:
        pipeline_id (Optional[str], optional): pipeline_id. Defaults to None and data
            is read from the environment variables.
        environment_id (Optional[str], optional): [description]. Defaults to None and data
            is read from the environment variables
        model_id (Optional[str], optional): [description]. Defaults to None.
    Returns:
        RunContext: the run context
    """
    pip_id = check_param(
        param_name="pipeline_id", param_var=pipeline_id, env_name=BEDROCK_PIPELINE_ID
    )
    env_id = check_param(
        param_name="environment_id", param_var=environment_id, env_name=BEDROCK_ENVIRONMENT_ID
    )
    return RunContext(pipeline_id=pip_id, model_id=model_id, environment_id=env_id)


def log_params(params: Mapping[str, str]):
    """To log training run parameters. This should be run inside a run context.

    Args:
        parameters (Mapping[str, str]): new params to be logged.
            This will override the old values in cases of duplicated keys
    """
    if bdrk.bedrock_client is None:
        raise BedrockClientNotFound
    run = bdrk.bedrock_client.update_training_run_params(
        pipeline_id=bdrk.bedrock_client.run_context.pipeline_id,
        run_id=bdrk.bedrock_client.run_context.run_id,
        parameters=params,
    )
    _logger.info(f"Params updated: {run.script_parameters}")


def log_model(path: str):
    """To log a trained model. This should be called inside a run context.

    Args:
        path (str): path to a model file or a directory.
    """
    if bdrk.bedrock_client is None:
        raise BedrockClientNotFound

    bdrk.bedrock_client.zip_and_upload_artefact(
        pipeline_id=bdrk.bedrock_client.run_context.pipeline_id,
        run_id=bdrk.bedrock_client.run_context.run_id,
        path=path,
    )
    _logger.info(f"Model logged: {path}")
