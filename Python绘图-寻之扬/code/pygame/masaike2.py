from pygame import *
from math import *
#需要先导入pygame
screen=display.set_mode((300,300))#图片的像素
m=image.load("input.jpg")#图片文件
screen.blit(m,(0,0))

mon=open("gen.py","w")#生成的这个PY文件再次单独运行便可实现图片的马赛克
mon.write("""from pygame import *
from math import *

screen=display.set_mode((300,300))
""")

running=True
display.flip()

for x in range(0,300,5):
    for y in range(0,300,5):

        c=str(screen.get_at((x,y)))
        mon.write("draw.rect(screen,"+c+",("+str(x)+","+str(y)+",4,4))\n")

    mon.write("display.flip()\n")


mon.write("""image.save(screen, "test.jpg")
running=True
while running:
    for evnt in event.get():
        if evnt.type==QUIT:
            running=False

quit()""")
mon.close()
