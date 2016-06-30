# -*- coding: utf-8 -*-
from lib.options import oparser
from lib.config import conf
from optparse import OptionParser
from optparse import OptionGroup
import urllib2
import threading
import Queue
import urllib
import sys
import getopt
import time
import logging

__author__ = "LoRexxar"

conf['resume'] = None
conf['ua'] = "Mozilla/5.0 （X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
conf['version'] = "v1.3.0"


def main():
    oparser()

if __name__ == '__main__':
    main()
