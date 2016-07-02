# -*- coding: utf-8 -*-
from lib.options import oparser
from lib.log import logger
from lib.config import conf

__author__ = "LoRexxar"


def main():
    logger.debug("Begin Scanner...")
    oparser()

if __name__ == '__main__':
    main()
