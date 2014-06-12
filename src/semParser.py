# -*- coding: utf-8 -*-
from copy import deepcopy
import nltk.sem.logic as lg
import operator
from myPrinter import MyPrinter
from buildtree import run_parser
from operator import itemgetter
from util import *
from sys import argv
import re

#Prover9().prove(c, [p1,p2])
#lgp = lg.LogicParser()


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


class SemParserV1(object):
    def __init__(self):
        self._traverse = {}
        self._chvar_dict = {}
    
    def reset(self):    
        self._traverse.clear()
        self._chvar_dict.clear()

    def get_parsed_sem(self,tree):
        self._traverse.clear()
        sem_str =  r"\P.( ((P)(e)) )((%s))"%(self.tree_traverse(tree)['sem'])
        #sem_str =  r"\P.( ((P)(e)) )((%s))"%(self.tree_traverse(tree)['sem'])
        return self.logic_parse(sem_str)

    def logic_parse(self, sem_str):
        #print sem_str
        return to_unicode(lg.LogicParser().parse(to_utf8_str(sem_str)).simplify().__str__())

    def gen_id(self, sem_str_raw):
        sem_str = to_unicode( sem_str_raw )
        ch_word = "".join(re.findall(ur'[\u4e00-\u9fff]+',sem_str))
        if ch_word not in self._chvar_dict.keys(): 
            self._chvar_dict.update({ch_word : len(self._chvar_dict)}) 
    #    print 'id',self._num_id
        return self._chvar_dict[ch_word]

    def gen_varname(self,pos,sem_str_raw):
        if pos[0] in ["N"]: 
            return "n%s"%(self.gen_id(sem_str_raw))

        elif (pos[0] in ["V"]) and (pos[0:2] not in ["VH"]):
            return "e%s"%(self.gen_id(sem_str_raw))

        else:
            return "d%s"%(self.gen_id(sem_str_raw))
        

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

        if pos[0] in ['P'] or pos[0:2] in ['DE'] :
            sem_str= r""
        else:
            sem_str= r"\x .%s(x)"%(tree[0])
#        if pos[0] in ['N'] :
#            #return "\p . p(%s,e)"%(tree[0])
#            #return "%s"%(tree[-1])
#            sem_str= r"\x .{pred}(x)".format(pred=ch_name)
#            #var_id="n%s"%(self.gen_id(tree[0]))
#
#        elif pos[0] in ['D'] :
#            #return "\p . p(%s,e)"%(tree[0])
#            #return "%s"%(tree[-1])
#            sem_str= r"\x .{pred}(x)".format(pred=ch_name)
#            #var_id="n%s"%(self.gen_id(tree[0]))
#
#        elif pos[0] in ['V'] :
#            sem_str= r"%s(e)"%(ch_name)
#
#        elif pos[0] in ['P'] :
#            sem_str= r""
        return sem_str
         

    def gen_node_sem_1(self, tree, role, pos):
        node_dict = self.tree_traverse(tree[0])
        #print node_dict['sem'] , pos
        #if role and role != "DUMMY":
        #    if "P" == pos[0] or "N" == pos[0] :
        #        node_sem_str = r'%s(%s)(%s)'%(node_dict['sem'], role, "n%s"%(self.gen_id()) )
        #        return lgp.parse(node_sem_str.encode('utf-8')).simplify().__str__().decode('utf-8')
        return node_dict['sem']
        

    def change_node_sem_1(self, sem, role, pos):
        if role and role != "DUMMY" and role != "Head" and sem !='' and role != "head" :
            #if pos[0] in ['P', 'N', 'D'] or pos[0:2] in ['VH']:
            #print 'sem',sem
            #print 'role',role
            #print 'self.varname',self.gen_varname(pos,sem) 
            node_sem_str = r'\P Q n m .(P(n) & Q(n,m))((%s))(%s)(%s)'%(sem, role , self.gen_varname(pos,sem))
            #print node_sem_str
            #print node_sem_str
            return self.logic_parse(node_sem_str)
        return sem



    def gen_node_sem_2(self, tree, role='', pos=''):
        assert len(tree) > 1 
        
        nary_dict =  map(lambda node : ( node['role'],node )
                              ,map(lambda subtree : self.tree_traverse(subtree)  , tree) )

        map(lambda n_elem : n_elem.update({ 'sem':self.change_node_sem_1(n_elem['sem'],n_elem['role'],n_elem['pos'])}) 
                             ,map(itemgetter(1),nary_dict)    )

        node_sem_ary = filter(lambda x : len(x) > 0,  map(itemgetter('sem'), map(itemgetter(1),nary_dict)))

        template_str = apply(lambda alpha_bet :
                        r"\ %s r.((%s))"%(" ".join(alpha_bet) , r" & ".join(map(lambda i : "%s(r)"%(i) ,  alpha_bet )))
                        , [map(lambda i : (chr(i+ord('A'))) , range(len(node_sem_ary)))] )
        
        sem_str = reduce(lambda a,b : "%s(%s)"%(a,b) , node_sem_ary , template_str )

        return self.logic_parse(sem_str)


if __name__ == "__main__" : # or __name__ == "semParser":
    sp = SemParserV1() 
    str_tree = _TEST_DICT[int(argv[1])]
    t1 = run_parser(str_tree)
    print sp.get_parsed_sem(t1).encode('utf-8')
