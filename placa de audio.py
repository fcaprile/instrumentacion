# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 03:26:49 2019

@author: Publico
"""
import pyaudio
import numpy as np
from matplotlib import pyplot as plt



#if p.is_format_supported(44100.0,  # Sample rate
#                         input_device=devinfo["index"],
#                         input_channels=devinfo['maxInputChannels'],
#                         input_format=pyaudio.paInt16):
#  print ('Yay!')


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

class OutputAudioDevice(AudioDevice):
    def __init__(self,fs=44100):
        super().__init__(fs)
        self.stream = self.p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output=True)
          
    def output_seno(self,frec,duration=3,volume=0.3):
        length=self.fs*duration
        seno = (np.sin(2*np.pi*np.arange(length)*frec/self.fs)).astype(np.float32)
        self.stream.write(volume*seno)
             
    def barrido(self,fi,ff,pasos,duration=3,volume=0.3):
        frecs=np.linspace(fi,ff,pasos)     
        for i in frecs:
            self.output_seno(i,duration,volume)
#        stream.stop_stream()
#        stream.close()
        
        self.p.terminate()

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
                        frames_per_buffer=self.CHUNK, # Cantidad de frames por buffer
                        input_device_index=1)  # Indice del dispositivo a usar. Si no especifico usa el por defecto y lo ignora si el input es 'False'

    def escuchar(self,duracion):
        frames=[]
        iteraciones=int((self.RATE / self.CHUNK) * duracion)
        if iteraciones==0:
            iteraciones=1
        for i in range(0, iteraciones):
            data = self.stream.read(self.CHUNK)  # Lee la data del audio del stream CHUNK
            frames.append(data)
        return np.fromstring(b''.join(frames),dtype=np.int16)
    
    def plot_input(self,duracion):
        data=self.escuchar(duracion)
        plt.plot(data)#mejorar para que plotee segun el tiempo
        
        
parlante=OutputAudioDevice(44100)
#parlante.barrido(500,2000,pasos=3,duration=1,volume=0.3)
parlante.info_devices()
microfono=InputAudioDevice(fs=44100)
microfono.plot_input(0.00001)
