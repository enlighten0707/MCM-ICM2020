# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 00:24:53 2020

@author: 86150
"""
import numpy as np
import pandas as pd
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
from sklearn.preprocessing import minmax_scale 

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
    
w = [ 0.42853548,  0.42085358,  0.15061094]

corpos = ['use','blow','power','time','set','price','heat','look','travel',
          'need','easi','light','quick','old','want','first','better','replac',
          'button','speed','heavi','thick','low','quiet','wall','cool','size',
          'differ','expect','qualiti','money','weight','compact','style',
          'never','problem','hand','longer','fold','noisi','color','strong',
          'howev','cheap','hope','hard','burn','previous','with','brush',
          'control','frizzi','head','read','expens','broke','temperatur',
          'place','want','straight','complaint','smell','nois','quieter',
          'plastic','damage']

f = pd.read_csv('./Data/hair_dryer.tsv', sep = '\t')
f = f[f.verified_purchase == 'Y']

f = f[f.product_parent == 732252283]
length = f.shape[0]
stars = f['star_rating'].tolist()
helpful_votes = f['helpful_votes'].tolist()
total_votes = f['total_votes'].tolist()

stars = np.array(stars)
helpful_votes = np.array(helpful_votes)
total_votes = np.array(total_votes)
review_head = f['review_headline'].tolist()
review_body = f['review_body'].tolist()

review_all=[]
for i in range(length) :
    review = review_head[i] + " " +review_body[i]
    review_all.append(review)
review_all = np.array(review_all)

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

helpful_ratio = np.zeros(length,dtype = np.float32)
for i in range(length):
    if total_votes[i]==0:
        continue
    helpful_ratio[i] = float(helpful_votes[i] / total_votes[i])
    
word_count = np.zeros(length)
for i in range (length):
    for token in tokens[i]:
        if token in corpos:
            word_count[i]+=1
            
helpful_votes_ = minmax_scale(helpful_votes)
helpful_ratio_ = minmax_scale(helpful_ratio)
word_count_ = minmax_scale(word_count)
#score = w[0] * stars + w[1]* helpful_votes + w[2]*helpful_ratio +w[3]*word_count


ideal = [np.max(helpful_votes_),np.max(helpful_ratio_),np.max(word_count_)]

scores = []
for i in range(length):
    scores.append(w[0]* (helpful_votes_[i]-ideal[0])* (helpful_votes_[i]-ideal[0])+ w[1] * (helpful_ratio_[i]-ideal[1])*(helpful_ratio_[i]-ideal[1]) + w[2]*(word_count_[i]-ideal[2])*(word_count_[i]-ideal[2]))

scores = np.array(scores)
index = np.argsort(scores)
print(review_all[index[0]])
#print(word_count[index[0]])
print(helpful_votes[index[0]])
print(total_votes[index[0]])
print('--------')
print(review_all[index[51]])
#print(word_count[index[0]])
print(helpful_votes[index[51]])
print(total_votes[index[51]])

print('--------')
print(review_all[index[199]])
#print(word_count[index[0]])
print(helpful_votes[index[199]])
print(total_votes[index[199]])

print('--------')
print(review_all[index[-1]])
#print(word_count[index[0]])
print(helpful_votes[index[-1]])
print(total_votes[index[-1]])
print(length)
