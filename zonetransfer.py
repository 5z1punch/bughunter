# coding:utf-8
"""
	jenkins 命令执行
"""

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import traceback
import os
import logging
import re
monkey.patch_all()
logpath = "temp/zonetransfer_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time()))
logging.getLogger().setLevel(logging.ERROR)

def check(task):
	domain = task[0]
	cmd_res = os.popen('nslookup -type=ns ' + domain).read()  # fetch DNS Server List
	dns_servers = re.findall('nameserver = (.*?)\n', cmd_res)
	for server in dns_servers:
		cmd_res = os.popen('dig @%s axfr %s' % (server, domain)).read()
		if cmd_res.find('Transfer failed.') < 0 and \
						cmd_res.find('connection timed out') < 0 and \
						cmd_res.find('XFR size') > 0:
			print("lucky")
			saveFile(domain,logpath)
"""
	检查结束后
"""
def clean():
	pass
"""
	测试
"""
def test(ip, port):
	check([ip, port])

def main():
	res = get_from_database(
		"select brother from blog.scan_scan_srcbrother")
	res = list(set(res))
	random.shuffle(res)
	p = Pool(200)
	p.map(check, res)
if __name__ == "__main__":
	print("String...")
	main()
	print("Finished...")
	clean()
