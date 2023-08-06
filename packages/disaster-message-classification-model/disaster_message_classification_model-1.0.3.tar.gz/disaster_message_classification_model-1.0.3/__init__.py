import logging
from disaster_messaging_classification_model.config import config, logging_config
from disaster_messaging_classification_model import (
    model,
    features,
    utils,
    visualizations,
)
import poetry_version


# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_config.get_console_handler())
logger.propagate = False

__version__ = poetry_version.extract(source_file=__file__)
