#!/usr/bin/env python2

import urllib2

hosts_list="./host_names"
ips_list="./ip"
error_out="./error_out"
output_file="./hosts"

def main():
    with open(hosts_list) as f:
        hosts=f.read().split("\n")
        hosts=[i for i in hosts if i]
    with open(ips_list) as f:
        ips=f.read().split("\n")
        ips=[i for i in ips if i]
    with open(error_out) as f:
        eo=f.read()
    d={}
    for i in hosts:
        ipi=iter(ips)
        while True:
            try:
                ip=ipi.next()
            except StopIteration:
                print "Host %s ; No IP Matched."%i
                print "Discard Host %s"%i
                break
            req=urllib2.Request(url="http://%s/"%ip,
                                headers={"Hosts":i})
            try:
                res=urllib2.urlopen(req)
            except Exception as e:
                print "Host %s ; IP %s ; Error Occurred:"%(i,ip)
                print e
                continue
            if res.read()!=eo:
                print "Host %s ; IP %s ; Matched!"%(i,ip)
                d[i]=ip
                break
            else:
                print "Host %s ; IP %s ; Not Matched!"%(i,ip)
    with open(output_file,'w') as f:
        f.wrtie("\n".join("\t".join(i) for i in d.items()))


if __name__ == '__main__':
    main()
