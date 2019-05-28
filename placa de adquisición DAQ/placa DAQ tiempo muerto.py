# -*- coding: utf-8 -*-
"""
Created on Wed May 22 03:33:32 2019

@author: Publico
"""

import nidaqmx
from matplotlib import pyplot as plt
import visa
import numpy as np
import time
from scipy.fftpack import fft,ifft

rm=visa.ResourceManager()

resource_name_gen=rm.list_resources()[0]
gen=rm.open_resource(resource_name_gen)




system = nidaqmx.system.System.local()
#system.driver_version
for device in system.devices:
    print(device.ai_max_multi_chan_rate)
#print(system.driver_version)    
#    
#cfg_sample_clk_timing

def fourier(y,fs):
    T=1/fs
    N=len(y)
#    x = np.linspace(0.0, N*T, N)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    yf=fft(y)
    return xf, 2.0/N * np.abs(yf[0:N//2])

fs=30000
frecuencias_usadas=np.linspace(1500,15000,100)
frecuencia_medida=[]

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev12/ai1",terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE)
    print(task.timing.cfg_samp_clk_timing(fs))
#    task.ai_channels.add_ai_voltage_chan("Dev12/ai9",terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE)
    a=10
    b=1000
    med=np.zeros([a*b])
    for i in range(a):
        med[i*b:(i+1)*b]=task.read(b)
    plt.plot(med,'b*')
#plt.plot(frecuencias_usadas,frecuencia_medida,'b*')
#plt.grid(True)
#plt.xlabel('Posición')
#plt.ylabel('Tension (V)')
#plt.title('Nyquist a fs='+str(fs))

#np.savetxt('tiempo muerto.txt',[med],delimiter='\t')
gen.close()
