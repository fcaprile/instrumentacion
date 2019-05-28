# -*- coding: utf-8 -*-
"""
Created on Wed May 29 02:47:09 2019

@author: Publico
"""
from scipy.optimize import curve_fit
tiempo_total=np.zeros(6)
for i in range(6):
    a=(i+2)*1000
    b=(i+1)*1000
    
    tension1=med[b:a]
    tiempo=np.linspace(0,1000/fs,1000)
    f=lambda x,A,x0: A*(x-x0)          
    #plt.plot(tiempo[b:a],tension1[b:a])
    
    popt, pcov = curve_fit(f,tiempo,tension1)
    
    plt.plot(tiempo,tension1,'b*')
    tiempo_largo=np.linspace(0,2000/fs,2000)
    plt.plot(tiempo_largo,f(tiempo_largo,*popt),'g-')
    posicion=a+1
    tiempox_1=tiempo[-1]
    tiempox_2=med[posicion]/popt[0]+popt[1]
    #    print(tension2[posicion]-popt[0]*(tiempox_2-popt[1]))
    
    #    plt.plot(tiempo[b-20:a+20],tension1[b-20:a+20],'b*')
    plt.plot(tiempox_2,med[posicion],'g*')
    #    plt.plot(tiempo[b:a],f(tiempo[b:a],*popt),'g-')
    tiempos_dif=tiempox_2-tiempox_1
    print('El tiempo es:',tiempos_dif)
    tiempo_total[i]=tiempox_2-tiempox_1
    
plt.hist(tiempo_total)
print('El tiempo promedio es:',np.mean(tiempo_total))
#el tiempo dio 0.0261