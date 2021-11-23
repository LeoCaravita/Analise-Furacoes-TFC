# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 21:09:08 2021

@author: Leonardo Caravita
"""
import pandas as pd
import numpy as np
import math

#Cada malha é uma quadrícula de 1km por 1km
class Malha:
    
    #Parâmetros de criação de cada malha
    def __init__(self, id, x, y, quantidade, vel_max):
        self.id = id
        self.x = x
        self.y = y
        self.quantidade = quantidade
        self.vel_max = vel_max 

    
    #Função que coleta os dados do CSV
    @staticmethod
    def get_dados(csv):
        df = pd.read_csv(csv)
        return df
    
    #Função que formata os dados do csv em matriz
    @staticmethod
    def matrix_shape(num_galpoes, num_rows, num_cols):
        matrix_ones = np.ones((num_rows,num_cols))
        
        linha = 0
        coluna = 0
        
        for item in num_galpoes:
            matrix_ones[linha,coluna] = item
            
            if (linha % (num_rows-1) == 0 and linha != 0):
                coluna = coluna + 1
                linha = -1
        
            linha = linha + 1
            
        return matrix_ones
    
    #Função que reorganiza os dados para plotar 
    @staticmethod
    def organized_matrix(matrix, num_rows, num_cols):
        i = num_rows - 1
        j = 0
        nova = np.ones((num_rows,num_cols))

        while i >= 0:
        
            nova[j,:] = matrix[i,:] 
            j = j + 1
            i = i - 1
        
        return nova
    
    #Função que calcula a distância da malha em relação a posição do tornado
    def distancia(self, X_tornado, Y_tornado):
            dist = math.sqrt((self.x - X_tornado)**2 + (self.y - Y_tornado)**2)           
            self.dist = dist
        
    #Função que calcula o ângulo entre cada quadícula e o trajeto do tornado, 
    #com base em sua posição
    def angulo_interno(self, X_tornado, Y_tornado, angulo_trajeto):
        
        #Transporta o centro do eixo para a posição do tornado no instante
        x_q = self.x - X_tornado
        y_q = self.y - Y_tornado
        
        #Calcula o coeficiente angular da reta formada entre o centro do tornado 
        #e o centro da quadrícula     
        
        
        if x_q != 0:
            m = math.degrees(math.atan(y_q/x_q))
        
        ang_int = 0
        
        angulo = angulo_trajeto
        
        
        if angulo_trajeto > 90 and angulo_trajeto < 270:
            angulo = angulo_trajeto - 180
        
        if angulo_trajeto >= 270 and angulo_trajeto < 360:
            angulo = angulo_trajeto - 360
        
    
        if y_q > 0 and x_q > 0:
            ang_int = abs(m - angulo)
        
        if y_q > 0 and x_q < 0:
            ang_int = 180 - abs(-m + angulo)
            
        if y_q < 0 and x_q < 0:
            ang_int = -abs(m - angulo) + 180
            
        if y_q < 0 and x_q > 0:
            ang_int = abs(-m + angulo)   
        
        if angulo_trajeto > 90 and angulo_trajeto < 270:
            ang_int = 180 - ang_int
            
        #Condições para multiplos de 90
        if angulo_trajeto == 0:
            if x_q > 0 and y_q == 0:
                ang_int = 0
            elif x_q < 0 and y_q == 0:
                ang_int = 180
        if angulo_trajeto == 90:
            if x_q == 0 and y_q > 0:
                ang_int = 0
            elif x_q == 0 and y_q < 0:
                ang_int = 180
        if angulo_trajeto == 180:
            if x_q > 0 and y_q == 0:
                ang_int = 180
            elif x_q < 0 and y_q == 0:
                ang_int = 0
        if angulo_trajeto == 270:
            if x_q == 0 and y_q > 0:
                ang_int = 180
            elif x_q == 0 and y_q < 0:
                ang_int = 0

            
        self.ang_interno = ang_int
        
        
        
        
        