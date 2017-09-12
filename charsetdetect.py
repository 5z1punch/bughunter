# coding:utf-8
"""
	网页字符集探测.
	未设置或者设置成gbk的网页,容易受到xss攻击

	item.taobao.com

"""

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import traceback
import logging
monkey.patch_all()
logpath = "temp/charsetdetect_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time())) + ".txt"
logging.getLogger().setLevel(logging.ERROR)
import requests

def run(domain,port):
	for suffix in ["/"]:
		if str(port) == "443":
			url = "https://{0}:{1}".format(domain, port)
		else:
			url = "http://{0}:{1}".format(domain, port)
		url = url + suffix
		try:
			r = requests.get(url)
			if "Content-Type" in r.headers.keys():
				temp = r.headers["Content-Type"].lower()
				if "gb2312" in temp or 'gbk' in temp:
					print(url,temp)
					saveFile(url + ":" + temp, logpath)
				else:
					print(temp)
			#if "<meta" in r.text:
			#	saveFile(url, logpath)
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
	main()
	print("Finished...")
	clean()
