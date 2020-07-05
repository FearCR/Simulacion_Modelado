from random import random
import math



def uniforme(a,b):
    r=random()
    x=(b-a)*r+a
    return int(x)

def normal(Mu,vari):
    r1 = random()
    r2 = random()
    Z=(-2*math.log(r1))
    Z=pow(Z,1/2)
    pi=math.pi
    Z=Z*(math.cos(2*pi*r2))
    x=(vari*Z)+Mu
    if x<0:
        x=-1*x
    return int(x)

def exponencial(lamb):
    r = random()
    x=(-math.log(1-r))/lamb
    return int(x)

def convolucion(Mu,vari):
    Z=0
    for i in range(1,13):
        r = random()
        Z=Z+r
    x = (vari * Z) + Mu
    return int(x)

def funcionDensidad(funcion,a,b):
    print("por implementar")



print(convolucion(25,100))