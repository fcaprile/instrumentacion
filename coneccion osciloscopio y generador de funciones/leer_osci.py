# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 07:24:41 2019

@author: Publico
"""

from matplotlib import pyplot as plt
import visa
import numpy as np
import time

rm=visa.ResourceManager()

resource_name_osci=rm.list_resources()[0]
osci=rm.open_resource(resource_name_osci)
def medir(ch):
    xze,xin,yze1,ymu1,yoff1=osci.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
#    yze2,ymu2,yoff2=osci.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
    osci.write('DAT:ENC RPB')
    osci.write('DAT:WID 1')
    osci.write('DAT:SOU CH{}'.format(ch) )
    data=osci.query_binary_values('CURV?', datatype='B',container=np.array)
    data=(data-yoff1)*ymu1+yze1
    tiempo = xze + np.arange(len(data)) * xin

    return tiempo,data


#print(gen.query('*IDN?'))
print(osci.query('*IDN?'))
tiempo,data=medir(1)
plt.plot(tiempo,data)
np.savetxt('lazo control 3V +-40 sleep100.txt',[tiempo,data],delimiter='\t')

#usamos R=