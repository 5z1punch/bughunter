#coding:utf-8
# 此脚本是将80端口的信息利用,如
# 网站title
# 网站证书中的域名信息
# 根目录是否可以列目录
'''
todo:列目录 site:xxx.com intext:index of
# 案例
http://static.hx99.net/static/bugs/wooyun-2016-0204624.html

字典也不够,http://static.hx99.net/static/bugs/wooyun-2014-056952.html 检测不出来
'''

'''
漏洞:
redmine未授权   https://feedback.fangdd.com/projects/android_app_feedback/issues?set_filter=1&tracker_id=1 泄露内部员工 和源码


'''
import urllib
from gevent import monkey
from gevent.pool import Pool
import time
from lib.lib import *
monkey.patch_all()
logging.getLogger().setLevel(logging.WARN)
import requests


titlelogpath = "temp/title_"+time.strftime("%Y-%m-%d_%H:%M",time.localtime(time.time()))
dirlogpath = "temp/dir_"+time.strftime("%Y-%m-%d_%H:%M",time.localtime(time.time()))
ssllogpath = "temp/ssl_"+time.strftime("%Y-%m-%d_%H:%M",time.localtime(time.time()))

#qingyu_cur.execute("truncate data_unserialize")
def results_to_database(test_ip,ip,port,res,res_len):
    conn = MySQLdb.connect('10.0.1.60', user='fscan', passwd='fscan123')
    cur = conn.cursor()
    #print "insert into fscanports.proxyexp(ip,port,response) values('{}','{}','{}')".format(ip,port,res)
    cur.execute("insert into fscanports.proxyexp(test_ip,ip,port,response,res_len) values('{}','{}','{}','{}','{}')".format(test_ip,ip,port,urllib.quote(res),res_len))
    conn.commit()
    cur.close()

def check(task):
	ip = task[0]
	port = str(task[1])
	domains = getdomainfromip(ip)
	for domain in domains:
		if port == "443":
			url = "https://"+domain+":"+port
		else:
			url = "http://"+domain+":"+port
		try:
			logging.debug("checking {0}".format(url))
			res = requests.get(url,timeout = 3)
			#
			title = re.findall("<title>(.*?)</title>",res.text,re.IGNORECASE)
			if len(title) > 0:
				title = title[0]
			else:
				title = ""
			saveFile("{0}-----{1}------{2}".format(url,title,len(res.text)),titlelogpath)
			if "index of /" in res.text.lower() or "directory list" in res.text.lower() or "- /</title>" in res.text.lower():
				if "ERROR: The requested URL could not be retrieved" not in title and "directory listing denied" not in res.text.lower():
					saveFile("{0}-----{1}------{2}".format(url, title, len(res.text)), dirlogpath)
			#results_to_database(ip,test_ip,port,res.status_code,len(res.text))
		except requests.exceptions.SSLError as e:
			temp = re.findall("hostname '([\d\.]+)' doesn't match [either of]*(.*)", str(e))
			if len(temp) > 0:
				saveFile(str(temp),ssllogpath)
			else:
				#print "xxxx",e,url
				pass
		except Exception as e:
			#results_to_database(ip,test_ip,port,"Exception",0)
			#print e
			pass

# 加不加 / 的区别
def check1(task):
	ip = task[0]
	port = task[1]
	if port == "443":
		url = "https://"+ip+":"+port
	else:
		url = "http://"+ip+":"+port
	try:
		url1 = url
		url2 = url + "/"
		res1 = requests.get(url1,timeout = 3)
		res2 = requests.get(url2,timeout = 3)
		if res1.text != res2.text:
			saveFile("{0}-----{1}------{2}".format(url, "", ""), "/tmp/diff")
	except Exception as e:
		#results_to_database(ip,test_ip,port,"Exception",0)
		#print e
		pass

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

