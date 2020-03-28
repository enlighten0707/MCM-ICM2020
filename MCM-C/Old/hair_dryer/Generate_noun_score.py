# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 20:46:04 2020

@author: 86150
"""

# key word top 200 ， 根据 Generate_tf_idf.py 生成的csv统计
key_noun = ['use','work','blow','power','set','time','heat','price','look',
            'last','travel','air','retract','button','speed','size',
            'qualiti','money','hold','weight','style','return','fold','color',
            'frizz']

key_adj = ['great','love','good','like','well','nice','recommend','best',
           'light','need','easi','quick','perfect','want','fast','small',
           'better','heavi','fine','happi','quiet','cool','excel','expect',
           'compact','pretti','worth','right','cheap','awesom','pleas','smooth',
           'problem','loud','disappoint','die','hard','hot']

key_other = ['cord','attach','bathroom']
reverse_word = ['no','not','without']

key_adj_pos = ['great','love','good','like','well','nice','recommend','best',
           'light','need','easi','quick','perfect','want','fast','small',
           'better','heavi','fine','happi','quiet','cool','excel','expect',
           'compact','pretti','worth','right','cheap','awesom','pleas','smooth']
key_adj_neg = ['problem','loud','disappoint','die','hard','hot']

import xlrd
import xlwt
import pickle
import numpy as np
import string
import pandas as pd
from sklearn import preprocessing

import nltk
from nltk.text import TextCollection
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk.stem

#nltk.download()
def data_write(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
    
    #将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        for j in range(len(data)):
            sheet1.write(i,j,data[j])
        i = i + 1
        
    f.save(file_path) #保存文件

file = '../Data/hair_dryer/hair_dryer.xlsx'
len_micro = 9811
data = xlrd.open_workbook(filename=file)
sheet = data.sheet_by_index(1) # verified
star = np.array(sheet.col_values(7))[1:]
helpful_vote = np.array(sheet.col_values(8))[1:]
vine_str = np.array(sheet.col_values(10))[1:]
review_head = np.array(sheet.col_values(12))[1:]
review_body = np.array(sheet.col_values(13))[1:]

star = np.round(star.astype(float))
review_all=[]
for i in range(len_micro) :
    review = review_head[i] + " " +review_body[i]
    review_all.append(review)
review_all = np.array(review_all)

#某一评论的权重 I = (std_helpfulness + 1) × (vine + 1)
helpful_vote = helpful_vote.astype(float)
helpful_vote=helpful_vote.reshape(-1,1)
min_max_scaler = preprocessing.MinMaxScaler()
helpful = min_max_scaler.fit_transform(helpful_vote)
helpful = helpful.reshape(len_micro)

vine = np.zeros(len_micro)
index=[]
for i,value in enumerate(vine_str):
    if value =='Y' or value =='y':
        index.append(i)
vine[index] = 1

review_weight = np.zeros(len_micro)
for i in range(len_micro):
    review_weight[i] = (helpful[i] + 1) * (vine[i] + 1)
review_weight=review_weight.reshape(-1,1)
min_max_scaler = preprocessing.MinMaxScaler()
review_weight = min_max_scaler.fit_transform(review_weight)
review_weight = review_weight.reshape(len_micro)


tokens= pickle.load(open('../Data/hair_dryer/tokens_dryer.pkl','rb'))
    
# informative data measures 
noun_score={}
noun_score_total={}
noun_score_array = np.zeros((len(key_noun),len_micro))
noun_fre = np.zeros(len(key_noun))

for noun_idx,noun in enumerate(key_noun):
    tmp = np.zeros(len_micro)
    for i,review in enumerate(tokens):
        if noun in review : 
            noun_fre[noun_idx] += 1
            noun_index = review.index(noun) # locate noun
            left = max(0, noun_index-5)
            right = min(len(review),noun_index+6)
            for adj in key_adj_pos:
                if adj in review[left:right]: #adj 在 noun 附近
                    adj_index = review.index(adj) # locate adj
                    left_adj = max(0,adj_index-2)
                    right_adj = min (len(review),adj_index+3)
                    if 'not' in review[left_adj:right_adj]: # neg emotion
                        tmp[i] -= 1
                    elif 'no' in review[left_adj:right_adj]: # neg emotion
                        tmp[i] -= 1
                    elif 'without' in review[left_adj:right_adj]: # neg emotion
                        tmp[i] -= 1
                    else:
                        tmp[i] += 1
            for adj in key_adj_neg:
                if adj in review[left:right]: #adj 在 noun 附近
                    adj_index = review.index(adj) # locate adj
                    left_adj = max(0,adj_index-2)
                    right_adj = min (len(review),adj_index+3)
                    if 'not' in review[left_adj:right_adj]: # neg emotion
                        tmp[i] += 1
                    elif 'no' in review[left_adj:right_adj]: # neg emotion
                        tmp[i] += 1
                    elif 'without' in review[left_adj:right_adj]: # neg emotion
                        tmp[i] += 1
                    else:
                        tmp[i] -= 1
    noun_score[noun] = tmp
    noun_score_total[noun] = sum(tmp)
    noun_score_array[noun_idx] = tmp

#noun_score_total = sorted(noun_score_total.items(), key=lambda item:item[1], reverse=True)
star = star.reshape(1,len_micro)
noun_score_array = np.concatenate((noun_score_array,star),axis=0)
noun_score_array = noun_score_array.T        
#data_write('../Data/hair_dryer/noun_score_array_dryer.xls', noun_score_array)

file = '../Data/hair_dryer/patial_coco.xlsx' # 读取利用matlab生成的偏相关系数
data = xlrd.open_workbook(filename=file)
sheet = data.sheet_by_index(0)
patial_coco = sheet.col_values(0)

# 计算feature weight u*v 目前存在负值，需要修正
noun_weight = []
for i in range(len(key_noun)):
    noun_weight.append(noun_fre[i] * patial_coco[i])

noun_weight = np.array(noun_weight)
key_noun = np.array(key_noun)
final_noun = key_noun[np.where(noun_weight>0)]
noun_weight = noun_weight[np.where(noun_weight>0)]

noun_weight_dic = {}
for i in range(len(final_noun)):
    noun_weight_dic[final_noun[i]] = noun_weight[i]
print(noun_weight_dic)



    
    





