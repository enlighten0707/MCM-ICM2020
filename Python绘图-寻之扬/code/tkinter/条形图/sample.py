# -*- coding: utf-8 -*-
from tkinter import*
import pandas as pd
import numpy as np
top=Tk()
cvs=Canvas(top,width=600,height=600)
cvs.grid()
data=pd.read_csv('data_week2015.csv')

day=data['day'].values
nums=data['nums'].values
for i in range(len(day)+1):
    cvs.create_arc(100+200*i/(len(day)+1),100+200*i/(len(day)+1),500-200*i/(len(day)+1),500-200*i/(len(day)+1),start=90,extent=-270)
columns=12
maxtheta=2*np.pi*3/4
maxx=-1
dr=200/(len(day)+1)
for i in range(len(nums)):
    if nums[i]>maxx:
        maxx=nums[i]
dnum=np.linspace(0,maxx,13)
for i in range(columns+1):
    theta=maxtheta*i/columns
    cvs.create_line(300,300,300+200*np.sin(theta),300-200*np.cos(theta))
    cvs.create_text(300+220*np.sin(theta),300-220*np.cos(theta),text=str(int(dnum[i])))
days=['星期天','星期一','星期二','星期三','星期四','星期五','星期六']
cols=['red','lightpink','orange','yellow','green','lightblue','blue']
for i in range(1,len(day)+1):
    for j in np.arange(dr*i,dr*(i+0.6),1):
        for k in np.linspace(0,maxtheta*nums[i-1]/maxx,80*i):
            x=300+j*np.sin(k)
            y=300-j*np.cos(k)
            cvs.create_rectangle(x,y,x+1,y+1,fill=cols[i-1],outline=cols[i-1])
    cvs.create_text(280,300-(i+0.3)*dr,text=days[i-1])
top.mainloop()
