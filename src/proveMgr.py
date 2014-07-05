# -*- coding: utf-8 -*-
from nltk import ResolutionProver
from nltk import TableauProver
from nltk import Prover9
from util import *
import nltk.sem.logic as lgc
import operator as opr
import logging
from myPrinter import MyPrinter
#logging.basicConfig(level=logging.DEBUG)



class ProveMgr(object):

    def __init__(self): 
        self._nine_prover = Prover9()
        self._tabu_prover = TableauProver()
        self._reso_prover = ResolutionProver()

    

    def prove(self, pre_str, con_str):
        pre, con = self.parse_logic(pre_str,con_str)
        return self._nine_prover.prove(con,pre,verbose=True)

    def parse_logic(self, pre_str, con_str):
        if isinstance( pre_str, str) or isinstance( pre_str, unicode):
            pre = [lgc.LogicParser().parse(to_utf8_str(pre_str))]
        elif isinstance( pre_str, list):
            pre = map(lambda s : lgc.LogicParser().parse(to_utf8_str(s)), pre_str)
        else:
            assert 0
        con = lgc.LogicParser().parse(to_utf8_str(con_str))
        return pre,con

       # else:
       #     return self.tabu_prover.prove(con,pre,verbose=True)
    
    def prove_prover(self, pre_str, con_str, prover):
        pre, con = self.parse_logic(pre_str,con_str)
        this_prover = {"nine"      : self._nine_prover,
                       "tableau"   : self._tabu_prover,
                       "resolution": self._reso_prover,
                        } [prover]
        return (this_prover.prove(con,pre,verbose=True),pre,con)

    def prove_prover_catch_output(self,pre_str,con_str, prover):
        (result, pre, con), output = apply(  capture_output(self.prove_prover), [ pre_str, con_str, prover] )
        return (result,pre,con,output)


    def prove_catch_unsolved(self,pre_str,con_str):
        print "!!!"
        pre, con = self.parse_logic(pre_str,con_str)
        con_split = self.logic_split_and(con)
        pre_split = self.logic_split_and(pre[0])
        word_pre = self.logic_and_getword(pre_split)
        word_con = self.logic_and_getword(con_split)
        knowledge_ary = []
        for w in word_pre:
            if w not in word_con: 
                w_arg_form = self.logic_word_form(pre_split, w)
                w_arg = w_arg_form.args[0]
                w_roles = self.logic_get_role(pre_split, w_arg, 'variables')  
                print w_arg
                if len(w_roles) > 0 and w_arg.__str__() !='e': 
                    assert len(w_roles) == 1
                    w_role_pred = w_roles[0].pred
                    w_con_roles= self.logic_get_role(con_split, w_role_pred, 'predicates')  
                    if len(w_con_roles) > 0:
                        assert len(w_con_roles) == 1
                        w_con_args= set(w_con_roles[0].args).difference(set(w_roles[0].args))
                        assert len(w_con_args) == 1
                        w_con_arg = w_con_args.pop()
                        w_con_form =  self.logic_arg_form(con_split, w_con_arg)
                        w_con_word = w_con_form.pred
                        lgf = "%s & %s -> %s & %s"%(w_arg_form, w_roles[0], w_con_form, w_con_roles[0])
                        print lgf
                        knowledge_ary.append({'w1':w,'w2':w_con_word,'lgf':lgf})
                else:
                    w_con_form = self.logic_arg_form(con_split,w_arg) 
                    w_con_word = w_con_form.pred
                    lgf = "%s -> %s"%(w_arg_form, w_con_form)
                    knowledge_ary.append({'w1':w,'w2':w_con_word,'lgf':lgf})
        MyPrinter( knowledge_ary)
        assert 0

    def logic_word_form(self, lgf_ary, w):
        return filter(lambda x: x.pred.__str__()==w, lgf_ary )[0]#.args[0]

    def logic_arg_form(self, lgf_ary, arg):
        return filter(lambda x: arg in x.args and len(x.args) == 1, lgf_ary )[0]#.pred
       
    def logic_get_role(self, lgf_ary, input_str, ftype):
        if ftype == 'variables':
            return filter(lambda x: input_str in x.args and len(x.args)>1, lgf_ary)
        elif ftype == 'predicates':
            return filter(lambda x: input_str == x.pred and len(x.args)>1, lgf_ary)
        else:
            assert 0

    def logic_and_getword(self, lgf_ary):
        return [x.pred.__str__() for x in  filter(lambda x: x.pred.__str__().find('A0X')!=-1, lgf_ary)]

    def logic_split_and(self, lgf): 
        if isinstance(lgf, lgc.AndExpression):
            lgf_0 , lgf_1 = lgf.first, lgf.second#lgf.visit(lambda x:x, lambda x:x)
            return [lgf_1] + self.logic_split_and(lgf_0)
        else:
            return [lgf]






    def logic_drop_var(self, lgf): 
        if isinstance(lgf, lgc.ApplicationExpression):
            lgf_0 , lgf_1 = lgf.visit(lambda x:x, lambda x:x)
            return lgf_0,lgf_1
        else:
            assert 0 

    def logic_same_variable(self, lgf_ary, lgf, ftype, inv=False):
        assert ftype == 'variables' or ftype == 'predicates'
        if not inv:
            return filter(lambda f : opr.attrgetter(ftype)(lgf)() \
                                     .issubset(opr.attrgetter(ftype)(f)()) ,lgf_ary)
        else:
            return filter(lambda f : not opr.attrgetter(ftype)(lgf)() \
                                     .issubset(opr.attrgetter(ftype)(f)()) ,lgf_ary)

    def prove_catch_unsolved_2(self,pre_str,con_str):
        (result, pre, con), output = apply(  capture_output(self.prove_prover), [ pre_str, con_str, "tableau"] )
        unsolved = apply(lambda opt_line : 
                            opr.itemgetter(filter(lambda i: opt_line[i] == 'AGENDA EMPTY' 
                                                ,range(1,len(opt_line)))[0]-1)(opt_line)
                                                    , [ map(lambda s : s.strip() ,  output.split('\n'))] )
        pre0 = pre[0]
        con_split = self.logic_split_and(con)
        pre0_split = self.logic_split_and(pre0)
        unsolved_lgf = lgc.LogicParser().parse(unsolved)
        #print con_split
        #print unsolved_lgf
        #print pre0_split
        con_label = self.logic_same_variable(
                             self.logic_same_variable(con_split, unsolved_lgf, 'variables')
                                      ,unsolved_lgf,'predicates',True)[0]
        #print con_label 
        pre0_label = self.logic_same_variable(pre0_split, con_label, 'predicates')[0]
        #print pre0_label
        pre0_var0, pre0_var1 = self.logic_drop_var(pre0_label)
        pre0_unsolved = self.logic_same_variable(
                                self.logic_same_variable(pre0_split, pre0_var0, 'variables')
                                        ,pre0_var1,'variables',True)[0]
        #print pre0_unsolved
        con_unsolved = unsolved_lgf.negate()
        missing_rule =  lgc.LogicParser().parse(
                            "%s -> %s"%(pre0_unsolved & pre0_label ,con_unsolved & con_label ))
        
        # pre
        return (con_unsolved.predicates().pop().__str__()  
              , pre0_unsolved.predicates().pop().__str__()
              , missing_rule.__str__())
