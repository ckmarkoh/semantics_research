# -*- coding: utf-8 -*-
from sys import argv
import semMgr as smg
import proveMgr as pv
import nltk.sem.logic as lgc
from operator import itemgetter
import sys, StringIO


_TEST_DICT = {
1:u"S(agent:NP(Head:Nb:布魯圖)|location:PP(Head:P21:在|DUMMY:NP(Head:Nc:元老院))|instrument:PP(Head:P39:用|DUMMY:NP(Head:Nab:刀子))|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
2:u"S(agent:NP(Head:Nb:布魯圖)|Head:VC2:刺殺|goal:NP(Head:Nba:凱撒))",
3:u"S(agent:NP(Head:Nba:馬英九)|time:Ndabd:今天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
4:u"S(agent:NP(Head:Nba:馬英九)|Head:VC31:發表|theme:NP(Head:Nad:演講))",
5:u"S(agent:NP(Head:Nb:江宜樺)|time:Dd:已|manner:VH11:清楚|Head:VC31:表達|theme:NP(Head:Nac:立場))",
6:u"S(agent:NP(Head:Nb:江宜樺)|Head:VC31:表達|theme:NP(Head:Nac:立場))",
7:u"S(agent:NP(Head:Nb:姚明)|theme:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(quantifier:DM:２００２年|agent:Nb:ＮＢＡ|Head:Nv:選秀)|Head:Ng:中))|agent:PP(Head:P02:被|DUMMY:NP(property:Nc:休斯敦|Head:Nba:火箭隊))|Head:VG1:選為|range:NP(property:Nab:狀元|Head:Nab:新秀))",
8:u"S(agent:NP(Head:Nb:姚明)|theme:PP(Head:P21:在|DUMMY:GP(DUMMY:NP(quantifier:DM:２００２年|agent:Nb:ＮＢＡ|Head:Nv:選秀)|Head:Ng:中))|agent:PP(Head:P02:被)|Head:VG1:選為|range:NP(property:Nab:狀元|Head:Nab:新秀))",
9:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:中研院))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
10:u"S(agent:NP(Head:Nba:馬英九)|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:臺北))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
99911:"S(agent:NP(Head:Nba:柯文哲)|time:Ndabd:昨天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:台大))|Head:VC31:發表|theme:NP(Head:Nad:演講))",
99912:"S(agent:NP(Head:Nba:柯文哲)|time:Ndabd:昨天|Head:VC31:發表|theme:NP(Head:Nad:演講))",
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
40702:"S(theme:NP(property:Na:車臣|property:Nac:共和國|Head:Ncb:首府)|Head:V_12:是|range:NP(property:Nb:格洛斯|Head:Nab:尼))",
40701:"S(theme:NP(property:Na:車臣|Head:Ncb:首府)|Head:VG2:為|range:NP(property:Nb:格洛斯|Head:Nab:尼))",
20801:"S(agent:NP(property:Na:生物|Head:Nab:晶片)|deontics:Dbab:可|Head:VC2:用於|goal:NP(DUMMY:NP(property:Nab:血庫|Head:Nv:篩檢)|Head:Cab:等)|complement:VP(goal:NP(property:VH16:標準化|Head:Nab:標)|Head:VC2:驗))",
20802:"S(agent:NP(property:Na:生物|Head:Nab:晶片)|deontics:Dbab:可|Head:VC2:用於|goal:NP(property:Nab:血庫|Head:Nv:篩檢))",
12701:"S(theme:NP(Head:Nba:若望保祿|quantifier:DM:二世)|Head:V_12:是|range:NP(property:Ncb:教廷|property:Nac:國家|Head:Nab:領導人))",
12702:"S(theme:NP(Head:Nba:若望保祿|quantifier:DM:二世)|Head:V_12:是|range:NP(property:Ncb:教廷|Head:Nab:領導人))",
9401:"S(theme:NP(property:Nb:千禧|Head:Ncb:巨蛋)|Head:V_12:是|range:NP(quantifier:DM:一座|property:VP‧的(head:VP(manner:Dh:專|comparison:PP(Head:P:為|DUMMY:VP(Head:VC2:迎接|goal:NP(property:Nb:千禧|Head:Nac:年)|complement:VP(Head:VA11:來臨)))|result:Cbca:而|Head:VH11:特別|duration:NP(Head:Nad:設計))|Head:DE:的)|property:Nac:科技|Head:Ncb:展覽館)",
9402:"S(theme:NP(property:Nb:千禧|Head:Ncb:巨蛋)|Head:V_12:是|range:NP(quantifier:DM:一座|predication:VP‧的(head:VP(manner:Dh:專|agent:PP(Head:P:為)|Head:VC2:迎接|goal:NP(quantifier:DM:２０００年|property:VP(Head:VA11:來臨|complement:VP(result:Cbca:而|Head:VH11:特別))|Head:Nad:設計))|Head:DE:的)|property:Nac:科技|Head:Ncb:展覽館))",
15201:"S(theme:NP(Head:Nba:張藝謀)|time:Dd:曾|topic:PP(Head:P35:與|DUMMY:NP(Head:Nb:鞏俐))|Head:V_12:是|range:NP(property:Nab:戀人|Head:Nad:關係))",
15202:"S(theme:Nba(DUMMY1:Nba:張藝謀|Head:Caa:與|DUMMY2:Nb:鞏俐)|time:Dd:曾|Head:VH11:相戀)",
42001:"S(theme:NP(Head:Nb:喬丹)|Head:VJ3:獲得|range:NP(quantifier:DM:五次|Head:Nb:NBA)|complement:VP(degree:Dfa:最|Head:V_2:有|range:NP(property:Nad:價值|Head:Nab:球員)))",
42002:"S(theme:NP(Head:Nb:喬丹|quantifier:DM:五度)|Head:VJ3:獲得|range:NP(Head:Nb:NBA)|complement:VP(degree:Dfa:最|Head:V_2:有|range:NP(property:Nad:價值|Head:Nab:球員)))",
13101:"S(time:NP(property:Nba:若望保祿|Head:Nd:二世)|Head:V_12:是|range:NP(property:Ncb:教廷|property:Nac:國家|Head:Nab:領導人))",
13102:"S(time:NP(property:Nba:若望保祿|Head:Nd:二世)|Head:V_12:是|range:NP(property:Ncb:教廷|property:Nac:國家|Head:Nab:領袖))",
7501:"S(agent:NP(property:Nab:藤|property:Nab:森|Head:Nab:總統)|time:Nd:2000年|location:PP(Head:P60:遭|DUMMY:NP(property:Nca:秘魯|Head:Nca:國會))|Head:VB11:免職)",
7502:"S(agent:NP(property:Nab:藤|Head:Nab:森)|time:Nd:2000年|location:PP(Head:P60:遭|DUMMY:NP(property:Nca:秘魯|Head:Nca:國會))|Head:VB11:免職)",
6601:"S(theme:NP(Head:Nca:安南)|Head:VJ3:來自|range:NP(property:Nca:非洲|Head:Nca:迦納))",
11101:"S(theme:NP(property:Nd:2000年|Head:Nb:娜拉提諾娃)|Head:VJ3:獲|complement:VP(Head:VJ1:列入|goal:NP(property:Ncc:國際|property:Nab:網球|Head:Nc:名人堂)))",
11102:"S(time:Nd:2000年|goal:NP(Head:Nb:娜拉提諾娃)|theme:PP(Head:P02:被)|Head:VJ1:納入|goal:NP(property:Ncc:國際|property:Nab:網球|Head:Nc:名人堂))",
10901:"S(agent:NP(property:Na:美國線|Head:Ncda:上)|Head:VC31:購併|theme:NP(property:Na:網景|property:Nad:通訊|Head:Ncb:公司))",
10902:"S(agent:NP(property:Nab:網|Head:Nac:景)|location:PP(Head:P02:被|DUMMY:NP(property:Na:美國線|Head:Ncda:上))|Head:VC31:收購)",
9401:"S(theme:NP(property:Nb:千禧|Head:Ncb:巨蛋)|Head:V_12:是|range:NP(quantifier:DM:一座|predication:VP‧的(head:VP(manner:Dh:專|agent:PP(Head:P:為)|Head:VC2:迎接|goal:NP(property:VP(time:Nd:千禧年|Head:VA11:來臨|complement:VP(result:Cbca:而|Head:VH11:特別))|Head:Nad:設計))|Head:DE:的)|property:Nac:科技|Head:Ncb:展覽館))",
9402:"S(theme:NP(property:NP(quantifier:Neu:千|Head:Nab:禧)|Head:Ncb:巨蛋)|Head:V_12:是|range:NP(quantifier:DM:一座|predication:VP‧的(head:VP(manner:Dh:專|agent:PP(Head:P:為)|Head:VC2:迎接|goal:NP(property:VP(time:Nd:2000年|Head:VA11:來臨|complement:VP(result:Cbca:而|Head:VH11:特別))|Head:Nad:設計))|Head:DE:的)|property:Nac:科技|Head:Ncb:展覽館))",
26701:"S(theme:NP(quantifier:Neu:千|property:Nd:禧年|Head:Nac:危機)|Head:VG1:俗稱|range:NP(DUMMY1:NP(property:Nb:Ｙ２Ｋ|Head:Nac:危機)|Head:Caa:或|DUMMY2:NP(property:Nb:千禧|Head:Nab:蟲)))",
26702:"S(theme:NP(quantifier:Neu:千|property:Nd:禧年|Head:Nac:危機)|time:Dd:又|Head:VG1:叫|range:NP(DUMMY1:NP(property:Nb:Ｙ２Ｋ|Head:Nac:危機)|Head:Caa:或|DUMMY2:NP(property:Nb:千禧|Head:Nab:蟲)))",
30201:"S(theme:NP(Head:Nca:印尼)|Head:V_12:是|range:NP(property:Nca:澳洲|property:VP‧的(head:VP(degree:Dfa:最|Head:VH13:大)|Head:DE:的)|property:Nad:貿易|Head:Nab:夥伴))",
30202:"S(theme:NP(Head:Nca:印尼)|Head:V_12:是|range:NP(property:Nca:澳洲|quantifier:Neu:第一|property:V‧的(head:VH13:大|Head:DE:的)|property:Nad:貿易|Head:Nab:夥伴))",
20401:"S(theme:NP(property:Naa:天然氣|Head:Nab:水合物)|Head:VG2:即|range:NP(property:Naa:甲烷|Head:Nab:水合物))",
20402:"S(theme:NP(property:Naa:天然氣|Head:Nab:水合物)|time:Dd:就|Head:V_12:是|range:NP(property:Naa:甲烷|Head:Naa:化合物))",
14001:"S(theme:NP(Head:Nba:伏明霞)|Head:VA12:出生|location:PP(Head:P23:於|DUMMY:NP(Head:Nca:湖北)))",
14002:"S(theme:NP(Head:Nba:伏明霞)|Head:V_12:是|range:NP(property:Nca:湖北|Head:Na:武漢人))",
13601:"S(theme:NP(property:Nba:芮氏|Head:Na:規模)|Head:V_12:是|range:NP(apposition:NP(property:Nca:美國|property:Nv4:地震|Head:Nab:學家)|Head:Nba:芮氏)|range:PP(Head:P21:在|DUMMY:NP(predication:VP‧的(head:VP(time:Nd:一九三五年|quantity:Dab:所|Head:VC31:創立)|Head:DE:的)|property:Nv1:計算|Head:Nac:公式)))",
13602:"S(theme:NP(property:Nba:芮氏|Head:Na:規模)|Head:V_12:是|range:NP(apposition:NP(property:Nca:美國|Head:Nab:科學家)|Head:Nba:芮氏)|range:VP(head:VP(quantity:Dab:所|Head:VC31:發明)|Head:DE:的))",
16201:"S(agent:NP(Head:Nb:鞏俐)|Head:VF1:申請|goal:VP(Head:VC1:就讀|goal:NP(property:Nca:北京|property:Ncb:大學|Head:Ncb:社會學系)))",
16202:"S(agent:NP(Head:Nb:鞏俐)|Head:VF1:申請|goal:VP(Head:VC1:就讀|goal:NP(property:Nca:北京|property:Ncb:大學|property:Ncb:社會學系|property:Na:碩士|Head:Nab:研究生)))",
16101:"S(agent:NP(Head:Nb:鞏俐)|time:Nd:1965年|Head:VC31:生)",
16102:"S(agent:NP(Head:Nb:鞏俐)|time:PP(Head:P21:在|DUMMY:NP(property:Nd:1965年|property:Nd:12月|Head:Nd:31日))|Head:VC31:生|location:PP(Head:P23:於|DUMMY:NP(property:Nca:遼寧|Head:Nca:瀋陽)))",
162022:"S(theme:NP(property:Nad:祖籍|property:Nca:山東|Head:Nca:濟南)|evaluation:Dbb:並|location:PP(Head:P21:在|DUMMY:NP(Head:Nep:此))|Head:VH11:長大)",
30301:"S(theme:NP(Head:Nca:印尼)|Head:V_12:是|range:NP(property:Nca:澳洲|property:VP‧的(head:VP(degree:Dfa:最|Head:VH13:大)|Head:DE:的)|property:Nad:貿易|Head:Nab:夥伴))",
30302:"S(theme:NP(Head:Nca:印尼)|Head:V_12:是|range:NP(property:Nca:澳洲|property:A‧的(head:A(degree:Dfa:最|Head:A:主要)|Head:DE:的)|property:Nad:貿易|Head:Nab:夥伴))",
25401:"S(theme:NP(Head:Nb:娜拉提諾娃)|quantity:Daa:一共|Head:VJ3:獲得|range:NP(quantifier:DM:18座|property:Nab:大滿貫|Head:Na:金杯))",
25402:"S(agent:NP(Head:Nb:娜拉提洛娃)|quantity:Daa:一共|Head:VC31:取得|aspect:Di:了|theme:NP(property:NP‧的(head:NP(quantifier:DM:58個|Head:Nab:大滿貫)|Head:DE:的)|Head:Na:金杯))",
22001:"S(theme:NP(Head:Nba:諾貝爾獎)|time:PP(Head:P23:於|DUMMY:NP(property:Nd:1901年|property:Nd:10月|Head:Nd:10日))|Head:VL2:開始|goal:VP(Head:VD1:頒發))",
22002:"S(agent:NP(Head:Nba:諾貝爾獎|quantifier:DM:首次)|Head:VB11:頒獎|result:VP(Head:VJ1:始於|goal:NP(property:NP(property:Nd:1901年|Head:Nd:10月)|Head:Neu:10)))",
14701:"S(theme:NP(property:V‧的(head:VH11:多才多藝|Head:DE:的)|Head:Nba:楊麗萍)|Head:VA4(Head:VA11:自編|Head:VA11:自導)|complement:VP(Head:VC31:自製|complement:VP(Head:VC2:自演|goal:NP(apposition:Nac:電影|Head:Nab:太陽鳥))))",
14702:"S(theme:NP(property:V‧的(head:VH11:多才多藝|Head:DE:的)|Head:Nba:楊麗萍)|evaluation:Dbb:還|Head:VA11:自編|complement:VP(Head:VA11:自導|complement:VP(Head:VC2:自演|aspect:Di:了|goal:NP(apposition:Nac:電影|Head:Nab:太陽鳥))))",
13201:"S(theme:NP(property:Nba:芮氏|Head:Na:規模)|Head:V_12:是|range:NP(property:NP‧的(head:NP(property:NP(property:Nv4:地震|Head:Na:規模)|property:Nv1:計算|Head:Nac:方式)|Head:DE:之)|Head:Neu:一))",
13202:"S(theme:NP(property:Nba:芮氏|Head:Na:規模)|Head:V_12:是|range:NP(property:NP(quantifier:DM:一種|property:Nv4:地震|Head:Na:規模)|property:Nv1:計算|Head:Nac:方式))",
4101:"S(theme:NP(property:NP‧的(head:NP(Head:NP(property:VH13:小|Head:Nab:泉)|Head:NP(property:VH11:純一|Head:Nab:郎))|Head:DE:的)|Head:Nab:長男)|Head:V_12:是|range:NP(apposition:Nab:藝人|property:VH13:小|property:Nb:泉孝|Head:Nba:太郎))",
4102:"S(theme:NP(property:NP‧的(head:NP(property:Nb:小泉|property:VH11:純一|Head:Nab:郎)|Head:DE:的)|Head:Nab:大兒子)|Head:V_12:是|range:NP(apposition:NP(property:Nb:小泉|Head:Nad:孝)|Head:Nba:太郎))",
}



def test(k1,k2):
    sm = smg.SemMgr()
    print "s1 --> s2  ??"
    t1 = _TEST_DICT[k1]
    t2 = _TEST_DICT[k2] 
    s1 = sm.str_tree_to_sem(t1)
    s2 = sm.str_tree_to_sem(t2)
    print ""
    print "semantic of s1:",s1
    print "semantic of s2:",s2

    r1 = sm.prover_prove([s1],s2)
    r2 = sm.prover_prove([s2],s1)
    print "s1 --> s2"
    print r1
    print "s2 --> s1"
    print r2
    return r1,r2


def test_single(k1,k2):

    sm = smg.SemMgr()
    t1 = _TEST_DICT[k1]
    t2 = _TEST_DICT[k2] 
    s1 = sm.str_tree_to_sem(t1)
    s2 = sm.str_tree_to_sem(t2)
    print s1
    print s2
    r1=sm.prover_prove_tabu([s1],s2)

    return r1 


def main():
    test_result = map(lambda i: test( (i+1)*2-1, (i+1)*2) , range(len(_TEST_DICT)/2))
    print map(itemgetter(0),test_result) 
    print map(itemgetter(1),test_result) 
    #print test_single(9, 10)



if __name__ == "__main__":
    main() 
