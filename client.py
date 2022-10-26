# -*- coding: utf-8 -*-
import base64
import json

try:
    import urllib
    import urllib2
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib import urlencode
    is_python3 = False
except:
    from urllib.request import Request
    from urllib.parse import urlencode
    from urllib.request import urlopen
    is_python3 = True


class Client:
    def __init__(self,email,key):
        self.email = email
        self.key = key
        self.base_url = "https://fofa.info"
        self.search_api_url = "/api/v1/search/all"
        self.login_api_url = "/api/v1/info/my"
        self.get_userinfo() #check email and key

    def get_userinfo(self):
        api_full_url = "%s%s" % (self.base_url,self.login_api_url)
        param = {"email":self.email,"key":self.key}
        res = self.__http_get(api_full_url,param)
        return json.loads(res)

    def get_data(self,query_str,page=1,fields="", size=100):
        res = self.get_json_data(query_str,page,fields,size)
        return json.loads(res)

    def get_json_data(self,query_str,page=1,fields="",size=100):
        api_full_url = "%s%s" % (self.base_url,self.search_api_url)
        param = {"qbase64":base64.b64encode(query_str.encode()),"email":self.email,"key":self.key,"page":page,"fields":fields, "size":str(size)}
        res = self.__http_get(api_full_url,param)
        return res


    def __http_get(self,url,param):
        param = urlencode(param)
        url = "%s?%s" % (url,param)
        try:
            req = Request(url)
            res = urlopen(url).read()
            #res = Request.urlopen(url).read()
            if is_python3:
                res = res.decode()
            if "errmsg" in res:
                raise RuntimeError(res)
        except Exception as e:
            print('errmag:\n')
            print(e)
            raise e
        return res
