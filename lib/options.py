# coding=utf-8
from optparse import OptionParser
from optparse import OptionGroup
import threading
import sys
import logging
import re
from tqdm import tqdm
from wordbuild import build_wordlist
from bruter import dir_bruter
from lib.config import conf
from lib.log import logger
from lib.log import log
from lib .wordbuild import  raw_words
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

    conf['url'] = (args.url.rstrip('/').rstrip('"').rstrip('\'') if args.url else "http://testphp.vulnweb.com/")

    # 处理下url用来log的名字
    name = re.findall("[\w\.-]+", conf['url'])
    try:
        conf['name'] = (name[1] if len(name) == 2 else name[0])
    except IndexError:
        errMsg = "url input error!"
        logger.error("url matching fail!")
        parser.error(errMsg)

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

    conf['loglevel'] = (args.loglevel if args.loglevel else 2)
    if conf['loglevel'] < 1 or conf['loglevel'] > 5:
        # loglevel: 1-5
        errMsg = "loglevel value error(input 1-5)"
        parser.error(errMsg)

    if conf['loglevel'] == 1:
        conf['loglevel'] = logging.CRITICAL
    elif conf['loglevel'] == 2:
        conf['loglevel'] = logging.ERROR
    elif conf['loglevel'] == 3:
        conf['loglevel'] = logging.WARN
    elif conf['loglevel'] == 4:
        conf['loglevel'] = logging.INFO
    elif conf['loglevel'] == 5:
        conf['loglevel'] = logging.DEBUG
    else:
        conf['loglevel'] = logging.ERROR

    # 开启log
    log(conf['name'], conf['loglevel'])

    # 设置扫描器字典

    wordlist_file = (args.filename if args.filename else "./dic/php.txt")
    word_queue = build_wordlist(wordlist_file)

    extensions = ['.bak', '.orig', '.inc', '.swp', '~']

    # 进度条
    pbar = tqdm(total=word_queue.qsize(), leave=False)

    # 开始扫描
    if args.extensions:
        tqdm.write('start scanning with extensions...')
        for i in range(conf['thread']):
            t = threading.Thread(target=dir_bruter, args=(word_queue, conf['url'], conf['stime'], extensions, pbar))
            t.start()
    else:
        tqdm('start scanning...')
        for i in range(conf['thread']):
            t = threading.Thread(target=dir_bruter, args=(word_queue, conf['url'], conf['stime'], None, pbar))
            t.start()
