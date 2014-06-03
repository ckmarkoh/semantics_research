#-*- coding:utf-8 -*-
from util import *

class PreProcessing(object):
    def __init__(self):
        self.num_map = {
           u"0":u"０", 
           u"1":u"１", 
           u"2":u"２", 
           u"3":u"３", 
           u"4":u"４", 
           u"5":u"５", 
           u"6":u"６", 
           u"7":u"７", 
           u"8":u"８", 
           u"9":u"９", 
        }
        self.eng_map = {
          u"A":u"Ａ", 
          u"B":u"Ｂ", 
          u"C":u"Ｃ", 
          u"D":u"Ｄ", 
          u"E":u"Ｅ", 
          u"F":u"Ｆ", 
          u"G":u"Ｇ", 
          u"H":u"Ｈ", 
          u"I":u"Ｉ", 
          u"J":u"Ｊ", 
          u"K":u"Ｋ", 
          u"L":u"Ｌ", 
          u"M":u"Ｍ", 
          u"N":u"Ｎ", 
          u"O":u"Ｏ", 
          u"P":u"Ｐ", 
          u"Q":u"Ｑ", 
          u"R":u"Ｒ", 
          u"S":u"Ｓ", 
          u"T":u"Ｔ", 
          u"U":u"Ｕ", 
          u"V":u"Ｖ", 
          u"W":u"Ｗ", 
          u"X":u"Ｘ", 
          u"Y":u"Ｙ", 
          u"Z":u"Ｚ", 
          u"a":u"ａ", 
          u"b":u"ｂ", 
          u"c":u"ｃ", 
          u"d":u"ｄ", 
          u"e":u"ｅ", 
          u"f":u"ｆ", 
          u"g":u"ｇ", 
          u"h":u"ｈ", 
          u"i":u"ｉ", 
          u"j":u"ｊ", 
          u"k":u"ｋ", 
          u"l":u"ｌ", 
          u"m":u"ｍ", 
          u"n":u"ｎ", 
          u"o":u"ｏ", 
          u"p":u"ｐ", 
          u"q":u"ｑ", 
          u"r":u"ｒ", 
          u"s":u"ｓ", 
          u"t":u"ｔ", 
          u"u":u"ｕ", 
          u"v":u"ｖ", 
          u"w":u"ｗ", 
          u"x":u"ｘ", 
          u"y":u"ｙ", 
          u"z":u"ｚ", 
        }

    def to_fullwidth_aux(self,s,dic):
        s = to_unicode(s)
        for w in dic.keys():
               if w in s:
                   s=s.replace(w, dic[w])
        return s

    def num_to_fullwidth(self,s):
        return self.to_fullwidth_aux(s,self.num_map)

    def eng_to_fullwidth(self,s):
        return self.to_fullwidth_aux(s,self.eng_map)

    def to_fullwidth(self,s):
        return self.eng_to_fullwidth(self.num_to_fullwidth(s))

    def remove
        
if __name__ == "__main__":
   p = PreProcessing() 
   s1=u"喬丹獲得五次NBA最有價值球員"
   s2=u"1999三月十二日，波蘭加入北約組織"
   print p.to_fullwidth(s1)
   print p.to_fullwidth(s2)
   t11=u"S(theme:NP(Head:Nb:喬丹)|Head:VJ3:獲得|range:NP(quantifier:DM:五次|Head:Nb:ＮＢＡ)|complement:VP(degree:Dfa:最|Head:V_2:有|range:NP(property:Nad:價值|Head:Nab:球員)))"
   t12=u"S(theme:NP(Head:Nb:喬丹)|Head:VJ3:獲得|range:NP(quantifier:DM:五次|Head:Nb:NBA   )|complement:VP(degree:Dfa:最|Head:V_2:有|range:NP(property:Nad:價值|Head:Nab:球員)))"
