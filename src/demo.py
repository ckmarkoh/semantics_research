# -*- coding: utf-8 -*-
from sys import argv
import semMgr as smg
from nltk import Prover9
import nltk.sem.logic as lgc

_DEMO_DICT ={
1:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
2:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))",
4:u"S(agent:NP(Head:Nb:江宜樺)|Head:VC31:表達|theme:NP(Head:Nac:立場))",
}

def demo1():
    sm = smg.SemMgr()
    print "s1 --> s2  ??"
    raw_str_1 = raw_input("sentence s1:")
    raw_str_2 = raw_input("sentence s2:")
    s1 = sm.str_raw_to_sem(raw_str_1)
    s2 = sm.str_raw_to_sem(raw_str_2)
    print ""
    print "semantic of s1:",s1
    print "semantic of s2:",s2
    p1 = lgc.LogicParser().parse(sm.sem_remove_chinese(s1).encode('utf-8'))
    p2 = lgc.LogicParser().parse(sm.sem_remove_chinese(s2).encode('utf-8'))
    print "s1 --> s2"
    print Prover9().prove(p2, [p1])


def demo2():
    sm = smg.SemMgr()
    print "s1 --> s2  ??"
    t1 = _DEMO_DICT[3]
    t2 = _DEMO_DICT[4] 
    s1 = sm.str_tree_to_sem(t1)
    s2 = sm.str_tree_to_sem(t2)
    print ""
    print "semantic of s1:",s1
    print "semantic of s2:",s2
    s = sm.sem_remove_chinese(s1).encode('utf-8')
    p1 = lgc.LogicParser().parse(sm.sem_remove_chinese(s1).encode('utf-8'))
    p2 = lgc.LogicParser().parse(sm.sem_remove_chinese(s2).encode('utf-8'))
    s0 = sm.sem_recover_chinese(s)
    print s
    print s0
    print "s1 --> s2"
    print Prover9().prove(p2, [p1])
    print "s2 --> s1"
    print Prover9().prove(p1, [p2])


if __name__ == "__main__":
    demo2() 
