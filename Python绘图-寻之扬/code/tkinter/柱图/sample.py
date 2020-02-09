import pandas as pd
import numpy as np
from tkinter import*
from math import*
top=Tk()
cvs=Canvas(top,width=600,height=600)
cvs.grid()
cvs.create_oval(100,100,500,500)
cvs.create_oval(150,150,450,450,dash=(1,2))
cvs.create_oval(200,200,400,400,dash=(3,3))
cvs.create_oval(250,250,350,350,dash=(4,4))
data_bar=pd.read_csv('data_bar.txt')
label=data_bar['names'].T.values
data=data_bar['nums'].T.values
maxx=-1
minn=1
for i in range(len(data_bar)):
  x=210*sin(pi*2*i/len(data_bar))
  y=210*cos(pi*2*i/len(data_bar))
  t=str(label[i])
  cvs.create_line(300,300,300-200*sin(pi*2*i/len(data_bar)),300-200*cos(pi*2*i/len(data_bar)))
  cvs.create_text(300+int(x),300-int(y),text=t)
  if (data[i]>maxx or maxx==-1): maxx=data[i]
  if (data[i]<minn or minn==1): minn=data[i]
width=10
if (minn>=0):
        for i in range(len(data_bar)):
             theta=2*pi*i/len(data_bar)
             length=int(200*data[i]/maxx)
             x0=int(300-(width/2)*cos(theta))
             y0=int(300-(width/2)*sin(theta))
             x1=int(x0+length*sin(theta))
             y1=int(y0-length*cos(theta))
             x2=int(x1+width*cos(theta))
             y2=int(y1+width*sin(theta))
             x3=int(300+(width/2)*cos(theta))
             y3=int(300+(width/2)*sin(theta))
             cvs.create_polygon(x0,y0,x1,y1,x2,y2,x3,y3,fill='red')
        for i in range(4):
                r=round(maxx/(4-i),2)
                cvs.create_text(300+50*(i+1),305,text=str(r),fill='blue')
if (minn<0):
        divide=int(4*maxx/(maxx-minn))
        for i in range(len(data_bar)):
                theta=2*pi*i/len(data_bar)
                if (data[i]<0):
                        length=50*(4-divide)*data[i]/(minn*(-1))
                else:
                        length=50*divide*data[i]/maxx
                x0=300+50*(4-divide)*sin(theta)
                y0=300-50*(4-divide)*cos(theta)
                x1=int(x0-(width/2)*cos(theta))
                y1=int(y0-(width/2)*sin(theta))
                x2=int(x1+length*sin(theta))
                y2=int(y1-length*cos(theta))
                x3=int(x2+width*cos(theta))
                y3=int(y2+width*sin(theta))
                x4=int(x3-length*sin(theta))
                y4=int(y3+length*cos(theta))
                cvs.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,fill='red')
        for i in range(1,4-divide):
                r=round(minn/(i+1),2)
                cvs.create_text(300+50*(i),305,text=str(r),fill='blue')
        cvs.create_text(300+50*(4-divide),305,text='0',fill='blue')
        for i in range(4-divide,4):
                r=round(maxx/(4-i),2)
                cvs.create_text(300+50*(i+1),305,text=str(r),fill='blue')
top.mainloop()
