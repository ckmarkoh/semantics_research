#-*- coding:utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*
import copy
import re
import requests
from util import *

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Accept-Encoding': 'gzip,deflate,sdch'
}

class GoogleSearcher(object):
    def __init__(self):
        self.url = "http://www.google.com.tw/search"
        self.xpath_abs = "//span[@class='st']//text()"
        self.xpath_title = "//h3[@class='r']//text()"
        pass
    
    def get_html(self,url,params):
        r = requests.get(url, params=params, headers=HEADERS)
        html = r.text
        return html

    def parse_html(self,html):
        result1 = xpath_parse_all(html,self.xpath_title)
        result2 = xpath_parse_all(html,self.xpath_abs)
        return map(lambda x: "%s %s"%(x[0],x[1]), zip(result1,result2))
        
    def get_search_result(self,word,limit=3):
        params = {'q': word, 'hl': 'zh-TW','filter':'0'}
        result = []
        for i in range(limit):
            params.update({'start':'%s'%(i*10)})            
            html = self.get_html(self.url,params)
            result.extend( self.parse_html(html))
        return result
    

if __name__ == "__main__":
   #result = GoogleSearcher().get_search_result("陽明山")
   print "\n".join(GoogleSearcher().get_search_result("陽明山")).encode('utf-8')


