#!/usr/bin/env python2


#Configuration Start
base_ip="203.208.46."
output_file="/usr/tmp/hosts"
random_range=5
time_out=5
thread_count=10
#Configuration End

#Check IP Script Start
import urllib2
import socket
import re
import time
import sys
import Queue
import threading
import random


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
        print_lock.acquire()
        print "Thread %d:Initializing..."%self.__num
        print_lock.release()
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

def check_ip():
    global ips,data_lock,print_lock
    socket.setdefaulttimeout(time_out)
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

    top=256
    for i in range(1,top):
        ip=base_ip+str(i)
        queue.put(ip)

    queue.join()

    ts=ips.keys()
    ts.sort()
    f=[ips[i].strip("[]") for i in ts ]
    print "IP Checking finished."
    return f

#Check IP Script End


# Needed data in hosts generating START
hosts=[
 '0.docs.google.com',
 '0.drive.google.com',
 '1.docs.google.com',
 '1.drive.google.com',
 '10.docs.google.com',
 '10.drive.google.com',
 '11.docs.google.com',
 '11.drive.google.com',
 '12.docs.google.com',
 '12.drive.google.com',
 '13.docs.google.com',
 '13.drive.google.com',
 '14.docs.google.com',
 '14.drive.google.com',
 '15.docs.google.com',
 '15.drive.google.com',
 '16.docs.google.com',
 '16.drive.google.com',
 '2.docs.google.com',
 '2.drive.google.com',
 '3.docs.google.com',
 '3.drive.google.com',
 '4.docs.google.com',
 '4.drive.google.com',
 '5.docs.google.com',
 '5.drive.google.com',
 '6.docs.google.com',
 '6.drive.google.com',
 '7.docs.google.com',
 '7.drive.google.com',
 '8.docs.google.com',
 '8.drive.google.com',
 '9.docs.google.com',
 '9.drive.google.com',
 'accounts.google.com',
 'accounts.l.google.com',
 'answers.google.com',
 'apis.google.com',
 'appengine.google.com',
 'apps.google.com',
 'appspot.l.google.com',
 'bks0.books.google.com',
 'bks1.books.google.com',
 'bks10.books.google.com',
 'bks2.books.google.com',
 'bks3.books.google.com',
 'bks4.books.google.com',
 'bks5.books.google.com',
 'bks6.books.google.com',
 'bks7.books.google.com',
 'bks8.books.google.com',
 'bks9.books.google.com',
 'blogsearch.google.com',
 'books.google.com',
 'browserchannel-docs.l.google.com',
 'browserchannel-spreadsheets.l.google.com',
 'browsersync.google.com',
 'browsersync.l.google.com',
 'buzz.google.com',
 'cache.l.google.com',
 'cache.pack.google.com',
 'calendar.google.com',
 'cbk0.google.com',
 'cbk1.google.com',
 'cbk2.google.com',
 'cbk3.google.com',
 'cbks0.google.com',
 'cbks1.google.com',
 'cbks2.google.com',
 'cbks3.google.com',
 'chart.apis.google.com',
 'chatenabled.mail.google.com',
 'checkout.google.com',
 'checkout.l.google.com',
 'chrome.google.com',
 'clients.l.google.com',
 'clients1.google.com',
 'clients2.google.com',
 'clients3.google.com',
 'clients4.google.com',
 'clients5.google.com',
 'clients6.google.com',
 'clients7.google.com',
 'code.google.com',
 'code.l.google.com',
 'csi.l.google.com',
 'desktop.google.com',
 'desktop.l.google.com',
 'desktop2.google.com',
 'developers.google.com',
 'ditu.google.com',
 'dl.google.com',
 'dl.l.google.com',
 'dl-ssl.google.com',
 'docs.google.com',
 'docs0.google.com',
 'docs1.google.com',
 'docs2.google.com',
 'docs3.google.com',
 'docs4.google.com',
 'docs5.google.com',
 'docs6.google.com',
 'docs7.google.com',
 'docs8.google.com',
 'docs9.google.com',
 'drive.google.com',
 'earth.google.com',
 'encrypted.google.com',
 'encrypted-tbn.l.google.com',
 'encrypted-tbn0.google.com',
 'encrypted-tbn1.google.com',
 'encrypted-tbn2.google.com',
 'encrypted-tbn3.google.com',
 'feedburner.google.com',
 'feedproxy.google.com',
 'filetransferenabled.mail.google.com',
 'finance.google.com',
 'fusion.google.com',
 'geoauth.google.com',
 'gg.google.com',
 'ghs.google.com',
 'ghs.l.google.com',
 'ghs46.google.com',
 'ghs46.l.google.com',
 'google.com',
 'googleapis.l.google.com',
 'googleapis-ajax.google.com',
 'googleapis-ajax.l.google.com',
 'googlecode.l.google.com',
 'google-public-dns-a.google.com',
 'google-public-dns-b.google.com',
 'goto.google.com',
 'groups.google.com',
 'groups.l.google.com',
 'groups-beta.google.com',
 'gxc.google.com',
 'id.google.com',
 'id.l.google.com',
 'images.google.com',
 'images.l.google.com',
 'investor.google.com',
 'jmt0.google.com',
 'kh.google.com',
 'kh.l.google.com',
 'khm.google.com',
 'khm.l.google.com',
 'khm0.google.com',
 'khm1.google.com',
 'khm2.google.com',
 'khm3.google.com',
 'khmdb.google.com',
 'khms.google.com',
 'khms.l.google.com',
 'khms0.google.com',
 'khms1.google.com',
 'khms2.google.com',
 'khms3.google.com',
 'labs.google.com',
 'large-uploads.l.google.com',
 'lh2.google.com',
 'lh2.l.google.com',
 'lh3.google.com',
 'lh4.google.com',
 'lh5.google.com',
 'lh6.google.com',
 'linkhelp.clients.google.com',
 'local.google.com',
 'm.google.com',
 'mail.google.com',
 'map.google.com',
 'maps.google.com',
 'maps.l.google.com',
 'maps-api-ssl.google.com',
 'mars.google.com',
 'mobile.l.google.com',
 'mobile-gtalk.l.google.com',
 'mobilemaps.clients.google.com',
 'mt.google.com',
 'mt.l.google.com',
 'mt0.google.com',
 'mt1.google.com',
 'mt2.google.com',
 'mt3.google.com',
 'mtalk.google.com',
 'mts.google.com',
 'mts.l.google.com',
 'mts0.google.com',
 'mts1.google.com',
 'mts2.google.com',
 'mts3.google.com',
 'music.google.com',
 'music-streaming.l.google.com',
 'mw1.google.com',
 'mw2.google.com',
 'news.google.com',
 'news.l.google.com',
 'pack.google.com',
 'photos.google.com',
 'photos-ugc.l.google.com',
 'picasa.google.com',
 'picasaweb.google.com',
 'picasaweb.l.google.com',
 'places.google.com',
 'play.google.com',
 'productforums.google.com',
 'profiles.google.com',
 'reader.google.com',
 'safebrowsing.cache.l.google.com',
 'safebrowsing.clients.google.com',
 'safebrowsing.google.com',
 'safebrowsing-cache.google.com',
 'sandbox.google.com',
 'sb.google.com',
 'sb.l.google.com',
 'sb-ssl.google.com',
 'sb-ssl.l.google.com',
 'scholar.google.com',
 'scholar.l.google.com',
 'script.google.com',
 'services.google.com',
 'sites.google.com',
 'sketchup.google.com',
 'sketchup.l.google.com',
 'spreadsheet.google.com',
 'spreadsheets.google.com',
 'spreadsheets.l.google.com',
 'spreadsheets0.google.com',
 'spreadsheets1.google.com',
 'spreadsheets2.google.com',
 'spreadsheets3.google.com',
 'spreadsheets4.google.com',
 'spreadsheets5.google.com',
 'spreadsheets6.google.com',
 'spreadsheets7.google.com',
 'spreadsheets8.google.com',
 'spreadsheets9.google.com',
 'spreadsheets-china.l.google.com',
 'suggestqueries.google.com',
 'suggestqueries.l.google.com',
 'support.google.com',
 'talkgadget.google.com',
 'tbn0.google.com',
 'tbn1.google.com',
 'tbn2.google.com',
 'tbn3.google.com',
 'toolbar.google.com',
 'toolbarqueries.clients.google.com',
 'toolbarqueries.google.com',
 'toolbarqueries.l.google.com',
 'tools.google.com',
 'tools.l.google.com',
 'translate.google.com',
 'trends.google.com',
 'upload.docs.google.com',
 'upload.drive.google.com',
 'uploads.code.google.com',
 'uploadsj.clients.google.com',
 'video.google.com',
 'video-stats.l.google.com',
 'voice.google.com',
 'wallet.google.com',
 'wifi.google.com',
 'wifi.l.google.com',
 'wire.l.google.com',
 'writely.google.com',
 'writely.l.google.com',
 'writely-china.l.google.com',
 'writely-com.l.google.com',
 'www.google.com',
 'www.l.google.com',
 'www2.l.google.com',
 'www3.l.google.com',
 'www4.l.google.com',
 'ytstatic.l.google.com',
 '0-open-opensocial.googleusercontent.com',
 '0-focus-opensocial.googleusercontent.com',
 '1-focus-opensocial.googleusercontent.com',
 '1-open-opensocial.googleusercontent.com',
 '1-ps.googleusercontent.com',
 '2-focus-opensocial.googleusercontent.com',
 '2-open-opensocial.googleusercontent.com',
 '2-ps.googleusercontent.com',
 '3-focus-opensocial.googleusercontent.com',
 '3-ps.googleusercontent.com',
 '3hdrrlnlknhi77nrmsjnjr152ueo3soc-a-calendar-opensocial.googleusercontent.com',
 '3-open-opensocial.googleusercontent.com',
 '4-ps.googleusercontent.com',
 '4fjvqid3r3oq66t548clrdj52df15coc-a-oz-opensocial.googleusercontent.com',
 '53rd6p0catml6vat6qra84rs0del836d-a-oz-opensocial.googleusercontent.com',
 '59cbv4l9s05pbaks9v77vc3mengeqors-a-oz-opensocial.googleusercontent.com',
 '8kubpeu8314p2efdd7jlv09an9i2ljdo-a-oz-opensocial.googleusercontent.com',
 'adstvca8k2ooaknjjmv89j22n9t676ve-a-oz-opensocial.googleusercontent.com',
 'a-oz-opensocial.googleusercontent.com',
 'blogger.googleusercontent.com',
 'bt26mravu2qpe56n8gnmjnpv2inl84bf-a-oz-opensocial.googleusercontent.com',
 'clients1.googleusercontent.com',
 'clients2.googleusercontent.com',
 'clients3.googleusercontent.com',
 'clients4.googleusercontent.com',
 'clients5.googleusercontent.com',
 'clients6.googleusercontent.com',
 'clients7.googleusercontent.com',
 'code-opensocial.googleusercontent.com',
 'debh8vg7vd93bco3prdajidmm7dhql3f-a-oz-opensocial.googleusercontent.com',
 'doc-00-7o-docs.googleusercontent.com',
 'doc-08-7o-docs.googleusercontent.com',
 'doc-0c-7o-docs.googleusercontent.com',
 'doc-0g-7o-docs.googleusercontent.com',
 'doc-0s-7o-docs.googleusercontent.com',
 'doc-10-7o-docs.googleusercontent.com',
 'doc-14-7o-docs.googleusercontent.com',
 'feedback.googleusercontent.com',
 'googlehosted.l.googleusercontent.com',
 'hsco54a20sh11q9jkmb51ad2n3hmkmrg-a-oz-opensocial.googleusercontent.com',
 'i8brh95qor6r54nkl52hidj2ggcs4jgm-a-oz-opensocial.googleusercontent.com',
 'images1-focus-opensocial.googleusercontent.com',
 'images2-focus-opensocial.googleusercontent.com',
 'images3-focus-opensocial.googleusercontent.com',
 'images4-focus-opensocial.googleusercontent.com',
 'images5-focus-opensocial.googleusercontent.com',
 'images6-focus-opensocial.googleusercontent.com',
 'images7-focus-opensocial.googleusercontent.com',
 'images8-focus-opensocial.googleusercontent.com',
 'images9-focus-opensocial.googleusercontent.com',
 'images-docs-opensocial.googleusercontent.com',
 'k6v18tjr24doa89b55o3na41kn4v73eb-a-oz-opensocial.googleusercontent.com',
 'lh1.googleusercontent.com',
 'lh2.googleusercontent.com',
 'lh3.googleusercontent.com',
 'lh4.googleusercontent.com',
 'lh5.googleusercontent.com',
 'lh6.googleusercontent.com',
 'mail-attachment.googleusercontent.com',
 'music.googleusercontent.com',
 'music-onebox.googleusercontent.com',
 'oauth.googleusercontent.com',
 'ob7f2qc0i50kbjnc81vkhgmb5hsv7a8l-a-oz-opensocial.googleusercontent.com',
 'ode25pfjgmvpquh3b1oqo31ti5ibg5fr-a-calendar.opensocial.googleusercontent.com',
 'qhie5b8u979rnch1q0hqbrmbkn9estf7-a-oz-opensocial.googleusercontent.com',
 'r70rmsn4s0rhk6cehcbbcbfbs31pu0va-a-oz-opensocial.googleusercontent.com',
 'rbjhe237k979f79d87gmenp3gejfonu9-a-oz-opensocial.googleusercontent.com',
 's1.googleusercontent.com',
 's2.googleusercontent.com',
 's3.googleusercontent.com',
 's4.googleusercontent.com',
 's5.googleusercontent.com',
 's6.googleusercontent.com',
 'spreadsheets-opensocial.googleusercontent.com',
 't.doc-0-0-sj.sj.googleusercontent.com',
 'themes.googleusercontent.com',
 'translate.googleusercontent.com',
 'u807isd5egseeabjccgcns005p2miucq-a-oz-opensocial.googleusercontent.com',
 'upt14k1i2veesusrda9nfotcrbp9d7p5-a-oz-opensocial.googleusercontent.com',
 'webcache.googleusercontent.com',
 'www.googleusercontent.com',
 'www-calendar-opensocial.googleusercontent.com',
 'www-fc-opensocial.googleusercontent.com',
 'www-focus-opensocial.googleusercontent.com',
 'www-gm-opensocial.googleusercontent.com',
 'www-kix-opensocial.googleusercontent.com',
 'www-open-opensocial.googleusercontent.com',
 'www-opensocial.googleusercontent.com',
 'www-opensocial-sandbox.googleusercontent.com',
 'www-oz-opensocial.googleusercontent.com',
 'csi.gstatic.com',
 'g0.gstatic.com',
 'g1.gstatic.com',
 'g2.gstatic.com',
 'g3.gstatic.com',
 'maps.gstatic.com',
 'mt0.gstatic.com',
 'mt1.gstatic.com',
 'mt2.gstatic.com',
 'mt3.gstatic.com',
 'mt4.gstatic.com',
 'mt5.gstatic.com',
 'mt6.gstatic.com',
 'mt7.gstatic.com',
 'ssl.gstatic.com',
 't0.gstatic.com',
 't1.gstatic.com',
 't2.gstatic.com',
 't3.gstatic.com',
 'www.gstatic.com',
 'lh1.ggpht.com',
 'lh2.ggpht.com',
 'lh3.ggpht.com',
 'lh4.ggpht.com',
 'lh5.ggpht.com',
 'lh6.ggpht.com',
 'nt0.ggpht.com',
 'nt1.ggpht.com',
 'nt2.ggpht.com',
 'nt3.ggpht.com',
 'nt4.ggpht.com',
 'nt5.ggpht.com',
 'appspot.com',
 'chrometophone.appspot.com',
 'evolutionofweb.appspot.com',
 'googcloudlabs.appspot.com',
 'gv-gadget.appspot.com',
 'magnifier.blogspot.com',
 'moderator.appspot.com',
 'newsfeed-dot-latest-dot-rovio-ad-engine.appspot.com',
 'productideas.appspot.com',
 'project-slingshot-gp.appspot.com',
 'r2303.latest.project-slingshot-hr.appspot.com',
 'r3085-dot-latest-dot-project-slingshot-gp.appspot.com',
 'r3091-dot-latest-dot-project-slingshot-gp.appspot.com',
 'r3101-dot-latest-dot-project-slingshot-gp.appspot.com',
 'r3269-dot-latest-dot-project-slingshot-gp.appspot.com',
 'r3432-dot-latest-dot-project-slingshot-hr.appspot.com',
 'r4681-dot-latest-dot-project-slingshot-hr.appspot.com',
 'r7647-dot-latest-dot-project-slingshot-hr.appspot.com',
 'wcproxyx.appspot.com',
 'www.appspot.com',
 'ajax.googleapis.com',
 'chart.googleapis.com',
 'fonts.googleapis.com',
 'maps.googleapis.com',
 'mt0.googleapis.com',
 'mt1.googleapis.com',
 'mt2.googleapis.com',
 'mt3.googleapis.com',
 'redirector-bigcache.googleapis.com',
 'translate.googleapis.com',
 'www.googleapis.com',
 'autoproxy-gfwlist.googlecode.com',
 'chromium.googlecode.com',
 'closure-library.googlecode.com',
 'earth-api-samples.googlecode.com',
 'gmaps-samples-flash.googlecode.com',
 'google-code-feed-gadget.googlecode.com',
 'blogsearch.google.cn',
 'ditu.google.cn',
 'gg.google.cn',
 'id.google.cn',
 'maps.gstatic.cn',
 'm.google.cn',
 'mt.google.cn',
 'mt0.google.cn',
 'mt1.google.cn',
 'mt2.google.cn',
 'mt3.google.cn',
 'news.google.cn',
 'scholar.google.cn',
 'translate.google.cn',
 'www.google.cn',
 'www.gstatic.cn',
 'accounts.google.com.hk',
 'blogsearch.google.com.hk',
 'books.google.com.hk',
 'clients1.google.com.hk',
 'desktop.google.com.hk',
 'encrypted.google.com.hk',
 'groups.google.com.hk',
 'gxc.google.com.hk',
 'id.google.com.hk',
 'images.google.com.hk',
 'm.google.com.hk',
 'maps.google.com.hk',
 'news.google.com.hk',
 'picasaweb.google.com.hk',
 'plus.url.google.com.hk',
 'scholar.google.com.hk',
 'toolbar.google.com.hk',
 'toolbarqueries.google.com.hk',
 'translate.google.com.hk',
 'translate.google.com.hk',
 'wenda.google.com.hk',
 'www.google.com.hk',
 'android.googlesource.com',
 'auth.keyhole.com',
 'chrome.angrybirds.com',
 'chromium.org',
 'codereview.chromium.org',
 'dev.chromium.org',
 'developer.android.com',
 'developer.chrome.com',
 'domains.googlesyndication.com',
 'earthengine.googlelabs.com',
 'feeds.feedburner.com',
 'g.co',
 'gmail.com',
 'goo.gl',
 'listen.googlelabs.com',
 'm.gmail.com',
 'm.googlemail.com',
 'market.android.com',
 'ngrams.googlelabs.com',
 'ssl.google-analytics.com',
 'www.chromium.org',
 'www.gmail.com',
 'www.googleadservices.com',
 'www.google-analytics.com',
 'www.googlelabs.com',
 'www.googlesource.com',
 'plus.google.com',
 'plus.url.google.com',
 'plusone.google.com']

base_hosts='''
#UPDATE:12-10-07 10:08

127.0.0.1	localhost
#SmartHosts START

#Google Services Start
%s
#Google Services End

#Facebook Start
69.171.225.13	api.facebook.com
61.213.189.98	b.static.ak.facebook.com
61.213.189.120	b.static.ak.fbcdn.net
66.220.145.63	bigzipfiles.facebook.com
61.213.189.113	creative.ak.fbcdn.net
184.31.111.139	connect.facebook.net
69.171.227.19	creativeupload.facebook.com
69.171.240.99	d.facebook.com
69.171.234.23	developers.facebook.com
66.220.152.16	facebook.com
61.213.189.113	fbcdn.net
64.213.102.26	fbcdn-profile-a.akamaihd.net
173.223.232.67	fbcdn-sphotos-a.akamaihd.net
69.171.237.18	graph.facebook.com
69.171.240.10	hphotos-ash4.fbcdn.net
66.220.151.22	hphotos-snc6.fbcdn.net
69.171.227.24	hphotos-snc7.fbcdn.net
66.220.144.43	ldap.thefacebook.com
118.214.190.105	profile.ak.facebook.com
61.213.189.114	profile.ak.fbcdn.net
69.171.247.22	s-static.facebook.com
61.213.189.113	s-hprofile-sf2p.fbcdn.net
184.26.194.110	s-static.ak.facebook.com
23.5.157.177	s-static.ak.fbcdn.net
69.63.189.76	star.facebook.com
61.213.189.98	static.ak.facebook.com
69.171.229.17	upload.facebook.com
66.220.144.41	vpn.tfbnw.net
120.29.145.50	vthumb.ak.fbcdn.net
66.220.151.31	vupload.facebook.com
69.171.225.31	www.connect.facebook.com
69.171.234.21	www.facebook.com
69.171.242.72	zh-CN.facebook.com
#Facebook End

#Dropbox START
199.47.217.179	dropbox.com
199.47.216.170	www.dropbox.com
#107.20.207.62	dl.dropbox.com
#107.20.207.62	dl-web.dropbox.com
#Dropbox END

#Flickr START
66.94.233.186	flickr.com
66.94.233.186	www.flickr.com
68.142.214.43	static.flickr.com
69.147.90.159	farm2.static.flickr.com
76.13.18.78	farm3.static.flickr.com
67.195.19.66	farm4.static.flickr.com
76.13.18.79	farm5.static.flickr.com
98.139.197.254	farm6.static.flickr.com
98.139.102.46	farm7.static.flickr.com
98.136.43.76	geo.yahoo.com
68.142.250.161	l.yimg.com
96.6.93.227	s.yimg.com
98.137.88.88	d.yimg.com
68.142.196.57	c5.ah.yahoo.com
124.108.120.124	sa.edit.yahoo.com
66.163.168.247	open.login.yahoo.com
209.191.92.114	login.yahoo.com
209.191.92.115	edit.yahoo.com
209.191.121.31	up.flickr.com
209.191.105.102	adjax.flickr.yahoo.com
204.0.5.35	content.yieldmanager.edgesuite.net
204.0.5.34	us.js2.yimg.com

#data from HostsX
76.13.18.78	bf1.farm3.static.flickr.com
76.13.18.78	farm3.static.flickr.com
76.13.18.78	gq1.farm3.static.flickr.com
76.13.18.78	sp1.farm3.static.flickr.com
76.13.18.79	bf1.farm5.static.flickr.com
76.13.18.79	farm5.static.flickr.com
76.13.18.79	gq1.farm5.static.flickr.com
98.139.102.46	bf1.farm7.static.flickr.com
98.139.102.46	farm7.static.flickr.com
98.139.102.46	gq1.farm7.static.flickr.com
98.139.102.46	ne1.farm7.static.flickr.com
98.139.197.254	bf1.farm6.static.flickr.com
98.139.197.254	farm6.static.flickr.com
98.139.197.254	gq1.farm6.static.flickr.com
#Flickr END

#Adobe Activation START
0.0.0.0	3dns-2.adobe.com
0.0.0.0	3dns-3.adobe.com
0.0.0.0	activate.adobe.com
0.0.0.0	activate-sea.adobe.com
0.0.0.0	activate-sjc0.adobe.com
0.0.0.0	adobe-dns.adobe.com
0.0.0.0	adobe-dns-2.adobe.com
0.0.0.0	adobe-dns-3.adobe.com
0.0.0.0	ereg.adobe.com
0.0.0.0	hl2rcv.adobe.com
0.0.0.0	practivate.adobe.com
0.0.0.0	wip3.adobe.com
0.0.0.0	activate.wip3.adobe.com
0.0.0.0	ereg.wip3.adobe.com
0.0.0.0	wwis-dubc1-vip60.adobe.com
#Adobe Activation END

#Wikipedia START
208.80.152.201	wikipedia.org
208.80.152.201	www.wikipedia.org
208.80.152.201	bits.wikipedia.org
208.80.152.201	en.wikipedia.org
208.80.152.201	zh.wikipedia.org
208.80.152.201	simple.wikipedia.org
208.80.152.201	wikibooks.org
208.80.152.201	www.wikibooks.org
208.80.152.201	en.wikibooks.org
208.80.152.201	zh.wikibooks.org
208.80.152.201	wikinews.org
208.80.152.201	www.wikinews.org
208.80.152.201	en.wikinews.org
208.80.152.201	zh.wikinews.org
208.80.152.201	wikiquote.org
208.80.152.201	www.wikiquote.org
208.80.152.201	en.wikiquote.org
208.80.152.201	zh.wikiquote.org
208.80.152.201	zh.wikisource.org
208.80.152.201	en.wikisource.org
208.80.152.201	wiktionary.org
208.80.152.201	www.wiktionary.org
208.80.152.201	en.wiktionary.org
208.80.152.201	zh.wiktionary.org
208.80.152.201	wikimedia.org
208.80.152.201	www.wikimedia.org
208.80.152.201	bugs.wikimedia.org
208.80.152.201	bugzilla.wikimedia.org
208.80.152.201	commons.wikimedia.org
208.80.152.201	dumps.wikimedia.org
208.80.152.201	download.wikimedia.org
208.80.152.201	irc.wikimedia.org
208.80.152.201	ftp.wikimedia.org
208.80.152.201	ganglia.wikimedia.org
208.80.152.201	mail.wikimedia.org
208.80.152.201	meta.wikimedia.org
208.80.152.201	news.wikimedia.org
208.80.152.201	noc.wikimedia.org
208.80.152.201	kate.wikimedia.org
208.80.152.201	kohl.wikimedia.org
208.80.152.201	stats.wikimedia.org
208.80.152.201	ticket.wikimedia.org
208.80.152.201	tools.wikimedia.org
208.80.152.211	upload.wikimedia.org
208.80.152.201	wikimediafoundation.org
208.80.152.201	www.wikimediafoundation.org
208.80.152.201	mediawiki.org
208.80.152.201	www.mediawiki.org
#Wikipedia END

#YouTube START
203.208.45.206	apiblog.youtube.com
203.208.45.206	help.youtube.com
203.208.45.206	i.ytimg.com
203.208.45.206	i1.ytimg.com
203.208.45.206	i2.ytimg.com
203.208.45.206	i3.ytimg.com
203.208.45.206	i4.ytimg.com
203.208.45.206	insight.youtube.com
203.208.45.206	m.youtube.com
203.208.45.206	s.ytimg.com
203.208.45.206	ytimg.l.google.com
#YouTube END

#SmartHosts END
'''

# Needed data in host generating END

#Generate Hosts Script Start
def generate_hosts(ips):
    if random_range>len(ips):
        raise Exception,"Not enough IPs!"
    out=""
    for i in hosts:
        out=out+"%s\t%s\n"%(ips[random.randrange(random_range)],i)
    print "Writing to %s..."%output_file
    with open(output_file,'w') as f:
        f.write(base_hosts%out)
    print "Finished."
#Generate Hosts Script End
    
if __name__ == '__main__':
    generate_hosts(check_ip())
