#!/usr/bin/env python2

import dns.resolver as m
import socket,sys
import threading,Queue

hosts_list="./host_names"
ipv6_hosts_list="./host_names_ipv6"
output_file="./hosts"
nameservers=["2001:4860:4860::8888","2001:4860:4860::8844"]
thread_count=5
    
time_out=5

class Worker(threading.Thread):
    def __init__(self,queue,num):
        threading.Thread.__init__(self)
        self.__queue=queue
        self.__num=num
    def run(self):
        global ips,data_lock,print_lock,solver,query_type
        print_lock.acquire()
        print "Thread %d:Initializing..."%self.__num
        print_lock.release()
        while True:
            host_name=self.__queue.get()
            try:
                print_lock.acquire()
                print "Thread %d: Querying host name %s"%(self.__num,host_name[1])
                print_lock.release()
                ans=solver.query(host_name[1],query_type)
                print_lock.acquire()
                print "Thread %d: Host name: %s; IP: %s"%(self.__num,host_name[1],ans[0])
                print_lock.release()
                data_lock.acquire()
                ips.append((host_name[0],host_name[1],ans[0]))
                data_lock.release()
            except Exception as e:
                print_lock.acquire()
                print "Thread %d:Host name %s ; Error Occourred"%(self.__num,host_name[1])
                print "Thread %d:Error Message:"%self.__num,e," Discarded."
                print_lock.release()
            finally:
                self.__queue.task_done()


def main(ipv6=False):
    global ips,data_lock,print_lock,solver,query_type
    socket.setdefaulttimeout(time_out)    
    if ipv6:
        hosts_name_file_name=ipv6_hosts_list
    else:
        hosts_name_file_name=hosts_list

    with open(hosts_name_file_name) as f:
        hosts=f.read().split("\n")
        hosts=[i for i in hosts if i]

    if ipv6:
        query_type="AAAA"
    else:
        query_type="A"

    solver=m.Resolver()
    solver.nameservers=nameservers
    
    ips=[]
    data_lock=threading.Lock()
    print_lock=threading.Lock()    
    queue=Queue.Queue()

    threads=[]
    for i in range(thread_count):
        j=Worker(queue,i)
        j.daemon=True
        j.start()
        threads.append(j)

    count=0
    for i in hosts:
        queue.put((count,i))
        count=count+1

    queue.join()

    print "Writing to file..."
    ips.sort(key=lambda x:x[0])
    ips=["%s %s"%(i[2],i[1]) for i in ips]
    with open(output_file,"w") as f:
        f.write("\n".join(ips))
    print "All finished."

if __name__ == '__main__':
    ipv6="-6" in sys.argv or "--ipv6" in sys.argv
    main(ipv6)
