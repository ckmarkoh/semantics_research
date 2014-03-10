# -*- coding: utf-8 -*-
from splinter import Browser
import re

def sinica_parse(raw_str):
    with Browser() as browser:
        browser.visit("http://parser.iis.sinica.edu.tw/")
        textarea=browser.find_by_xpath("//form[2]/table[1]/tbody[1]/tr[1]/td[1]/textarea[1]")
        textarea.fill(raw_str)
        parse_button=browser.find_by_xpath("//form[2]/table[1]/tbody[1]/tr[1]/td[1]/input[1]")
        parse_button.click()
        raw_result=browser.find_by_xpath("//table[@id='data_table']/tbody/tr/td/nobr")
        array_result=[]
        for rsl in raw_result:
            str_result=re.match("#[^S]+(S[^#]+)#.*",rsl.text)
            if str_result:
                array_result.append(str_result.group(1))
        return array_result


def main():
    target_str=u"小明玩棒球。小華今天很早就起床了。"
    result=sinica_parse(target_str)
    print result

def build_tree():
    pass

if __name__=="__main__":
    main()

