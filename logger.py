"""Create a logging function for each module to use."""
import logging


def get_logger(mod_name: str, log_name: str = "dash") -> logging.Logger:
    """Retun logger object."""
    log_format = "%(asctime)s: %(name)s: %(levelname)s: %(message)s"
    # create logger
    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter(log_format)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger
