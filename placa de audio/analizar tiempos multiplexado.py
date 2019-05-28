# -*- coding: utf-8 -*-
"""
Created on Mon May 20 22:37:47 2019

@author: ferchi
"""
import math as m
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

tiempo1,tiempo2,tension1,tension2=np.loadtxt('multiplexado_300Hz.txt',delimiter='\t')

#plt.plot(tiempo1,tension1,'b*')
#plt.plot(tiempo2,tension2,'g*')

pico1_1=detect_peaks(tension1,mph=0.5,mpd=10)[0]
pico1_2=detect_peaks(tension1,mph=0.5,mpd=10)[1]

#plt.plot(tiempo1[pico1_1],tension1[pico1_1],'g*')
#plt.plot(tiempo1[pico1_2],tension1[pico1_2],'g*')

sample_rate=300*(pico1_2-pico1_1)

tiempo1=np.arange(0,1/sample_rate*10240,1/sample_rate)

a=pico1_2
b=int(pico1_2-(pico1_2-pico1_1)/2)

f=lambda x,A,x0: A*(x-x0)          
#plt.plot(tiempo1[b:a],tension1[b:a])

popt, pcov = curve_fit(f,tiempo1[b:a],tension1[b:a])

#plt.plot(tiempo1[b-50:a+50],tension1[b-50:a+50],'b*')
#plt.plot(tiempo1[b:a],f(tiempo1[b:a],*popt),'g-')

tiempox_1=tiempo1[380]
tiempox_2=tension2[381]/popt[0]+popt[1]
print(tiempox_2-tiempox_1)
print(tension2[380]-popt[0]*(tiempox_2-popt[1]))

plt.plot(tiempo1[b-50:a+50],tension1[b-50:a+50],'b*')
plt.plot(tiempox_2,tension2[381],'g*')



