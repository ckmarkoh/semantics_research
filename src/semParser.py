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


class SemParserV2(object):
    def __init__(self):
        self._traverse = {}
        self._chvar_dict = {}
    
    def reset(self):    
        self._traverse.clear()
        self._chvar_dict.clear()

    def get_parsed_sem(self,tree):
        self._traverse.clear()
        sem_str =  r"\P.( ((P)(e)) )((%s))"%(self.tree_traverse(tree)['sem'])
        #print sem_str
        #sem_str =  r"\P.( ((P)(e)) )((%s))"%(self.tree_traverse(tree)['sem'])
        return self.logic_parse(sem_str)

    def logic_parse(self, sem_str):
        #print sem_str
        return to_unicode(lg.LogicParser().parse(to_utf8_str(sem_str)).simplify().__str__())

    def get_ch_word(self,sem_str):
        return  "".join(re.findall(ur'[\u4e00-\u9fff]+',to_unicode(sem_str)))

    def gen_id(self, sem_str_raw):
        #sem_str = to_unicode( sem_str_raw )
        #ch_word = "".join(re.findall(ur'[\u4e00-\u9fff]+',sem_str))
        ch_word = self.get_ch_word(sem_str_raw)
        if ch_word not in self._chvar_dict.keys(): 
            self._chvar_dict.update({ch_word : len(self._chvar_dict)}) 
    #    print 'id',self._num_id
        return self._chvar_dict[ch_word]

    def gen_varname(self,pos,sem_str_raw):
        if pos[0] in ["N"]: 
            return "n%s"%(self.gen_id(sem_str_raw))
        elif ((pos[0] in ["V"]) and (pos[0:2] not in ["VH"])) or (pos[0] in ["S"]):
            return "e%s"%(self.gen_id(sem_str_raw))
        else:
            return "n%s"%(self.gen_id(sem_str_raw))
        

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
        

    def change_node_sem_1(self, sem_input, role, pos):
        if type(sem_input) is list:
            assert len(sem_input[0]) == 2
            if role and role not in [ "DUMMY","DUMMY1","DUMMY2"]  and role not in [ "Head","head"] :
                sem_output = map(lambda sem, role, pos :self.logic_parse(
                                r'\P Q n m .(P(n) & Q(n,m))((%s))(%s)(%s)'%(sem, role , self.gen_varname(pos,sem))) 
                                    ,sem_input[0],[role]*len(sem_input[0]),[pos]*len(sem_input[0]))
                sem_str = sem_input[1]%(sem_output[0],sem_output[1])
                return self.logic_parse(sem_str)
            else:
                return sem_input 
        elif type(sem_input) in [unicode,str]:
            sem = sem_input
            if role and role not in [ "DUMMY","DUMMY1","DUMMY2"]  and role not in [ "Head","head"]  and sem !='' :
                node_sem_str = r'\P Q n m .(P(n) & Q(n,m))((%s))(%s)(%s)'%(sem, role , self.gen_varname(pos,sem))
                return self.logic_parse(node_sem_str)
            return sem
        else:
            assert 0
        #sem_str = template_str%(node_sem_ary[0],node_sem_ary[1])

    #def change_node_sem_1_sub(self, sem, role, pos):
    #    if role and role not in [ "DUMMY","DUMMY1","DUMMY2"]  and role not in [ "Head","head"]  and sem !='' :
    #        node_sem_str = r'\P Q n m .(P(n) & Q(n,m))((%s))(%s)(%s)'%(sem, role , self.gen_varname(pos,sem))
    #        return self.logic_parse(node_sem_str)
    #    return sem

    def gen_node_sem_2(self, tree, role='', pos=''):
        assert len(tree) > 1 
        nary_dict =  map(lambda node : ( node['role'],node )
                              ,map(lambda subtree : self.tree_traverse(subtree)  , tree) )

        map(lambda n_elem : n_elem.update({ 'sem':self.change_node_sem_1(n_elem['sem'],n_elem['role'],n_elem['pos'])}) 
                             ,map(itemgetter(1),nary_dict)    )
        
        head_node = dict(nary_dict).get('Head')

        neg_sign = apply(lambda x: '' if len(x)%2==0 else '-'
                         ,[filter(lambda x:x[0]=='negation', nary_dict)])

        
        if head_node["pos"] == "Caa":
            node_sem_ary,template_str = self.gen_sem_coordination(nary_dict, head_node)
            return [node_sem_ary,template_str]
        #elif head_node["sem"]
        elif type(head_node["sem"]) is list:
            #head_node["sem"]
            node_sem_ary,template_str = self.gen_sem_coordination_2(nary_dict,neg_sign)
            sem_str = map(lambda x: reduce(lambda a,b : "%s(%s)"%(a,b) , node_sem_ary+[x] , template_str ),head_node["sem"][0])
            #head_node["sem"][0]
            #MyPrinter(sem_str)
            #MyPrinter(node_sem_ary)
            #MyPrinter(template_str)
            node_sem_ary_2 = map(self.logic_parse,sem_str)
            return [node_sem_ary_2,head_node["sem"][1]]
            #assert 0
        else:
            sem_is_list =filter(lambda sem: type(sem) is list, map(itemgetter("sem"),map(itemgetter(1) ,nary_dict)))
            if len(sem_is_list) > 0 and head_node["sem"] =="":
                print len(sem_is_list)
                assert len(sem_is_list) ==1
                #MyPrinter(sem_is_list[0])
                return sem_is_list[0]
            #for nary in nary_dict:
            #    MyPrinter(nary[1])
                #assert 0
            else:
                node_sem_ary,template_str = self.gen_sem_multinode(nary_dict,neg_sign)
                sem_str = reduce(lambda a,b : "%s(%s)"%(a,b) , node_sem_ary , template_str )
                #print  'head',head_node
                #print 'node_sem_ary'
                #MyPrinter(node_sem_ary)
                #print 'template_str'
                #MyPrinter(template_str)
                #print sem_str
                #sem_str = self.gen_sem_multinode(nary_dict,neg_sign)
                return self.logic_parse(sem_str)


    def gen_sem_multinode(self, nary_dict, neg):
        node_sem_ary = filter(lambda x : len(x) > 0,  map(itemgetter('sem')
                                               , map(itemgetter(1),filter(lambda x:x[0]!='negation' ,nary_dict))
                                              ))
        template_str = apply(lambda alpha_bet :
                        r"\ %s r.(%s(%s))"%(" ".join(alpha_bet),neg, r" & ".join(map(lambda i : "%s(r)"%(i) ,  alpha_bet )))
                        , [map(lambda i : (chr(i+ord('A'))) , range(len(node_sem_ary)))] )
        return node_sem_ary, template_str
        #print template_str
        #sem_str = reduce(lambda a,b : "%s(%s)"%(a,b) , node_sem_ary , template_str )
        #return sem_str

    def gen_sem_coordination_2(self, nary_dict, neg):
        node_sem_ary = filter(lambda x : len(x) > 0,  map(itemgetter('sem')
                                            , map(itemgetter(1), filter(lambda x:x[0]!='Head' ,nary_dict))
                                           ))
        template_str = apply(lambda alpha_bet :
                        r"\ %s r.(%s(%s))"%(" ".join(alpha_bet),neg, r" & ".join(map(lambda i : "%s(r)"%(i) ,  alpha_bet )))
                        , [map(lambda i : (chr(i+ord('A'))) , range(len(node_sem_ary)+1))] )
        return node_sem_ary, template_str

    def gen_sem_coordination(self, nary_dict, head_node):
        node_sem_ary = filter(lambda x : len(x) > 0,  map(itemgetter('sem')
                                            , map(itemgetter(1), filter(lambda x:x[0]!='Head' ,nary_dict))
                                           ))
        assert len(node_sem_ary)==2
        ch_word = self.get_ch_word(head_node['sem'])
        if ch_word in [u'和',u'跟',u'與',u'同',u'暨',u'及',u'又',u'而',u'且' ]:
            template_str = r"\P Q r.(P(r) & Q(r))(%s)(%s)"
        elif ch_word in [u'或',u'或者',u'還是',u'或是']:
            template_str = r"\P Q r.(P(r) | Q(r))(%s)(%s)"
        else:
            print "Non support coordination"
            assert 0
        #sem_str = template_str%(node_sem_ary[0],node_sem_ary[1])
        return node_sem_ary,template_str#,sem_str
            #TODO  

if __name__ == "__main__" : # or __name__ == "semParser":
    sp = SemParserV2() 
    str_tree = _TEST_DICT[int(argv[1])]
    t1 = run_parser(str_tree)
    print sp.get_parsed_sem(t1).encode('utf-8')
