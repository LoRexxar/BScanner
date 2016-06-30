# coding=utf-8
import urllib
import urllib2
import time
from lib.config import conf

__author__ = "LoRexxar"


def dir_bruter(word_queue, target_url, stime, extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()

        attempt_list = []

        # 检查是否有文件扩展名，如果没有就是我们要暴力破解的路径
        # if "." not in attempt:
        # 	attempt_list.append("%s/" % attempt)
        # else:
        attempt_list.append("%s" % attempt)

        # 如果我们想暴力扩展
        if extensions:
            for extension in extensions:
                if extension == ".swp":
                    attempt_list.append("/.%s%s" % (attempt.strip('/'), extension))
                else:
                    attempt_list.append("%s%s" % (attempt, extension))

        # 迭代我们想要尝试的文件列表
        for brute in attempt_list:
            url = "%s%s" % (target_url, urllib.quote(brute))
            # print url
            try:
                headers = {}
                headers["User-Agent"] = conf['ua']
                r = urllib2.Request(url, headers=headers)

                response = urllib2.urlopen(r)

                # 请求完成后睡眠
                time.sleep(stime)

                if len(response.read()):
                    print "[%d] => %s" % (response.code, url)

            except urllib2.URLError, e:
                if hasattr(e, 'code') and e.code != 404:
                    print "!!! %d => %s" % (e.code, url)
    exit(0)