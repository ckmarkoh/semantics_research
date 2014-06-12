# -*- coding: utf-8 -*-
from splinter import Browser
import re
from sys import argv
import time
import requests
from util import *
from buildtree import run_parser
from urlparse import urlparse,urljoin

import urllib, urllib2, cookielib

class CkipParser(object):
    def __init__(self):
        self._sleep = 0
        self._url = "http://parser.iis.sinica.edu.tw/"


   #     self._headers = {
   #         'User-Agent':
   #             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
   #              AppleWebKit/537.36 (KHTML, like Gecko) \
   #              Chrome/27.0.1453.93 Safari/537.36',
   #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   #         'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
   #         'Accept-Encoding': 'gzip,deflate,sdch'
   #     }
   # def request_post(url, data, self.headers=__HEADERS ):
   #     post = requests.post
   #     r = post(url, data=data, headers=headers )
   #     return r

    def read_data_from_browser(self, raw_str):
        with Browser('chrome') as browser:
            browser.visit(self._url)
            textarea=browser.find_by_xpath("//form[2]/table[1]/tbody[1]/tr[1]/td[1]/textarea[1]")
            textarea.fill(to_unicode(raw_str))
            parse_button=browser.find_by_xpath("//form[2]/table[1]/tbody[1]/tr[1]/td[1]/input[1]")
            parse_button.click()
            time.sleep(self._sleep)
            raw_result=browser.find_by_xpath("//table[@id='data_table']/tbody/tr/td/nobr")
        return raw_result

    def read_data_from_urllib(self, raw_str):
        input_str = to_unicode(raw_str)
        string = input_str.encode('cp950')
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 Gecko/20100101 Firefox/29.0'),
            ('referer', self._url), ('Host', urlparse(self._url).netloc)
        ]
        pre_page = urllib.urlopen(self._url).read()
        fid = re.search('name="id" value="(\d+)"', pre_page).group(1)
        postdata = urllib.urlencode({ 'myTag':string,'id':fid})
        html = opener.open(urljoin(self._url,'svr/webparser.asp'), postdata).read().decode('cp950')
        raw_result = xpath_parse_all(html,"//table[@id='data_table']/tr/td/nobr")
        return raw_result

    def sinica_parse(self, raw_str, run_type="urllib"):
        array_result = []
        while len(array_result) == 0 :
            print "connect ckip"
            if run_type == "browser":
                raw_result = self.read_data_from_browser(raw_str)
            elif run_type == "urllib":
                raw_result = self.read_data_from_urllib(raw_str)
            else:
                assert 0
        for rsl in raw_result:
            str_result=re.match("#[^S]+(S[^#]+)#.*",rsl.text)
            if str_result:
                array_result.append(str_result.group(1))
        return array_result
            
    def sinica_parse_0(self, raw_str, run_type="urllib"):
        return  self.sinica_parse(raw_str,run_type)[0]

    def sinica_parse_print_0(self, raw_str, run_type="urllib"):
        str_tree = self.sinica_parse_0(raw_str,run_type)
        print to_utf8_str(str_tree )
        return str_tree 

    def str_raw_to_str_tree(self, raw_str ,to_print=True):
        if to_print:
            return self.sinica_parse_print_0(raw_str)
        else:
            return self.sinica_parse_0(raw_str)

    def str_tree_to_tree(self, str_tree):
        str_tree_re = re.search(r"#[0-9.:]*\[[0-9]\] ([^#]+)#",str_tree)
        if str_tree_re:
            str_tree = str_tree_re.group(1)
            print str_tree
        return run_parser(str_tree)




def main():
    #print CkipParser().sinica_parse(u"馬英九在中研院發表演講")
    pass
    #target_str=argv[1]
    #result=sinica_parse(target_str)
    #for rsl in result:
    #    print rsl 

def build_tree():
    pass

if __name__=="__main__":
    main()

