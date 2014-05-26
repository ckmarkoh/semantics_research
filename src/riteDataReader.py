# -*- coding: utf-8 -*-
from util import *
from myPrinter import MyPrinter
_DATA_PATH = "../data/RITE1_CT_dev_mc.txt"


class RiteDataReader(object):
    def __init__(self):
        self.raw_data = "".join(open_and_read(_DATA_PATH))
        self.attr_template = '//pair[@{attr}="{val}"]/@{attr2}'
        self.data_template = '//pair[@{attr}="{val}"]/t{n}/text()'

    def select_by_xpath(self,xpath):
        return xpath_parse_all(self.raw_data,xpath)

    def select_by_template(self,t_attr,t_val):
        a1 = self.select_by_xpath(self.attr_template.format(attr=t_attr,val=t_val,attr2="label"))
        a2 = self.select_by_xpath(self.attr_template.format(attr=t_attr,val=t_val,attr2="id"))
        t1 = self.select_by_xpath(self.data_template.format(attr=t_attr,val=t_val,n=1))
        t2 = self.select_by_xpath(self.data_template.format(attr=t_attr,val=t_val,n=2))
        print len(a1)
        print len(a2)
        print len(t1)
        print len(t2)
        assert len(a1) == len(a2) == len(t1) ==len(t2)
        return [{"label":a1[i],"id":a2[i],"t1":t1[i],"t2":t2[i]} for i in range(len(a1))]
        #return zip(t1,t2)
    
    def select_by_label(self,val):
        return self.select_by_template("label",val)

if __name__ == "__main__": 
    r = RiteDataReader()
    MyPrinter(r.select_by_label("R")).print_data()
