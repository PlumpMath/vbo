#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo import APIClient
import urllib,httplib,cookielib,urllib2

class weibo( object ):
    def __init__(self,APP_KEY,APP_SECRET,CALLBACK_URL,ACCOUNT,PASSWORD):
        self.client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        self.APP_KEY = APP_KEY
        self.APP_SECRET = APP_SECRET
        self.CALLBACK_URL = CALLBACK_URL
        self.ACCOUNT = ACCOUNT
        self.PASSWORD = PASSWORD
        #最终获得的access token
        self.TOKEN = ''
        self.EXPIRES = -1
        cj = cookielib.CookieJar()
        proxies = {"http":"host","https":"host"}
        self.opener = urllib2.build_opener(urllib2.ProxyHandler(proxies),urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(self.opener)
        self.opener.addheaders = [('User-agent', 'IE')]

    def __getCode(self):
        '''
        自动获得认证码
        '''
        url = self.client.get_authorize_url()
        conn = httplib.HTTPSConnection('host',80)
        conn.set_tunnel('api.weibo.com',443)
        conn.connect()
        postdata = urllib.urlencode({'client_id':self.APP_KEY,'response_type':'code','redirect_uri':self.CALLBACK_URL,'action':'submit','userId':self.ACCOUNT,'passwd':self.PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
        conn.request('POST','/oauth2/authorize',postdata,{'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
        res = conn.getresponse()
        print 'headers===========',res.getheaders()
        print 'msg===========',res.msg
        print 'status===========',res.status
        print 'reason===========',res.reason
        print 'version===========',res.version
        location = res.getheader('location')
        print location
        if location is None:
            print u'登陆微博失败，请检查用户名和密码'
            return False

        code = location.split('=')[1]
        conn.close()
        #print code
        return code

    def auth(self):
        '''
        微博登陆认证
        '''
        if self.TOKEN == '':
            code = self.__getCode()
            if code == False:
                return
            r = self.client.request_access_token(code)
            self.TOKEN = r.access_token
            self.EXPIRES = r.expires_in

        #print self.TOKEN

        #有了access_token后，可以做任何事情了
        self.client.set_access_token(self.TOKEN, self.EXPIRES)
        return True

    def send(self,text):
        '''
        发送微博
        '''
        self.client.statuses.update.post(status=text)

APP_KEY = '962858254' #youre app key 
APP_SECRET = '77a13dbdd8b8514c812d84fd6e12a53c' #youre app secret  
CALLBACK_URL = 'http://www.scottqian.com'
ACCOUNT = 'mail'#your email address
PASSWORD = 'pas'     #your pw

w = weibo(APP_KEY,APP_SECRET,CALLBACK_URL,ACCOUNT,PASSWORD)
if w.auth():
    #w.send('在vim中发微博测试')
    pass
#print client.statuses.user_timeline.get()
