import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
from evse_controller.utils.config import config
from evse_controller.utils.paths import get_log_dir

def setup_logging():
    """Setup logging configuration"""
    # Get configured console level
    console_level = getattr(logging, config.get('logging.console_level', 'WARNING').upper())
    file_level = getattr(logging, config.get('logging.file_level', 'INFO').upper())
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s.%(msecs)03d %(levelname)8s - %(message)s',
        datefmt='%H:%M:%S'
    ))
    console_handler.setLevel(console_level)

    logger = logging.getLogger('evse_controller')
    logger.setLevel(logging.DEBUG)  # Keep root logger at DEBUG to allow all potential levels
    logger.addHandler(console_handler)

    # Get log directory from paths utility
    log_dir = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d %(levelname)8s %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler
    log_file = log_dir / f"{config.get('logging.file_prefix', 'evse')}.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=int(config.get('logging.max_bytes', 10485760)),
        backupCount=int(config.get('logging.backup_count', 30))
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(file_level)

    logger.addHandler(file_handler)
    
    return logger

# Convenience functions
def debug(msg): logging.getLogger('evse_controller').debug(msg)
def info(msg): logging.getLogger('evse_controller').info(msg)
def warning(msg): logging.getLogger('evse_controller').warning(msg)
def error(msg): logging.getLogger('evse_controller').error(msg)
def critical(msg): logging.getLogger('evse_controller').critical(msg)
