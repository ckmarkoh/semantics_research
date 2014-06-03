# -*- coding: utf-8 -*-
from nltk import Tree
#from sys import argv
#from buildtree import run_parser, treestr_to_tree
#from connect_ckip import sinica_parse, sinica_parse_0
from myPrinter import MyPrinter
import semMgr as smg
import ckipParser as ckp
import proveMgr as pv
import nltk.sem.logic as lgc
from optparse import OptionParser
import argparse
#Prover9().prove(c, [p1,p2])


_INPUT_DICT_SIMPLE = {
0:u"S(agent:NP(property:N‧的(head:Nca:臺灣|Head:DE:的)|Head:Ncb:大學)|manner:VH11:懇切|Head:VE12:呼籲|theme:NP(property:VH11:平和|Head:Nad:理性))",
1:u"S(agent:NP(Head:Nhaa:我)|Head:VC2:幫助|goal:NP(property:Nbc:陳|Head:Nab:小姐))",
2:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
3:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
4:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
5:u"S(agent:NP(Head:Nb:布魯圖)|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒)) ",
6:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
7:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))", 
8:u"S(agent:NP(Head:Nb:姚明)|theme:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(quantifier:DM:２００２年|agent:Nb:ＮＢＡ|Head:Nv:選秀)|Head:Ng:中))|agent:PP(Head:P02:被|DUMMY:NP(property:Nc:休斯敦|Head:Nba:火箭隊))|Head:VG1:選為|range:NP(property:Nab:狀元|Head:Nab:新秀))",
9:u"S(agent:NP(Head:Nb:姚明)|theme:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(quantifier:DM:２００２年|agent:Nb:ＮＢＡ|Head:Nv:選秀)|Head:Ng:中))|agent:PP(Head:P02:被)|Head:VG1:選為|range:NP(property:Nab:狀元|Head:Nab:新秀))",
}
_INPUT_DICT = {
11:"S(agent:NP(Head:Nba:柯文哲)|time:Ndabd:昨天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:台大))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
12:"S(agent:NP(Head:Nba:柯文哲)|time:Ndabd:昨天|Head:VC31:發表|theme:NP(Head:Nad:演講))",
201:u"S(theme:NP(property:N‧的(head:Nca:香港|Head:DE:的)|Head:Nad(DUMMY1:Nad:主權|Head:Caa:和|DUMMY2:Nab:領土))|Head:V_12:是|range:PP(Head:P21:在|DUMMY:NP(property:DM:１９９７年|predication:VP‧的(head:VP(location:PP(Head:P06:由|DUMMY:NP(Head:Nca:英國))|Head:V(Head:VD1:歸還|Head:VD1:給)|goal:NP(property:Nca:中國))|Head:DE:的))))",
202:u"S(theme:Nca:香港|time:PP(Head:P21:在|DUMMY:DM:１９９７年)|Head:VC1:回歸|goal:NP(Head:Nca:中國))",
212:u"S(theme:NP(quantifier:DM:１９９７年|Head:Nca:香港)|Head:VC1:回歸|goal:NP(Head:Nca:中國))",
301:u"S(time:GP(DUMMY:S(theme:NP(quantifier:DM:一九九一年|property:Nca:波斯灣|Head:Nac:戰爭)|Head:VH16:結束)|Head:Ng:時)|agent:NP(Head:Nb:雅辛)|time:Dd:又|Head:VC:帶|aspect:Di:著|theme:NP(Head:Nab:家人)|complement:VP(Head:VC1:移居|goal:NP(Head:Nca:約旦)))",
501:u"S(location:GP(DUMMY:NP(property:DM:二次|property:Ncb:世界|Head:Nad:大戰)|Head:Ng:時)|agent:NP(property:Nca:日本|Head:Nca:廣島)|agent:PP(Head:P60:遭)|Head:VC32:投|theme:NP(Head:Nab:原子彈))",
502:u"S(agent:Nca:廣島|condition:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(property:DM:二次|property:Ncb:世界|Head:Nad:大戰)|Head:Ng:時))|agent:PP(Head:P60:遭|DUMMY:NP(Head:Nab:原子彈))|Head:VC2:轟炸)",
1101:u"S(agent:NP(DUMMY1:NP(property:Nb:畢蘭德拉|Head:Nab:國王)|Head:Caa:和|DUMMY2:NP(apposition:Nab:皇后|Head:Nb:艾斯瓦利亞))|time:PP(Head:P21:在|DUMMY:DM:１９９７年)|Head:VA4:結婚)",
1102:u"S(theme:NP(DUMMY1:Nb:畢蘭德拉|Head:Caa:和|DUMMY2:Nb:艾斯瓦利亞)|Head:V_12:是|range:NP(Head:Naeb:夫妻))",
1801:u"S(agent:NP(property:Nca:尼泊爾|property:Nb:毛派|property:Nv4:叛亂|Head:Nab:份子)|condition:PP(Head:P21:在|DUMMY:NP(property:NP(property:VH11:新|Head:Nab:國王)|Head:Nad:大壽))|time:Ndabf:前夕|Head:VC2:發動|goal:NP(Head:Nv1:攻擊))",
1802:u"S(agent:NP(property:Nca:尼泊爾|property:Nb:毛派|property:Nv4:叛亂|Head:Na:分子)|condition:PP(Head:P21:在|DUMMY:NP(property:NP(property:VH11:新|Head:Nab:國王)|Head:Nad:華誕))|time:Ndabf:前夕|Head:VC2:發動|goal:NP(Head:Nv1:攻擊))",
2401:u"S(theme:NP(property:Nb:希拉瑞|Head:Nab:爵士)|Head:V_12:是|range:NP(predication:S‧的(head:S(agent:NP(Head:Nad:首位)|manner:VH11:成功|Head:VC2:攀上|goal:NP(Head:Na:聖母峰))|Head:DE:的)|Head:Nab:人))",
2402:u"S(theme:NP(property:Nb:希拉瑞|Head:Nab:爵士)|time:Dd:即|Head:V_12:是|range:NP(property:GP(DUMMY:VP(Head:V_2:有|range:NP(Head:Nac:紀錄))|Head:Ng:以來)|quantifier:DM:第１位|predication:VP‧的(head:VP(Head:VC1:登上|goal:NP(Head:Na:聖母峰))|Head:DE:的)|Head:Nab:人))",
}


def main():
    sm = smg.SemMgr()
    #cp = ckp.CkipParser()
    parser = argparse.ArgumentParser(prog='main')
    parser.add_argument('itype', metavar='itype', choices=['raw','treestr','id']
                        , type=str, help='input type: %(choices)s ')
    parser.add_argument('otype', metavar='otype', choices=['tree', 'sem', 'lsem','prove']
                        , type=str, help='output type: %(choices)s ')
    parser.add_argument('inpstr', metavar='str', nargs='*', type=str, help='input string 1')
#    parser.add_argument('--id', metavar='id', type=id, help='test file path')
    
    args = parser.parse_args()

    #print args
     #a=  lambda(x,f: reduce( apply(f,[x]) 
     
    input_str = args.inpstr

    #print input_str
    t1 = None
    if args.itype == 'raw':
        flist = [ sm.str_raw_to_str_tree,  sm.str_tree_to_tree]

    elif args.itype == 'treestr':
        flist = [sm.str_tree_to_tree]

    elif args.itype == 'id':
        flist = [lambda x : _INPUT_DICT[int(x)],sm.str_tree_to_tree ]
        
    t_list = map(lambda y : reduce(lambda x,f: f(x), flist , y) , input_str)
     
    if args.otype == 'tree':
        for t in t_list:
            t.draw()

    elif args.otype == 'sem':
        s_list = map(lambda t :  sm.tree_to_sem(t) ,t_list)
        for s in s_list:
            print s 

    elif args.otype == 'lsem':
        s_list = map(lambda t :  sm.tree_to_sem_latex(t) ,t_list)
        for s in s_list:
            print s

    elif args.otype == 'prove':
        s_list = map(lambda t :  sm.tree_to_sem(t) ,t_list)
        print pv.ProveMgr().prove( map( lambda s : sm.sem_remove_chinese(s) , s_list[0:-1]) , sm.sem_remove_chinese(s_list[-1]))


if __name__ == "__main__"  :
    main()
