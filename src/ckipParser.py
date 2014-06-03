# -*- coding: utf-8 -*-
from splinter import Browser
import re
from sys import argv
import time
import requests
from util import *
from buildtree import run_parser


class CkipParser(object):
    def __init__(self):
        self._sleep=1
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

    def sinica_parse(self, raw_str, run_type="browser"):
        if run_type == "browser":
            with Browser('chrome') as browser:
                browser.visit("http://parser.iis.sinica.edu.tw/")
                textarea=browser.find_by_xpath("//form[2]/table[1]/tbody[1]/tr[1]/td[1]/textarea[1]")
                textarea.fill(to_unicode(raw_str))
                parse_button=browser.find_by_xpath("//form[2]/table[1]/tbody[1]/tr[1]/td[1]/input[1]")
                parse_button.click()
                time.sleep(self._sleep)
                raw_result=browser.find_by_xpath("//table[@id='data_table']/tbody/tr/td/nobr")
                #print raw_result
                array_result=[]
                for rsl in raw_result:
                    str_result=re.match("#[^S]+(S[^#]+)#.*",rsl.text)
                    if str_result:
                        array_result.append(str_result.group(1))
                return array_result
        else:
            pass
            
    def sinica_parse_0(self, raw_str, run_type="browser"):
        return  self.sinica_parse(raw_str,run_type)[0]

    def sinica_parse_print_0(self, raw_str, run_type="browser"):
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
    pass
    #target_str=argv[1]
    #result=sinica_parse(target_str)
    #for rsl in result:
    #    print rsl 

def build_tree():
    pass

if __name__=="__main__":
    main()

