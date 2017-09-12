#coding:utf-8
# 函数库
import logging
import random
import redis
import re
logging.getLogger().setLevel(logging.ERROR)
from db.myMysql import mymysql
from config import *
import MySQLdb
from dns.resolver import NoNameservers,NoAnswer,NXDOMAIN,Timeout
from dns.resolver import Resolver

# 记录字符串到文件
def saveFile(s,filepath):
	try:
		f = open(filepath,"a")
		f.write(s.strip()+"\n")
		f.close()
	except Exception as e:
		logging.info("Exception saving file!!!")

# 将ip和domain插到scan_scan_domain_bak表中
def result_to_database(ip,domain):
	m = mymysql(db=mysql_db, host=mysql_server, user=mysql_user, passwd=mysql_pass, port=mysql_port)
	m.insert(table="scan_scan_domain_bak", columns=("ip", "domain"), data=[(ip, domain)])

'''
	domain2 是由 domain1 关联出的域名
    domain1:fangdd.com
    domain2:xf.fangdd.com
    comment:"第三方扫描"
'''
def result_to_domaindatabase(domain1,domain2,comment):
	m = mymysql(db=mysql_db, host=mysql_server, user=mysql_user, passwd=mysql_pass, port=mysql_port)
	m.insert(table="scan_scan_domain_domain", columns=("domain1", "domain2","comment"), data=[(domain1, domain2, comment)])

#返回域名的所有A记录
def getA(domain):
	ret = []
	try:
		for i in Resolver().query(domain, "A"):
			ret.insert(0, str(i))
	#except NoNameservers:
	#	pass
	#except NoAnswer:
	#	pass
	#except NXDOMAIN:
	#	pass
	#except Timeout:
	#	pass
	except Exception as e:
		#import traceback
		#print traceback.print_exc()
		print(e)
		pass
	finally:
		return ret

#从数据库中返回记录
#去重,随机
def get_from_database(sql="select brother from blog.scan_scan_srcbrother"):
    #conn = MySQLdb.connect('10.0.1.60', user='fscan', passwd='fscan123')
    conn = MySQLdb.connect(mysql_server, user=mysql_user, passwd=mysql_pass, port=mysql_port)
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    res = list(set(res))
    random.shuffle(res)
    return res
#更新sql
def update_database(sql=""):
    conn = MySQLdb.connect(mysql_server, user=mysql_user, passwd=mysql_pass)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    return res
# 爆破子域名
def brutesub(domain):
	if domain.startswith("www."):
		saveFile(domain, "/tmp/tobrute")
	if isdomain(domain):
		try:
			redis_conn = redis.Redis(host=redis_server, port=6379, password=redis_password)
			if not redis_conn.sismember("domainbrute_set", domain):
				redis_conn.lpush("domainbrute", domain)
				redis_conn.sadd("domainbrute_set", domain)
		except Exception as e:
			print(e)

# 返回可以爆破的x级子域名 (x >= 2)
# subdomain:tc.test.esf.fangdd.com
# domain:fangdd.com
# 返回 [test.esf.fangdd.com,esf.fangdd.com]

# 测试:getsub("tc.test.esf.fangdd.com","fangdd.com")
# "www.tc.esf.fangdd.com"  这种www很例外,需要剔除掉.
def getsub(subdomain,domain = ""):
	ret = []
	# 除掉www
	if subdomain.startswith("www."):
		subdomain = subdomain.replace("www.","")
	domain_len = len(domain.split("."))
	subdomain_len = len(subdomain.split("."))
	if (subdomain_len - domain_len) > 1:
		for i in range(1,subdomain_len - domain_len):
			ret.insert(0, ".".join(subdomain.split(".")[i:]))
	return ret
'''
   爆破可能的子域名
   subdomain: tc.esf.fangdd.com
   domain: esf.fangdd.com
'''
def pushsub(subdomain,domain = ""):
	for i in getsub(subdomain,domain):
		brutesub(i)

# 判断是否合法域名
def isdomain(s):
	for i in [",","<",">","(",")"]:
		if i in s:
			return False
	return True

# ip端口扫描任务下发
# 爆破子域名
def nmapip(ip):
	try:
		redis_conn = redis.Redis(host=redis_server, port=6379, password=redis_password)
		if not redis_conn.sismember("nmap_set", ip):
			redis_conn.lpush("nmap", ip)
			redis_conn.sadd("nmap_set", ip)
	except Exception as e:
		print(e)
def nmapfromdatabase():
	res = get_from_database("select distinct(ip) from blog.scan_scan_domain_bak")
	for i in res:
		nmapip(i[0])
'''
	根据ip 返回域名
	针对nginx,apache多Host的情况 很常见,非常需要
	todo:也可以用来判断CDN,但是针对CDN的ip如何处置?
'''
def getdomainfromip(ip):
	res = get_from_database("select distinct(domain) from blog.scan_scan_domain where ip='{0}'".format(ip))
	ret = []
	for i in res:
		if i[0] == '' or i[0].startswith('IPc'):
			continue
		ret.insert(0,i[0])
	ret.insert(0,ip)
	return ret
'''
	根据 ip 和 port 生成 url
'''
def setUrl(ip,port,uri = ""):
	uri = uri.lstrip("/")
	if str(port) == 443:
		return "https://{0}:{1}/{2}".format(ip,port,uri)
	else:
		return "http://{0}:{1}/{2}".format(ip,port,uri)
'''
	根据ip,port返回url
'''
def geturlfromipport(ip, port):
	ret = []
	for domain in getdomainfromip(ip):
		if port == "443":
			url = "https://" + domain + ":" + port
		else:
			url = "http://" + domain + ":" + port
		ret.insert(0, url)
	return ret

# 判断内网ip
def ip_into_int(ip):
# 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
# (((((192 * 256) + 168) * 256) + 1) * 256) + 13
	return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))
'''
	判断是否是内网ip
'''
def is_internal_ip(ip):
    if str(ip).startswith("127.0.0"):
	return True
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c

def is_ip(x):
	if len(re.findall("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", x)) > 0:
		return True
	return False

#print(is_ip("xx.com"))
#print(is_ip("1.1.1.1"))

#nmapfromdatabase()
#getdomainfromip("113.31.22.248")
#

#brutesub("fangdd.com")
