# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 04:18:06 2019

@author: Publico
"""
from matplotlib import pyplot as plt
import visa
import numpy as np

rm=visa.ResourceManager()

class Instrumento:
    
    def __init__ (self, resource_name):
        self.inst=rm.open_resource(resource_name)

    def idn(self):
        return self.inst.query('*IDN?')

        
class Osciloscopio(Instrumento):
    
    def __init__ (self, serial):
        resource_name = 'USB0::0x0699::0x0368::{}::INSTR'.format(serial)
        super().__init__(resource_name)
    
    def get_config(self):
        xze,xin,yze1,ymu1,yoff1=self.inst.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
        yze2,ymu2,yoff2=self.inst.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
        
        return xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2
        
    def capture_channel(self, ch):    
        osci.write('DAT:ENC RPB')
        osci.write('DAT:WID 1')
        osci.write('DAT:SOU CH{}'.format(ch) )
        data=self.inst.query_binary_values('CURV?', datatype='B',container=np.array)
        data=(data-yoff1)*ymu1+yze1
        tiempo = xze + np.arange(len(data)) * xin
        plt.plot(tiempo, data)
        
class GeneradorFunciones(Instrumento):
    
    def __init__ (self, serial):
        resource_name = 'USB0::0x0699::0x0346::{}::INSTR'.format(serial)
        super().__init__(resource_name)
    
    def freq(f):   
        self.inst.write('FREQ{}'.format(f))
    def shape(shape):
        self.inst.write('FUNC{}'.format(shape))
        
        
osc=Osciloscopio('C017067')
osc.idn()
osc.get_config()
osc.capture_channel(1)

gen=GeneradorFunciones('C036492')
gen.idn()
gen.freq(10**5)
gen.shape('SIN')
#o1.setup()