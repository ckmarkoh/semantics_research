# -*- coding: utf-8 -*-
from copy import deepcopy
import nltk.sem.logic as lg
import operator
from MyPrinter import MyPrinter
from util import *
import re

#Prover9().prove(c, [p1,p2])
#lgp = lg.LogicParser()


class SemParserV1(object):
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



