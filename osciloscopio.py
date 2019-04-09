# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:10:43 2019
@author: Publico
"""
from matplotlib import pyplot as plt
import visa
import numpy as np

rm=visa.ResourceManager()

resource_name=rm.list_resources()[0]#'USB0::0x0699::0x0363'*?
                                                                                                                                                                                                        

osci=rm.open_resource(resource_name)
        
print(osci.query('*IDN?'))



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


tiempo,data=medir(1)



plt.plot(tiempo, data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')