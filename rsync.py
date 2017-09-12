#!/usr/bin/env python
#coding:utf-8

import subprocess
import time
import threading
import MySQLdb
from lib.lib import *
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()

timeout = 30
ip = "61.135.159.21"
rsync_binary = "/usr/bin/rsync"
test_upload_file = "test"
# args = "--password-file=/etc/passwd"
fileLock = threading.Lock()
logpath = "temp/rsync_"+time.strftime("%Y-%m-%d_%H:%M",time.localtime(time.time()))

def listModule(ip,module,port):
    cmd = "{} {}::{} --port={}".format(rsync_binary, ip, module ,str(port))
    starttime = time.time()
    run_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        if run_proc.poll() is not None:
            break
        endtime = time.time()
        # print endtime - starttime
        if int(endtime - starttime) > timeout:
            run_proc.terminate()
            break
    (stdoutput, erroutput) = run_proc.communicate()
    if '-' in stdoutput:
        saveFile("{0}:{1}---{2}".format(ip, port , cmd),logpath)
        print("vul => list \"{}\" module".format(module))

def writeModule(ip,module,port):
    cmd = "{} {} {}::{} --port={}".format(rsync_binary, test_upload_file, ip, module ,str(port))
    starttime = time.time()
    try:
        run_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            if run_proc.poll() is not None:
                break
            endtime = time.time()
            # print endtime - starttime
            if int(endtime - starttime) > timeout:
                run_proc.terminate()
                break
        (stdoutput, erroutput) = run_proc.communicate()
        #print "erroutput => {}".format(erroutput)
        #print "----"
        # erroutput => rsync error: received SIGINT, SIGTERM, or SIGHUP (code 20) at /BuildRoot/Library/Caches/com.apple.xbs/Sources/rsync/rsync-47/rsync/rsync.c(244) [sender=2.6.9]
        # 会莫名其妙出现上面的错误
        if "Password" in erroutput or "denied" in erroutput or "ERROR: module is read only" in erroutput or "ERROR: Unknown" in erroutput or "rsync error" in erroutput:
            pass
        else:
            saveFile("{0}:{1}---{2}".format(ip, port, cmd), logpath)
            print("vul => write \"{}\" module".format(module))
    except Exception as e:
        #print "vul => write \"{}\" module".format(module)
        pass

def check(x):
    ip = x[0]
    port = x[1]
    print("checking ip {}".format(ip))
    for domain in getdomainfromip(ip):
        try:
            cmd = "{} {}:: --port={}".format(rsync_binary, domain , str(port))
            run_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdoutput, erroutput) = run_proc.communicate()
            for module in stdoutput.split("\n"):
                if module.strip() == "":
                    continue
                '''
                # fix "\t"
                    sersync        	rsync include files
                    mainpage       	rsync include files
                    cnmo_mtouch    	rsync include files
                    include-cnmo_rsync	rsync include files
                '''
                module = module.split(" ")[0]
                module = module.split("\t")[0]
                print("checking module => {}".format(module))
                listModule(domain,module,port)
                writeModule(domain,module,port)
        except Exception as e:
            print(e)


"""
	检查结束后
"""
def clean():
	pass
"""
	测试
	test('202.108.14.87',873)
"""
def test(ip, port):
	check([ip, port])

def main():
    res = get_from_database(
        "select address,port from blog.scan_scan_port where port like '873' or service like '%rsync%' or service ='' or service='unknown'")
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


