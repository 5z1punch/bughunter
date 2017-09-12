# coding:utf-8
"""
	jenkins 命令执行
"""

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import traceback
import logging
import pymongo
monkey.patch_all()
logpath = "temp/rsync_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time()))
logging.getLogger().setLevel(logging.ERROR)

def check(task):
	ip = task[0]
	port = str(task[1])
	# 忽略内网ip扫描
	if is_internal_ip(ip):
		return
	try:
		conn = pymongo.MongoClient(ip, port, socketTimeoutMS=3000)
		dbs = conn.database_names()
		return ip + ' -> ' + '|'.join(dbs) if dbs else False
	except Exception:
		return False
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
		"select address,port from blog.scan_scan_port where service like 'http%' or service ='' or service='unknown' or port='80'")
	res = list(set(res))
	random.shuffle(res)
	p = Pool(200)
	p.map(check, res)
if __name__ == "__main__":
	print("String...")
	#main()
	print("Finished...")
	clean()
