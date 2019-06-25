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
from scipy.ndimage.measurements import center_of_mass
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
    mask = gray < 40
#    lenx,leny=np.shape(gray)
#    mask=np.zeros(np.shape(gray))
#    for i in range(lenx):
#        for j in range(leny):
#            if gray[i,j]<35:
#                mask[i,j]=0
    posx, posy = center_of_mass(mask)
    matriz = np.zeros_like(gray)
    matriz[mask] = 255
    return posx, posy, matriz

def medir_centro(dev,angulo):
    dev.angulo=angulo
    time.sleep(tiempo_espera)
    rval, frame = vc.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    posx,posy,matriz=calcular_centro(gray)
    return posx,posy,matriz

def chi(Xc,args):
    xc,yc,R=Xc
    x1,y1,x2,y2,x3,y3=args
    return abs(3*R**2-(x1-xc)**2-(y1-yc)**2-(x2-xc)**2-(y2-yc)**2-(x3-xc)**2-(y3-yc)**2)#-(x4-xc)**2-(y4-yc)**2


angulo_a_mandar=0
xc=0
yc=0
r=0
inicio=True
tiempo_espera=0.75
angulo0=0 #por si hace falta agregarlo
integral=0
error_anterior=0
pcrit=5
kp=-0.5*0.6
ki=2*kp/pcrit*0.7
kd=kp*pcrit/8*1.5
set_point=0

if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:        
        print('Hola')            
        while rval:
            if inicio==True:
                titas=[]
                derivadas=[]
                integrales=[]
                errores=[]
                angulo_a_mandar=0
                error_anterior=0
                integral=0
                time.sleep(0.2)
                posx1,posy1,matriz=medir_centro(dev,20)
                posx2,posy2,matriz=medir_centro(dev,40)
                posx3,posy3,matriz=medir_centro(dev,80)
                x0=np.array([320,240,50])
                puntos=np.array([posx1,posy1,posx2,posy2,posx3,posy3])
                res=minim(chi,x0,puntos)
                xc,yc,r=res.x
                print('El centro es',xc,yc )
                inicio=False
            
            rval, frame = vc.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            posx,posy,matriz=calcular_centro(gray)
            
            if posx-len(gray[0,:])/2==0:
                tita=1
            else:
                tita=math.atan2((posy-yc),(posx-xc))*180/np.pi+set_point
            print('El angulo es:',tita)            
            cv2.imshow("la magia", -matriz+255)            
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                matriz=np.zeros((4,len(titas)))
                matriz[0,:]=np.array(titas)
                matriz[1,:]=np.array(derivadas)
                matriz[2,:]=np.array(integrales)
                matriz[3,:]=np.array(errores)
                np.savetxt('titas,derivadas,integrales,errores,kp=0,5,ki0,7,kd1,5.txt',matriz,delimiter='\t')
                break
            if key == 32: # apretando espacio renueva medicion del centro
                inicio=True
            if key == 113: # apretando q cambia set point
                set_point=float(input())
            integral+=tita
            derivative=(tita-error_anterior)
            titas.append(tita)
            integrales.append(integral)
            derivadas.append(derivative)
            angulo_a_mandar+=tita*kp+derivative*kd+integral*ki
            errores.append(angulo_a_mandar)
            if abs(angulo_a_mandar)>90:
                angulo_a_mandar=0
                error_anterior=0
                integral=0
                
            print('Estamos mandando:',angulo_a_mandar+90)
            dev.angulo=angulo_a_mandar+90
            error_anterior=tita
            time.sleep(tiempo_espera)
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