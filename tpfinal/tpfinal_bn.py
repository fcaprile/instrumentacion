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
from scipy.optimize import minimize as minim
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

def medir_centro(dev,angulo):
    dev.angulo=angulo
    rval, frame = vc.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    posx,posy,matriz=calcular_centro(gray)
    return posx,posy

def chi(Xc,args):
    xc,yc,R=Xc
    x1,y1,x2,y2,x3,y3=args
    return abs(3*R**2-(x1-xc)**2-(y1-yc)**2-(x2-xc)**2-(y2-yc)**2-(x3-xc)**2-(y3-yc)**2)#-(x4-xc)**2-(y4-yc)**2


angulo_a_mandar=0
xc=0
yc=0
r=0
inicio=True

if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:        
        print('Hola')            
        while rval:
            if inicio==True:
                posx1,posy1=medir_centro(dev,0)
                posx2,posy2=medir_centro(dev,60)
                posx3,posy3=medir_centro(dev,120)
                x0=np.array([320,240,50])
                puntos=np.array([posx1,posy1,posx2,posy2,posx3,posy3])
                res=minim(chi,x0,puntos)
                xc,yc,r=res.x
                inicio=False
            
            rval, frame = vc.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            posx,posy,matriz=calcular_centro(gray)
            
            if posx-len(gray[0,:])/2==0:
                tita=1
            else:
                tita=math.atan2((posy-yc),(posx-xc))*180/np.pi
            print('El angulo es:',tita)            
            cv2.imshow("la magia", matriz)            
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
            if key == 32: # apretando espacio renueva medicion del centro
                inicio=True
            angulo0=0 #por si hace falta agregarlo
            angulo_a_mandar+=angulo0+tita*0.2
            if abs(angulo_a_mandar)>90:
                angulo_a_mandar=0
            print('Estamos mandando:',angulo_a_mandar+90)
            dev.angulo=angulo_a_mandar+90
        cv2.destroyWindow("preview")

'''
                dev.angulo=0
                rval, frame = vc.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                posx1,posy1,matriz=calcular_centro(gray)
                dev.angulo=60
                rval, frame = vc.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                posx2,posy2,matriz=calcular_centro(gray)
                dev.angulo=120
                rval, frame = vc.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                posx3,posy3,matriz=calcular_centro(gray)
'''

'''
#                tita_rad=math.atan((posy-240)/(posx-320))
#            if posy<240 and posy<320:
#                tita=tita_rad/np.pi*180
#            if posy>240 and posy<320:
#                tita=-tita_rad/np.pi*180
#            if posy<240 and posy>320:
#                tita=tita_rad/np.pi*180
#            if posy>240 and posy>320:
#                tita=-tita_rad/np.pi*180
            
#            print(posx,posy,tita)        
'''
