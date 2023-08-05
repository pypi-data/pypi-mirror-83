import inspect
import logging.handlers
import os
import sys


def setup_logging(
        filename: str = "./file.log",
        when: str = "W0",
        backup_count: int = 0,
        level_file: str = "DEBUG",
        level_console: str = "INFO",
) -> logging.getLogger:
    """Setup customised logging."""
    script_logger = logging.getLogger(__name__)
    script_logger.setLevel(logging.DEBUG)
    try:
        file_log_handler = logging.handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=backup_count,
        )
        file_log_handler.setLevel(level_file.upper())

        file_log_format = logging.Formatter(
            "%(asctime)s %(levelname)s %(process)d %(filename)s %(funcName)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
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
    console_log_handler = logging.StreamHandler()
    console_log_handler.setLevel(level_console.upper())
    console_log_format = logging.Formatter("[%(levelname)-8s] %(message)s")
    console_log_handler.setFormatter(console_log_format)
    script_logger.addHandler(console_log_handler)
    return script_logger
