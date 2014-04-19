# -*- coding: utf-8 -*-
from nltk import Tree
from sys import argv
from buildtree import run_parser
from connect_ckip import sinica_parse
from MyPrinter import MyPrinter
import semparser as sp


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
    parsed_data = sinica_parse(raw_data)
    parsed_data_0 = parsed_data[0]
    tree = run_parser(parsed_data_0)
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
    tree = tree_choice(2)
    #tree = main()
    #result = tree_traverse(tree)
    
    

if __name__ == "__main__":
    tree = main()
    reload(sp)
    print  sp.SemParserV1(tree).get_sem()

