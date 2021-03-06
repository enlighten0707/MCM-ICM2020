# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 22:08:47 2020

@author: 86150
"""

import xlrd
import xlwt
import numpy as np
import string
import pandas as pd
import  pickle
import re
from sklearn import preprocessing
import nltk
from nltk.corpus import stopwords
import nltk.stem
from nltk.text import TextCollection
from nltk.tokenize import word_tokenize
from key_word_list import key_noun, key_adj, key_other, key_adj_pos, key_adj_neg,reverse_word

replacement_patterns = [
(r'won\'t', 'will not'),
(r'haven\'t','have not'),
(r'can\'t', 'cannot'),
(r'i\'m', 'i am'),
(r'ain\'t', 'is not'),
(r'(\w+)\'ll', '\g<1> will'),
(r'(\w+)n\'t', '\g<1> not'),
(r'(\w+)\'ve', '\g<1> have'),
(r'(\w+)\'s', '\g<1> is'),
(r'(\w+)\'re', '\g<1> are'),
(r'(\w+)\'d', '\g<1> would'),]

class RegexpReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s
        
def Generate_keyword(obj,length):
    orig_file = './Data/'+obj+'/'+obj+'.xlsx'
    data = xlrd.open_workbook(filename=orig_file)
    sheet = data.sheet_by_index(1)
    review_head = np.array(sheet.col_values(12))[1:]
    review_body = np.array(sheet.col_values(13))[1:]
    
    review_all=[]
    for i in range(length) :
        review = review_head[i] + " " +review_body[i]
        review_all.append(review)
    review_all = np.array(review_all)
    
    # 制作每一条review的词汇表，文本预处理，具体函数可以查一下资料
    tokens=[]
    for i,review in enumerate(review_all):
        review = review.lower()
        replacer = RegexpReplacer()
        review = replacer.replace(review)
        remove = str.maketrans('','',string.punctuation) 
        review = review.translate(remove)
        token = nltk.word_tokenize(review)
        token = [w for w in token if w == 'not' or not w in stopwords.words('english')] 
        s = nltk.stem.SnowballStemmer('english')  
        token = [s.stem(ws) for ws in token]
        tokens.append(token)
    token_file = './Data/'+ obj +'/tokens.pkl'
    f=open(token_file,'wb')
    pickle.dump(tokens,f)
    f.close()
    
    #建立语料库
    corpus=TextCollection(tokens) 
    
    tf={}
    tf_idf={}
    for review in tokens:
        for word in review:
            if word not in tf :
                tf_=corpus.tf(word,corpus)
                tf[word]=tf_
            if word not in tf_idf :
                tf_idf_=corpus.tf_idf(word,corpus)
                tf_idf[word] = tf_idf_
                
    tf_sorted = sorted(tf.items(), key=lambda item:item[1], reverse=True)
    tf_idf_sorted = sorted(tf_idf.items(), key=lambda item:item[1], reverse=True)
    
    pd.DataFrame(tf_sorted).to_csv('./Data/'+obj+'/tf_sorted.csv')
    pd.DataFrame(tf_idf_sorted).to_csv('./Data/'+obj+'/tf_idf_sorted.csv')

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

def Generate_feature(obj,length):
    file = './Data/'+obj+ '/' + obj +'.xlsx'
    data = xlrd.open_workbook(filename=file)
    sheet = data.sheet_by_index(1) # verified
    star = np.array(sheet.col_values(7))[1:]
#    helpful_vote = np.array(sheet.col_values(8))[1:]
#    helpful_vote = np.array(sheet.col_values(8))[1:]
#    vine_str = np.array(sheet.col_values(10))[1:]
    review_head = np.array(sheet.col_values(12))[1:]
    review_body = np.array(sheet.col_values(13))[1:]
    
    star = np.round(star.astype(float))
#    helpful_vote = np.round(star.astype(float))
    review_all=[]
    for i in range(length) :
        review = review_head[i] + " " +review_body[i]
        review_all.append(review)
    review_all = np.array(review_all)
    
    #某一评论的权重 I = (std_helpfulness + 1) × (vine + 1) 暂时没有加上权重
#    helpful_vote = helpful_vote.astype(float)
#    helpful_vote=helpful_vote.reshape(-1,1)
#    min_max_scaler = preprocessing.MinMaxScaler()
#    helpful = min_max_scaler.fit_transform(helpful_vote)
#    helpful = helpful.reshape(length)
#    
#    vine = np.zeros(length)
#    index=[]
#    for i,value in enumerate(vine_str):
#        if value =='Y' or value =='y':
#            index.append(i)
#    vine[index] = 1
#    
#    review_weight = np.zeros(length)
#    for i in range(length):
#        review_weight[i] = (helpful[i] + 1) * (vine[i] + 1)
#    review_weight=review_weight.reshape(-1,1)
#    min_max_scaler = preprocessing.MinMaxScaler()
#    review_weight = min_max_scaler.fit_transform(review_weight)
#    review_weight = review_weight.reshape(length)
#    
    token_file = './Data/'+ obj +'/tokens.pkl'
    tokens= pickle.load(open(token_file,'rb'))
        
    # informative data measures 
    noun_score={}
    noun_score_total={}
    noun_score_array = np.zeros((len(key_noun[obj]),length))
#    noun_fre = np.zeros(len(key_noun[obj]))
    
    for noun_idx,noun in enumerate(key_noun[obj]):
        tmp = np.zeros(length)
        for i,review in enumerate(tokens):
            if noun in review : 
#                noun_fre[noun_idx] += 1
                noun_index = review.index(noun) # locate noun
                left = max(0, noun_index-5)
                right = min(len(review),noun_index+6)
                for adj in key_adj_pos[obj]:
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
                for adj in key_adj_neg[obj]:
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
    star = star.reshape(1,length)
#    helpful_vote = helpful_vote.reshape(1,length)
#    noun_score_array = np.concatenate((noun_score_array,star),axis=0)
#    noun_score_array = noun_score_array.T        
#    data_write('./Data/'+obj+'/noun_score_array.xls', noun_score_array)
    noun_score_array = np.concatenate((noun_score_array,star),axis=0)
    noun_score_array = noun_score_array.T        
    data_write('./Data/'+obj+'/noun_score_array.xls', noun_score_array)

def Generate_feature_2c(obj,file,sells):
#    noun_weight = pickle.load(open('./Data/'+ obj +'/noun_weight.pkl','rb'))
    review_head = np.array(file.review_headline)
    review_body = np.array(file.review_body)
    
    
    assert len(review_head) == len(review_body)
    length = len(review_head)
    review_all=[]
    for i in range(length) :
        if type(review_head[i])== float or type(review_body[i])==float:
            continue
        review = review_head[i] + " " +review_body[i]
        review_all.append(review)
    review_all = np.array(review_all)
    
    # 制作每一条review的词汇表，文本预处理
    tokens=[]
    for i,review in enumerate(review_all):
        review = review.lower()
        replacer = RegexpReplacer()
        review = replacer.replace(review)
        remove = str.maketrans('','',string.punctuation) 
        review = review.translate(remove)
        token = nltk.word_tokenize(review)
        token = [w for w in token if w == 'not' or not w in stopwords.words('english')] 
        s = nltk.stem.SnowballStemmer('english')  
        token = [s.stem(ws) for ws in token]
        tokens.append(token)
    
    # 统计noun_adj pair 计算情感色彩
    noun_score={}
    for noun_idx,noun in enumerate(key_noun[obj]):
        tmp = 0
        for i,review in enumerate(tokens):
            if noun in review : 
                noun_index = review.index(noun) # locate noun
                left = max(0, noun_index-5)
                right = min(len(review),noun_index+6)
                for adj in key_adj_pos[obj]:
                    if adj in review[left:right]: #adj 在 noun 附近
                        adj_index = review.index(adj) # locate adj
                        left_adj = max(0,adj_index-2)
                        right_adj = min (len(review),adj_index+3)
                        if 'not' in review[left_adj:right_adj]: # neg emotion
                            tmp -= 1
                        elif 'no' in review[left_adj:right_adj]: # neg emotion
                            tmp -= 1
                        elif 'without' in review[left_adj:right_adj]: # neg emotion
                            tmp -= 1
                        else:
                            tmp += 1
                for adj in key_adj_neg[obj]:
                    if adj in review[left:right]: #adj 在 noun 附近
                        adj_index = review.index(adj) # locate adj
                        left_adj = max(0,adj_index-2)
                        right_adj = min (len(review),adj_index+3)
                        if 'not' in review[left_adj:right_adj]: # neg emotion
                            tmp += 1
                        elif 'no' in review[left_adj:right_adj]: # neg emotion
                            tmp += 1
                        elif 'without' in review[left_adj:right_adj]: # neg emotion
                            tmp += 1
                        else:
                            tmp -= 1
        noun_score[noun] = tmp
    feature_score = 0
#    for noun in key_noun[obj]:
#        if noun in noun_weight:
#            feature_score += noun_weight[noun] * noun_score[noun]
    feature_score /= sells
    return feature_score
            
    
    
def Generate_feature_weight(obj,length):
    file = './Data/'+obj+'/patial_coco.xlsx' # 读取利用matlab生成的偏相关系数
    data = xlrd.open_workbook(filename=file)
    sheet = data.sheet_by_index(0)
    patial_coco = sheet.col_values(0)
    
    token_file = './Data/'+ obj +'/tokens.pkl'
    tokens= pickle.load(open(token_file,'rb'))
    noun_fre = np.zeros(len(key_noun[obj]))
    for noun_idx,noun in enumerate(key_noun[obj]):
        for i,review in enumerate(tokens):
            if noun in review : 
                noun_fre[noun_idx] += 1
    # 计算feature weight u*v 存在负值，需要修正
    noun_weight = []
    for i in range(len(key_noun[obj])):
        noun_weight.append(noun_fre[i] * patial_coco[i])
    
    noun_weight = np.array(noun_weight)
    key_noun[obj] = np.array(key_noun[obj])
    final_noun = key_noun[obj][np.where(noun_weight>0)]
    noun_weight = noun_weight[np.where(noun_weight>0)]
    
    noun_weight_dic = {}
    for i in range(len(final_noun)):
        noun_weight_dic[final_noun[i]] = noun_weight[i]
    print(noun_weight_dic)
    
    file = './Data/'+ obj +'/noun_weight.pkl'
    f=open(file,'wb')
    pickle.dump(noun_weight_dic,f)
    f.close()
