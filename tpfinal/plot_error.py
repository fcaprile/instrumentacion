# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 04:03:07 2019

@author: Publico
"""
import matplotlib.pyplot as plt
import numpy as np
titas,derivadas,integrales,errores=np.loadtxt('titas,derivadas,integrales,errores,kp=0,2,ki0,7.txt',delimiter='\t')
plt.plot(titas,'b',label='Error')
plt.plot(derivadas,'r',label='Derivativo')
plt.plot(integrales,'g',label='Integral')
plt.plot(errores,'y',label='Integral')
plt.labels()
plt.show()
