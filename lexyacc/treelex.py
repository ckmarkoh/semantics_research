# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc
import pprint
from nltk import Tree
from MyPrinter import MyPrinter

# List of token names.   This is always required
tokens = (
   'TAG',
   'COLON',
   'PIPE',
   'HAN',
   'NUM',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_TAG     = r'[A-Za-z][A-Za-z0-9]*'
t_COLON   = r':'
t_PIPE    = r'\|'
t_HAN     = ur'[\u4e00-\u9fff]+'
t_NUM     = r'[0-9]+'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()
#lexer.input(data)

# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok: break      # No more input
#    print tok


def p_elm_han(p):
    'elm : tag COLON han'
    #p[0]= " %s :: %s"%(p[1],p[3])
    p[0] = {} 
    p[0].update(p[1])
    p[0].update(p[3])
    #print p[0]

def p_elm_col(p):
    'elm : tag pars'
    #p[0]= " %s :: pars:%s"%(p[1],p[2])
    p[0] = {} 
    p[0].update(p[1])
    p[0].update(p[2])
    #print p[0]

def p_col_semGroup(p):
    'pars : LPAREN semGroup RPAREN'
    #p[0]= "( %s ) "%(p[2])
    p[0]={'2_pars':p[2]}

def p_semGroup_sem(p):
    'semGroup : semelm '
    #p[0]= "%s"%(p[1])
    p[0]=[]
    p[0].append(p[1])

def p_semGroup_semGroup(p):
    'semGroup : semelm PIPE semGroup'
    #p[0]= " %s | %s "%(p[1],p[3])
    p[0]=[p[1]]+p[3]

def p_sem_elm(p):
    'semelm : sem COLON elm'
    #p[0]= " %s :: %s "%(p[1],p[3])
    p[0]={}
    p[0].update(p[1])
    p[0].update(p[3])

def p_tagval(p):
    'tag : TAG'
    #p[0]="tag(%s)"%(p[1])
    p[0]={'2_tag':p[1]}

def p_semval(p):
    'sem : TAG'
    #p[0]="sem(%s)"%(p[1])
    p[0]={'1_sem':p[1]}

def p_hanval(p):
    'han : HAN'
    #p[0]="han(%s)"%(p[1])
    p[0]={'3_han':p[1]}

def p_nanval(p):
    'han : NUM'
    #p[0]="han(%s)"%(p[1])
    p[0]={'3_num':p[1]}

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

parser = yacc.yacc()

#data = u'S(hypothesis:Cbaa:1|experiencer:NP(Head:Nhac:您)|Head:VK2:2|goal:NP(quantifier:Neqa:大量|Head:Nad:剖析))'
data = u'S(hypothesis:Cbaa:如果|experiencer:NP(Head:Nhac:您)|Head:VK2:需要|goal:NP(quantifier:Neqa:大量|Head:Nad:剖析))'
result = parser.parse(data)
#pprint.pprint( result)
MyPrinter(result).print_data()
