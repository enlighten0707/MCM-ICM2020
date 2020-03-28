# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 22:27:43 2020

@author: 86150
"""
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import math
from sklearn.preprocessing import minmax_scale 

obj = 'hair_dryer'
length = 9811
corpos = ['use','blow','power','time','set','price','heat','look','travel',
          'need','easi','light','quick','old','want','first','better','replac',
          'button','speed','heavi','thick','low','quiet','wall','cool','size',
          'differ','expect','qualiti','money','weight','compact','style',
          'never','problem','hand','longer','fold','noisi','color','strong',
          'howev','cheap','hope','hard','burn','previous','with','brush',
          'control','frizzi','head','read','expens','broke','temperatur',
          'place','want','straight','complaint','smell','nois','quieter',
          'plastic','damage']

def Process(x,length):
    x = minmax_scale(x,feature_range=(0.002,0.998))
    y = x/sum(x)   
    z = np.log(y)
    k = y*z
    e = sum(k)
    e /=math.log(length)
    e += 1 
    return e

f = pd.read_csv('./Data/hair_dryer.tsv', sep = '\t')
f = f[f.verified_purchase == 'Y']

stars = f['star_rating'].tolist()
helpful_votes = f['helpful_votes'].tolist()
total_votes = f['total_votes'].tolist()
stars = np.array(stars)
helpful_votes = np.array(helpful_votes)
total_votes = np.array(total_votes)

helpful_ratio = np.zeros(length,dtype = np.float32)
for i in range(length):
    if total_votes[i]==0:
        continue
    helpful_ratio[i] = float(helpful_votes[i] / total_votes[i])



#计算熵权
token_file = './Data/'+ obj +'/tokens.pkl'
tokens=pickle.load(open(token_file,'rb'))

word_count = np.zeros(length)
for i in range (length):
    for t in tokens[i]:
        if t in corpos:
            word_count[i] +=1
            


x = []
#x.append(Process(stars,length))
x.append(Process(helpful_votes,length))
x.append(Process(helpful_ratio,length))
x.append(Process(word_count,length))

w = x/sum(x)
print(x)
print(w)
w = [ 0.42853548,  0.42085358,  0.15061094]
#w = [0.03818942,  0.41216996,  0.40478143,  0.1448592 ]




    



