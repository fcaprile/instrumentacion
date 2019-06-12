# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 05:10:00 2019

@author: Publico
"""
import lantz
import time
from lantz.ino import INODriver, QuantityFeat, BoolFeat

class Servo(INODriver):       
    angulo = QuantityFeat('Angulo', setter=True)
    enable = BoolFeat('ENABLE')

if __name__ == '__main__':
    with Servo.via_packfile('Servo.pack.yaml') as dev:
        print('Hola, maestros de la programacion y el universo')
        for i in range(150):
            dev.angulo=i*1.0
        for i in range(150):
            dev.angulo=150-i
