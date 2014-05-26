# -*- coding: utf-8 -*-
import sys, StringIO

import lxml.html as HTML                                                                                                               
def to_unicode(sem_str_raw):
    if isinstance( sem_str_raw, str):
        sem_str = sem_str_raw.decode('utf-8') 
    elif isinstance( sem_str_raw, unicode):
        sem_str = sem_str_raw
    else:
        assert 0
    return sem_str
def to_utf8_str(sem_str_raw):
    if isinstance( sem_str_raw, str):
        sem_str = sem_str_raw
    elif isinstance( sem_str_raw, unicode):
        sem_str = sem_str_raw.encode('utf-8') 
    else:
        assert 0
    return sem_str

def capture_output(fn):
    def inner(*args, **kwargs):
        old_stdout = sys.stdout
        capturer = StringIO.StringIO()
        sys.stdout = capturer
        #capture start
        result=fn(*args, **kwargs)
        ## capture end
        sys.stdout = old_stdout
        output = capturer.getvalue()
        return result,output
    return inner
    

def xpath_parse_all(html,xpath):
    return HTML.document_fromstring(html).xpath(xpath)

def xpath_parse_one(html,xpath,xid=0): 
    result = xpath_parse_all(html,xpath)
    if xid >= len(result):
         return "" 
    else:
         return xpath_parse_all(html,xpath)[xid]
