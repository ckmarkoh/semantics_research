# -*- coding: utf-8 -*-
from nltk import ResolutionProver
from nltk import TableauProver
from nltk import Prover9
from util import *
import nltk.sem.logic as lgc
import operator as opr
import logging
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
        (result, pre, con), output = apply(  capture_output(self.prove_prover), [ pre_str, con_str, "tableau"] )
        unsolved = apply(lambda opt_line : 
                            opr.itemgetter(filter(lambda i: opt_line[i] == 'AGENDA EMPTY' 
                                                ,range(1,len(opt_line)))[0]-1)(opt_line)
                                                    , [ map(lambda s : s.strip() ,  output.split('\n'))] )
        pre0 = pre[0]
        #print unsolved
        #print result
        #pre0 = lgc.LogicParser().parse('( agent(n0,e) & A0X99AC_0X82F1_0X4E5D(n0) & A0X4E2D_0X7814_0X9662(d1) & location(d1,e) & A0X767C_0X8868(e) & A0X6F14_0X8B1B(n2))')
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


        

    def logic_same_variable(self, lgf_ary, lgf, ftype, inv=False):
        assert ftype == 'variables' or ftype == 'predicates'
        if not inv:
            return filter(lambda f : opr.attrgetter(ftype)(lgf)() \
                                     .issubset(opr.attrgetter(ftype)(f)()) ,lgf_ary)
        else:
            return filter(lambda f : not opr.attrgetter(ftype)(lgf)() \
                                     .issubset(opr.attrgetter(ftype)(f)()) ,lgf_ary)

            

    
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
