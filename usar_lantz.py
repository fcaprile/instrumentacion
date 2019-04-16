# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 03:03:39 2019

@author: Publico
"""
from lantz import MessageBasedDriver
from lantz import Feat, Action
import numpy as np
from matplotlib import pyplot as plt
import time

class Osciloscopio(MessageBasedDriver):
 
    """Tektronix TDS1012 100MHz 2 Channel Digital Storage Oscilloscope
    """
    MANUFACTURER_ID = '0x0699'

    @Feat()
    def idn(self):
        """ Identify the Osciloscope
        """
        return self.query('*IDN?')
    

    @Feat(limits=(1,2))
    def datasource(self):
        """ Retrieves the data source from which data is going to be taken. 
            TDS1012 has 2 channels
        """
        self.channel=self.query('DAT:SOU?')
        return self.channel

    @datasource.setter
    def datasource(self,value):
        self.write('DAT:SOU CH{}'.format(value))
        
    @Action()
    def acquire_parameters(self):
        xze,xin,yze1,ymu1,yoff1=self.resource.query_ascii_values('WFMPRE:XZE?;XIN?;CH1:YZE?;YMU?;YOFF?',separator=';')
        yze2,ymu2,yoff2=self.resource.query_ascii_values('WFMPRE:CH2:YZE?;YMU?;YOFF?',separator=';')
        
        return xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2
    
    @Action()
    def data_setup(self):
        """ Sets the way data is going to be encoded for sending. 
        """
        self.write('DAT:ENC RPB')
        self.write('DAT:WID 1')
        
    @Action()
    def plot_curve(self,start=1,stop=2500):
        """ Gets data from the oscilloscope. It accepts setting the start and 
            stop points of the acquisition (by default the entire range).
        """
        parameters = self.acquire_parameters()
        self.data_setup()
        self.write('DAT:STAR {}'.format(start))
        self.write('DAT:STOP {}'.format(stop))
        data = np.array(self.resource.query_binary_values('CURV?'))
        xze,xin,yze1,ymu1,yoff1,yze2,ymu2,yoff2=parameters
        data=(data - float(yoff1))*ymu1+yze1
        tiempo = xze + np.arange(len(data)) * xin
        plt.plot(tiempo,data)


class Fungen(MessageBasedDriver):

    @Feat()
    def idn(self):
        """ Identify the Osciloscope
        """
        return self.query('*IDN?')

    
    @Feat()
    def frequency(self):
        return self.query('FREQ?')
        
    @frequency.setter
    def frequency(self,value):
        self.write('FREQ{}'.format(value))

def barrido(osci,gen,fi, ff, pasos,channel=1):
    osci.datasource= channel
    c=0
    tiempo=np.zeros([pasos,2500])
    voltaje=np.zeros([pasos,2500])
    for i in np.linspace(fi, ff, pasos):
        gen.frequency=i
        plt.figure(num=i, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
        tiempo,voltaje=osci.plot_curve()
        c+=1
        time.sleep(0.1)
        


gen=Fungen()
gen.initialize()

osci=Osciloscopio('USB0::0x0699::0x0363::C065087::INSTR')
osci.initialize()


barrido(gen, osci,10**5,4*10**5,4)
#falta cmabiar base de tiempo y de voltaje

#6para usar unidades:
#    set_query=MessageBasedDriver.write
#    
#    frequency=mfeats.QuantityFeat('FREQ?','FREQ{}',units='KHz')
