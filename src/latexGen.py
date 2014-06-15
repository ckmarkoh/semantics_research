#-*- coding:utf-8 -*-
import re
from sys import argv
from util import gen_ch_id
class LatexGen(object):
    def __init__(self):
        self.reset_ltree

    def reset_ltree(self):
        self.buff=[]
        self.nc=0

    def get_inc_nc(self):
        self.nc+=1
        return "N%s"%(self.nc)

    def tree_to_latex(self,tree):  
        self.reset_ltree()
        self.buff.append( r"\Tree")
        self.tree_traverse(tree,0)
        return "\n".join(self.buff)

    def tree_traverse(self,tree,level):
        if self.tree_is_terminal(tree):
            self.print_node(tree.node.split(":"),level=level,dot='[.')
            self.print_node([tree[0]],level=level+1,dot='')
            self.buff.append( " "*level+"]")
        else:
            if tree.node != 'Node':
                self.print_node(tree.node.split(":"),level=level,dot='[.')
                for ts in tree:
                    self.tree_traverse(ts,level+1)
                self.buff.append(" "*level+"]")
            else:
                for ts in tree:
                    self.tree_traverse(ts,level)

    def tree_is_terminal(self, tree):
        if len( tree) == 1:
            if  isinstance( tree[0], unicode):
                return True
        return False
 
    def print_node(self,t,dot='.',level=0):
        if len(t)==1:
            self.buff.append( " "*(level)+r"%s\node(%s){%s};"%(dot,self.get_inc_nc(),t[0]) )
        else:
            self.buff.append( " "*(level)+\
            r"%s\node(%s){\begin{tabular}{c}%s\\%s\end{tabular}};"%(dot,self.get_inc_nc(),t[0],t[1]))

    def sem_to_latex(self,sem):
        sem_ch = re.search(ur'([\u4e00-\u9fff\uff01-\uff5e]+)',sem)
        ch_dict = {}
        while sem_ch != None: 
            ch = sem_ch.group()
            ch_id = gen_ch_id(ch)
            ch_dict.update( {ch_id: ch} )
            sem = sem.replace(ch,r"\text{%s}"%(ch_id))
            sem_ch = re.search(ur'([\u4e00-\u9fff\uff01-\uff5e]+)',sem)
        for ch_id in ch_dict:
            sem = sem.replace(ch_id,ch_dict[ch_id])
        sem = sem.replace('&',r'\wedge')
        sem = sem.replace('->',r'\rightarrow')
        return sem

if __name__ == "__main__":
   ltg = LatexGen()
   print ltg.sem_to_latex(argv[1].decode('utf-8'))
