#-*- coding:utf-8 -*-
from httpInterface import RequestInterface
from util import * 
import re

class ClsaInterface(object):

    def __init__(self):
        self.interface = RequestInterface()
        self.url= "http://www.lsa.url.tw/modules/lsa/lsa_pairwise_comparison.php"
        self.xpath = "/html/body/table//tr/td/div/div/form/table//tr/td/font//text()[4]"
        self.data = {
            'query':'',
            'action':'results',
            'txt_semanticspace':'asbc200w',
            'txt_comptype':'t2t',
            'txt_dimension':'300',
            'mnu_chmode':'T',
            'keyword':'',
            'keyword2':'',
            'Submit':'Get Cosine'
        }

    def get_lsa(self,w1,w2):
        self.data.update({'keyword':to_utf8_str(w1)})
        self.data.update({'keyword2':to_utf8_str(w2)})
        html = self.interface.request_post(self.url,self.data)
        data = xpath_parse_one(html,self.xpath)
        item = re.search(r"[0-9.]+", data)
        if item != None:
            return item.group()
        else:
            return ""

if __name__ == "__main__": 
    print ChineseLsaInterface().get_lsa(u"醫生",u"護士")
    print ChineseLsaInterface().get_lsa(u"醫生",u"他你")

