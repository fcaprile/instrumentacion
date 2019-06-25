# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 03:32:32 2019

@author: Publico
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 02:29:29 2019

@author: Publico
"""

import lantz
import time
from lantz.ino import INODriver, QuantityFeat, BoolFeat
import cv2
import numpy as np
import math
#cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

class Servo(INODriver):       
    angulo = QuantityFeat('Angulo', setter=True)
    enable = BoolFeat('ENABLE')

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
else:
    rval = False

def calcular_centro(gray):
    posx=0
    posy=0
    cont=0
    matriz=np.zeros([len(gray[:,0]),len(gray[0,:])])+255
    for i in range(len(gray[:,0])):
        for j in range(len(gray[0,:])):
            if gray[i,j]<35:
                matriz[i,j]=0
                posx+=j
                posy+=i
                cont+=1
    if cont==0:
        cont=1
    posx/=cont
    posx=640-posx
    posy/=cont
    posy=480-posy
    return posx,posy,matriz

angulo_a_mandar=0
posxc=0
posyc=
inicio=0
if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:        
        print('Hola')            
        while rval:
            if inicio==0:
                dev.angulo=0
                rval, frame = vc.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                posx1,posy1,matriz=calcular_centro(gray)
                dev.angulo=30
                rval, frame = vc.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                posx2,posy2,matriz=calcular_centro(gray)
#                dev.angulo=120
#                rval, frame = vc.read()
#                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                posx3,posy3,matriz=calcular_centro(gray)

            d=posy1-posy2/-0.5
            

            rval, frame = vc.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            posx,posy=calcular_centro(gray)
            
            if posx-len(gray[0,:])/2==0:
                tita=1
            else:
#                tita_rad=math.atan((posy-240)/(posx-320))
                tita=math.atan2((posy-240),(posx-320))*180/np.pi
#            if posy<240 and posy<320:
#                tita=tita_rad/np.pi*180
#            if posy>240 and posy<320:
#                tita=-tita_rad/np.pi*180
#            if posy<240 and posy>320:
#                tita=tita_rad/np.pi*180
#            if posy>240 and posy>320:
#                tita=-tita_rad/np.pi*180
            
#            print(posx,posy,tita)        
            print('El angulo es:',tita)            
            cv2.imshow("la magia", matriz)            
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
            angulo0=0
            angulo_a_mandar+=angulo0+tita*0.2
            if abs(angulo_a_mandar)>90:
                angulo_a_mandar=0
            print('Estamos mandando:',angulo_a_mandar+90)
            dev.angulo=angulo_a_mandar+90
        cv2.destroyWindow("preview")


