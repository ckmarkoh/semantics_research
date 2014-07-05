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
1:"S(agent:NP(Head:Nba:小明)|Head:VC2:玩|goal:NP(Head:Nab:電腦))",
2:"S(agent:NP(Head:Nba:小明)|location:PP(Head:P21:在|DUMMY:NP(Head:Ncb:家))|Head:VC2:玩|goal:NP(Head:Nab:電腦))",
3:"S(agent:NP(Head:Nba:小明)|time:Ndabd:昨天|Head:VC2:玩|goal:NP(Head:Nab:電腦))",
4:"S(agent:NP(Head:Nba:小明)|Head:VC2:玩|goal:NP(property:Nab:電腦|Head:Nac:遊戲))",
5:"S(agent:NP(apposition:Nab:校長|Head:Nb:楊泮池)|Head:VA4:致辭)",
6:"S(agent:NP(property:Nb:楊泮池|Head:Nab:校長)|Head:VA4:致辭)",
7:"S(theme:NP(Head:Nb:楊泮池)|Head:V12:是|range:NP(property:Nca:台大|Head:Nab:校長))",
8:"S(theme:NP(Head:Nb:楊泮池)|Head:V12:是|range:NP(property:Nca:台灣|property:Ncb:大學|Head:Nab:校長))",
9:"S(agent:NP(Head:Nba:小明)|Head:VC2:玩|goal:NP(property:V‧的(head:VH11:刺激|Head:DE:的)|property:Nab:電腦|Head:Nac:遊戲))",
10:"S(agent:NP(Head:Nba:小明)|agent:PP(Head:P21:在)|Head:VC2:玩|goal:NP(Head:Nab:電腦))",
11:"S(agent:NP(Head:Nba:小華)|Head:VE2:說|goal:S(agent:NP(Head:Nba:小明)|agent:PP(Head:P21:在)|Head:VC2:玩|goal:NP(Head:Nab:電腦)))",
12:"S(agent:NP(Head:Nba:小明)|Head:VC2:玩|goal:NP(property:N‧的(head:Nab:爸爸|Head:DE:的)|Head:Nab:電腦))",
13:"S(agent:NP(Head:Nba:小華)|Head:VE2:看|goal:S(agent:NP(Head:Nba:小明)|Head:VC2:玩|goal:NP(Head:Nab:電腦)))",
14:"S(agent:NP(Head:Nba:小華)|Head:VE2:說|goal:S(agent:NP(Head:Nba:小明)|location:PP(Head:P21:在|DUMMY:NP(Head:Ncb:家))|Head:VC2:玩|goal:NP(property:VP‧的(head:VP(degree:Dfa:最|Head:VH11:新)|Head:DE:的)|property:Nab:電腦|Head:Nac:遊戲)))",
15:"S(agent:NP(DUMMY1:Nba:小明|Head:Caa:和|DUMMY2:Nba:小華)|agent:PP(Head:P21:在)|Head:VC2:玩|goal:NP(Head:Nab:電腦))",
16:"S(agent:NP(DUMMY1:Nba(DUMMY1:Nba:小明|Head:Caa:、|DUMMY2:Nba:小華)|Head:Caa:和|DUMMY2:Nba:小王)|agent:PP(Head:P21:在)|Head:VC2:玩|goal:NP(Head:Nab:電腦))",
17:"S(agent:NP(Head:Nba:小明)|Head:VP(DUMMY1:VP(Head:VC2:玩|goal:NP(Head:Nab:電腦))|Head:Caa:或|DUMMY2:VP(Head:VC2:看|goal:NP(Head:Nab:電視))))",
18:"S(agent:NP(DUMMY1:Nba:小明|Head:Caa:或|DUMMY2:Nba:小華)|agent:PP(Head:P21:在)|Head:VC2:玩|goal:NP(Head:Nab:電腦))",
19:"S(agent:NP(Head:Nba:小明)|Head:VC2:玩|goal:Nab(DUMMY1:Nab:電腦|Head:Caa:或|DUMMY2:Nab:手機))",
20:"S(agent:NP(Head:Nba:小明)|Head:VC2:玩|goal:Nab(DUMMY1:Nab:電腦|Head:Caa:和|DUMMY2:Nab:手機))",
21:"S(agent:NP(Head:Nba:小明)|Head:VP(DUMMY1:VP(negation:Dc:不|Head:VC2:玩|goal:NP(Head:Nab:電腦))|Head:Caa:且|DUMMY2:VP(negation:Dc:不|Head:VC2:看|goal:NP(Head:Nab:電視))))",
22:"S(agent:NP(Head:Nba:小華)|target:PP(Head:P63:跟|DUMMY:NP(Head:Nab:同學))|Head:VE2:說|goal:S(agent:NP(property:N‧的(head:Ncb:隔壁班|Head:DE:的)|Head:Nba:小明)|Head:VP(DUMMY1:VP(negation:Dc:不|Head:VC2:玩|goal:NP(Head:Nab:電腦))|Head:Caa:又|DUMMY2:VP(negation:Dc:不|Head:VC2:看|goal:NP(Head:Nab:電視)))))",
23:"S(agent:NP(Head:Nba:小明)|negation:Dc:沒有|Head:VC2:玩)",
24:"S(agent:NP(Head:Nba:小明)|negation:Dc:沒有|negation:Dc:不|Head:VC2:玩)",
25:"S(agent:NP(Head:Nba:小明)|location:PP(Head:P21:在|DUMMY:NP(Head:Ncb:家))|Head:VA4:讀書|complement:VP(negation:Dc:不|Head:VC2:玩|goal:NP(Head:Nab:電腦)))",
26:"S(agent:NP(quantifier:Neqa:所有|Head:Nab:同學)|Head:VC2:通過|goal:NP(Head:Nad:考試))",
27:"S(agent:NP(quantifier:Neqa:所有|Head:Nab:同學)|quantity:Dab:都|Head:VC2:通過|goal:NP(Head:Nad:考試))",
28:"S(agent:NP(quantifier:Neqa:有些|Head:Nab:同學)|Head:VC2:通過|goal:NP(Head:Nad:考試))",
29:"S(experiencer:NP(Head:Nhaa:我們)|Head:VK1:喜歡|goal:NP(property:N‧的(head:Nad:黃色|Head:DE:的)|Head:Nad(DUMMY1:Nab:蝴蝶|Head:Caa:或|DUMMY2:Nab:蜜蜂)))",
30:"S(experiencer:NP(Head:Nhaa:我們)|Head:VK1:喜歡|goal:NP(property:Nad:蟲|Head:NP(property:N‧的(head:Nad:黃色|Head:DE:的)|property:VH13:大|Head:Nad(DUMMY1:Nab:蝴蝶|Head:Caa:或|DUMMY2:Nab:蜜蜂))))",
31:"S(agent:NP(Head:Nba:小華)|target:PP(Head:P63:跟|DUMMY:NP(Head:Nab:同學))|Head:VE2:說|goal:S(agent:NP(property:N‧的(head:Ncb:隔壁班|Head:DE:的)|Head:Nba:小明)|negation:Dc:不|Head:VC2:玩|goal:NP(DUMMY1:Nab:電腦|Head:Caa:和|DUMMY2:Nab:手機)))",
32:"S(theme:NP(Head:Nba:小明)|Head:VA4(DUMMY1:VA11:跑|Head:Caa:又|DUMMY2:VA11:跳))",
33:"S(agent:NP(Head:Nba:小明)|Head:VC2:通過|goal:NP(Head:Nad:考試))",
34:"S(theme:NP(quantifier:DM:每個|Head:Nab:學生)|quantity:Dab:都|Head:V_2:有|range:NP(quantifier:Neqa:一些|Head:Nac:作業))",
35:"S(agent:NP(Head:Nba:小明)|Head:VE2:說|goal:NP(agent:Nhaa:他|Head:VC2:通過|goal:NP(Head:Nad:考試)))",
36:"S(apposition:NP(property:Nca:台大|Head:Nab:教授)|Head:Nb:黃鐘楊)",
37:"S(agent:NP(Head:Nb:黃鐘楊)|Head:VA4:任教|location:PP(Head:P23:於|DUMMY:NP(Head:Nca:台大)))",
38:"S(goal:NP(Head:Nba:小明)|agent:PP(Head:P02:被|DUMMY:NP(Head:Nab:狗))|Head:VC2:咬)",
39:"S(agent:NP(Head:Nab:狗)|Head:VC2:咬|goal:NP(Head:Nba:小明))",
40:"S(agent:NP(Head:Nab:學生)|agent:PP(Head:P62:向|DUMMY:NP(property:Nbc:柯|Head:Nad:文哲))|Head:VE11:問|theme:NP(Head:Nac:問題))",
41:"S(goal:NP(property:Nbc:柯|Head:Nad:文哲)|agent:PP(Head:P02:被|DUMMY:NP(Head:Nab:學生))|Head:VE11:問|theme:NP(Head:Nac:問題))",
42:"S(experiencer:NP(Head:Nb:柯文哲)|Head:VK1:希望|goal:S(agent:NP(property:Nv:在場|Head:Nab:同學)|Head:VC31:建立|theme:NP(possessor:N‧的(head:Nhab:自己|Head:DE:的)|property:Nad:人生|Head:Nad:哲學)))",
43:"S(experiencer:NP(Head:Nb:柯文哲)|Head:VK1:希望|goal:S(agent:NP(Head:Nab:同學)|Head:VC31:建立|theme:NP(property:Nad:人生|Head:Nad:哲學)))",
44:"S(agent:NP(property:Nbc:柯|Head:Nad:文哲)|negation:Dc:沒有|Head:VC31:發表|theme:NP(Head:Nad:演講))",
45:"S(agent:NP(property:Nbc:柯|Head:Nad:文哲)|time:Ndabd:今天|negation:Dc:沒有|Head:VC31:發表|theme:NP(Head:Nad:演講))",
46:"S(agent:NP(property:Nbc:柯|Head:Nad:文哲)|time:PP(Head:P21:在|DUMMY:Ndaad(DUMMY1:Ndabd:昨天|Head:Caa:和|DUMMY2:Ndabd:今天))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
47:"S(agent:NP(property:Nbc:柯|Head:Nad:文哲)|time:PP(Head:P21:在|DUMMY:Ndaad(DUMMY1:Ndabd:昨天|Head:Caa:或|DUMMY2:Ndabd:今天))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
48:"S(agent:NP(Head:Nb:柯文哲)|Head:VC31:發表|theme:NP(Head:Nac:演說))",
49:"S(agent:NP(apposition:Nab:學生|Head:Nb:王小明)|Head:VC2:玩|goal:NP(Head:Nab:電腦))",
50:"S(theme:NP(Head:Nba:王小明)|Head:V_12:是|range:NP(Head:Nab:學生))",
51:"S(theme:NP(Head:Nab:同學)|Head:V_2:有|range:NP(apposition:NP(property:VP(Head:VE2:聽)|Head:Nab:醫師)|Head:NP(property:Nbc:柯|Head:Nad:文哲))|complement:VP(Head:VC31:發表|theme:NP(Head:Nad:演講)))",
52:"S(theme:NP(Head:Nab:同學)|Head:V_2:有|complement:VP(Head:VE2:聽|goal:S(agent:NP(Head:Nb:柯文哲)|Head:VC31:發表|theme:NP(Head:Nad:演講))))",
53:"S(agent:NP(apposition:Nab:醫師|Head:Nb:柯文哲)|Head:VC31:發表|theme:NP(Head:Nad:演講))",
54:"S(theme:NP(Head:Nab:同學)|Head:V_2:有|complement:VP(Head:VE2:聽|goal:S(agent:NP(apposition:Nab:醫師|Head:Nb:柯文哲)|Head:VC31:發表|theme:NP(Head:Nad:演講))))",
55:"S(agent:NP(quantifier:Neqa:所有|Head:Nab:同學)|quantity:Dab:都|deixis:Dbab:來|Head:VE2:聽|goal:NP(Head:Nad:演講))",
56:"S(agent:NP(quantifier:Neqa:所有|property:Nad:大一|Head:Nab:同學)|quantity:Dab:都|deixis:Dbab:來|Head:VE2:聽|goal:NP(Head:Nad:演講))",
57:"S(agent:NP(Head:Nb:柯文哲)|Head:VE2:說|goal:NP(Head:Nhaa:他)|goal:VP(deontics:Dbab:要|Head:VC2:參選))",
58:"S(agent:NP(Head:Nb:柯文哲)|Head:VE2:說|goal:NP(Head:Nhab:自己)|goal:VP(deontics:Dbab:要|Head:VC2:參選))",
59:"S(agent:NP(property:Nbc:柯|property:Nad:文哲|Head:Nab:醫師)|Head:VC31:發表|theme:NP(Head:Nad:演講))",
60:"S(agent:NP(apposition:Nab:醫師|Head:Nb:柯文哲)|Head:VC31:發表|theme:NP(Head:Nad:演講))",
61:"S(time:NP(property:Nbc:柯|Head:Nad:文哲)|Head:V_12:是|range:NP(property:Nca:台大|predication:VP‧的(head:VP(Head:VC31:附設|theme:NP(Head:Ncb:醫院))|Head:DE:的)|Head:Nab:醫師))",
62:"S(time:NP(property:Nbc:柯|Head:Nad:文哲)|Head:V_12:是|range:NP(property:NP‧的(head:NP(property:Nv4:教學|Head:Ncb:醫院)|Head:DE:的)|Head:Nab:醫師))",
63:"S(agent:NP(property:Nbc:柯|Head:Nad:文哲)|Head:VC2:打|goal:NP(quantifier:DM:這場|Head:Nad:選戰))",
64:"S(agent:NP(property:Nbc:柯|Head:Nad:文哲)|Head:VC2:評|goal:NP(quantifier:DM:這場|Head:Nad:選戰))",
65:"S(agent:NP(Head:Nb:卡塔米)|Head:VE2:主張|goal:Nad(DUMMY1:VP(Head:VC2:開放|goal:Nad:人權)|Head:Caa:和|DUMMY2:NP(property:Nad:民主|Head:Nv:改革)))",
66:"S(agent:NP(Head:Nb:卡塔米)|Head:VE2:主張|goal:NP(property:Nad:民主|Head:Nv:改革))",
67:"S(theme:NP(property:Nca:台灣|predication:VP‧的(head:VP(location:PP(Head:P19:從|DUMMY:NP(Head:Nca:印度))|Head:VC31:進口)|Head:DE:的)|property:A:主要|Head:Nab:產品)|Head:V_12:是|range:NP(DUMMY1:NP(Head:Nad:化工)|Head:Caa:和|DUMMY2:NP(property:A:原|Head:Naeb:物料)))",
68:"S(theme:NP(property:Nca:台灣|predication:VP‧的(head:VP(location:PP(Head:P19:自|DUMMY:NP(Head:Nca:印度))|Head:VC31:進口)|Head:DE:的)|property:A:主要|Head:Nab:產品)|Head:V_12:是|range:NP(DUMMY1:NP(Head:Nad:化工)|Head:Caa:和|DUMMY2:NP(Head:Naeb:原物料)))",
69:"S(theme:NP(Head:Nca:安南)|Head:VJ3:出身|range:PP(Head:P23:於|DUMMY:NP(property:Nca:非洲|Head:Nca:迦納)))",
70:"S(theme:NP(Head:Nca:安南)|Head:VJ3:來自|range:NP(property:Nca:非洲|Head:Nca:迦納))",
71:"S(theme:NP(property:Nab:小泉|Head:Nab:純一郎)|time:Nd:２００１年|Head:VJ3:贏得|range:NP(property:Nba:自民黨|property:Nab:總裁|Head:Nad:選戰))",
72:"S(theme:NP(property:Nab:小泉|Head:Nab:純一郎)|time:Nd:２００１年|negation:Dc:未|Head:VJ3:贏得|range:NP(property:Nba:自民黨|property:Nab:總裁|Head:Nad:選戰))",
73:"S(theme:NP(property:Nba:思科|Head:Ncb:公司)|Head:V_12:是|range:NP(property:VP‧的(head:VP(location:Nce:全球|degree:Dfa:最|Head:VH13:大)|Head:DE:的)|Head:VP(property:Nac:網路|property:VD1:供應|Head:NP(Head:Ncb:公司))))",
74:"S(theme:NP(Head:Nba:微軟)|Head:V_12:是|range:NP(property:Nce:全球|property:VP(degree:Dfa:最|Head:VH13:大)|property:Nac:軟體|Head:Ncb:公司))",
75:"S(theme:NP(apposition:Nad:人稱|Head:Nb:喬丹)|Head:V_12:為|range:NP(property:N‧的(head:Nab:籃球|Head:DE:之)|Head:Nac:神))",
76:"S(agent:NP(Head:Nab:人)|Head:VE2:稱|goal:S(theme:NP(Head:Nb:喬丹)|Head:V_12:為|range:NP(property:N‧的(head:Nab:籃球|Head:DE:之)|Head:Nac:神)))",
77:"S(agent:NP(Head:Nab:藤森)|time:Nd:兩千年|location:PP(Head:P02:被|DUMMY:NP(property:Nca:秘魯|Head:Nca:國會))|Head:VB11:免職)",
78:"S(agent:NP(property:Nab:藤森|Head:Nab:總統)|time:Nd:兩千年|location:PP(Head:P02:被|DUMMY:NP(property:Nca:秘魯|Head:Nca:國會))|Head:VB11:免職)",
79:"S(theme:NP(property:NP‧的(head:NP(property:Nab:小泉|Head:Nab:純一郎)|Head:DE:的)|Head:Nab:長男)|Head:V_12:是|range:NP(apposition:Nab:藝人|property:Nab:小泉|Head:Nba:孝太郎))",
80:"S(theme:NP(property:NP‧的(head:NP(property:Nab:小泉|Head:Nab:純一郎)|Head:DE:的)|Head:Nab:大兒子)|Head:V_12:是|range:NP(property:Nab:小泉|Head:Nba:孝太郎))",
81:"S(apposition:NP(property:Nca:大陸|property:Nba:海爾|property:Nab:集團|Head:Nab:總裁)|Head:Nb:張瑞敏)",
82:"S(apposition:NP(property:Nca:大陸|property:Nba:海爾|property:Nab:集團|Head:Nab:總經理)|Head:Nb:張瑞敏)",
83:"S(apposition:NP(property:N‧的(head:Nca:巴基斯坦|Head:DE:的)|Head:Nab:宿敵)|Head:Nca:印度)",
84:"S(apposition:NP(property:N‧的(head:Nca:巴基斯坦|Head:DE:的)|Head:Nab:好朋友)|Head:Nca:印度)",
}


def main():
    sm = smg.SemMgr()
    #cp = ckp.CkipParser()
    parser = argparse.ArgumentParser(prog='main')
    parser.add_argument('itype', metavar='itype', choices=['raw','treestr','id']
                        , type=str, help='input type: %(choices)s ')
    parser.add_argument('otype', metavar='otype', choices=['tree','ltree','sem', 'lsem','prove']
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

    elif args.otype == 'ltree':
        s_list = map(lambda t :  sm.tree_to_latex(t) ,t_list)
        for s in s_list:
            print s

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
