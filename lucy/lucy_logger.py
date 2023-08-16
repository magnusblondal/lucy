import os

class LucyLogger(object):
    @staticmethod
    def path():
        return f"{os.getcwd()}/logs"