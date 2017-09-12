#coding:utf-8
'''
	PUT方法扫描
	activemq fileserver PUT 响应状态码是204
	案例(activemq):
	https://github.com/phith0n/vulhub/tree/activemq-cve-2016-3088/activemq/CVE-2016-3088

	todo:
	AttributeError: 'module' object has no attribute 'kqueue'
'''

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
monkey.patch_all()
import requests

logpath = "temp/put_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time()))
logging.getLogger().setLevel(logging.ERROR)

def run(domain,port):
	for suffix in ["/.vimrc","/fileserver/.vimrc","/file/.vimrc"]:
		if str(port) == "443":
			url = "https://{0}:{1}".format(domain, port)
		else:
			url = "http://{0}:{1}".format(domain, port)
		url = url + suffix
		try:
			res = requests.put(url)
			if res.status_code == 204:
				print("lucky")
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
	main()
	print("Finished...")
	clean()
