# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 17:51:03 2020

@author: 86150
"""

import xlrd
import numpy as np
import string
import pandas as pd
import  pickle
import re

import nltk
from nltk.corpus import stopwords
import nltk.stem
from nltk.text import TextCollection
from nltk.tokenize import word_tokenize
#nltk.download()

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
        

if __name__ == '__main__':
    len_micro = 1095
    file = './Data/microwave.xlsx'
    data = xlrd.open_workbook(filename=file)
    sheet = data.sheet_by_index(1)
    review_head = np.array(sheet.col_values(12))[1:]
    review_body = np.array(sheet.col_values(13))[1:]
    
    review_all=[]
    for i in range(len_micro) :
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
    f=open('./Data/tokens_micro.pkl','wb')
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
    
    pd.DataFrame(tf_sorted).to_csv('./Data/tf_sorted_microwave.csv')
    pd.DataFrame(tf_idf_sorted).to_csv('./Data/tf_idf_sorted_microwave.csv')
