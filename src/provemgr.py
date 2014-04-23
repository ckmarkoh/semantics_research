# -*- coding: utf-8 -*-
from nltk import ResolutionProver
from nltk import TableauProver
from nltk import Prover9
from util import *
import nltk.sem.logic as lgc


class ProveMgr(object):

    def __init__(self): 
        self.prover = Prover9()
        self.tabu_prover = TableauProver()

    def prove(self, pre_str, con_str, tabu=False):
        if isinstance( pre_str, str) or isinstance( pre_str, unicode):
            pre = [lgc.LogicParser().parse(to_utf8_str(pre_str))]
        elif isinstance( pre_str, list):
            pre = map(lambda s : lgc.LogicParser().parse(to_utf8_str(s)), pre_str)
        else:
            assert 0
        con = lgc.LogicParser().parse(to_utf8_str(con_str))
        if not tabu:
            return self.prover.prove(con,pre)
        else:
            return self.tabu_prover.prove(con,pre,verbose=True)
   
