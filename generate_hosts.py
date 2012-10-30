#!/usr/bin/env python2

import urllib2
import sys
import random
import socket

hosts_list="./host_names"
ips_list="./ip"
error_out="./error_out"
output_file="./hosts"

ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4"
time_out=5

def main(no_check=False):
    socket.setdefaulttimeout(time_out)
    with open(hosts_list) as f:
        hosts=f.read().split("\n")
        hosts=[i for i in hosts if i]
    with open(ips_list) as f:
        ips=f.read().split("\n")
        ips=[i for i in ips if i]

    if no_check:
        num=int(raw_input("Enter the range to choose IP in:"))
        if num>len(ips):
            raise Exception,"Not enough IPs!"
        print "Writing to file..."
        with open(output_file,'w') as f:
            for i in hosts:
                f.write("%s\t%s\n"%(ips[random.randrange(num)],i))
        print "Finished."
        return

    with open(error_out) as f:
        eo=f.read()
    d={}
    for i in hosts:
        for mode in ["http","https"]:
            print "Host %s ; Start checking in mode %s."%(i,mode)
            ipi=iter(ips)
            passed=False
            while True:
                try:
                    ip=ipi.next()
                except StopIteration:
                    print "Host %s ; No IP Matched in %s mode."%(i,mode)
                    break
                req=urllib2.Request(url="%s://%s/"%(mode,ip),
                                    headers={"Host":i,
                                             "User-Agent":ua})
                try:
                    res=urllib2.urlopen(req)
                    if res.read()!=eo:
                        print "Host %s ; IP %s ; Matched!"%(i,ip)
                        passed=True
                        d[i]=ip
                        break
                    else:
                        print "Host %s ; IP %s ; Not Matched!"%(i,ip)
                except Exception as e:
                    print "Host %s ; IP %s ; Error Occurred:"%(i,ip)
                    print e
                    continue
            if passed:
                break
        if not passed:
            print "Discard Host %s."%i

    with open(output_file,'w') as f:
        f.write("\n".join("\t".join(i) for i in d.items()))


if __name__ == '__main__':
    no_check="-n" in sys.argv or "--no-check" in sys.argv
    main(no_check)
