import logging
from lib.config import conf

__author__ = "LoRexxar"

# logfile = (conf['url']+".log" if conf['url'] else "test.log")

logger = logging.getLogger('ScannerLog')


def log(name, loglevel):

    f = open("./log/" + name + ".log", 'a+')
    Log_Handle = logging.StreamHandler(f)
    # Log_Handle = logging.StreamHandler(sys.stdout)
    FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] [%(thread)d] %(message)s", "%H:%M:%S")
    Log_Handle.setFormatter(FORMATTER)
    logger.addHandler(Log_Handle)
    logger.setLevel(loglevel)
