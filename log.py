from global_consts import *
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

def setup_logger(name, path):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not os.path.exists(path):
        os.makedirs(path)
    log_filename = f"{path}/{name}_{LOG_FILE_NAME}"  
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
    log_filename = log_filename + "_" + timestamp + ".log"

    formatter = logging.Formatter(fmt = '[%(levelname)s][%(asctime)s.%(msecs)03d][%(name)s]: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

    day_file_handler = TimedRotatingFileHandler(filename=log_filename, when="midnight", interval=1, backupCount=LOG_MAX_FILES)
    day_file_handler.setFormatter(formatter)
    logger.addHandler(day_file_handler)

    return logger, (day_file_handler,)