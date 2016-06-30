 # -*- coding: utf-8 -*- 
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

# threads  = 50
# target_url = "http://www.wooyun.org/".rstrip('/')
# wordlist_file = "./php.txt"
resume = None
user_agent = "Mozilla/5.0 （X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def build_wordlist(wordlist_file):
	# 读入字典文件
	fd = open(wordlist_file,"rb")
	raw_words = fd.readlines()
	fd.close()

	found_resume = False
	words = Queue.Queue()

	for word in raw_words:
		word = word.rstrip()

		# 这功能暂时没开

		if resume is not None:
			if found_resume:
				words.put(word)
			else:
				if word == resume:
					found_resume = True
					print "Resuming wordlist from : %s" % resume

		else:
			words.put(word)


	return words

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
				headers["User-Agent"] = user_agent
				r = urllib2.Request(url, headers=headers)

				response = urllib2.urlopen(r)
				
				# 请求完成后睡眠
				time.sleep(stime)
				
				if len(response.read()):
					print "[%d] => %s" % (response.code, url)

			except urllib2.URLError,e:
				if hasattr(e, 'code') and e.code != 404:
					print "!!! %d => %s" % (e.code, url)
	exit(0)


def main(argv):

	# 处理参数
	parser = OptionParser()
	parser.version = "v1.2.1"

	parser.add_option("--version", "-v", dest="showVersion",action="store_true",help="show program's version and exit")

	# 必选参数
	target = OptionGroup(parser, "Target", "At least one of these options has to be provided to define the target(s)")

	target.add_option("-u", dest="url", help="Target URL")
	target.add_option("--test", dest="test", action="store_true", help="auto test")

	# 可选参数
	opt = OptionGroup(parser, "Options", "Optional parameters")

	opt.add_option("-t","--thread", dest="thread", type="int", help="thread number(default 30)")
	opt.add_option("-e","--ext", dest="extensions", action="store_true", help="Whether to use file extension(default false)")
	opt.add_option("-f","--filename",dest="filename",help="Scanner dictionary (default ./php.txt)")
	opt.add_option("-s","--sleeptime", dest="stime", type="int", help="Each request of sleep time (default 1)")
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

	target_url = (args.url.rstrip('/').rstrip('"').rstrip('\'') if args.url else "http://www.wooyun.org")

	threads = (args.thread if args.thread else 30)

	if threads < 1 or threads > 50:
		# 线程数为0-50
		errMsg = "thread value error (1-50)"
		parser.error(errMsg)
	
	# 设置睡眠时间
	stime = (args.stime if args.stime else 1)

	if stime < 0 or stime > 10:
		# 睡眠时间为0-10
		errMsg = "time value error (0-10)"
		parser.error(errMsg)

	loglevel = (args.loglevel if args.loglevel else 4)
	if loglevel < 1 or loglevel > 5:
		# loglevel: 1-5
		errMsg = "loglevel value error(input 1-5)"
		parser.error(errMsg)

	if loglevel == 1:
		loglevel = logging.CRITICAL
	elif loglevel == 2:
		loglevel = logging.ERROR
	elif loglevel == 3:
		loglevel = logging.WARN
	elif loglevel == 4:
		loglevel = logging.INFO
	elif loglevel == 5:
		loglevel = logging.DEBUG
	else:
		loglevel = logging.ERROR

	# logfile = (target_url+".log" if target_url else "test.log")

	logger = logging.getLogger('SpiderLog')
	# f = open("./log/" + logfile, 'a+')
	# Log_Handle = logging.StreamHandler(f)
	# # Log_Handle = logging.StreamHandler(sys.stdout)
	# FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] [%(thread)d] %(message)s", "%H:%M:%S")
	# Log_Handle.setFormatter(FORMATTER)
	# logger.addHandler(Log_Handle)
	logger.setLevel(loglevel)
	
	# 设置扫描器字典

	wordlist_file =(args.filename if args.filename else "./dic/php.txt")
	word_queue = build_wordlist(wordlist_file)
	
	extensions = ['.bak','.orig','.inc','.swp','~']

	# 开始扫描
	if args.extensions:
		print '[*]   start scanning with extensions...'
		for i in range(threads):
				t = threading.Thread(target=dir_bruter, args=(word_queue,target_url,stime,extensions,))
				t.start()
	else:
		print '[*]   start scanning...'
		for i in range(threads):
				t = threading.Thread(target=dir_bruter, args=(word_queue,target_url,stime,))
				t.start()


if __name__ == '__main__':
	main(sys.argv)