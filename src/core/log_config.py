import logging
import os

LOG_LEVEL_NAME: str = "LOG_LEVEL"


def get_log_level() -> int:
    level_name: str | None = os.getenv(LOG_LEVEL_NAME)
    if level_name is None:
        # Fallback to info level logging in case unspecified
        level_name = "info"
    level_map = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }
    return level_map.get(level_name.strip().lower(), logging.INFO)


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("albot")
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(get_log_level())
    logger.propagate = False
    return logger
