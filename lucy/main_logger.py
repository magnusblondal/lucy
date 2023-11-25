import logging
from lucy.lucy_logger import LucyLogger

LOGGING_LEVEL = "DEBUG"

LOG_IN_STDOUT = False
LOG_IN_FILE = True
LOG_FILENAME = "lucy"

# formatter = logging.Formatter('[%(asctime)s]  [%(levelname)5s]  [%(threadName)10s]  [%(name)10s]  %(message)s')


class MainLogger(LucyLogger):

    @staticmethod
    def get_logger(name):
        format = '[%(asctime)s | %(levelname)s | %(threadName)s | %(name)s]  %(message)s'
        path = LucyLogger.path()
        logger = logging.getLogger(name)
        logger.setLevel(LOGGING_LEVEL)
        formatter = logging.Formatter(format)

        if LOG_IN_FILE and path and LOG_FILENAME:
            file_handler = logging.FileHandler(
                "{0}/{1}.log".format(path, LOG_FILENAME), mode="a")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        if LOG_IN_STDOUT:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        return logger

