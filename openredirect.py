#coding:utf-8
# 此脚本检测 重定向漏洞 , 案例来自 hackone
# http://offsecbyautomation.com/Open-Redirection-Bobrov/
from gevent import monkey
from gevent.pool import Pool
import time
from lib.lib import *
monkey.patch_all()
logging.getLogger().setLevel(logging.WARN)
import requests
import traceback


logpath = "temp/redirect_"+time.strftime("%Y-%m-%d_%H:%M",time.localtime(time.time()))
# http://offsecbyautomation.com/Open-Redirection-Bobrov/

def run(domain,port):
	for suffix in ["//xxxxxxxxx/.."]:
		if str(port) == "443":
			url = "https://{0}:{1}".format(domain, port)
		else:
			url = "http://{0}:{1}".format(domain, port)
		url = url + suffix
		try:
			res = requests.get(url, allow_redirects = False)
			if "Location" in res.headers and (
					res.headers["Location"] == "//xxxxxxxxx/.." or res.headers["Location"] == "//xxxxxxxxx/../"):
				print("lucky")
				saveFile(ip + ":" + port, logpath)
		except requests.RequestException as e:
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
	test("184.168.221.46",80)
"""
def test(ip, port):
	run(ip, port)

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
