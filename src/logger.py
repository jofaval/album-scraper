# create console handler and set level to debug
import logging

# pseudo-singleton experience/instance
static_logger: logging.Logger


def get_logger(level: int = logging.NOTSET) -> logging.Logger:
    """Generates the appropriate logger"""
    global static_logger

    if static_logger:
        return static_logger

    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s;%(levelname)s;%(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    logger = logging.getLogger("webscrapper")
    logger.setLevel(level)
    logger.addHandler(ch)

    static_logger = logger
    return static_logger
