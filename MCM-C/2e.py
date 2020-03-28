# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 13:01:19 2020

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

# 构造 target : star rating 
# 构造 data : review_all 
np.set_printoptions(suppress = True)
proportion_cut = 0.2

f = pd.read_csv('./Data/hair_dryer.tsv', sep = '\t')
f = f[f.verified_purchase == 'Y']
target = f ['star_rating']
target = np.array(target.tolist())
review_head =  f ['review_headline']
review_body=  f ['review_body']
review_all = review_head + review_body
review_all = np.array(review_all.tolist())

tokens=[]
sentences = []
for i,review in enumerate(review_all):
    review = str(review)
    review = review.lower()
    replacer = RegexpReplacer()
    review = replacer.replace(review)
    remove = str.maketrans('','',string.punctuation) 
    review = review.translate(remove)
    token = nltk.word_tokenize(review)
    token = [w for w in token if not w in stopwords.words('english')] 
    s = nltk.stem.SnowballStemmer('english')  
    token = [s.stem(ws) for ws in token]
    sentence = ' '.join(token)
    tokens.append(token)
    sentences.append(sentence)

#Extracting features from text files 
   
from sklearn.feature_extraction.text import CountVectorizer  # sklearn中的文本特征提取组件中，导入特征向量计数函数

print('-----')
count_vect = CountVectorizer()  # 特征向量计数函数
X_train_counts = count_vect.fit_transform(sentences)  # 对文本进行特征向量处理
#print(X_train_counts)  # 特征向量和特征标签
#print(X_train_counts.shape)  # 形状
print('-----')
words = {v : k for k, v in count_vect.vocabulary_.items()}

#tf-idf:词频-逆文档频率

#from sklearn.feature_extraction.text import TfidfTransformer  # sklearn中的文本特征提取组件中，导入词频统计函数
#
#tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)  # 建立词频统计函数,注意这里idf=False
#print(tf_transformer)  # 输出函数属性 TfidfTransformer(norm=u'l2', smooth_idf=True, sublinear_tf=False, use_idf=False)
#X_train_tf = tf_transformer.transform(X_train_counts)  # 使用函数对文本文档进行tf-idf频率计算
#print(X_train_tf)
#print('-----')
#print(X_train_tf.shape)
#print('-----')

#    Training a classifier 训练一个分类器
#    scikit-learn中包括这个分类器的许多变量，最适合进行单词计数的是多项式变量。

from sklearn.naive_bayes import MultinomialNB  # 使用sklearn中的贝叶斯分类器，并且加载贝叶斯分类器

# 中的MultinomialNB多项式函数
clf = MultinomialNB()  # 加载多项式函数
x_clf = clf.fit(X_train_counts, target)  # 构造基于数据的分类器
print(x_clf)  # 分类器属性：MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
print('-----')
coef = np.array(clf.coef_)
#count = np.array(clf.feature_count_)
print(coef)
print(coef.shape)
print('-----')

descriptor = ['like','good','well','great','fine','nice','recommend',
              'realli',
              'need','better','want','expect'
              'low','disappoint','old']

#word_index = []
#for idx,word in count_vect.vocabulary_.items():
#    if words in descriptor:
#        word_index.append(idx)
        
#for i in range(5):
#    prob = np.array(coef[i])
#    feature_word = []
#    feature_prob = []
#    for idx in word_index :
#        feature_word.append(words[idx])
#        feature_prob.append(prob[idx])
#    
#    for i in range(len(word_index)):
#        print(feature_word[i], feature_prob[i])
#    print('------')
    
for i in range(5):
    prob = np.array(coef[i])
    index = np.argsort(-prob)
    index = index[:60]
    feature_word = []
    feature_prob = []
    for idx in index :
        feature_word.append(words[idx])
        feature_prob.append(prob[idx])
    
    for i in range(60):
        print(feature_word[i], feature_prob[i])
    print('------')
#features = []
#for i in range(5):
#    prob = np.array(coef[i])
##    index = []
##    feature = []
#    index = np.argsort(prob)
#    for i in range(len(prob)):
#        if prob[i] > -8 :
#            index.append(i)
#            feature.append(words[i])
#    features.append(feature)
#print(features)