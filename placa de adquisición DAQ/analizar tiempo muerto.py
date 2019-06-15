# -*- coding: utf-8 -*-
"""
Created on Wed May 29 02:47:09 2019

@author: Publico
"""
from scipy.optimize import curve_fit

a=55
b=31

f=lambda x,A,x0: A*(x-x0)          
#plt.plot(tiempo[b:a],tension1[b:a])

popt, pcov = curve_fit(f,tiempo[b:a],tension1[b:a])

plt.plot(tiempo[b-20:a+20],tension1[b-20:a+20],'b*')
plt.plot(tiempo[b:a],f(tiempo[b:a],*popt),'g-')
#%%
tiempos_dif=0
for posicion in range(13):
    posicion+=b+1
    tiempox_1=tiempo[posicion]
    tiempox_2=tension2[posicion]/popt[0]+popt[1]
    print(tiempox_2-tiempox_1)
#    print(tension2[posicion]-popt[0]*(tiempox_2-popt[1]))
    
#    plt.plot(tiempo[b-20:a+20],tension1[b-20:a+20],'b*')
#    plt.plot(tiempox_2,tension2[posicion],'g*')
#    plt.plot(tiempo[b:a],f(tiempo[b:a],*popt),'g-')
    tiempos_dif+=tiempox_2-tiempox_1
print('Promedio es:',tiempos_dif/14)    
#el tiempo dio 1.15*10**-5