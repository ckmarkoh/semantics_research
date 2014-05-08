# -*- coding:utf-8 -*-
from sqliteInterface import SQLiteInterface 
from util import *
from operator import itemgetter
from MyPrinter import MyPrinter
import re

_CWN_PATH = '../data/cwn_dirty.sqlite'

class GcwnInterface(SQLiteInterface):
    def __init__(self):
        super(GcwnInterface, self).__init__(_CWN_PATH)
            
    def get_lemma(self, lemma): 
        return self.select('cwn_lemma'
                           ,where=' lemma_type="%s" '%(lemma)
                          )

    def get_sense(self, lemma_id):
        return self.select('cwn_sense'
                           ,column=['sense_id','sense_def']
                           ,where='lemma_id = "%s"'%(lemma_id)
                          )
    def get_facet(self,sense_id):
        return self.select('cwn_facet'
                           ,column=['facet_id','facet_def']
                           ,where='sense_id = "%s"'%(sense_id)
                          )

    #def get_relation(self,cwn_id):
    #    return self.select('cwn_relation'
    #                       ,where='cwn_id = "%s"'%(cwn_id)
    #                      )

    def get_relation(self,cwn_id):
        return self.select('cwn_relation'
                           ,column=['rel_type','rel_lemma', 'rel_cwnid','cwn_symbol.label_zhTw', 'cwn_symbol.label_en']
                           ,other_str="""
                            left join cwn_symbol
                            on cwn_relation.rel_type = cwn_symbol.cwn_symbol
                            where cwn_relation.cwn_id = "%s";
                            """%(cwn_id)
                          # ,where='cwn_id = "%s"'%(cwn_id)
                          )
        #print result
        #return result

    def get_lemma_relation(self,lemma):
        relation_ary_raw = []
        lemma_id_ary = map(itemgetter('lemma_id'), self.get_lemma(to_utf8_str(lemma)))
        for lemma_id in lemma_id_ary:
            sense_id_ary = map(itemgetter('sense_id'), self.get_sense(lemma_id))
            for sense_id in sense_id_ary:
                relation_ary_raw.extend(self.get_relation(sense_id))
                facet_id_ary = map(itemgetter('facet_id'), self.get_facet(sense_id))
                for facet_id in facet_id_ary:
                    relation_ary_raw.extend(self.get_relation(facet_id))
        relation_result = {} 
        for relation in relation_ary_raw:
            if relation['cwn_symbol.label_en'] not in relation_result.keys():
               relation_result.update({relation['cwn_symbol.label_en']:[]})
            relation_result.get(relation['cwn_symbol.label_en']).append(re.sub(r'[0-9]','',relation['rel_lemma']))
        for relation_type in relation_result.keys():
            relation_result[relation_type] = set(relation_result[relation_type])

        return relation_result

def main():
    cwn = CwnInterface()
    MyPrinter(cwn.get_lemma_relation(u"演說".encode('utf-8'))).print_data()
    MyPrinter(cwn.get_lemma_relation(u"狗".encode('utf-8'))).print_data()
    MyPrinter(cwn.get_lemma_relation(u"棒".encode('utf-8'))).print_data()
    MyPrinter(cwn.get_lemma_relation(u"吸".encode('utf-8'))).print_data()
    MyPrinter(cwn.get_lemma_relation(u"好".encode('utf-8'))).print_data()

if __name__ == "__main__":
    main()
