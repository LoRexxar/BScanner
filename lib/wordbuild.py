# coding=utf-8
import Queue
from lib.config import conf
from lib.log import logger

__author__ = "LoRexxar"


def build_wordlist(wordlist_file):
    # 读入字典文件
    fd = open(wordlist_file, "rb")
    logger.info("start wordlist build...")
    raw_words = fd.readlines()
    logger.info("This dictionary contains %s rows" % len(fd.readlines()))
    if len(fd.readlines()) == 0:
        logger.error("This dictionary id empty...")
    fd.close()

    found_resume = False
    words = Queue.Queue()

    for word in raw_words:
        word = word.rstrip()

        # 这功能暂时没开

        if conf['resume'] is not None:
            if found_resume:
                words.put(word)
            else:
                if word == conf['resume']:
                    found_resume = True
                    print "Resuming wordlist from : %s" % conf['resume']

        else:
            words.put(word)

    logger.info("wordlist build is complete...")
    return words
