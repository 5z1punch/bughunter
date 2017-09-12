#coding:utf-8
'''
	discuz识别
'''

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import traceback
monkey.patch_all()
logpath = "temp/discuz_"+time.strftime("%Y-%m-%d_%H:%M",time.localtime(time.time()))
import requests


def run(domain,port):
	for suffix in ["/forum.php"]:
		if str(port) == "443":
			url = "https://{0}:{1}".format(domain, port)
		else:
			url = "http://{0}:{1}".format(domain, port)
		url = url + suffix
		try:
			r = requests.get("{0}".format(url))
			if "discuz_tips.js" in r.text:
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
		run(domain,port)

'''
	检查结束后
'''
def clean():
	pass

'''
	测试
'''
def test(ip, port):
	check([ip, port])

def main():
	res = get_from_database(
		"select address, port from blog.scan_scan_port where service like 'http%' or service ='' or service='unknown' or port='80'")
	res = list(set(res))
	random.shuffle(res)
	p = Pool(200)
	p.map(check, res)
if __name__ == "__main__":
	run("vpn.bugzilla.dev.data.zabbix.autodiscover.passport.wechat.google.ttlrc.com","8443")
	clean()
