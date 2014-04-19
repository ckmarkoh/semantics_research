# -*- coding: utf-8 -*-
from nltk import Tree
from copy import deepcopy
import nltk.sem.logic as lg
import operator
from MyPrinter import MyPrinter
from buildtree import run_parser
from connect_ckip import sinica_parse
import re

#Prover9().prove(c, [p1,p2])
#lgp = lg.LogicParser()


_TEST_DICT = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
6:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
7:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))", 
}


class SemParserV1(object):
    def __init__(self):
    #    self._num_id = 0
        self._traverse = {}
        self._chvar_dict = {}
    
    def reset(self):    
    #    self._num_id = 0
        self._traverse.clear()
        self._chvar_dict.clear()

    def get_parsed_sem(self,tree):
        self._traverse.clear()
        return self.tree_traverse(tree)['sem']
        #if id(tree) not in self._sem_result:
        #    self._sem_result.update({id(tree):self.tree_traverse(tree)})
        #return self._sem_result[id(tree)]
    #def get_nooch_sem(self,tree):
    #    ch_sem = self.get_parsed_sem(self,tree)
        
    #def gen_id_aux(self):
    #    self._num_id += 1
    #    return self._num_id

    def gen_id(self, sem_str):
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
        if pos[0] in ['N'] :
            #return "\p . p(%s,e)"%(tree[0])
            #return "%s"%(tree[-1])
            return r"\P x . (P(x,e) & %s(x))"%(tree[0])

        elif pos[0] in ['D'] :
            #return "\p . p(%s,e)"%(tree[0])
            #return "%s"%(tree[-1])
            return r"\P x . (P(x,e) & %s(x))"%(tree[0])

        elif pos[0] in ['V'] :
            return r"%s(e)"%(tree[0])

        elif pos[0] in ['P'] :
            return r""
         

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
                node_sem_str = r'%s(%s)(%s)'%(sem, role, "n%s"%(self.gen_id(sem)) )
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
        
            #print nary_dict
            #print map (lambda s :  nary_dict[s]['sem']  , nary_dict.keys()) 
            #print " & ".join([ n_head['sem'] ] + map (lambda s :  nary_dict[s]['sem']  , nary_dict.keys()) )
            return "exists e (%s)"%(" & ".join([ n_head['sem'] ] + map (lambda s :  nary_dict[s]['sem']  , nary_dict.keys()) ))

        elif n_head['pos'][0] in ["P"] :

            return " & ".join(map (lambda s :  nary_dict[s]['sem']  , nary_dict.keys()))


class SemMgr(object):
    def __init__(self):  
        self._str_tree_dict = {} 
        self._chvar_dict = {}
        self._sem_parser=SemParserV1()

    def gen_ch_id(self, ch_word):
        return 'A'+"_".join([hex(ord(c)).upper() for c in ch_word])

    def str_raw_to_sem(self, raw_str):
        return self.str_tree_to_sem(sinica_parse(raw_str)[0])

    def str_tree_to_sem(self,str_tree): 
        return self.tree_to_sem(run_parser(str_tree))

    def tree_to_sem(self,tree):
        if tree.__str__() not in self._str_tree_dict.keys():
            self._str_tree_dict.update({tree.__str__() : self._sem_parser.get_parsed_sem(tree)})
        return self._str_tree_dict[tree.__str__()]

    def sem_no_chinese(self,sem_str):
        ch_word_list = re.findall(ur'[\u4e00-\u9fff]+',sem_str)
        map(lambda  ch_word :  self._chvar_dict.update({ch_word : self.gen_ch_id(ch_word)}) 
                                if ch_word not in self._chvar_dict.keys() else None , ch_word_list )
        return reduce(lambda x,y : x.replace(y,self._chvar_dict[y]) , ch_word_list , sem_str)
        


if __name__ == "__main__":
    sm = SemMgr()
    tree_str = _TEST_DICT[7]
    s1 = sm.str_tree_to_sem(tree_str)
    print s1
#class ProveMgr(object):
#    def 
