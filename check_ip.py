#!/usr/bin/env python2
import urllib2
import socket
import re
import time
import sys
import Queue
import threading

time_out=5
output_file="./ip"
thread_count=5

class Worker(threading.Thread):
    def __init__(self,host,path,pattern,queue,num):
        threading.Thread.__init__(self)
        self.__host=host
        self.__path=path
        self.__pattern=pattern
        self.__queue=queue
        self.__num=num
    def run(self):
        global ips,data_lock,print_lock
        print "Thread %d:Initializing..."%self.__num
        while True:
            ip=self.__queue.get()
            try:
                req=urllib2.Request(url="http://%s%s"%(ip,self.__path))
                if self.__host:
                    req.add_header("Host",self.__host)
                time1=time.time()
                res=urllib2.urlopen(req)
                time2=time.time()
                t=time2-time1
                if re.search(self.__pattern,res.read())!=None:
                    print_lock.acquire()
                    print "Thread %d:IP %s ; TIME %f ms ; Accepted."%(self.__num,ip,t*1000)
                    print_lock.release()
                    data_lock.acquire()
                    ips[t]=ip
                    data_lock.release()
                else:
                    print_lock.acquire()
                    print "Thread %d:IP %s ; Discarded."%(self.__num,ip)
                    print_lock.release()
            except Exception as e:
                print_lock.acquire()
                print "Thread %d:IP %s ; Error Occourred"%(self.__num,ip)
                print "Thread %d:Error Message:"%self.__num,e," Discarded."
                print_lock.release()
            finally:
                self.__queue.task_done()

def main(specify=False,ipv6=False):
    global ips,data_lock,print_lock
    socket.setdefaulttimeout(time_out)
    base_ip=raw_input("Input base IP:")
    if specify:
        host_name=raw_input("Input host name:")
        request_path=raw_input("Input request path:")
        pattern=raw_input("Input search pattern:")
    else:
        host_name=""
        request_path="/"
        pattern="<title>Google</title>"

    ips={}
    data_lock=threading.Lock()
    print_lock=threading.Lock()
    queue=Queue.Queue()

    threads=[]
    for i in range(thread_count):
        j=Worker(host_name,request_path,pattern,queue,i)
        j.daemon=True
        j.start()
        threads.append(j)

    if ipv6:
        top=65536
    else:
        top=256
    for i in range(1,top):
        if ipv6:
            i=hex(i).split("x")[-1]
            ip="[%s%s]"%(base_ip,i)
        else:
            ip=base_ip+str(i)
        queue.put(ip)

    queue.join()

    print "Writing to file..."
    ts=ips.keys()
    ts.sort()
    with open(output_file,"a") as f:
        f.write("\n".join(ips[i].strip("[]") for i in ts ))
    print "All finished."

if __name__ == '__main__':
    specify="-s" in sys.argv or "--specify" in sys.argv
    ipv6="-6" in sys.argv or "--ipv6" in sys.argv
    main(specify,ipv6)
