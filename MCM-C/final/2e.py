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

# target : star rating 
# data : review_all 
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
from sklearn.feature_extraction.text import CountVectorizer  

print('-----')
count_vect = CountVectorizer()  
X_train_counts = count_vect.fit_transform(sentences)  
print('-----')
words = {v : k for k, v in count_vect.vocabulary_.items()}

from sklearn.naive_bayes import MultinomialNB  

#MultinomialNB
clf = MultinomialNB()  
x_clf = clf.fit(X_train_counts, target)  
print(x_clf)#MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
print('-----')
coef = np.array(clf.coef_)
print(coef)
print(coef.shape)
print('-----')

descriptor = ['like','good','well','great','fine','nice','recommend',
              'realli',
              'need','better','want','expect'
              'low','disappoint','old']


