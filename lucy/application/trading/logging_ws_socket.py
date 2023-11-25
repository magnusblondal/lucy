import logging
from lucy.lucy_logger import LucyLogger

LOGGING_LEVEL = "DEBUG"

LOG_IN_STDOUT = True
LOG_IN_FILE = True
LOG_FILENAME = "futures_ws"


class SocketLogger(LucyLogger):
    @staticmethod
    def get_logger(name):
        path = LucyLogger.path()
        logger = logging.getLogger(name)
        logger.setLevel(LOGGING_LEVEL)
        formatter = logging.Formatter(
            '[%(asctime)s]  [%(levelname)5s]  [%(threadName)10s]  [%(name)10s]  %(message)s')

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
