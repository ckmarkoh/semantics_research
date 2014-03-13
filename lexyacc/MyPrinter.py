# -*- coding: utf-8 -*
"""
    @filename: MyPrinter.py
    @author: Mark Chang 
    @date: 2014/3/12
"""

class MyPrinter(object):
    def __init__(self,data):
        self.data=data

    def print_data(self):
        print self.classifier(self.data,0)

    def classifier(self,d,l):
        if type(d) is dict:
            return self.print_dict(d,l)
        elif type(d) is list:
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
                            (",%s"%(self.level(l))).join( ["%s:%s"%(dkey,self.classifier(d[dkey],l+1)) for dkey in d.keys()] ),
                            self.level(l)
                            )

    def print_list(self,d,l):
        return "[%s %s %s]"%(
                            self.level(l),
                            (",%s"%(self.level(l))).join( ["%s"%(self.classifier(di,l+1)) for di in d] ),
                            self.level(l)
                            )
        
    def print_unicode(self,d):
        return "%s"%(d)#.encode('utf-8'))

    def print_str(self,d):
        return "%s"%(d.decode('utf-8'))

    def print_str2(self,d):
        return "%s"%(d)
    
    def level(self,l):
        return "\n%s"%("".join(["   " for i in range(l)]))
