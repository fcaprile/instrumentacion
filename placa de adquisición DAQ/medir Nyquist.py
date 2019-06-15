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

fs=10000
frecuencias_usadas=np.linspace(1500,15000,100)
frecuencia_medida=[]

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev12/ai1",terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE)
    print(task.timing.cfg_samp_clk_timing(fs))
    task.ai_channels.add_ai_voltage_chan("Dev12/ai9",terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE)
    tension=task.read(1000)
    plt.plot(tension[0])
#    for f in frecuencias_usadas:
#        gen.write('FREQ %f' % f)
#    #    print(task.read()) 
#        tension=task.read(5000)   
#    #    plt.plot(tension) 
##       metodo fft
        frecuencias,amplitudes=fourier(tension,fs)
        posicion_frec=detect_peaks(amplitudes,mph=max(amplitudes)*0.75,mpd=1)[0]
        frecuencia_maxima=frecuencias[posicion_frec]
        frecuencia_medida.append(frecuencia_maxima)


#       metodo detectar picos
#        posicion_picos=detect_peaks(tension, mph=0.1, mpd=5)
##        duracion=1/400000*1000
#        periodo=(posicion_picos[1]-posicion_picos[0])*1/fs
##        frecuencia_medida.append(1/(duracion/len(posicion_picos)))
#        frecuencia_medida.append(1/periodo)
#        print(frecuencia)
plt.plot(frecuencias_usadas,frecuencia_medida,'b*')
plt.grid(True)
plt.xlabel('Frecuencia enviada (Hz)')
plt.ylabel('Frecuencia medida (Hz)')
plt.title('Nyquist a fs='+str(fs))

#np.savetxt('Nyquist a fs='+str(fs)+'.txt',[frecuencias_usadas,frecuencia_medida])
gen.close()
