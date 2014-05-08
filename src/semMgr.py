# -*- coding: utf-8 -*-
import nltk.sem.logic as lg
import operator as opr
import sys, StringIO
from ckipParser import CkipParser
from semParser import SemParserV1
from proveMgr import ProveMgr
from cwnInterface import CwnInterface
from util import *
import re



_TEST_DICT = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
6:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
7:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))", 
9:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
10:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:臺北))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
11:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nad:演講))",
12:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nac:演說))",
13:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nac:說話))",
}


class SemMgr(object):
    def __init__(self):  
        self._str_tree_dict = {} 
        self._chvar_dict = {}
        self._sem_parser = SemParserV1()
        self._ckip_parser = CkipParser()
        self._pm = ProveMgr()
        self._cwn = CwnInterface()

    def gen_ch_id(self, ch_word):
        return 'A'+"_".join(map(lambda c: hex(ord(c)).upper() , ch_word ))

    def str_raw_to_sem(self, raw_str):
        return self.str_tree_to_sem(self._ckip_parser.str_raw_to_str_tree(raw_str))

    def str_tree_to_sem(self,str_tree): 
        return self.tree_to_sem(self._ckip_parser.str_tree_to_tree(str_tree))

    def tree_to_sem(self,tree):
        if tree.__str__() not in self._str_tree_dict.keys():
            self._str_tree_dict.update({tree.__str__() : self._sem_parser.get_parsed_sem(tree)})
        return self._str_tree_dict[tree.__str__()]

    
    def sem_conversion_chinese(self,sem_input,no_ch=True):
        if isinstance( sem_input, list):
            return map(lambda sem_str : self.sem_conversion_chinese(sem_str,no_ch) ,sem_input)

            #return map(lambda sem_str : self.sem_recover_chinese(sem_str) ,sem_input)
        elif isinstance( sem_input, str) or isinstance( sem_input, unicode):
            sem_str = to_unicode(sem_input) 
            if no_ch:
                ch_word_list = re.findall(ur'[\u4e00-\u9fff\uff01-\uff5e]+',sem_str)
                map(lambda  ch_word :  self._chvar_dict.update({ch_word : self.gen_ch_id(ch_word)}) 
                                        if ch_word not in self._chvar_dict.keys() else None , ch_word_list )
                return reduce(lambda x,y : x.replace(y,self._chvar_dict[y]) , ch_word_list , sem_str)

            else:
                return reduce(lambda  mstr, key_val : mstr.replace(key_val[1],key_val[0])
                              , self._chvar_dict.items() , sem_str)
        else:
            assert 0
        
    def sem_remove_chinese(self,sem_input):
        return self.sem_conversion_chinese(sem_input,True)


    def sem_recover_chinese(self,sem_input):
        return self.sem_conversion_chinese(sem_input,False)


    def prover_prove(self, pre_str, con_str):
        return self._pm.prove(self.sem_remove_chinese(pre_str)
                                    ,self.sem_remove_chinese(con_str))

    def prover_prove_tabu(self, pre_str, con_str):
        return self._pm.prove(self.sem_remove_chinese(pre_str)
                                    ,self.sem_remove_chinese(con_str),tabu=True)

    def prover_catch_unsolved(self,pre_str_raw,con_str_raw):
        pre_str, con_str = self.sem_remove_chinese(pre_str_raw),self.sem_remove_chinese(con_str_raw)
        con_unsolved, pre_unsolved, unsolved_rule =   self._pm.prove_catch_unsolved(pre_str,con_str)
        return self.sem_recover_chinese( [ pre_unsolved, con_unsolved, unsolved_rule] )

    def cwn_check_entail(self,w1,w2):
        return w2 in self._cwn.get_entail_lemma(w1)
    
    def prover_fix_entail(self, pre_str_raw, con_str_raw):
        unsolved =  self.prover_catch_unsolved(pre_str_raw, con_str_raw)
        if unsolved == False:
            return False
        solved = self.cwn_check_entail(unsolved[0],unsolved[1])
        if solved:
           return unsolved[2]
        else:
            return False
    
        

if __name__ == "__main__" :#or __name__ == "semmgr":
    sm = SemMgr()
    #tree_str = _TEST_DICT[1]
    s1 = _TEST_DICT[10]
    s2 = _TEST_DICT[13]
    t1 =  sm.str_tree_to_sem(s1)
    t2 =  sm.str_tree_to_sem(s2)
    print t1
    print t2
    print sm.prover_prove([t1],t2)
    uns = sm.prover_fix_entail(t1, t2) 
    if uns:
        print uns
        print sm.prover_prove([t1,uns],t2)
    else:
        print False
    #print unsolved_rule
    #t1 = run_parser(tree_str)
    #s1 = sm.str_tree_to_sem(tree_str)
    #print s1
