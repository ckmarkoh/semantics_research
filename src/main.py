# -*- coding: utf-8 -*-
from nltk import Tree
from sys import argv
from buildtree import run_parser
from connect_ckip import sinica_parse
from copy import deepcopy
import nltk.sem.logic as logic
import operator
lgp = logic.LogicParser()


_INPUT_DICT = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
4:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
5:u"S(agent:NP(Head:Nb:布魯圖)|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒)) ",
6:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
}

_NUM_ID = 0

def gen_id():
    global _NUM_ID 
    _NUM_ID += 1
    return _NUM_ID

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
    input_str = _INPUT_DICT[6]
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

def tree_is_pos(tree):
    if len( tree) == 1:
        if  isinstance( tree[0], unicode):
            return True
    return False

def tree_traverse(tree):
    role, pos = split_role_pos(tree.node)
    if tree_is_pos(tree):
        return {'role':role, 'pos':pos, 'sem':gen_leave_sem(tree, role, pos)}

    elif len(tree) == 1:
        node_dict = tree_traverse(tree[0])
        if role:
            node_dict.update({'role':role, 'pos':pos, 'sem':gen_node_sem_1(tree, role, pos)})
        return node_dict
    else:
        return {'role':role, 'pos':pos, 'sem':gen_node_sem_2(tree)}

def gen_leave_sem(tree, role, pos):
    assert(tree_is_pos(tree))
    if "N" == pos[0]:
        #return "\p . p(%s,e)"%(tree[0])
        #return "%s"%(tree[-1])
        return r"\P x . (P(x,e) & %s(x))"%(tree[0])

    elif "V" == pos[0]:
        return r"%s(e)"%(tree[0])

    elif "P" == pos[0]:
        return r""

def gen_node_sem_1(tree, role, pos):
    node_dict = tree_traverse(tree[0])
    print node_dict['sem'] , pos
    if role and role != "DUMMY":
        if "P" == pos[0] or "N" == pos[0] :
            node_sem_str = r'%s(%s)(%s)'%(node_dict['sem'], role, "n%s"%(gen_id()) )
            return lgp.parse(node_sem_str.encode('utf-8')).simplify().__str__().decode('utf-8')
    return node_dict['sem']
    


def gen_node_sem_2(tree, role='', pos=''):
    assert len(tree) > 1 
    
    nary_dict = dict( map(lambda node : ( node['role'],node )
                          ,map(lambda subtree : tree_traverse(subtree)  , tree) ))

    n_head = nary_dict.pop('Head')

    if "V" == n_head['pos'][0] :
    #    node_sem_str = reduce(lambda x, y: r'%s(%s)'%(x, y) 
    #                          , [ nary_dict.pop(s)['sem'] for s in ['agent','goal']   ] , n_head['sem'] )
    #    node_sem_str = reduce(lambda x, y: r'%s & %s'%(x, y) 
    #                          , [ nary_dict.pop(s)['sem'] for s in nary_dict.keys() ] , node_sem_str )
        #node_sem_str = reduce(lambda x, y: r'%s & %s'%(x, y) 
        #                      , [ nary_dict.pop(s)['sem'] for s in nary_dict.keys() ] , n_head['sem'] )

        #return node_sem_str
        #return lgp.parse(node_sem_str.encode('utf-8')).simplify().__str__().decode('utf-8')

        return "exist e.(%s)"%(" & ".join([ n_head['sem'] ] + map (lambda s :  nary_dict[s]['sem']  , nary_dict.keys()) ))
    elif "P" == n_head['pos'][0] :
       # reduce(lambda x, y: r'%s & %s'%(x, y) 
       #                       , [ nary_dict.pop(s)['sem'] for s in nary_dict.keys() ] , n_head['sem'] )
        return " & ".join(map (lambda s :  nary_dict[s]['sem']  , nary_dict.keys()))
    #    node_sem_str = reduce(lambda x, y: r'%s(%s)'%(x, y) 
    #                          , [ nary_dict.pop(s)['sem'] for s in nary_dict.keys() ] , n_head['sem'] )


    


if __name__ == "main":
    tree = tree_choice(4)
    #tree = main()
    #result = tree_traverse(tree)
    

if __name__ == "__main__":
    tree = main()
    result = tree_traverse(tree)
    print result['sem']
