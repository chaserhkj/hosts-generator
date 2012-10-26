#!/usr/bin/env python2
import urllib2
import socket
import re

time_out=5
output_file="./ip"
base_ip="203.208.47."

def main():
    socket.setdefaulttimeout(time_out)
    for i in range(1,256):
        ip=base_ip+str(i)
        try:
            res=urllib2.urlopen("http://%s/"%ip)
        except Exception as e:
            print "IP %s ; Error Occourred:"%ip
            print e
            continue
        if re.search("<title>Google</title>",res.read())!=None:
            print "IP %s ; Accepted."%ip
            with open(output_file,"a") as f:
                f.write(ip+"\n")
        else:
            print "IP %s ; Discarded."%ip


if __name__ == '__main__':
    main()
