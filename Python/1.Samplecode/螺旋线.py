import turtle as t
from random import randint as rint
t.shape("turtle")
t.pensize(5)
t.colormode(255)
t.bgcolor("black")
t.tracer(False)
for x in range(700):
	t.color(rint(0,255),rint(0,255),rint(0,255))
	t.circle(2*(1+x/4),5)
	t.speed(20)
	t.tracer(True)
 