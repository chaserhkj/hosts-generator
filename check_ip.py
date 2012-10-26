#!/usr/bin/env python2
import urllib2
import socket
import re
import time

time_out=5
output_file="./ip"
base_ip="203.208.47."

def main():
    socket.setdefaulttimeout(time_out)
    ips={}
    for i in range(1,256):
        ip=base_ip+str(i)
        try:
            time1=time.time()
            res=urllib2.urlopen("http://%s/"%ip)
            time2=time.time()
            t=time2-time1
            if re.search("<title>Google</title>",res.read())!=None:
                print "IP %s ; TIME %f ms ; Accepted."%(ip,t*1000)
                ips[t]=ip
            else:
                print "IP %s ; Discarded."%ip
        except Exception as e:
            print "IP %s ; Error Occourred:"%ip
            print e
    ts=ips.keys().sort()
    with open(output_file,"a") as f:
        f.write("\n".join(ips[i] for i in ts ))

if __name__ == '__main__':
    main()
