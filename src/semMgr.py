# -*- coding: utf-8 -*-
import nltk.sem.logic as lg
import operator as opr
import sys, StringIO
from ckipParser import CkipParser
from semParser import SemParserV2
from proveMgr import ProveMgr
from cwnInterface import CwnInterface
from clsaInterface import ClsaInterface
from latexGen import LatexGen
from util import *
import re
from myPrinter import MyPrinter



_TEST_DICT = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
4:u"S(agent:NP(Head:Nb:布魯圖)|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
5:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
7:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))", 
8:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
9:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:研究院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
10:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:臺北))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
11:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nad:演講))",
12:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nac:演說))",
13:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nac:說話))",
14:u"S(theme:NP(Head:Nba:若望保祿|quantifier:DM:二世)|Head:V_12:是|range:NP(property:Ncb:教廷|property:Nac:國家|Head:Nab:領導人))",
15:u"S(theme:NP(Head:Nba:若望保祿|quantifier:DM:二世)|Head:V_12:是|range:NP(property:Ncb:教廷|property:Nac:國家|Head:Nab:領袖))",
15201:"S(theme:NP(Head:Nba:張藝謀)|time:Dd:曾|topic:PP(Head:P35:與|DUMMY:NP(Head:Nb:鞏俐))|Head:V_12:是|range:NP(property:Nab:戀人|Head:Nad:關係))",
15202:"S(theme:Nba(DUMMY1:Nba:張藝謀|Head:Caa:與|DUMMY2:Nb:鞏俐)|time:Dd:曾|Head:VH11:相戀)",
20:u"S(agent:NP(Head:Nb:海生館)|Head:VE2:研究|goal:S(agent:NP(apposition:Nab:人員|Head:Nb:謝泓諺)|Head:VE2:發現|goal:S(theme:NP(property:Na:水螅體|Head:Nad:數量)|Head:VH16: 增加)))",
21:u"S(agent:NP(apposition:NP(property:Nb:海生館|property:Nv:研究|Head:Nab:人員)|Head:Nb:謝泓諺)|Head:VE2:發現|goal:S(theme:NP(property:Na:>水螅體|Head:Nad:數量)|Head:VH16:增加))",
22:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
23:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:研究院))|Head:VC31:公開|theme:NP(Head:Nad:演說))",
}


class SemMgr(object):
    def __init__(self):  
        self._str_tree_dict = {} 
        self._chvar_dict = {}
        self._sem_parser = SemParserV2()
        self._ckip_parser = CkipParser()
        self._pm = ProveMgr()
        self._cwn = CwnInterface()
        self._clsa = ClsaInterface()
        self._lgen = LatexGen()

    #def gen_ch_id(self, ch_word):
    #    return 'A'+"_".join(map(lambda c: hex(ord(c)).upper() , ch_word ))

    def str_raw_to_str_tree(self,raw_str):
        return self._ckip_parser.str_raw_to_str_tree(raw_str)

    def str_tree_to_tree(self,str_tree):
        return self._ckip_parser.str_tree_to_tree(str_tree)

    def str_raw_to_sem(self, raw_str):
        #return self.str_tree_to_sem(self._ckip_parser.str_raw_to_str_tree(raw_str))
        return self.str_tree_to_sem(self.str_raw_to_str_tree(raw_str))

    def str_tree_to_sem(self,str_tree): 
        return self.tree_to_sem(self.str_tree_to_tree(str_tree))

    def tree_to_sem(self,tree):
        if tree.__str__() not in self._str_tree_dict.keys():
            self._str_tree_dict.update({tree.__str__() : self._sem_parser.get_parsed_sem(tree)})
        return self._str_tree_dict[tree.__str__()]
   

    def tree_to_latex(self,tree):  
        ltree = self._lgen.tree_to_latex(tree)
        return ltree

    def sem_to_latex(self,sem):  
        lsem = self._lgen.sem_to_latex(to_unicode(lsem))
        return lsem 

    def tree_to_sem_latex(self,tree):  
        sem = self.tree_to_sem(tree)
        lsem = self._lgen.sem_to_latex(sem)
        #sem_ch = re.search(ur'([\u4e00-\u9fff\uff01-\uff5e]+)',sem)
        #ch_dict = {}
        #while sem_ch != None: 
        #    ch = sem_ch.group()
        #    ch_id = self.gen_ch_id(ch)
        #    ch_dict.update( {ch_id: ch} )
        #    sem = sem.replace(ch,r"\text{%s}"%(ch_id))
        #    sem_ch = re.search(ur'([\u4e00-\u9fff\uff01-\uff5e]+)',sem)
        #for ch_id in ch_dict:
        #    sem = sem.replace(ch_id,ch_dict[ch_id])
        #sem = sem.replace('&',r'\wedge')
        return lsem


    def sem_conversion_chinese(self,sem_input,no_ch=True):
        if isinstance( sem_input, list):
            return map(lambda sem_str : self.sem_conversion_chinese(sem_str,no_ch) ,sem_input)

            #return map(lambda sem_str : self.sem_recover_chinese(sem_str) ,sem_input)
        elif isinstance( sem_input, str) or isinstance( sem_input, unicode):
            sem_str = to_unicode(sem_input) 
            if no_ch:
                ch_word_list = re.findall(ur'[\u4e00-\u9fff\uff01-\uff5e]+',sem_str)
                map(lambda  ch_word :  self._chvar_dict.update({ch_word : gen_ch_id(ch_word)}) 
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

    def prover_prove_output(self, pre_str, con_str, prover):
        result = self._pm.prove_prover_catch_output(self.sem_remove_chinese(pre_str)
                                    ,self.sem_remove_chinese(con_str)
                                    ,prover 
                                    )
        return self.sem_recover_chinese(result[3])

    def prover_prove_select(self, pre_str, con_str, prover):
        return self._pm.prove_prover(self.sem_remove_chinese(pre_str)
                                    ,self.sem_remove_chinese(con_str)
                                    ,prover 
                                    )
         

    def prover_catch_unsolved(self,pre_str_raw,con_str_raw):
        pre_str, con_str = self.sem_remove_chinese(pre_str_raw),self.sem_remove_chinese(con_str_raw)
        con_unsolved, pre_unsolved, unsolved_rule =   self._pm.prove_catch_unsolved(pre_str,con_str)
        return self.sem_recover_chinese( [ pre_unsolved, con_unsolved, unsolved_rule] )

    
    def prover_fix_entail(self, pre_str_raw, con_str_raw):
        unsolved =  self.prover_catch_unsolved(pre_str_raw, con_str_raw)
        if unsolved == False:
            return False
        solved = self.cwn_check_entail(unsolved[0],unsolved[1])
        if solved:
           return unsolved[2]
        else:
            solved = self.clsa_check_entail(unsolved[0],unsolved[1])
            if solved:
                return unsolved[2]
            else:
                return False

    def cwn_check_entail(self,w1,w2):
        return w2 in self._cwn.get_entail_lemma(w1)

    def clsa_check_entail(self,w1,w2):
        return 0.2 < self._clsa.get_lsa(w1,w2)
        


def main(sm):
    s = _TEST_DICT[20]  
    t = sm.str_tree_to_tree(s)
    sm.tree_to_latex(t)

def case1(sm):
    t1 = u"巴西隊(n1) & agent(n1,e) &   首場(d0) & quantifier(d0,n5) & 比賽(n5) & time(n5,e)     & 獲得(e) & 勝利(n3) & goal(n3,e)"
    t2 = u"巴西隊(n1) & agent(n1,e) & 第一場(d4) & quantifier(d4,n3) & 比賽(n5) & property(n5,n3)& 拿下(e) & 勝利(n3) & goal(n3,e)"
    t3 = u"首場(d0) & quantifier(d0,n5) -> 第一場(d4) & quantifier(d4,n3)"
    t4 = u"獲得(e) -> 拿下(e)"
    t5 = u"比賽(n5) & time(n5,e) -> 比賽(n5) & property(n5,n3)"
    MyPrinter(sm.prover_prove_select([t1,t3,t4,t5],t2,"nine"))

def case2(sm):
    t1=" theme(n1,e) & AA(n1) & BB(e) & theme(n2,e) & CC(n2)"
    t2=" theme(n1,e) & AA(n1) & BB(e) & theme(n3,e) & DD(n3)"
    t3=" theme(n2,e) & CC(n2) ->        theme(n3,e) & DD(n3) "
    MyPrinter(sm.prover_prove_select([t1],t2,"tableau"))

def case3(sm):
    #cwn:11,12 
    #clsa:8,9
    s1 = _TEST_DICT[22]
    s2 = _TEST_DICT[23]
    t1 =  sm.str_tree_to_sem(s1)
    t2 =  sm.str_tree_to_sem(s2)
    print t1.encode('utf-8')
    print t2.encode('utf-8')
    sm.prover_catch_unsolved([t1],t2)

if __name__ == "__main__" :#or __name__ == "semmgr":
    sm = SemMgr()
    case2(sm)
