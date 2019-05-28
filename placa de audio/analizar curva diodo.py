# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
import sys

t,V_total,V_d=np.loadtxt('Diodo.txt',delimiter='\t')

V_total=V_total[200:]
V_d=V_d[200:]
I=(V_total+max(V_total))/1200#divido por la R de 1.2K
V_d-=min(V_d)

f=lambda x,A,g: A*(np.exp(x*g)-1)

ini=np.array([0.00003,0.02])                        
popt, pcov = curve_fit(f,V_d*1000,I,p0=ini)

plt.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')

#plotear (graficar)
plt.rcParams['font.size']=17#tamaño de fuente
plt.plot(V_d*1000,I*1000,'b-',label='Medicion')#x e y deben ser vectores del mismo tamaño

xx=np.linspace(min(V_d*1000),max(V_d*1000),10000)
#plt.plot(xx,f(xx,*ini)*1000)
plt.plot(xx,f(xx,*popt)*1000,'g-',label='Ajuste',linewidth=3)
plt.grid(True) # Para que quede en hoja cuadriculada
plt.ylabel('Corriente (mA)')
plt.xlabel('Tension (mV)')
plt.legend(loc = 'best') 

