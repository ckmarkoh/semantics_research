# -*- coding: utf-8 -*-
from nltk import Tree
from sys import argv
from buildtree import run_parser
from connect_ckip import sinica_parse




def parse_and_build_tree(raw_data):
    #data = u'S(hypothesis:Cbaa:如果|experiencer:NP(Head:Nhac:您)|Head:VK2:需要|goal:NP(quantifier:Neqa:大量|Head:Nad:剖析))'
    parsed_data=sinica_parse(raw_data)
    parsed_data_0=parsed_data[0]
    #print parsed_data_0
    tree=run_parser(parsed_data_0)
    #tree.chomsky_normal_form()
    tree.pprint()
    tree.draw()


def main():
    #parse_and_build_tree(argv[1])
    #parse_and_build_tree("臺灣的大學懇切呼籲平和理性") 
    #input_str_de=u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))"
    #input_str=u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))"
    input_str=u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))"
    tree=run_parser(input_str)
    tree.draw()

if __name__ == "__main__":
    main()

