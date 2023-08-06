# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Download and load model explanation configuration."""
from typing import Any, Dict
import json
import logging
import os
import time

from azureml.automl.core._downloader import Downloader
from azureml.automl.core.shared import logging_utilities


RawFeatureImportanceParameter = "RawGlobalAndLocal"


logger = logging.getLogger(__name__)


class AutoMLModelExplanationConfig:
    """Holder for model explanation configurations."""

    CONFIG_DOWNLOAD_PREFIX = "https://aka.ms/automl-resources/configs/"
    CONFIG_DOWNLOAD_FILE = "model_explanation_config_v1.0.json"
    REMOTE_CONFIG_DOWNLOAD_FILE = "model_explanation_config_v1.1.json"

    DEFAULT_CONFIG_PATH = "../model_explanation_config_v1.0.json"

    def get_config(self, is_remote: bool = False) -> Dict[str, Any]:
        """Provide configuration."""
        file_path = None
        try:
            if is_remote:
                file_path = Downloader.download(self.CONFIG_DOWNLOAD_PREFIX,
                                                self.REMOTE_CONFIG_DOWNLOAD_FILE, os.getcwd(),
                                                prefix=str(time.time()))
            else:
                file_path = Downloader.download(self.CONFIG_DOWNLOAD_PREFIX, self.CONFIG_DOWNLOAD_FILE,
                                                os.getcwd(), prefix=str(time.time()))
            if file_path is None:
                # bail out, the enclosing block with catch the exception, proceeding with defaults
                msg = "Failed to get the ModelExplanation configuration file."
                logger.error(msg)
                raise ValueError(msg)

            with open(file_path, 'r') as f:
                model_exp_config = json.load(f)  # type: Dict[str, Any]
                logger.debug("Successfully downloaded the model explanations configuration from the remote.")
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            logger.debug("Error encountered reading model explanation configuration. Falling back to default "
                         "configuration")
            model_exp_config = self.default()

        if file_path is not None:
            os.remove(file_path)
        return model_exp_config

    def default(self) -> Dict[str, Any]:
        """Return the default back up configuration."""
        default_config_path = os.path.abspath(os.path.join(__file__, self.DEFAULT_CONFIG_PATH))
        with open(default_config_path, "r") as f:
            result = json.loads(f.read())  # type: Dict[str, Any]
            logger.debug("Read model explanations config from SDK.")
            return result
