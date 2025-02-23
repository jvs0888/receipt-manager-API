import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler


def init_logger(name: str = "logger",
                file_log: bool = True,
                stream_log: bool = True,
                rotate: bool = True) -> logging.Logger:

    log_directory: str = os.path.join(Path(__file__).parent.parent, "logs")
    if not os.path.exists(log_directory):
        try:
            os.makedirs(log_directory)
        except Exception as e:
            exit(f"failed to create log directory on a path :: {log_directory} :: {e}")

    log_filename: str = f"{name}_{str(datetime.now().date())}.log"
    log_filepath: str = os.path.join(log_directory, log_filename)

    logger: logging.Logger = logging.getLogger(f"{name}.error")
    logger.setLevel(logging.INFO)
    formatter: logging.Formatter = logging.Formatter(
        fmt=u"%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")

    if file_log:
        if rotate:
            file_handler: logging.FileHandler = RotatingFileHandler(log_filepath, maxBytes=1000000, backupCount=1)
        else:
            file_handler: logging.FileHandler = logging.FileHandler(log_filepath)

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if stream_log:
        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


web_server = sys.argv[0].split("/")[-1]
logger: logging.Logger = init_logger(name=web_server)
