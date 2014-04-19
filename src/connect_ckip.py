# -*- coding: utf-8 -*-
from splinter import Browser
import re
from sys import argv
import time
import requests


_SLEEP=1

__HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
         AppleWebKit/537.36 (KHTML, like Gecko) \
         Chrome/27.0.1453.93 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Accept-Encoding': 'gzip,deflate,sdch'
}



def request_post(url, data, headers=__HEADERS ):
    #if __DELAY :
    #    time.sleep(offset+(sleep*random()))
        #time.sleep(__SLEEP)
    post = requests.post
    r = post(url, data=data, headers=headers )
    return r


def sinica_parse(raw_str,run_type="browser"):
    if run_type == "browser":
        with Browser('chrome') as browser:
            browser.visit("http://parser.iis.sinica.edu.tw/")
            textarea=browser.find_by_xpath("//form[2]/table[1]/tbody[1]/tr[1]/td[1]/textarea[1]")
            textarea.fill(raw_str.decode('utf-8'))
            parse_button=browser.find_by_xpath("//form[2]/table[1]/tbody[1]/tr[1]/td[1]/input[1]")
            parse_button.click()
            time.sleep(_SLEEP)
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
        


def main():
    target_str=argv[1]
    result=sinica_parse(target_str)
    for rsl in result:
        print rsl 

def build_tree():
    pass

if __name__=="__main__":
    main()

