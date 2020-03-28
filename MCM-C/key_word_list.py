# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 22:16:27 2020

@author: 86150
"""
product = ['microwave','hair_dryer','pacifier']
key_noun = {}
key_adj = {}
key_other = {}
key_adj_pos = {}
key_adj_neg ={}

reverse_word = ['no','not','without']

key_noun[product[0]] = ['look','work','price','use','size','space','buy','qualiti','fit',
            'oven','instal','money','door','rang','time',
            'open','whirlpool','button','power','turntabl','heat','design',
            'return','repair','servic','fix','plate','noisi',
            'advertis','function','stop','cook','counter',
            'cabinet','push','hole','reheat','brand','steel','countertop',
            'clean']
key_adj[product[0]] = ['great','good','perfect','small','nice','littl','love','well',
           'like','happi','fine','easi','valu','excel','right',
           'best','compact','save','recommend','better','new','exact',
           'fantast','expect','awesom','pleas','ok','simpl',
           'limit','big','fast','cheap','satisfi','pretti',
           'easili','reliabl','quiet','larg','top','effici',
           'glad','new','stainless','warm','need','want',
           'damag','issu','wast','bad','problem','poor','terribl',
             'low','disappoint','hard']
key_other[product[0]] = ['job','unit','far','year','month','paint','kitchen','week',
             'basic','replac','food','dinner','sharp']

key_adj_pos[product[0]] = ['great','good','perfect','small','nice','littl','love','well',
           'like','happi','fine','easi','valu','excel','right',
           'best','compact','save','recommend','better','new','exact',
           'fantast','expect','awesom','pleas','ok','simpl',
           'limit','big','fast','cheap','satisfi','pretti',
           'easili','reliabl','quiet','larg','top','effici',
           'glad','new','stainless','warm','need','want']
key_adj_neg[product[0]] = ['damag','issu','wast','bad','problem','poor','terribl',
             'low','disappoint','hard']

key_noun[product[1]] = ['use','work','blow','power','set','time','heat','price','look',
            'last','travel','air','retract','button','speed','size',
            'qualiti','money','hold','weight','style','return','fold','color',
            'frizz']

key_adj[product[1]] = ['great','love','good','like','well','nice','recommend','best',
           'light','need','easi','quick','perfect','want','fast','small',
           'better','heavi','fine','happi','quiet','cool','excel','expect',
           'compact','pretti','worth','right','cheap','awesom','pleas','smooth',
           'problem','loud','disappoint','die','hard','hot']
key_other[product[1]]= ['cord','attach','bathroom']

key_adj_pos[product[1]] = ['great','love','good','like','well','nice','recommend','best',
           'light','need','easi','quick','perfect','want','fast','small',
           'better','heavi','fine','happi','quiet','cool','excel','expect',
           'compact','pretti','worth','right','cheap','awesom','pleas','smooth']

key_adj_neg[product[1]] = ['problem','loud','disappoint','die','hard','hot']



key_noun[product[2]] = ['use','work','time','look','hold','fit','clean','size',
        'wash','price','sleep','design','suck']

key_adj[product[2]] = []

key_adj_pos[product[2]] = ['great','like','cute','good','easi','well','perfect',
                           'nice','best','recommend','soft','favorit','happi']

key_adj_neg[product[2]] = ['need','hard','wish','expect',]