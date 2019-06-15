# -*- coding: utf-8 -*-
"""
Created on Wed May 29 02:47:09 2019

@author: Publico
"""
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

tiempo_total=np.zeros(8)
fs=30000
dt=1/fs
tension=np.loadtxt('C:/Users/ferchi/Desktop/github labo 6/instrumentacion/placa de adquisición DAQ/tiempo muerto.txt',delimiter='\t')
tiempo=np.arange(0,len(tension)*dt,dt)
plt.plot(tiempo*1000,tension)
plt.grid(True)
plt.xlabel('Tiempo (ms)')
plt.ylabel('Tension (V)')

for i in range(8):
    a=(i+1)*1000
    b=(i)*1000+150
    f=lambda x,A,x0: A*(x-x0)          
    #plt.plot(tiempo[b:a],tension1[b:a])
    
    popt, pcov = curve_fit(f,tiempo[b:a],tension[b:a])
    tiempox_1=tiempo[a]
    tiempox_2=tension[a+1]/popt[0]+popt[1]
    print(popt[0])
    #    print(tension2[posicion]-popt[0]*(tiempox_2-popt[1]))
    
    plt.plot(tiempo[b:a]*1000,f(tiempo[b:a],*popt),'g-')
#    plt.plot(tiempox_2,tension[posicion],'g*')
    #    plt.plot(tiempo[b:a],f(tiempo[b:a],*popt),'g-')
    tiempos_dif=tiempox_2-tiempox_1
    print('El tiempo es:',tiempos_dif)
    tiempo_total[i]=tiempox_2-tiempox_1
    
#plt.hist(tiempo_total)
#plt.grid(True)
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Cantidad')
print('El tiempo promedio es:',np.mean(tiempo_total))
#el tiempo dio 0.0261