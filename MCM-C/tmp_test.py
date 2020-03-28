# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 23:48:05 2020

@author: 86150
"""
import numpy as np
import pandas as pd
import re
import string
import xlrd
import xlwt
import  pickle
from sklearn import preprocessing
import nltk
from nltk.corpus import stopwords
import nltk.stem
from nltk.text import TextCollection
from nltk.tokenize import word_tokenize

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
#from ult_feature import Generate_feature_2c

#f = pd.read_csv('./Data/hair_dryer.tsv', sep = '\t')
#f = f[f.verified_purchase == 'Y']
#sells = f['product_parent'].value_counts()
#f = f.iloc[::-1, :]
#group_data = f.groupby('product_parent')
#print('Preprocessing Complete!\n')
#
#for (prod_parent, file) in group_data:
##    print(prod_parent)
#    avg_feature = Generate_feature_2c('hair_dryer',file)
#    print(avg_feature)

#f = pd.read_csv('./Data/hair_dryer.tsv', sep = '\t')
#f = f[f.verified_purchase == 'Y']
#star = f ['star_rating']
#review_head =  f ['review_headline']
#review_body=  f ['review_body']
#review_all = review_head + review_body
#review_all = review_all.tolist()
#print(type(review_all))
#print(type(review_all[0]))
#
#tokens=[]
#sentences = []
#for i,review in enumerate(review_all):
#    review = str(review)
#    review = review.lower()
#    replacer = RegexpReplacer()
#    review = replacer.replace(review)
#    remove = str.maketrans('','',string.punctuation) 
#    review = review.translate(remove)
#    token = nltk.word_tokenize(review)
#    token = [w for w in token if not w in stopwords.words('english')] 
#    s = nltk.stem.SnowballStemmer('english')  
#    token = [s.stem(ws) for ws in token]
#    sentence = ' '.join(token)
#    tokens.append(token)
#    sentences.append(sentence)
#print(tokens)
#print(sentences)
#print(type(sentences))
#print(type(sentences[0]))



        