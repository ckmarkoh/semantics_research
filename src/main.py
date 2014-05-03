# -*- coding: utf-8 -*-
from nltk import Tree
#from sys import argv
from buildtree import run_parser, treestr_to_tree
from connect_ckip import sinica_parse, sinica_parse_0
from MyPrinter import MyPrinter
import semMgr as smg
import proveMgr as pv
import nltk.sem.logic as lgc
from optparse import OptionParser
import argparse
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
8:u"S(agent:NP(Head:Nb:姚明)|theme:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(quantifier:DM:２００２年|agent:Nb:ＮＢＡ|Head:Nv:選秀)|Head:Ng:中))|agent:PP(Head:P02:被|DUMMY:NP(property:Nc:休斯敦|Head:Nba:火箭隊))|Head:VG1:選為|range:NP(property:Nab:狀元|Head:Nab:新秀))",
9:u"S(agent:NP(Head:Nb:姚明)|theme:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(quantifier:DM:２００２年|agent:Nb:ＮＢＡ|Head:Nv:選秀)|Head:Ng:中))|agent:PP(Head:P02:被)|Head:VG1:選為|range:NP(property:Nab:狀元|Head:Nab:新秀))"
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


#if __name__ == "main":
#    reload(smg)
#    sm = smg.SemMgr()
#    tree = tree_choice(7)
#    s1 = sm.tree_to_sem(tree)
#    print s1
    #tree = main()
    #result = tree_traverse(tree)
    
def test1():
    sm = smg.SemMgr()
    s1 = sm.tree_to_sem(tree_choice(4))
    s2 = sm.tree_to_sem(tree_choice(3))
    print s1
    print s2
    #p1 = lgc.LogicParser().parse(sm.sem_remove_chinese(s1).encode('utf-8'))
    #p2 = lgc.LogicParser().parse(sm.sem_remove_chinese(s2).encode('utf-8'))
    print "s1 --> s2"
    print pv.ProveMgr().prove(sm.sem_remove_chinese(s1), sm.sem_remove_chinese(s2))
    print "s2 --> s1"
    print pv.ProveMgr().prove(sm.sem_remove_chinese(s2), sm.sem_remove_chinese(s1))



if __name__ == "__main__"  :
    sm = smg.SemMgr()
    parser = argparse.ArgumentParser(prog='main')
    parser.add_argument('itype', metavar='itype', choices=['raw','id','treestr']
                        , type=str, help='input type: %(choices)s ')
    parser.add_argument('otype', metavar='otype', choices=['tree', 'sem','prove']
                        , type=str, help='output type: %(choices)s ')
    parser.add_argument('inpstr', metavar='str', nargs='*', type=str, help='input string 1')
#    parser.add_argument('--id', metavar='id', type=id, help='test file path')
    
    args = parser.parse_args()

    #print args
     #a=  lambda(x,f: reduce( apply(f,[x]) 
     
    input_str = args.inpstr

    print input_str
    t1 = None
    if args.itype == 'raw':
        flist = [sinica_parse_print_0,treestr_to_tree ]
        #tree_str = sinica_parse_0(input_str)
        #t1 =  treestr_to_tree(tree_str)

    elif args.itype == 'treestr':
        flist = [treestr_to_tree ]
        #t1 =  treestr_to_tree(input_str)

    elif args.itype == 'id':
        flist = [lambda x : _INPUT_DICT[int(x)],treestr_to_tree ]
        
    t_list = map(lambda y : reduce(lambda x,f: f(x), flist , y) , input_str)
     
    if args.otype == 'tree':
        for t in t_list:
            t.draw()

    elif args.otype == 'sem':
        s_list = map(lambda t :  sm.tree_to_sem(t) ,t_list)
        for s in s_list:
            print t 

    elif args.otype == 'prove':
        s_list = map(lambda t :  sm.tree_to_sem(t) ,t_list)
        print pv.ProveMgr().prove( map( lambda s : sm.sem_remove_chinese(s) , s_list[0:-1]) , sm.sem_remove_chinese(s_list[-1]))

    #s1 = args
    #print s1
    #demo1() 
#    test1()
#    t1 = tree_choice(3)
#    t2 = tree_choice(4)
#    s1 = sm.tree_to_sem(t1)
#    s2 = sm.tree_to_sem(t2)
#    print s1
#    #print sm.sem_remove_chinese(s1)
#    print s2
#    #print sm.sem_remove_chinese(s2)
#    p1 = lgc.LogicParser().parse(sm.sem_remove_chinese(s1).encode('utf-8'))
#    p2 = lgc.LogicParser().parse(sm.sem_remove_chinese(s2).encode('utf-8'))
#    #print p1.__str__()
#    #print p2.__str__()
#    print Prover9().prove(p1, [p2])
#    #  smg.SemParserV1(tree).get_sem()

