#!/usr/bin/env python2
import urllib2
import socket
import re
import time
import sys

time_out=5
output_file="./ip"

def main(specify=False,ipv6=False):
    socket.setdefaulttimeout(time_out)
    base_ip=raw_input("Input base IP:")
    if specify:
        host_name=raw_input("Input host name:")
        request_path=raw_input("Input request path:")
        pattern=raw_input("Input search pattern:")
    else:
        request_path="/"
        pattern="<title>Google</title>"
    ips={}
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
        try:
            req=urllib2.Request(url="http://%s%s"%(ip,request_path))
            if specify:
                req.add_header("Host",host_name)
            time1=time.time()
            res=urllib2.urlopen(req)
            time2=time.time()
            t=time2-time1
            if re.search(pattern,res.read())!=None:
                print "IP %s ; TIME %f ms ; Accepted."%(ip,t*1000)
                ips[t]=ip
            else:
                print "IP %s ; Discarded."%ip
        except Exception as e:
            print "IP %s ; Error Occourred:"%ip
            print e
    ts=ips.keys()
    ts.sort()
    with open(output_file,"a") as f:
        f.write("\n".join(ips[i] for i in ts ))

if __name__ == '__main__':
    specify="-s" in sys.argv or "--specify" in sys.argv
    ipv6="-6" in sys.argv or "--ipv6" in sys.argv
    main(specify,ipv6)
