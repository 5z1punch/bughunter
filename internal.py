#!/usr/bin/env python
#coding:utf-8
'''
	#此脚本粗略绕过内网ip限制
	X-FORWAR-FOR 配置成三个内网地址去访问域名,比较不加X-FORWAR-FOR 的页面
'''

import MySQLdb
import hashlib
import random
import time
import traceback
from gevent import monkey
from gevent.pool import Pool
import re
monkey.patch_all()
import requests


def saveFile(s,filepath):
	try:
		f = open(filepath,"a")
		f.write(s.strip()+"\n")
		f.close()
	except Exception,e:
		logging.info("Exception saving file!!!")
#根据
#acccess.log访问日志
#响应中的关键字
def check(x):
    ip = x[0]
    port = x[1]
    if str(port) == 443:
	    return
    print "checking ip {}".format(ip)
    #temp1 = hashlib.new('md5', str(random.randrange(100000, 999999)) + '|' + str(time.time())).hexdigest()
    #hash = "lilishow.top/{0}/{1}".format("proxy",ip+"_"+str(port))
    hash = "proxytest{2}.{0}.{1}.fq1ezq.ceye.io".format(ip,port,str(random.randrange(1000,9999)))
    try:
	    #varify(ip,port,hash,"proxy")
	    res = requests.get("http://{}".format(hash),proxies={"http":"{}:{}".format(ip,port)},timeout = 20)
	    title = re.findall("<title>(.*?)</title>", res.text)
	    if len(title) > 0:
		    title = title[0]
	    else:
		    title = ""
	    saveFile("{0}:{1}-----{2}------{3}".format(ip, port, title, len(res.text)),
	             "/tmp/proxytest")
    except Exception,e:
	    print e
	    #try:
		#    res = requests.get("https://{}".format(hash), proxies={"https": "{}:{}".format(ip, port)})
	    #except Exception, e:
		#    print traceback.print_exc()
	    pass

def get_from_database():
	#conn = MySQLdb.connect('10.0.1.60', user='fscan', passwd='fscan123')
	conn = MySQLdb.connect('10.0.1.27', user='fscan', passwd='fscan123')
	cur = conn.cursor()
	#cur.execute("select ip,port from test.port where service like 'http%' or port='80' or port='443' or service ='' or service='unknown'")
	cur.execute("select address,port from blog.scan_scan_port where service like 'http%' or port='80' or port='443' or service ='' or service='unknown'")
	res = cur.fetchall()
	cur.close()
	return res
def results_to_database(ip,port,vuln_type,table = "vuln"):
    conn = MySQLdb.connect('128.199.172.16', user='root', passwd='toorsec!502')
    cur = conn.cursor()
    cur.execute("insert into fscanports.{}(ip,port,vuln_type) values('{}','{}','{}')".format(table,ip,port,vuln_type))
    conn.commit()
    cur.close()
    '''
		    CREATE TABLE `cloudeye` (
		  `id` int(4) NOT NULL AUTO_INCREMENT,
		  `ip` varchar(200) NOT NULL,
		  `hash` varchar(100) NOT NULL,
		`vuln_type` varchar(20) NOT NULL,
		`port` varchar(10) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=latin1
	'''
def varify(ip,port,hash,vuln_type):
	conn = MySQLdb.connect(host='10.0.1.60', user='fscan', passwd='fscan123')
	cur = conn.cursor()
	cur.execute("insert into fscanports.cloudeye(ip,port,hash,vuln_type)values('{}','{}','{}','{}')".format(ip,port,hash,vuln_type))
	conn.commit()
	conn.close()
'''
	测试功能是否可用
	http://ceye.io/record/query 应该有 proxytest.10.0.1.27.3128.fq1ezq.ceye.io 记录
'''
def test():
	# 测试环境  10.0.1.27上有一个squid服务
	check(('10.0.1.27', 3128))
'''
	运行实际功能
'''
def run():
	res = get_from_database()
	res = list(set(res))
	print "共检查{0}个IP".format(len(res))
	p = Pool(200)
	p.map(check, res)

if __name__ == "__main__":
	run()
