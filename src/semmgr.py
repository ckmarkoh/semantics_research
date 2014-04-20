
# -*- coding: utf-8 -*-
import nltk.sem.logic as lg
import operator
from buildtree import run_parser
from connect_ckip import sinica_parse
from semparser import SemParserV1
import re


_TEST_DICT = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
6:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
7:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))", 
}


class SemMgr(object):
    def __init__(self):  
        self._str_tree_dict = {} 
        self._chvar_dict = {}
        self._sem_parser = SemParserV1()

    def gen_ch_id(self, ch_word):
        return 'A'+"_".join([hex(ord(c)).upper() for c in ch_word])

    def str_raw_to_sem(self, raw_str):
        return self.str_tree_to_sem(sinica_parse(raw_str)[0])

    def str_tree_to_sem(self,str_tree): 
        return self.tree_to_sem(run_parser(str_tree))

    def tree_to_sem(self,tree):
        if tree.__str__() not in self._str_tree_dict.keys():
            self._str_tree_dict.update({tree.__str__() : self._sem_parser.get_parsed_sem(tree)})
        return self._str_tree_dict[tree.__str__()]

    def sem_no_chinese(self,sem_str):
        ch_word_list = re.findall(ur'[\u4e00-\u9fff]+',sem_str)
        map(lambda  ch_word :  self._chvar_dict.update({ch_word : self.gen_ch_id(ch_word)}) 
                                if ch_word not in self._chvar_dict.keys() else None , ch_word_list )
        return reduce(lambda x,y : x.replace(y,self._chvar_dict[y]) , ch_word_list , sem_str)


if __name__ == "__main__" or __name__ == "semmgr":
    sm = SemMgr()
    tree_str = _TEST_DICT[1]
    t1 = run_parser(tree_str)
    #s1 = sm.str_tree_to_sem(tree_str)
    #print s1
