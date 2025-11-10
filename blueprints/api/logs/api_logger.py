import logging
import logging.config
import yaml
import os 

PROJECT_ROOT = os.getcwd()

class RelativePathFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            record.relativepath = os.path.relpath(record.pathname, PROJECT_ROOT)
        except ValueError:
            record.relativepath = record.pathname
        return True

# set up logger configuration for api log file 
def setup_logger() -> logging.Logger:
    
    # ensure the logs directory exists if not create it
    os.makedirs(os.path.join(PROJECT_ROOT, 'logs'), exist_ok=True)
    
    # load logging configuration from yaml file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config_log.yaml')
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    
    # add relative path filter to the api logger
    logger = logging.getLogger("api")
    for handler in logger.handlers:
        handler.addFilter(RelativePathFilter())

    return logger
