# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 07:23:52 2019

@author: Publico
"""

import cv2

vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
#print(sum(sum(frame[:,:,0]))/255,sum(sum(frame[:,:,1]))/255,sum(sum(frame[:,:,2]))/255)

rojo=0
for i in range(len(frame[:,0,0])):
    for j in range(len(frame[0,:,0])):
        rojo+=frame[i,j,0]
verde=0
for i in range(len(frame[:,0,0])):
    for j in range(len(frame[0,:,0])):
        verde+=frame[i,j,1]
azul=0
for i in range(len(frame[:,0,0])):
    for j in range(len(frame[0,:,0])):
        azul+=frame[i,j,2]
print(rojo,verde,azul)        
cv2.destroyWindow("preview")

