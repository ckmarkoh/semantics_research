#-*- coding:utf-8 -*-
import requests

class RequestInterface(object):
    def __init__(self):
       self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Accept-Encoding': 'gzip,deflate,sdch'
            }
    def request_post(self,url,data,encoding='utf-8'):
        r = requests.post(url,
                          data = data, 
                          headers = self.headers)
        r.encoding = encoding
        return r.text

    def request_get(self,url,data,encoding='utf-8'):
        r = requests.get(url, 
                         data = data, 
                         headers = self.headers)
        r.encoding = encoding
        return r.text
