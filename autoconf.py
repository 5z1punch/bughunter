import os
whitelist = ["autoconf.py","blank.py","config.py","jenkins.py"]
for i in os.listdir("."):
	if i.endswith(".py"):
		str = '''
[program:{0}]
command=/usr/local/bin/python {0}
directory=/root/bughunter
'''.format(i)
		print str

	res = requests.get(url)
	if "Hypertext Transfer Protocol -- HTTP/1.1" in res.text:
		print "found"
		saveFile(url, logpath)