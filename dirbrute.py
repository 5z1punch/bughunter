#coding:utf-8
'''
	爆破目录,暂时用BBscan扫描
'''

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import os
monkey.patch_all()

def check(temp):
    ip = temp[0]
    port = temp[1]
    domains = getdomainfromip(ip)
    for domain in domains:
        print "checking ip {}".format(domain)
        url = "http://{}:{}".format(domain,port)
        print "python3 dirbrute/dirsearch.py -u \"{0}\" -e php".format(url)
	os.system("python3 dirbrute/dirsearch.py -u \"{0}\" -e php,jsp,html".format(url))

def test():
	#check(('127.0.0.1',"8089/samples-spring-1.2.3"))
	check(('127.0.0.1',"8080"))


def run():
	res = get_from_database("select address,port from blog.scan_scan_port where service like 'http%' or port='80' or port='443' or service ='' or service='unknown'")
	res = list(set(res))
	print "检查共{0}个IP".format(len(res))
	p = Pool(200)
	p.map(check, res)
if __name__ == "__main__":
	run()
