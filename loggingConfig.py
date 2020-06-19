import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os


QUERY = 21
logging.addLevelName(QUERY, "QUERY")
def query(self, message, *args, **kws):
    if self.isEnabledFor(QUERY):
        # Yes, logger takes its '*args' as 'args'.
        self._log(QUERY, message, args, **kws)
logging.Logger.query = query


def initLogging(root=None, loggingLvl = None):
    # logging.basicConfig(filename='FinanceManager.log', filemode='w', level=logging.DEBUG, format='TJTJTJ %(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    if loggingLvl is None:
        loggingLvl = logging.DEBUG

    rootLogger = logging.getLogger('')
    rootLogger.handlers = []
    rootLogger.setLevel(loggingLvl)

    #formatters
    # fileFormatter = logging.Formatter('%(name)s -- %(asctime)s : [%(levelname)s] %(message)s (%(filename)s lineno: %(lineno)d)')
    consoleFormatter = logging.Formatter('%(name)s -- %(asctime)s : [%(levelname)s] %(message)s (%(filename)s lineno: %(lineno)d)')
    uiFormatter = logging.Formatter(' %(levelname)s: %(message)s')


    #Console Handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(consoleFormatter)
    rootLogger.addHandler(console)

    #file Handler
    #
    # fileName = '..\\logs\\main.log'
    # if root is not None:
    #     fileName = os.path.abspath(os.path.join(root, fileName))
    #
    #
    # fileHandler = RotatingFileHandler(filename=fileName, mode='w'
    #                                   , maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
    # fileHandler.setLevel(logging.DEBUG)
    # fileHandler.setFormatter(fileFormatter)
    # rootLogger.addHandler(fileHandler)



