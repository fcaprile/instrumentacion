# -*- coding: utf-8 -*-
"""
Created on Wed May 15 05:14:31 2019

@author: Publico
"""

import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import time
import math as m
import visa
import numpy as np
import time

rm=visa.ResourceManager()

resource_name_gen=rm.list_resources()[0]

gen=rm.open_resource(resource_name_gen)



def sacar_silencio(tension,floor=50):
    sin_silencio=[]
    for i in tension:
        if abs(i)>floor:
            sin_silencio.append(float(i))
    return sin_silencio

class AudioDevice():
    def __init__(self,fs):
        self.p = pyaudio.PyAudio()
        self.fs=fs

    def info_devices(self):
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        #p.get_default_output_device_info()
        
        for i in range (0,numdevices):
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                        print ("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0,i).get('name'))
        
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                        print ("Output Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0,i).get('name'))
        
        devinfo = self.p.get_device_info_by_index(1)
        print ("Selected device is ",devinfo.get('name'))
       

class InputAudioDevice(AudioDevice):
    def __init__(self,fs=44100,CHUNK=1024,FORMAT=pyaudio.paInt16,CHANNELS=1):
        self.CHUNK = CHUNK  # Cantidad de frames por buffer
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.RATE = fs
        super().__init__(fs)
        self.stream = self.p.open(format=self.FORMAT,     # Tipos de formato paFloat32, paInt32, paInt24, paInt16, paInt8, paUInt8, paCustomFormat   
                        channels=self.CHANNELS,  #  Numero de canales
                        rate=self.RATE,          #  frecuencia de muestreo
                        input=True,   #   Especifica si es un input stream. Defecto = False
                        frames_per_buffer=self.CHUNK,
                        input_device_index=1)  # Indice del dispositivo a usar. Si no especifico usa el por defecto y lo ignora si el input es 'False'

    def escuchar(self,duracion):
        frames=[]
        for i in range(0, m.ceil((self.RATE / self.CHUNK) * duracion)):
            data = self.stream.read(self.CHUNK)  # Lee la data del audio del stream CHUNK
            frames.append(data)
        return np.fromstring(b''.join(frames),dtype=np.int16)

    def medir_VRMS(self,duracion):
        tension=self.escuchar(duracion)
        VRMS=np.mean(np.sqrt(tension**2))
        return VRMS,tension
    
    def plot_input(self,duracion):
        data=self.escuchar(duracion)
        plt.plot(data)#mejorar para que plotee segun el tiempo

microfono=InputAudioDevice(fs=96000,CHUNK=2048,CHANNELS=2)

c=0
tensiones=microfono.escuchar(0.1)

tiempo=np.linspace(0,0.1,len(tensiones))

t1=tiempo[::2]
t2=tiempo[1::2]
V1=tensiones[::2]*0.5/10000
V2=tensiones[1::2]*0.5/10000

plt.plot(t1,V1,'b*')
plt.plot(t2,V2,'r*')

#V1=V1[200:]
#V2=V2[200:]
#Id=(V1+max(V1))/1200
#plt.figure(num=0, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
#plt.plot(Id)
#plt.grid(True) # Para que quede en hoja cuadriculada
#plt.title('Grafico ejemplo')
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Corriente (A)')
#plt.legend(loc = 'best') 
#
#plt.figure(num=1, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
#plt.plot(V2)
#plt.grid(True) # Para que quede en hoja cuadriculada
#plt.title('Grafico ejemplo')
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Tension (V)')
#plt.figure(num=2, figsize=(8, 4), dpi=80, facecolor='w', edgecolor='k')
#plt.plot(V2,Id,'b*')
#plt.grid(True) # Para que quede en hoja cuadriculada
#plt.title('Grafico ejemplo')
#plt.xlabel('Tension (V)')
#plt.ylabel('Corriente (A)')
##10000 son 500mV
#
#
#
#t=np.arange(0,0.10458,1/96000)
#
#M=t,V1,V2
#
#np.savetxt('diodo.txt',M, delimiter='\t')

