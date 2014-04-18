# -*- coding: utf-8 -*-
from nltk import Tree
from sys import argv
from buildtree import run_parser
from connect_ckip import sinica_parse
from copy import deepcopy
import nltk.sem.logic as logic
lgp = logic.LogicParser()


_INPUT_DICT = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
4:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
}

def parse_and_build_tree(raw_data):
    parsed_data = sinica_parse(raw_data)
    parsed_data_0 = parsed_data[0]
    #print parsed_data_0
    tree = run_parser(parsed_data_0)
    #tree.chomsky_normal_form()
    tree.pprint()
    tree.draw()


def main():
    input_str = _INPUT_DICT[4]
    tree = run_parser(input_str)
    return tree
    #tree.draw()


def split_role_pos(node_str):
    str_split = node_str.split(':')
    if len(str_split) > 1:
        return str_split[0],str_split[1]
    else:
        if str_split[0] == 'S':
            return 'Sentence',str_split[0]
        else:
            return None,str_split[0]

def change_role_pos(node_dict, role, pos):
    node_dict.update({'role':role})
    node_dict.update({'pos':pos})

def tree_is_pos(tree):
    if len( tree) == 1:
        if  isinstance( tree[0], unicode):
            return True
    return False

def tree_traverse(tree):
    role, pos = split_role_pos(tree.node)
    if tree_is_pos(tree):
        node_dict={}
        change_role_pos( node_dict, role,pos )
        gen_leave_sem( node_dict, tree, pos)

    elif len(tree) == 1:
        node_dict = tree_traverse(tree[0])
        if role:
            change_role_pos(node_dict, role, pos)
    else:
        node_dict={}
        change_role_pos(node_dict, tree, pos)
        gen_node_sem(node_dict, tree)

    return node_dict

def gen_leave_sem(node_dict,tree,pos):
    assert(tree_is_pos(tree))
    if "N" in pos:
        node_dict.update({'sem' : "%s"%(tree[0])})
    elif "V" in pos:
        node_dict.update({'sem' : r"\x y.%s(x,y)"%(tree[0])})

def gen_node_sem(node_dict,tree):
    assert  len(tree) > 1 
    node_ary = map(lambda subtree :   tree_traverse(subtree)  , tree)
    node_ary_dict = { node['role']:node for node in node_ary }
    
    simplify_seq = ['','Head','agent','goal']   

    node_sem_str = reduce(lambda x, y: r'%s(%s)'%(x, node_ary_dict[y]['sem'])                    
                          , filter(lambda z :  z in node_ary_dict.keys() or z == '' ,simplify_seq ))

    node_sem = lgp.parse(node_sem_str.encode('utf-8')).simplify().__str__().decode('utf-8')
    node_dict.update({'sem':node_sem})

if __name__ == "main":
    tree = main()
    result = tree_traverse(tree)
    

if __name__ == "__main__":
    tree = main()
    result = tree_traverse(tree)
    print result['sem']

