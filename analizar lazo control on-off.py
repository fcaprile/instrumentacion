# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:32:30 2019

@author: ferchi
"""
import numpy as np
from matplotlib import pyplot as plt

tiempo,data=np.loadtxt('lazo control 2,5V +-36 sleep200 paso 1V.txt')
plt.rcParams['font.size']=17#tamaño de fuente
plt.plot(tiempo,data,'b*')
plt.grid(True) # Para que quede en hoja cuadriculada
plt.xlabel('Tiempo (s)')
plt.ylabel('Tensión (V)')
plt.legend(loc = 'best') 
#%%
a=25
b=170
#plt.plot(tiempo[a:b],data[a:b],'b*')
print(np.mean(data[a:b]))
a=260
b=370
#plt.plot(tiempo[a:b],data[a:b],'b*')
print(np.mean(data[a:b]))



