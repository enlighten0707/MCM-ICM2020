# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 21:14:13 2020

@author: 86150
"""

# key word top 200 ， 根据 Generate_tf_idf.py 生成的csv统计
key_noun = ['look','work','price','use','size','space','buy','qualiti','fit',
            'oven','instal','money','door','rang','time',
            'open','whirlpool','button','power','turntabl','heat','design',
            'return','repair','servic','fix','plate','noisi',
            'advertis','function','stop','cook','counter',
            'cabinet','push','hole','reheat','brand','steel','countertop',
            'clean']
key_adj = ['great','good','perfect','small','nice','littl','love','well',
           'like','happi','fine','easi','valu','excel','right',
           'best','compact','save','recommend','better','new','exact',
           'fantast','expect','awesom','pleas','ok','simpl',
           'limit','big','fast','cheap','satisfi','pretti',
           'easili','reliabl','quiet','larg','top','effici',
           'glad','new','stainless','warm','need','want',
           'damag','issu','wast','bad','problem','poor','terribl',
             'low','disappoint','hard']
key_other = ['job','unit','far','year','month','paint','kitchen','week',
             'basic','replac','food','dinner','sharp']
reverse_word = ['no','not','without']

key_adj_pos = ['great','good','perfect','small','nice','littl','love','well',
           'like','happi','fine','easi','valu','excel','right',
           'best','compact','save','recommend','better','new','exact',
           'fantast','expect','awesom','pleas','ok','simpl',
           'limit','big','fast','cheap','satisfi','pretti',
           'easili','reliabl','quiet','larg','top','effici',
           'glad','new','stainless','warm','need','want']
key_adj_neg = ['damag','issu','wast','bad','problem','poor','terribl',
             'low','disappoint','hard']

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


file = './Data/microwave/microwave.xlsx'
len_micro = 1095
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

#对每一形容词，选出该词出现的所有review，对star-rating求加权平均数，即得到该词语的感情色彩指标
#解决 not 的问题, 句子近邻搜索
#不存在adj匹配的问题
tokens= pickle.load(open('./Data/microwave/tokens_micro.pkl','rb'))
#adj_review = {}
#false_pos_cnt={}
#for adj in key_adj:
#    false_pos_cnt[adj]=0
#    tmp = np.zeros(len_micro)
#    for i,review in enumerate(tokens):
#        flag=True
#        if i==1040 and adj == 'disappoint':
#            continue
#        if i ==1069 and adj == 'reliabl':
#            continue
#        if adj in review :
#            adj_index = review.index(adj) # locate adj
#            left = max(0,adj_index-5)
#            right = min (len(review),adj_index+6)
#            for reverse in reverse_word:
#                if reverse in review[left:right]:# false postive ,not 在 adj 附近
#                    tmp[i] = (6 - star[i]) * review_weight[i] # add weight
#                    false_pos_cnt[adj]+=1
#                    flag=False       
#            if flag == True:
#                tmp[i] = star[i] * review_weight[i]               
#    adj_review[adj] = tmp
#print(false_pos_cnt['disappoint'])
#tmp = adj_review['good']
#tmp = tmp[np.where(tmp > 0)]
#print(tmp)
#print(len(tmp))
#adj_score = {} # 是否需要归一化？
#for adj in adj_review:
#    tmp = adj_review[adj]
#    tmp = tmp [np.where(tmp>0)]
#    adj_score[adj] = np.mean(tmp)
#    
#adj_score = sorted(adj_score.items(), key=lambda item:item[1], reverse=True)
#print(adj_score)

# 构建noun 的对应adj
    
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
#data_write('./Data/noun_score_array.xls', noun_score_array)

file = './Data/microwave/patial_coco.xlsx' # 读取利用matlab生成的偏相关系数
data = xlrd.open_workbook(filename=file)
sheet = data.sheet_by_index(0)
patial_coco = sheet.col_values(0)

# 计算feature weight u*v 目前存在负值，需要修正
noun_weight = []
for i in range(len(key_noun)):
    noun_weight.append(noun_fre[i] * patial_coco[i])

print(noun_weight)
noun_weight = np.array(noun_weight)
key_noun = np.array(key_noun)
key = key_noun[np.where(noun_weight<0)] 
print(key)

    
    





