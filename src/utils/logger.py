import json
import logging
import logging.config
import os

def setup_logging(default_path='../config/logging_config.json', default_level=logging.INFO):
    """Setup logging configuration"""
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        logging.warning("Logging config file not found! Using basic config.")

logger = logging.getLogger(__name__)
