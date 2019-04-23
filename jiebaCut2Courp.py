# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 23:15:26 2019

@author: BOSS
"""
import csv
import jieba
import jieba.analyse

jieba.set_dictionary("data/dict.big.txt")
jieba.load_userdict("data/CIS_Dict.txt")
# jieba.analyse.set_stop_words("data/stop_words.txt")

csvInPath = "data/in.csv"
csvOutPath = "data/out2cut.csv"

csvIn = open(csvInPath , newline='', encoding='utf-8-sig')
rowlists = csv.reader(csvIn)
csvOut = open(csvOutPath, "w", newline='', encoding='utf-8-sig')
writer = csv.writer(csvOut)
# str = "小姐，大家好。高雄縣市已經合併，陳市長一直強調「無縫接軌」強調火星人，"
for row in rowlists:
    str1 = row[7].replace("\r\n", "").replace(" ", "").replace("：", "").replace("，", "").replace("！", "").replace("、", "").replace("。", "")
    str1 = str1.replace("「", "").replace("」", "").replace("？", "")
    strCut = jieba.cut(str1)
    strCut = " ".join(strCut)
    writer.writerow([row[0], row[1], row[2],row[3], row[4], row[5],row[6],strCut])
    # writer.writerow(row)

csvOut.close()
csvIn.close()

