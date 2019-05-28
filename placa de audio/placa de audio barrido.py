# -*- coding: utf-8 -*-
"""
Created on Wed May  8 02:59:48 2019

@author: Publico
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 03:26:49 2019
@author: Publico
"""
import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import time
import math as m

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

class OutputAudioDevice(AudioDevice):
    def __init__(self,fs=44100):
        super().__init__(fs)
        self.stream = self.p.open(format=pyaudio.paFloat32,channels=1,rate=fs,output=True)
          
    def output_seno(self,frec,duracion=1,volume=1):#ver de usar callback
        length=self.fs*duracion
        seno = (np.sin(2*np.pi*np.arange(length)*frec/self.fs)).astype(np.float32)
        self.stream.write(volume*seno)#ver si se encuentra un modo de envio por tiempo indefinido
             
    def output_cuadrada(self,frec,duracion=1,volume=0.3):#ver de usar callback
        length=self.fs*duracion
        cuad=np.zeros(length)
        for i in range(length):
            if i>length/3 and i<length/3*2:
                cuad[i]=1
        self.stream.write(volume*seno)#ver si se encuentra un modo de envio por tiempo indefinido

    def barrido(self,fi,ff,pasos,duration=3,volume=1):
        frecs=np.linspace(fi,ff,pasos)     
        for i in frecs:
            self.output_seno(i,duration,volume)
        
    def stop(self):
        self.stream.stop_stream()

    def close(self):
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
        
def barrido(salida, entrada,frecuencias,n_periodos=5,plot=False,volumen=1): # falta normalizar
    VRMS=[]
    for f in frecuencias:
        c=0
        dt=1/f*n_periodos
        tension=entrada.escuchar(dt*25)
#        time.sleep(dt*1)
        salida.output_seno(frec=f,duracion=dt*10,volume=volumen) # ver de que cambie el volumen segun la tension recibida anteriormente, para poder medir con mayor precision              
#        salida.stop()
#        plt.plot(tension)
        time.sleep(10*dt)
        tension=np.array(sacar_silencio(tension))
        V2=np.mean(abs(tension))
        while V2<50 and c<10:
            c+=1
            tension=entrada.escuchar(dt*25)
            salida.output_seno(frec=f,duracion=dt*10,volume=volumen) # ver de que cambie el volumen segun la tension recibida anteriormente, para poder medir con mayor precision              
            tension=np.array(sacar_silencio(tension))
            time.sleep(10*dt)
            V2=np.mean(abs(tension))                    
        VRMS.append(V2)
    if plot==True:
        VRMS=np.array(VRMS)
        plt.plot(frecuencias,VRMS,'b*')
        plt.grid(True) # Para que quede en hoja cuadriculada
        plt.title('Respuesta en frecuencia')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('VRMS (V)')
    return VRMS    
        
parlante=OutputAudioDevice(96000)
#parlante.info_devices()
microfono=InputAudioDevice(fs=96000,CHUNK=2048)
#microfono.plot_input(0.00001)
frecuencias=np.logspace(2,4,10)*1
frecuencias=np.linspace(100,1000,200)
#frecuencias=np.array([5000,6000])

vol=1
respuesta=barrido(parlante,microfono,frecuencias,20,plot=True,volumen=1)
salida=parlante
entrada=microfono

R=22000
R=150000
C=1.1*10**-9
fc=1/2/np.pi/R/C
print('corte=',fc)

M=(frecuencias,respuesta)
np.savetxt('AMP.txt',M)

#se uso lm741



