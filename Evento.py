# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 23:24:53 2021

@author: Leo
"""
import math
import pandas as pd
import numpy as np

#Cria a classe para a trajetoria do tornado
class Trajetoria:
    
    #Parâmetros de criação da trajetória
    def __init__(self, num_rows, num_cols, angulo):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.angulo = angulo    
        
    def gerar(self, num_divisoes):
        distancia = int(round(self.num_cols/num_divisoes,0))     
        centro_X = self.num_cols/2
        centro_Y = self.num_rows/2
        
        X = []
        Y = []
        
        for i in range(0,self.num_cols,distancia):
            xi = i - centro_X
            yi = self.num_rows/2 - centro_Y
            
            alfa = math.radians(self.angulo)
            
            X.append(xi*math.cos(alfa) - yi*math.sin(alfa) + centro_X)
            Y.append(yi*math.cos(alfa) + xi*math.sin(alfa) + centro_Y)      
        
        self.x = X
        self.y = Y
        
#Cria a classe para o evento tornado
class Tornado:
       
    #Parâmetros de criação do tornado
    def __init__(self, vt, rm, deltap0, e_hollandB, e_a, angulo):
        self.Vt = vt
        self.Rm = rm
        self.DeltaP0 = deltap0
        self.e_HollandB = e_hollandB
        self.e_a = e_a
        self.angulo = angulo
        
    #função para calcular a duração do tornado
    def intervalo_tempo(self, distancia):        
        
        distancia = distancia*1000 #Convete a distancia para metros
        self.duracao = distancia/(self.Vt*3600) #Retorna a duração em horas
        
    #Função para conveter o vento a 3000m de altura para 300m
    def converter_vel(self, distancia, Rm):
        if(distancia < (Rm - 7.4)):
            adj = 1.25
        if(distancia >= (Rm - 7.4) and distancia < (Rm + 7.4)):
            adj = 1.25 - (0.2/14.8)*(distancia - (Rm - 7.4))
        if(distancia >= (Rm + 7.4) and distancia < (Rm + 30.0)):
            adj = 1.05 - (0.05/22.6)*(distancia - (Rm + 7.4))
        if(distancia >= (Rm + 30.0)):
            adj = 1.00
            
        return adj
        
        
        
        
                 