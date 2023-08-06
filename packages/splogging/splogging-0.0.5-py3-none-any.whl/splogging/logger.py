"""Provide an easy and flexible way to quickly activate logging in your script."""

import logging.handlers
import sys
from os import PathLike
from typing import Optional, Union


def setup_logging(  # pylint: disable=too-many-arguments
    name: Optional[str] = None,
    filename: Union[str, PathLike] = "./splog.log",
    when: str = "W0",
    backup_count: int = 0,
    file_level: Optional[str] = "DEBUG",
    file_format: Optional[
        str
    ] = "%(asctime)s %(levelname)s %(process)d %(filename)s %(funcName)s %(message)s",
    file_log_datefmt: str = "%Y-%m-%d %H:%M:%S",
    console_level: Optional[str] = "INFO",
    console_format: Optional[str] = "%(asctime)s [%(levelname)-8s] %(message)s",
    console_log_datefmt: str = "%H:%M:%S",
) -> logging.Logger:
    """Initiate customised logging.

    Parameters:
    - name: Can be left empty. Useful only when creating multiple, separate loggers.
    - filename: Path and name of logfile.
    - when: Defines when to rotate the log file. Check docs.python.org for more info (see link below).
    - backup_count: Number of backups to keep (set to 0 to keep all rotated logs).
    - file_level: Save log messages that have this or a higher level. Set to None to disable logging to file.
    - file_format: Format of message saved to file. Check docs.python.org for more info.
    - file_log_datefmt: Format of timestamp in the log message, saved to file.
    - console_level: Display log messages that have this or a higher level. Set to None to disable logging to console.
    - console_format: Format of message, displayed in the console. Check docs.python.org for more info.
    - console_log_datefmt: Format of timestamp in the message, displayed in the console.

    References:
    - Handler: https://docs.python.org/3/library/logging.handlers.html?highlight=logging#timedrotatingfilehandler
    - Formatter: https://docs.python.org/3/library/logging.html#formatter-objects
    """
    script_logger = logging.getLogger(name)
    script_logger.setLevel(logging.DEBUG)
    if file_level is not None:
        try:
            file_log_handler = logging.handlers.TimedRotatingFileHandler(
                filename=filename, when=when, backupCount=backup_count,
            )
            file_log_handler.setLevel(file_level.upper())

            file_log_format = logging.Formatter(
                fmt=file_format, datefmt=file_log_datefmt,
            )
            file_log_handler.setFormatter(file_log_format)
            script_logger.addHandler(file_log_handler)
            script_logger.propagate = False
        except PermissionError:
            script_logger.error(f"{sys.exc_info()[1]} <PermissionError>")
            sys.exit()
        except AttributeError:
            script_logger.error(f"{sys.exc_info()[1]} <AttributeError>")
            sys.exit()
        except FileNotFoundError:
            script_logger.error(f"{sys.exc_info()[1]} <FileNotFoundError>")
            sys.exit()
        except ValueError:
            script_logger.error(f"{sys.exc_info()[1]} <ValueError>")
            sys.exit()
    if console_level is not None:
        console_log_handler = logging.StreamHandler()
        console_log_handler.setLevel(console_level.upper())
        console_log_format = logging.Formatter(
            fmt=console_format, datefmt=console_log_datefmt
        )
        console_log_handler.setFormatter(console_log_format)
        script_logger.addHandler(console_log_handler)
    return script_logger
