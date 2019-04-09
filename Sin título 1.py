# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 02:44:36 2019

@author: Publico
"""

class Milista:

    def __init__(self, contenido):
        self.contenido = contenido
        
    def duplicar(self):
        y=[]
        for elemento in self.contenido:
            y.append(2 * elemento)
        return y
    
x = Milista([1, 2, 3])
print(x)
print (x.duplicar())
            