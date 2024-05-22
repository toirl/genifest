import logging
from typing import Optional

import structlog

_logger: Optional[structlog.stdlib.BoundLogger] = None

verbosity2loglevel = {0: logging.ERROR, 1: logging.WARN, 2: logging.INFO, 3: logging.DEBUG}


def setup_logging(verbosity: int = 0) -> structlog.stdlib.BoundLogger:
    log_level = verbosity2loglevel.get(verbosity, logging.NOTSET)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )

    global _logger
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    _logger = logger
    return logger


def get_logger() -> structlog.stdlib.BoundLogger:
    global _logger
    if _logger is None:
        return setup_logging()
    else:
        return _logger
