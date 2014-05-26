#-*- coding:utf-8 -*-
import requests
import lxml.html as HTML                                                                                                               
from util import *

_HEADERS = {
'User-Agent':
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/27.0.1453.93 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
'Accept-Encoding': 'gzip,deflate,sdch'
}
#payload = {'myTag':u'我們都喜歡蝴蝶'.encode('big5'), 
#           'MyServer': '1',
#           'id':'59545349',
#           'submit':'submit',
#          }
#r = requests.post("http://140.109.19.112/svr/webparser.asp", data=payload,headers = _HEADERS)
#r.encoding='big5'
payload = {
'query':'',
'action':'results',
'txt_semanticspace':'asbc200w',
'txt_comptype':'t2t',
'txt_dimension':'300',
'mnu_chmode':'T',
'keyword':u'醫生'.encode('utf-8'),
'keyword2':u'護士'.encode('utf-8'),
'Submit':'Get Cosine'
}
r = requests.post("http://www.lsa.url.tw/modules/lsa/lsa_pairwise_comparison.php" , 
                  data = payload,
                  headers = _HEADERS)
r.encoding='utf-8'
print xpath_parse_one(r.text,"/html/body/table//tr/td/div/div/form/table//tr/td/font//text()[4]")
