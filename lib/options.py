# coding=utf-8
from optparse import OptionParser
from optparse import OptionGroup
import threading
import sys
import logging
from wordbuild import build_wordlist
from bruter import dir_bruter
from lib.config import conf

__author__ = "LoRexxar"


def oparser():
    # 处理参数
    parser = OptionParser()
    parser.version = conf['version']

    parser.add_option("--version", "-v", dest="showVersion", action="store_true",
                      help="show program's version and exit")

    # 必选参数
    target = OptionGroup(parser, "Target", "At least one of these options has to be provided to define the target(s)")

    target.add_option("-u", dest="url", help="Target URL")
    target.add_option("--test", dest="test", action="store_true", help="auto test")

    # 可选参数
    opt = OptionGroup(parser, "Options", "Optional parameters")

    opt.add_option("-t", "--thread", dest="thread", type="int", help="thread number(default 30)")
    opt.add_option("-e", "--ext", dest="extensions", action="store_true",
                   help="Whether to use file extension(default false)")
    opt.add_option("-f", "--filename", dest="filename", help="Scanner dictionary (default ./php.txt)")
    opt.add_option("-s", "--sleeptime", dest="stime", type="int", help="Each request of sleep time (default 1)")
    opt.add_option("-l", dest="loglevel", type="int", help="log level(1-5) "
                                                           "1, CRITICAL; "
                                                           "2, ERROR(default); "
                                                           "3, WARN; "
                                                           "4, INFO; "
                                                           "5, DEBUG;")

    parser.add_option_group(target)
    parser.add_option_group(opt)

    (args, _) = parser.parse_args(sys.argv)

    if args.showVersion:
        print parser.version
        print "-- By LoRexxar"
        exit(0)

    if not (args.url or args.test):
        errMsg = "missing a mandatory option (-u) or (--test), "
        errMsg += "use -h for basic or --help for advanced help"
        parser.error(errMsg)

    conf['url'] = (args.url.rstrip('/').rstrip('"').rstrip('\'') if args.url else "http://www.wooyun.org")
    conf['thread'] = (args.thread if args.thread else 30)

    if conf['thread'] < 1 or conf['thread'] > 50:
        # 线程数为0-50
        errMsg = "thread value error (1-50)"
        parser.error(errMsg)

    # 设置睡眠时间
    conf['stime'] = (args.stime if args.stime else 1)

    if conf['stime'] < 0 or conf['stime'] > 10:
        # 睡眠时间为0-10
        errMsg = "time value error (0-10)"
        parser.error(errMsg)

    conf['loglevel'] = (args.loglevel if args.loglevel else 4)
    if conf['loglevel'] < 1 or conf['loglevel'] > 5:
        # loglevel: 1-5
        errMsg = "loglevel value error(input 1-5)"
        parser.error(errMsg)

    if conf['loglevel'] == 1:
        loglevel = logging.CRITICAL
    elif conf['loglevel'] == 2:
        loglevel = logging.ERROR
    elif conf['loglevel'] == 3:
        loglevel = logging.WARN
    elif conf['loglevel'] == 4:
        loglevel = logging.INFO
    elif conf['loglevel'] == 5:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.ERROR

    # logfile = (conf['url']+".log" if conf['url'] else "test.log")

    logger = logging.getLogger('SpiderLog')
    # f = open("./log/" + logfile, 'a+')
    # Log_Handle = logging.StreamHandler(f)
    # # Log_Handle = logging.StreamHandler(sys.stdout)
    # FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] [%(thread)d] %(message)s", "%H:%M:%S")
    # Log_Handle.setFormatter(FORMATTER)
    # logger.addHandler(Log_Handle)
    logger.setLevel(loglevel)

    # 设置扫描器字典

    wordlist_file = (args.filename if args.filename else "./dic/php.txt")
    word_queue = build_wordlist(wordlist_file)

    extensions = ['.bak', '.orig', '.inc', '.swp', '~']

    # 开始扫描
    if args.extensions:
        print 'start scanning with extensions...'
        for i in range(conf['thread']):
            t = threading.Thread(target=dir_bruter, args=(word_queue, conf['url'], conf['stime'], extensions,))
            t.start()
    else:
        print 'start scanning...'
        for i in range(conf['thread']):
            t = threading.Thread(target=dir_bruter, args=(word_queue, conf['url'], conf['stime'],))
            t.start()
