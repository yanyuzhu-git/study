from turtle import *
import time
 
 
def setTurtle():
    # 窗口大小
    screensize(900, 700, 'pink')
    # 颜色
    color('red', 'pink')
    # 笔粗细
    pensize(3)
    # 速度
    speed(6)
    # 提笔
    penup()
 
 
def getStart(h):
    # 去到的坐标,窗口中心为0,0
    goto(0, -180)
    r = h / 5
    drawBigL(r, h)
    drawBigArc(r, 140)
    drawBigArc(r, 70)
    drawBigR(r, h)
    centerRange()
    drawHope()
    drawName()
 
 
def drawBigL(r, h):
    colors = ['red', 'orange', 'yellow', '#87CEEB', 'violet', 'red']
    for i in range(int(240 / h) + 1):
        seth(0)
        color(colors[i], colors[i + 1])
        drawHeart(r)
        seth(140)
        fd(h)
 
 
def drawBigArc(r, rad):
    colors = ['red', 'orange', 'yellow', 'SkyBlue', 'violet', 'red']
    for i in range(50):
        if (i % 10 == 0):
            color(colors[int(i / 10)], colors[int(i / 10) + 1])
            seth(0)
            drawHeart(r)
            seth(rad - (i + 1) * 4)
        rt(4)
        fd(10.5)
 
 
def drawBigR(r, h):
    colors = ['red', 'orange', 'yellow', 'SkyBlue', 'violet', 'red']
    for i in range(int(240 / h) + 1):
        color(colors[i], colors[i + 1])
        seth(0)
        drawHeart(r)
        setheading(220)
        fd(h)
 
 
def drawHeart(r):
    down()
    begin_fill()
    factor = 180
    seth(45)
    circle(-r, factor)
    fd(2 * r)
    right(90)
    fd(2 * r)
    circle(-r, factor)
    end_fill()
    up()
 
 
# 在心中写字
def centerRange():
    for i in range(6):
        drawCenter(i)
        time.sleep(1)
 
 
def drawCenter(i):
    goto(0, 0)
    colors = ['red', 'orange', 'yellow', 'SkyBlue', 'violet', 'red']
    pencolor(colors[i])
    # 在心中写字 font可以设置字体自己电脑有的都可以设 align开始写字的位置
    #write('love ...', font=('gungsuh', 30,), align="center")
    up()
 
# 写寄语
def drawHope():
    pencolor('black')
    goto(-300, -220)
    showturtle()
    write('晚上的鞭炮再响，', font=('华文行楷', 25,), align="center", move=True)
    goto(-300, -270)
    write('也没有我想你那么想。', font=('华文行楷', 25,), align="center", move=True)
 
# 写署名
def drawName():
    pencolor('black')
    goto(250, -250)
    showturtle()
    write('七夕，就帮你到这了！', font=('gungsuh', 20,), align="center", move=True)
 
 
setTurtle()
getStart(80)
 
# 点击窗口关闭
window = Screen()
window.exitonclick()
