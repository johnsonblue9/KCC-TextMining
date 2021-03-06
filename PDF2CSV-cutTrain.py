# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:12:20 2019

@author: b1075
"""

# PDF2CSV-cutTrain.py
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import io
import os.path
import glob
import pandas as pd
import csv

def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            #codec = 'utf-8'
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            #converter = TextConverter(resource_manager, codec, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            print(text)
            yield text
            # close open handles
            converter.close()
            fake_file_handle.close()


def export_as_csv(pdf_path, csv_path, csv2, isNew):
    SliceLen = 150
    global seqNo, seqNo2
    if isNew:
        opMode = "w"
    else:
        opMode = 'a'
    #with open(csv_path, opMode, newline='', encoding='utf-8-sig') as csv_file:
    csv_file = open(csv_path, opMode, newline='', encoding='utf-8-sig')
    writer = csv.writer(csv_file)
        
    csv2_file = open(csv2, opMode, newline='', encoding='utf-8-sig')
    writer2 = csv.writer(csv2_file)
        
    PageNo = 0
    Segment = 0
    mDate = ""
    if isNew:
        # write fieldName into CSV head
        writer.writerow(['SeqNo', '屆次', '日期', 'FileName', 'PageNo', 'Segment', '類別', '財政', 'Text'])
        writer2.writerow(['SeqNo', '屆次', '日期', 'FileName', 'PageNo', 'Segment', '類別', '財政', 'Text'])
    pdfName = os.path.basename(pdf_path)
    fnList = pdfName.split("-")
    termNo = fnList[0] + "屆" + fnList[1] + "次"
        
    for page in extract_text_by_page(pdf_path):
        PageNo += 1 
        n = len(page) // SliceLen
        text = page[0:SliceLen -1]
        dateStart = text.find("中華民國")
        if dateStart != -1:
            dateEnd = text.find("日",dateStart,dateStart+30)
            if dateEnd != -1:
                mDate = text[dateStart+4:dateEnd].strip()
                mY = int(mDate.split("年")[0]) + 1911
                mDate = mDate.replace("年","-").replace("月","-").replace(" ","")
                mDate = str(mY) + "-" + mDate.split("-")[1] + "-" + mDate.split("-")[2]
                    
        for i in range(0,n):
            strBegin =  i * SliceLen
            strEnd = (i+1) * SliceLen -1
            Segment = i + 1
            text = page[strBegin:strEnd]
            seqNo += 1
            #print("text before split----------------------------")
            if (PageNo % 5 == 0) and (Segment == 3) and (seqNo2 < 2000):
                seqNo2 += 1
                writer2.writerow([seqNo, termNo, mDate, pdfName, PageNo, Segment, "", "", text])
            else:
                writer.writerow([seqNo, termNo, mDate, pdfName, PageNo, Segment, "", "", text])
    csv_file.close()
    csv2_file.close()

# pdf_path = "D://CIS PDF Test/"
pdf_path = "D://CIS PDF/" 
pdfs = glob.glob("{}/*.pdf".format(pdf_path))
seqNo = 0
seqNo2 = 0
newFlag = True
csv_path = 'Out150No3rd.csv'
csv_path2 = 'Out150-Only3rd.csv'
for pdf in pdfs:
    export_as_csv(pdf, csv_path, csv_path2, newFlag)
    newFlag = False
