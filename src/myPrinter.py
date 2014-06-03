# -*- coding: utf-8 -*
"""
    @filename: MyPrinter.py
    @author: Mark Chang 
    @date: 2014/3/12
"""
import json
import codecs
from sys import argv

class MyPrinter(object):
    def __init__(self,data,str_close=False,to_print=True):
        self.data=data
        self.str_close=str_close
        if to_print:
            self.print_data()
        

    def __str__(self):
        return self.classifier(self.data,0)

    def print_data(self):
        print self.__str__().encode('utf-8')

    def classifier(self,d,l):
        if type(d) is dict:
            return self.print_dict(d,l)
        elif type(d) in [list,tuple,set]:
            return self.print_list(d,l)
        elif type(d) is unicode:
            return self.print_unicode(d)
        elif type(d) is str:
            return self.print_str(d) 
        else:        
            return self.print_str2(d)

    def print_dict(self,d,l):
        return "{%s %s %s}"%(
                            self.level(l),
                            (",%s"%(self.level(l))).join( ["%s:%s"%(self.classifier(dkey,l+1),self.classifier(d[dkey],l+1)) for dkey in d.keys()] ),
                            self.level(l)
                            )

    def print_list(self,d,l):
        return "[%s %s %s]"%(
                            self.level(l),
                            (",%s"%(self.level(l))).join( ["%s"%(self.classifier(di,l+1)) for di in d] ),
                            self.level(l)
                            )
        
    def print_unicode(self,d):
        if self.str_close:
            return "\"%s\""%(d)#.encode('utf-8'))
        else:
            return "%s"%(d)#.encode('utf-8'))

    def print_str(self,d):
        if self.str_close:
            return "\"%s\""%(d.decode('utf-8'))
        else:
            return "%s"%(d.decode('utf-8'))

    def print_str2(self,d):
        if self.str_close:
            return "\"%s\""%(d)
        else:
            return "%s"%(d)
    
    def level(self,l):
        return "\n%s"%("".join(["   " for i in range(l)]))

def print_json(source_name):
    f2= codecs.open(source_name,'r','utf-8')
    this_json=json.loads("".join(f2.readlines()))
    #for x in this_json:
    #    print x
    MyPrinter(this_json).print_data()
    print "total:",len(this_json)
    f2.close()

if __name__=="__main__":
    print_json(argv[1])
