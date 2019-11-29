import logging
import pathlib
from typing import Union


def get_logger(
    name: Union[pathlib.Path, str] = None, file: Union[pathlib.Path, str] = None
) -> logging.Logger:
    """Return a logger with the specified name, logging to the specified
       file. If name is not specified default to the name of the calling
       file. If file is not specified log to the main app log"""
    name = str(name) if name else __name__
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '<p class="traceback">%(name)-12s: %(levelname)-8s %(message)s</p>'
        '<pre class="traceback">%(traceback)s</pre>'
    )

    file = file if file else "app.html"
    fh = logging.FileHandler(file)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger
