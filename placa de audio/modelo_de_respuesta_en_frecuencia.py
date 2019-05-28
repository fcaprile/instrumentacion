# -*- coding: utf-8 -*-
"""
Created on Wed May 15 03:59:06 2019

@author: Publico
"""

Created on Mon May 13 18:28:38 2019

@author: ferchi

import numpy as np
from matplotlib import pyplot as plt
import math as m
from scipy.optimize import curve_fit 

data=np.loadtxt('Curva_caracterizacion.txt')

#plt.plot(data[0,:],data[1,:])

frecuencias = data[0,:]
tensiones = data[1,:]


frecuencias2=[]#estos serian los vectores finales sin nans poneles el nombre que quieras
tensiones2=[]

for i in range(len(tensiones)):
    if np.isnan(tensiones[i])==False and np.isinf(tensiones[i])==False and np.isnan(frecuencias[i])==False and np.isinf(frecuencias[i])==False:
        tensiones2.append(tensiones[i])
        frecuencias2.append(frecuencias[i])
        
        
frecuencias2=np.array(frecuencias2)
tensiones2=np.array(tensiones2)
plt.figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
plt.rcParams['font.size']=17#tamaño de fuente

plt.plot(frecuencias2,tensiones2,'b-',label='Respuesta real')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Tensión (sin unidades)')

#%%
#amplitud=señal/8000
#ajuste=lambda x,a,b,x0,y0: a*np.exp(b*(x-x0))+y0
ajuste=lambda x,a,y0: a*x+y0

infi = int(np.where(abs(frecuencias2-16700)==min(abs(frecuencias2-16700)))[0])
sup = int(np.where(abs(frecuencias2-22000)==min(abs(frecuencias2-22000)))[0])

iniciales=np.array([-600,18200])#valores iniciales del ajuste
xx=np.linspace(min(frecuencias2[infi:sup]),max(frecuencias2[infi:sup]),1000)                    
popt, pcov = curve_fit(ajuste, frecuencias2[infi:sup], tensiones2[infi:sup],p0=iniciales)

# Ahora creo una curva teórica a partir del modelo ajustado
times = xx
model = ajuste(times, *popt)

#plt.plot(times, model,  '-g',linewidth=4)


#%%
def funcion_respuesta(datax):
    respuesta=np.zeros(len(datax))
    c1=0
    c2=0
    for i in range(len(datax)):
        if datax[i]<150 and c1==0:
            print('Frecuencia muy pequeña!')
            c1=1
        if 150<=datax[i]<=16700:
            respuesta[i]=8250
        if 16700<datax[i]<=22000:
            respuesta[i]=-1.4101777*datax[i]+31767.199
        if 22000<datax[i] and c2==0:
            print('Frecuencia muy alta!')
            c2=1
    return respuesta

plt.plot(frecuencias,funcion_respuesta(frecuencias),'g-',label='Modelo',linewidth=4)                     
plt.legend(loc = 'best')