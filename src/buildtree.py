# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc
from nltk import Tree

# List of token names.   This is always required
tokens = (
   'TAG',
#   'STS',
   'COLON',
   'PIPE',
   'HAN',
   'NUM',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_TAG     = r'[A-Za-z][A-Za-z0-9_]*'
#t_STS     = r'[A-Z]'
t_COLON   = r':'
t_PIPE    = r'\|'
t_HAN     = ur'[\u4e00-\u9fff]+'
t_NUM     = r'[0-9]+'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code

# Define a rule so we can track line numbers
#def t_newline(t):
#    r'\n+'
#    t.lexer.lineno += len(t.value)
#
## A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'
#
## Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    #print t.value
    #t.value=t.value[1:]
    #t.value[0]=t.value[0].replace()
    t.lexer.skip(1)

#lexer.input(data)

# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok: break      # No more input
#    print tok
def p_start(p):
    'start : tag pars'
    p[0]= u"( %s %s )"%(p[1],p[2])

def p_st_1(p):
    'st : labl COLON han'
    p[0]= "( %s %s )"%(p[1],p[3])

def p_st_2(p):
    'st : labl pars' 
    p[0]= "( %s %s )"%(p[1],p[2])

def p_pars_stg(p):
    'pars : LPAREN stGropu RPAREN'
    p[0]= "(Node %s )"%(p[2])

def p_stg_st(p):
    'stGropu : st'
    p[0]= "%s"%(p[1])

def p_stg_stg(p):
    'stGropu : st PIPE stGropu'
    p[0]= "%s %s"%(p[1],p[3])


def p_labl_sem(p):
    'labl : sem COLON tag'
    p[0]= "%s:%s"%(p[1],p[3])
    

#def p_stsval(p):
#    'sts : STS'
#    p[0]="sts:%s"%(p[1])

def p_tagval(p):
    'tag : TAG'
    p[0]="%s"%(p[1])


def p_semval(p):
    'sem : TAG'
    p[0]="%s"%(p[1])

def p_hanval(p):
    'han : HAN'
    p[0]="%s"%(p[1])

def p_nanval(p):
    'han : NUM'
    p[0]="%s"%(p[1])

# Error rule for syntax errors
def p_error(p):
    print "Syntax error",(p)

lexer = lex.lex()
parser = yacc.yacc()



def run_parser(data):
    #data = u'S(hypothesis:Cbaa:如果|experiencer:NP(Head:Nhac:您)|Head:VK2:需要|goal:NP(quantifier:Neqa:大量|Head:Nad:剖析))'
    data=data.replace(u'\u2027\u7684','_DE')
    #print [data]
    result = parser.parse(data)
    
#    print result
    tree=Tree.parse(result)
#    tree.chomsky_normal_form()
#    tree.pprint()
#    tree.draw()
    return tree

def treestr_to_tree(data):
    return run_parser(data)
#print [argv[1]]
#input_data=u'S(hypothesis:Cbaa:如果|experiencer:NP(Head:Nhac:您)|Head:VK2:需要|goal:NP(quantifier:Neqa:大量|Head:Nad:剖析))'
#run(input_data)
