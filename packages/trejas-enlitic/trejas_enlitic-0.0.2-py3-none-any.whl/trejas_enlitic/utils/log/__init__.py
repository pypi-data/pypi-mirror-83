import logging


def setup_logging(logger: logging.RootLogger) -> logging.RootLogger:
    """ Create the Logging handler for the CLI. This setups a log handler that support logging in color.

    Args:
        logger: Root logging object.
    Returns:
        logger: Root logging object.
    """
    import colorlog

    logger.handlers = []

    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s:%(lineno)d]%(reset)s %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red, bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(40)

    logger.debug("Logging level changed...")
    logger.debug(logging.root.level)

    return logger
