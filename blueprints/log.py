import logging
import logging.config
import yaml
from pathlib import Path

class log_type:
    api = "api"
    web = "web"
    general = "general"

PROJECT_ROOT = Path.cwd()

class RelativePathFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            record.relativepath = Path(record.pathname).relative_to(PROJECT_ROOT)
        except ValueError:
            record.relativepath = record.pathname
        return True

# set up logger configuration for api log file 
def setup_logger(log_type: str) -> logging.Logger:
    
    try:
        api_log_dir = PROJECT_ROOT / 'blueprints' / 'api' / 'logs'
        web_log_dir = PROJECT_ROOT / 'blueprints' / 'website' / 'logs'
        general_log_dir = PROJECT_ROOT / 'blueprints' / 'logs'
        
        # ensure the logs directory exists if not create it
        api_log_dir.mkdir(parents=True, exist_ok=True)
        web_log_dir.mkdir(parents=True, exist_ok=True)
        general_log_dir.mkdir(parents=True, exist_ok=True)
        
        # load logging configuration from yaml file
        config_path = PROJECT_ROOT / 'blueprints' / 'config.yaml'
        
        if not config_path.exists():
            raise FileNotFoundError(f"Logging config file not found: {config_path}")
        
        with config_path.open('r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        
        # add relative path filter to the api logger
        logger = logging.getLogger(log_type)
        relative_path_filter = RelativePathFilter()
        logger.addFilter(relative_path_filter)
        
        return logger
        
    except Exception as e:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
        )
        fallback_logger = logging.getLogger('fallback')
        fallback_logger.error(f"Failed to setup logger {log_type}: {e}")
        return logging.getLogger(log_type)