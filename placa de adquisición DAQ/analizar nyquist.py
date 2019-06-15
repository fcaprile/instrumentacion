# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 16:34:03 2019

@author: ferchi
"""
f_e,f_m=np.loadtxt('Nyquist a fs=10000.txt')
plt.plot(f_e,f_m,'b*',label='fs=10 kHz')
f_e,f_m=np.loadtxt('Nyquist a fs=11000.txt')
plt.plot(f_e,f_m,'g*',label='fs=11 kHz')
f_e,f_m=np.loadtxt('Nyquist a fs=12500.txt')
plt.plot(f_e,f_m,'r*',label='fs=12,5 kHz')
plt.rcParams['font.size']=12#tamaño de fuente
plt.grid(True)
plt.xlabel('Frecuencia enviada (Hz)')
plt.ylabel('Frecuencia medida (Hz)')
plt.legend(loc = 'best') 

