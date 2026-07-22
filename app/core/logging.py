import logging

logger = logging.getLogger(__name__)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
