# -*- coding: utf-8 -*-
from nltk import Prover9
from util import *
import nltk.sem.logic as lgc


class ProveMgr(object):

    def __init__(self): 
        self.prover = Prover9()

    def prove(self, pre_str, con_str):
        if isinstance( pre_str, str) or isinstance( pre_str, unicode):
            pre = [lgc.LogicParser().parse(to_utf8_str(pre_str))]
        elif isinstance( pre_str, list):
            pre = map(lambda s : lgc.LogicParser().parse(to_utf8_str(s)), pre_str)
        else:
            assert 0
        con = lgc.LogicParser().parse(to_utf8_str(con_str))
        return self.prover.prove(con,pre)
