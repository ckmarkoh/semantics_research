# -*- coding: utf-8 -*-
from sys import argv
import semMgr as smg
import proveMgr as pv
import nltk.sem.logic as lgc
from operator import itemgetter
import sys, StringIO


_TEST_DICT = {
1:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
2:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
3:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
4:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nad:演講))",
5:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))",
6:u"S(agent:NP(Head:Nb:江宜樺)|Head:VC31:表達|theme:NP(Head:Nac:立場))",
7:u"S(agent:NP(Head:Nb:姚明)|theme:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(quantifier:DM:２００２年|agent:Nb:ＮＢＡ|Head:Nv:選秀)|Head:Ng:中))|agent:PP(Head:P02:被|DUMMY:NP(property:Nc:休斯敦|Head:Nba:火箭隊))|Head:VG1:選為|range:NP(property:Nab:狀元|Head:Nab:新秀))",
8:u"S(agent:NP(Head:Nb:姚明)|theme:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(quantifier:DM:２００２年|agent:Nb:ＮＢＡ|Head:Nv:選秀)|Head:Ng:中))|agent:PP(Head:P02:被)|Head:VG1:選為|range:NP(property:Nab:狀元|Head:Nab:新秀))",
9:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
10:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:臺北))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
}



def test(k1,k2):
    sm = smg.SemMgr()
    print "s1 --> s2  ??"
    t1 = _TEST_DICT[k1]
    t2 = _TEST_DICT[k2] 
    s1 = sm.str_tree_to_sem(t1)
    s2 = sm.str_tree_to_sem(t2)
    print ""
    print "semantic of s1:",s1
    print "semantic of s2:",s2

    r1 = sm.prover_prove([s1],s2)
    r2 = sm.prover_prove([s2],s1)
    print "s1 --> s2"
    print r1
    print "s2 --> s1"
    print r2
    return r1,r2


def test_single(k1,k2):

    sm = smg.SemMgr()
    t1 = _TEST_DICT[k1]
    t2 = _TEST_DICT[k2] 
    s1 = sm.str_tree_to_sem(t1)
    s2 = sm.str_tree_to_sem(t2)
    print s1
    print s2
    r1=sm.prover_prove_tabu([s1],s2)

    return r1 


def main():
    test_result = map(lambda i: test( (i+1)*2-1, (i+1)*2) , range(len(_TEST_DICT)/2))
    print map(itemgetter(0),test_result) 
    print map(itemgetter(1),test_result) 
    #print test_single(9, 10)



if __name__ == "__main__":
    main() 
