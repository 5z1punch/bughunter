#coding:utf-8
'''
	supervisor识别
		http://10.0.1.28:32809/stylesheets/supervisor.css
		响应中有 =ORDER
'''

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import requests
monkey.patch_all()
logpath = "temp/supervisor_"+time.strftime("%Y-%m-%d_%H:%M",time.localtime(time.time()))

def run(domain,port):
	for suffix in ["/stylesheets/supervisor.css"]:
		if str(port) == "443":
			url = "https://{0}:{1}".format(domain, port)
		else:
			url = "http://{0}:{1}".format(domain, port)
		url = url + suffix
		try:
			r = requests.get(url)
			if "=ORDER" in r.text:
				saveFile(url, logpath)
		except requests.RequestException:
			pass
		except Exception as e:
			print(traceback.print_exc())
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
	#main()
	print("Finished...")
	clean()
