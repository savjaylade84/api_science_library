import logging
import logging.config
import yaml
import os 

# set up logger configuration for api log file 
def setup_logger() -> logging.Logger:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config_log.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    return logging.getLogger("api")