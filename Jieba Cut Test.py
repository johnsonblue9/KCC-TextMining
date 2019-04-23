# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 21:01:22 2019

@author: BOSS
"""
import jieba
import jieba.analyse

jieba.set_dictionary("data/dict.big.txt")
jieba.load_userdict("data/CIS_Dict.txt")
# jieba.analyse.set_stop_words("data/stop_words.txt")

str = "小姐，大家好。高雄縣市已經合併，陳市長一直強調「無縫接軌」強調火星人，"
str += "到目前為止，在各方面的交接、運作，大致上還算不錯；但是有一小部分，高雄縣、高雄市留下來的法令規範有不一樣的地方，"
str += "教育局范長巽綠：要如何做處理，我相信還有其他的問題，大家要再研議、協商，看要如何修改。高雄縣市合併以後， 長期照護協會要何去何從，我們都知道"

str2 = "這些方向應該沒有問題，我們是往非營利幼兒園的模式所以用人等會一 這些方向應該沒有問題，"
str2 += "我們是往非營利幼兒園的模式所以用人等會一 這些方向應該沒有問題，"
str2 += "周議員玲妏：我們就往這個方向來邁進，真的不容許再為建設而浪費麼多從中央申請"
seg_list = jieba.cut(str2)
print ("Inputs: ")
print(" / ".join(seg_list))
print("")
keywords = jieba.analyse.extract_tags(str2,10)
print ("Keywords: ")
print(" / ".join(keywords))

