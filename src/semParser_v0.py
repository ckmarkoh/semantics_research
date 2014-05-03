# -*- coding: utf-8 -*-
from copy import deepcopy
import nltk.sem.logic as lg
import operator
from MyPrinter import MyPrinter
from buildtree import run_parser
from sys import argv
from util import *
import re


_TEST_DICT = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
4:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
5:u"S(agent:NP(Head:Nb:布魯圖)|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒)) ",
6:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
7:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))", 
}


## DONE
#2 : exists e (發表(e) & (theme(n3,e) & 演講(n3)) & (location(n2,e) & 中研院(n2)) & (agent(n0,e) & 馬英九(n0)) & (time(n1,e) & 今天(n1)))
#3 : exists e (刺殺(e) & (goal(n1,e) & 凱撒(n1)) & (agent(n0,e) & 布魯圖(n0)))
#6 : exists e (刺殺(e) & (instrument(n2,e) & 刀子(n2)) & (location(n1,e) & 元老院(n1)) & (agent(n0,e) & 布魯圖(n0)) & (goal(n3,e) & 凱撒(n3)))
#7 : exists e (表達(e) & (theme(n2,e) & 立場(n2)) & 清楚(e,manner) & (agent(n0,e) & 江宜樺(n0)) & (time(n1,e) & 已(n1)))
## NOT OK
#0 : exists e (呼籲(e) & None(theme) & 懇切(e,manner) & None(agent))
#1 : exists e (幫助(e) & None(goal) & (agent(n0,e) & 我(n0)))
##



class SemParserV0(object):
    def __init__(self):
        self._traverse = {}
        self._chvar_dict = {}
    
    def reset(self):    
        self._traverse.clear()
        self._chvar_dict.clear()

    def get_parsed_sem(self,tree):
        self._traverse.clear()
        return self.tree_traverse(tree)['sem']

    def gen_id(self, sem_str_raw):
        sem_str = to_unicode( sem_str_raw )
        ch_word = "".join(re.findall(ur'[\u4e00-\u9fff]+',sem_str))
        if ch_word not in self._chvar_dict.keys(): 
            self._chvar_dict.update({ch_word : len(self._chvar_dict)}) 
    #    print 'id',self._num_id
        return self._chvar_dict[ch_word]

    def split_role_pos(self, node_str):
        str_split = node_str.split(':')
        if len(str_split) > 1:
            return str_split[0],str_split[1]
        else:
            if str_split[0] == 'S':
                return 'Sentence',str_split[0]
            else:
                return None,str_split[0]

    def tree_is_pos(self, tree):
        if len( tree) == 1:
            if  isinstance( tree[0], unicode):
                return True
        return False

    def tree_traverse(self, tree):
        if id(tree) in self._traverse.keys():
            return self._traverse[id(tree)]
            
        role, pos = self.split_role_pos(tree.node)
        if self.tree_is_pos(tree):
            node_dict =  {'role':role, 'pos':pos, 'sem':self.gen_leave_sem(tree, role, pos)}

        elif len(tree) == 1:
            node_dict = deepcopy(self.tree_traverse(tree[0]))
            if role:
                node_dict.update({'role':role, 'pos':pos, 'sem':self.gen_node_sem_1(tree, role, pos)})
        else:
            node_dict = {'role':role, 'pos':pos, 'sem':self.gen_node_sem_2(tree)}
        
        self._traverse.update({id(tree):node_dict}) 
        #print node_dict
        return node_dict

    def gen_leave_sem(self, tree, role, pos):
        assert(self.tree_is_pos(tree))
        ch_name = tree[0].encode('utf-8')
        if pos[0] in ['N'] :
            #return "\p . p(%s,e)"%(tree[0])
            #return "%s"%(tree[-1])
            sem_str= r"\P . (P({var},e) & {pred}({var}))".format(pred=ch_name, var="n%s"%(self.gen_id(ch_name)))
            #var_id="n%s"%(self.gen_id(tree[0]))

        elif pos[0] in ['D'] :
            #return "\p . p(%s,e)"%(tree[0])
            #return "%s"%(tree[-1])
            sem_str= r"\P . (P({var},e) & {pred}({var}))".format(pred=ch_name, var="n%s"%(self.gen_id(ch_name)))
            #var_id="n%s"%(self.gen_id(tree[0]))

        elif pos[0] in ['V'] :
            sem_str= r"%s(e)"%(ch_name)

        elif pos[0] in ['P'] :
            sem_str= r""
        return sem_str.decode('utf-8')
         

    def gen_node_sem_1(self, tree, role, pos):
        node_dict = self.tree_traverse(tree[0])
        #print node_dict['sem'] , pos
        #if role and role != "DUMMY":
        #    if "P" == pos[0] or "N" == pos[0] :
        #        node_sem_str = r'%s(%s)(%s)'%(node_dict['sem'], role, "n%s"%(self.gen_id()) )
        #        return lgp.parse(node_sem_str.encode('utf-8')).simplify().__str__().decode('utf-8')
        return node_dict['sem']
        

    def change_node_sem_1(self, sem, role, pos):
        if role and role != "DUMMY" and sem !='':
            if pos[0] in ['P', 'N', 'D'] or pos[0:2] in ['VH']:
                node_sem_str = r'%s(%s)'%(sem, role )
                #print node_sem_str
                return lg.LogicParser().parse(node_sem_str.encode('utf-8')).simplify().__str__().decode('utf-8')
        return sem



    def gen_node_sem_2(self, tree, role='', pos=''):
        assert len(tree) > 1 
        
        nary_dict = dict( map(lambda node : ( node['role'],node )
                              ,map(lambda subtree : self.tree_traverse(subtree)  , tree) ))

        #MyPrinter(nary_dict).print_data()
        map(lambda n_elem : n_elem.update({ 'sem':self.change_node_sem_1(n_elem['sem'],n_elem['role'],n_elem['pos'])}) 
        #                    if 'P(x,e)' in n_elem['sem'] else n_elem 
                             ,nary_dict.values()    )

        n_head = nary_dict.pop('Head')

        if n_head['pos'][0] in ["V"] :
        
            return "exists e (%s)"%(" & ".join([ n_head['sem'] ] + map (lambda s :  nary_dict[s]['sem']  , nary_dict.keys()) ))

        elif n_head['pos'][0] in ["P"] :

            return " & ".join(map (lambda s :  nary_dict[s]['sem']  , nary_dict.keys()))



if __name__ == "__main__" #or __name__ == "semParser":
    sm = SemParserV0() 
    tree_str = _TEST_DICT[int(argv[1])]
    t1 = run_parser(tree_str)
    print sm.get_parsed_sem(t1)
