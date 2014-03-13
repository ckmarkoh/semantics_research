# -*- coding: utf-8 -*-
from nltk import Tree
from sys import argv
from buildtree import run_parser
from connect_ckip import sinica_parse




def parse_and_build_tree(raw_data):
    #data = u'S(hypothesis:Cbaa:如果|experiencer:NP(Head:Nhac:您)|Head:VK2:需要|goal:NP(quantifier:Neqa:大量|Head:Nad:剖析))'
    parsed_data=sinica_parse(raw_data)
    parsed_data_0=parsed_data[0]
    tree=run_parser(parsed_data_0)
    tree.chomsky_normal_form()
    tree.pprint()
    tree.draw()


def main():
    parse_and_build_tree(argv[1])
    

if __name__ == "__main__":
    main()

