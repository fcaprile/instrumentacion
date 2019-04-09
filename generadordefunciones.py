# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 03:22:51 2019

@author: Publico
"""
from matplotlib import pyplot as plt
import visa
import numpy as np
import time

rm=visa.ResourceManager()

resource_name_gen=rm.list_resources()[1]
resource_name_osci=rm.list_resources()[0]

gen=rm.open_resource(resource_name_gen)

osci=rm.open_resource(resource_name_osci)

def medir(ch):
    xze,xin,yze1,ymu1,yoff1=osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
    yze2,ymu2,yoff2=osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
    osci.write('DAT:ENC RPB')
    osci.write('DAT:WID 1')
    osci.write('DAT:SOU CH{}'.format(ch) )
    data=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    data=(data-yoff1)*ymu1+yze1
    tiempo = xze + np.arange(len(data)) * xin

    return tiempo,data


#print(gen.query('*IDN?'))
print(osci.query('*IDN?'))

def barrido(fi, ff, pasos):
    c=0
    tiempo=np.zeros([pasos,2500])
    voltaje=np.zeros([pasos,2500])
    for i in np.linspace(fi, ff, pasos):
        gen.write('FREQ %f' % i)
        tiempo[c,:],voltaje[c,:]=medir(1)
        c+=1
        time.sleep(0.1)
    return tiempo, voltaje
        

tiempo,voltaje=barrido(10**6,4*10**6,3)

for i in range(3):
    plt.figure(num=i, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(tiempo[i,:],voltaje[i,:])

