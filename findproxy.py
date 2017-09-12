#!/usr/bin/env python
#coding:utf-8
"""
	#此脚本粗略检测出代理服务器
	DNS服务由 http://ceye.io/record/index 提供
	如果碰到 proxytest.140.205.250.51.443.fq1ezq.ceye.io 这种结果,很可能就是误报.不清楚他们的nginx是怎么配置的.
"""


import time
import traceback
from gevent import monkey
from gevent.pool import Pool
import re
from lib.lib import *
monkey.patch_all()
logpath = "temp/proxy_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time()))
logging.getLogger().setLevel(logging.ERROR)
import requests

#根据
#acccess.log访问日志
#响应中的关键字

def run(domain,port):
	for suffix in ["/"]:
		try:
			url = "http://proxytest.{2}.{0}.{1}.fq1ezq.ceye.io".format(domain, port, str(random.randrange(1000, 9999)))
			res = requests.get(url, proxies={"http": "{}:{}".format(domain, port)}, timeout=20)
			title = re.findall("<title>(.*?)</title>", res.text)
			if len(title) > 0:
				title = title[0]
			else:
				title = ""
			saveFile("{0}:{1}-----{2}------{3}".format(domain, port, title, len(res.text)),logpath)
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
def test():
	# 测试环境  10.0.1.27上有一个squid服务
	check(('10.0.1.27', 3128))
'''
	运行实际功能
'''
def main():
	res = get_from_database("select address,port from blog.scan_scan_port where service like 'http%' or port='80' or port='443' or service ='' or service='unknown'")
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
