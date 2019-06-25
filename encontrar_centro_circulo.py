# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 22:56:47 2019

@author: ferchi
"""

from scipy.optimize import minimize as minim
import numpy as np
from matplotlib import pyplot as plt

def chi(Xc,args):
    xc,yc,R=Xc
    x1,y1,x2,y2,x3,y3,x4,y4=args
    return abs(3*R**2-(x1-xc)**2-(y1-yc)**2-(x2-xc)**2-(y2-yc)**2-(x3-xc)**2-(y3-yc)**2)#-(x4-xc)**2-(y4-yc)**2

#def chi(Xc,args):
#    a=Xc
#    x=args
#    return abs(a-x)
#
puntos=np.array([10,10,-10,10,0,-14.14,14.14,0])
#puntos=2
x0=np.array([0,0,14.14])
#x0=np.array([0])

res = minim(chi,x0,puntos)
print(res.x)
plt.plot(10,10,'b*')
plt.plot(-10,10,'b*')
plt.plot(0,-14.14,'b*')

def plot_circulo(xc,yc,r,puntos=100):
    tita=np.linspace(0,2*np.pi,puntos)
    plt.plot(r*np.cos(tita)-xc,r*np.sin(tita)-yc,'g')

plot_circulo(*res.x)
