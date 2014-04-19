# -*- coding: utf-8 -*-
from nltk import Tree
from sys import argv
from buildtree import run_parser
from connect_ckip import sinica_parse
from MyPrinter import MyPrinter
import semparser as sp
from nltk import Prover9
import nltk.sem.logic as lgc

#Prover9().prove(c, [p1,p2])


_INPUT_DICT = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
4:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
5:u"S(agent:NP(Head:Nb:布魯圖)|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒)) ",
6:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
7:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))", 
}



def parse_and_build_tree(raw_data):
    tree = run_parser(sinica_parse(raw_data)[0])
    #tree.chomsky_normal_form()
    tree.pprint()
    tree.draw()

def tree_choice(idx):
    input_str = _INPUT_DICT[idx]
    return run_parser(input_str)

def main():
    input_str = _INPUT_DICT[2]
    tree = run_parser(input_str)
    return tree
    #tree.draw()


if __name__ == "main":
    reload(sp)
    sm = sp.SemMgr()
    tree = tree_choice(7)
    s1 = sm.tree_to_sem(tree)
    print s1
    #tree = main()
    #result = tree_traverse(tree)
    
def test1():
    sm = sp.SemMgr()
    s1 = sm.tree_to_sem(tree_choice(4))
    s2 = sm.tree_to_sem(tree_choice(3))
    print s1
    print s2
    p1 = lgc.LogicParser().parse(sm.sem_no_chinese(s1).encode('utf-8'))
    p2 = lgc.LogicParser().parse(sm.sem_no_chinese(s2).encode('utf-8'))
    print "s1 --> s2"
    print Prover9().prove(p2, [p1])



if __name__ == "__main__":
    #demo1() 
    test1()
#    t1 = tree_choice(3)
#    t2 = tree_choice(4)
#    s1 = sm.tree_to_sem(t1)
#    s2 = sm.tree_to_sem(t2)
#    print s1
#    #print sm.sem_no_chinese(s1)
#    print s2
#    #print sm.sem_no_chinese(s2)
#    p1 = lgc.LogicParser().parse(sm.sem_no_chinese(s1).encode('utf-8'))
#    p2 = lgc.LogicParser().parse(sm.sem_no_chinese(s2).encode('utf-8'))
#    #print p1.__str__()
#    #print p2.__str__()
#    print Prover9().prove(p1, [p2])
#    #  sp.SemParserV1(tree).get_sem()

