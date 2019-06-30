# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 19:00:06 2019

@author: ferchi
"""

import math as m
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from array import array
import os
import sys
from scipy.integrate import quad as inte

carpeta='C:/Users/ferchi/Desktop/github labo 6/instrumentacion/tpfinal/mediciones/pid/totodsloserrores/'

lista=[]
for archivo in os.listdir(carpeta):
    if archivo.endswith(".txt"):
        lista.append(archivo)

for nombre in lista:
#nombre='titas,derivadas,integrales,errores,kp=0,2,ki0,7.txt'
    titas,derivadas,integrales,errores=np.loadtxt(carpeta+nombre)
    plt.plot(titas,'b-',label='Proporcional')
    plt.plot(derivadas,'g-',label='Derivativo')
    plt.plot(integrales,'y-',label='Integral')
    plt.plot(errores,'k-',label='Error total')
    plt.grid(True) # Para que quede en hoja cuadriculada
    plt.legend(loc = 'best') 
    plt.title(nombre)
    plt.xlabel('Paso')
    plt.ylabel('Error')
    plt.savefig(nombre+'.png')
    plt.clf()
    plt.close()


