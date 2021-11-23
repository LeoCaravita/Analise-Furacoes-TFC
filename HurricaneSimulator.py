# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 18:52:05 2021

@author: Leonardo Caravita
"""
from Dados import Malha
from Evento import Trajetoria
from Evento import Tornado
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import random
import time
import scipy.interpolate as interpolate
from scipy.stats import poisson
import os
from pathlib import Path
import csv
from matplotlib import style
import matplotlib.cm as cm   
import matplotlib as mpl

style.use('default')
#%% PLOTAGEM DA CAMADA DE EXPOSIÇÃO ORIGINAL 34X45

num_rows = 45   #Numero de linhas do grid de exposicao
num_cols = 34   #Numero de colunas do grid de exposicao

#Coleta os dados do csv
dados1 = Malha.get_dados("DadosGalpoes.csv")
  
#Monta uma matriz com os dados coletados
malha1 = Malha.matrix_shape(dados1["Quantidade"], num_rows, num_cols) 

#Reorganiza os dados para plotagem
malha_plot1 = Malha.organized_matrix(malha1, num_rows, num_cols)

#Plotagem da layer de exposicao
# plt.pcolor(malha_plot1,cmap = 'turbo', edgecolors='k', linewidth=1)
# plt.tight_layout()
# plt.gca().set_aspect('equal', adjustable='box')
# plt.title("Camada de exposição 34x45")
# plt.colorbar(label = "Número de Galpões")
# plt.show()

#%% PLOTAGEM DA CAMADA DE EXPOSIÇÃO EXTENDIDA 45x45

num_rows = 45   #Numero de linhas do grid de exposicao
num_cols = 45   #Numero de colunas do grid de exposicao

#Coleta os dados do csv
dados2 = Malha.get_dados("DadosGalpoesExtendidos.csv")
  
#Monta uma matriz com os dados coletados
malha2 = Malha.matrix_shape(dados2["Quantidade"], num_rows, num_cols) 

#Reorganiza os dados para plotagem
malha_plot2 = Malha.organized_matrix(malha2, num_rows, num_cols)

#Plotagem da layer de exposicao
# def plotar():
#     plt.figure()
#     plt.pcolor(malha_plot2,cmap = 'turbo', edgecolors='k', linewidth=1)
#     plt.tight_layout()
#     plt.gca().set_aspect('equal', adjustable='box')
#     #plt.title("Camada de exposição 45x45")
#     #plt.title("Trajetos de maior e menor dano")  
#     plt.colorbar(label = "Número de Galpões")
#     #plt.show()
    
# plotar()



#%% VULNERABILIDADES   

#Coleta os dados do csv
vulnerabilidade1 = Malha.get_dados("Vulnerabilidade1.csv")
vulnerabilidade2 = Malha.get_dados("Vulnerabilidade2.csv")
vulnerabilidade3 = Malha.get_dados("Vulnerabilidade3.csv")
    
v_x_1 = vulnerabilidade1["Velocidade"]*0.44704*3.6
v_y_1 = vulnerabilidade1["Probabilidade"]

v_x_2 = vulnerabilidade2["Velocidade"]*0.44704*3.6
v_y_2 = vulnerabilidade2["Probabilidade"]

v_x_3 = vulnerabilidade3["Velocidade"]*0.44704*3.6
v_y_3 = vulnerabilidade3["Probabilidade"]

# plt.figure()
# plt.grid()
# plt.plot(v_x_1,v_y_1, linewidth=2, color = 'g')
# plt.plot(v_x_2,v_y_2, linewidth=2, color = 'orange')
# plt.plot(v_x_3,v_y_3, linewidth=2, color = 'r')
# plt.grid(linestyle='dashed', alpha = 0.4)
# plt.xlabel('Velocidade da Rajada de Vento [Km/h]')
# plt.ylabel('Probabilidade de Falha')
# plt.legend(['Estado de Dano 1', 'Estado de Dano 2', 'Estado de Dano 3'], loc=0)
# plt.show()

#%% ATRIBUIÇÃO DAS PROPRIEDADES DE CADA QUADRÍCULA

#Cria uma lista para salvar todas as quadrículas
exposicao = list() 
contador = 0
y = 0.5

#Percorre cada linha da malha
for linha in malha2:
    x = 0.5
    #Percorre cada item (coluna) da linha
    for item in linha:
        #Cria um objeto da classe Malha pra cada quadrícula
        exposicao.append(Malha(contador + 1,x,y,dados2["Quantidade"][contador],0))
        x = x + 1
        contador = contador + 1
    y = y + 1

#%%FUNÇÃO PARA DEFINIR AS COORDENADAS DA TRAJETÓRIA DO TORNADO

#Variáveis
angulo_inicial = 280
angulo_final = 360
angulo_incremento = 10
num_deslocamentos = 10
trajetorias = list() 
contador = 0

#Repetição para variar o angulo e coletar as coordenadas
for angulo in range(angulo_inicial,angulo_final,angulo_incremento):   
    trajetorias.append(Trajetoria(num_rows, num_cols, angulo))
    trajetorias[contador].gerar(num_deslocamentos) 
    contador = contador + 1

#%% PLOTAGEM DAS TRAJETÓRIAS DOS TORNADOS
# Descomente para ver a projeção das trajetórias dos tornados
# plotar()
#Repetição para variar o angulo
# for angulo in range(angulo_inicial-90,angulo_final-90,angulo_incremento):   
#     #plotar() #Plota a layer de exposição vazia    
#     trajetoria_plot = Trajetoria(num_rows, num_cols, angulo) #Passa os parâmetros inciais da classe
#     trajetoria_plot.gerar(num_deslocamentos) #Gera os pontos da trajetória com base no número de deslocamentos desejado
    
#     if angulo == angulo_inicial-90:
#         for i in range(0,len(trajetoria_plot.x)-1,1):        
#                 plotar()
#                 plt.arrow(trajetoria_plot.x[i], trajetoria_plot.y[i], 
#                           trajetoria_plot.x[i+1]-trajetoria_plot.x[i], 
#                           trajetoria_plot.y[i+1]-trajetoria_plot.y[i],
#                           color = 'r', head_width=1,head_length=0.8) 
#                 plt.show()
#     elif angulo == angulo_final-100:
#         for i in range(0,len(trajetoria_plot.x)-1,1):        
#                 plotar()
#                 plt.arrow(trajetoria_plot.x[i], trajetoria_plot.y[i], 
#                           trajetoria_plot.x[i+1]-trajetoria_plot.x[i], 
#                           trajetoria_plot.y[i+1]-trajetoria_plot.y[i],
#                           color = 'g', head_width=1,head_length=0.8)           
#                 plt.show()
#     else:
#         for i in range(0,len(trajetoria_plot.x)-1,1):        
#                 plotar()
#                 plt.arrow(trajetoria_plot.x[i], trajetoria_plot.y[i], 
#                           trajetoria_plot.x[i+1]-trajetoria_plot.x[i], 
#                           trajetoria_plot.y[i+1]-trajetoria_plot.y[i],
#                           color = 'r', head_width=1,head_length=0.8) 
#                 plt.show()
    

# plt.show()

#%% GERAÇÃO DAS VARIÁVEIS ALEATÓRIAS DOS TORNADOS
num_tornados = 10000
tornados = list()

def GerarRm():
    Rm = np.random.weibull(2.4736,num_tornados)*28.666 #Raio dos máximos ventos
    return Rm

def GerarVt():
    #Vt = [25, 25 ,25]  #Velocidade de translação da tempestade (m/s)
    Vt = np.random.lognormal(1.616,0.365,num_tornados)
    return Vt
def GerarDeltaP0():
    #DeltaP0 = np.random.weibull(3.465,1000)*64.831 #Diferença de pressão central inicial (mb)
    DeltaP0  = np.random.lognormal(3.19,0.7,num_tornados) #Huang
    #DeltaP0  = np.random.lognormal(3.0621,0.5936,num_tornados) #India
    return DeltaP0

def GerarE_HollandB():
    e_HollandB = np.random.normal(0, 0.286,num_tornados) #Erro do termo do parâmetro de Holland B 
    return e_HollandB

def GerarE_a():
    e_a = np.random.normal(0, 0.0158,num_tornados) #Erro da constante de enchimento 
    return e_a

#%%PLOTAGEM DAS VARIÁVEIS
#Descomente para plotar

# def plotar_variavel(x, legenda, titulo):
#     fig, ax1 = plt.subplots()
#     ax1.set_xlabel(legenda)
#     ax1.set_ylabel('PDF', color = 'g')
#     ax1.hist(x,50, edgecolor='black', density=True, linewidth=1, alpha = 0.8, color = 'g')
#     ax1.axvline(np.mean(x), label = 'Média: {:.2f}'.format(np.abs(np.mean(x))), color='r', linestyle='dashed', linewidth=1)
#     ax1.legend(loc = 'upper left')
#     #ax1.grid()

#     ax2 = ax1.twinx()
#     ax2.set_ylabel('CDF', color = 'b')
#     ax2.hist(x,50, edgecolor='black', density=True, cumulative = True,linewidth=1, alpha = 0.6)
    
#     #ax2.grid()

#     #plt.title(titulo)
#     plt.show()

# x1 = GerarE_HollandB()
# plotar_variavel(x1, 'Erro B', 'Erro do Parâmetro de Holland B')

# x2 = GerarE_a()
# plotar_variavel(x2, 'Erro a','Erro da Constante de Enchimento')

# x3 = GerarRm()
# plotar_variavel(x3, 'Rm [Km]', 'Raio das Máximas Velocidades')

# x4 = GerarDeltaP0()
# plotar_variavel(x4, 'DeltaP0 [mb]', 'Diferença de Pressão Inicial')

# x5 = GerarVt()
# plotar_variavel(x5, 'Vt [m/s]', 'Velocidade de Translação do Furacão')


    
#%% PLOTAGEM DAS VELOCIDADES E FALHAS
#Para plotar, descomentar o linha que chama a função na próxima seção

def plotar(tipo):
    plt.close()
    vetor = np.ones((num_rows,num_cols))
    contador = 0
    for c in range(0,num_rows):
        for r in range(0,num_cols):
            if tipo == "vel":
                vetor[r,c] = exposicao[contador].vw*3.6      
                
            contador = contador + 1      
    
    vetor_plot = Malha.organized_matrix(vetor, num_rows, num_cols)
    plt.figure()
    plt.pcolor(vetor_plot,cmap = 'turbo', edgecolors='k', linewidth=1)
    plt.tight_layout()
    plt.gca().set_aspect('equal', adjustable='box') 
    plt.colorbar(label = "Velocidade [Km/h]")
    plt.show()

#%% FUNÇÃO QUE CALCULA A PROBABILIDADE DE FALHA DADA A VELOCIDADE DO VENTO
def p_falha(v_x, v_y, vel):    

    if vel <= v_x.min():
        prob = 0
    elif vel >= v_x.max():
        prob = 1
    else:
        prob = interpolate.interp1d(v_x, v_y, kind='linear')(vel)
    #plt.figure()
    #plt.plot(v_x,v_y)
    #plt.plot(vel, prob, 'ro-')
    return prob

#%%SALVAR OS RESULTADOS

dir = os.getcwd() + '\Resultados2'

Path(dir).mkdir(exist_ok=True)

headerList = ['Simulacao', 'V_max', 'Rm', 'Vt', 'Delta_P0',
              'Falhas_1','Falhas_2','Falhas_3']
    
def salvar(arquivo,v1,v2,v3,v4,v5,v6,v7,v8):
        
    with open(arquivo, 'w', newline='') as file:
        dw = csv.DictWriter(file, delimiter=',',  
                            fieldnames=headerList) 
        dw.writeheader()
        
        for i in range(0, num_tornados): 
            writer = csv.writer(file)
            writer.writerow([v1[i],v2[i],v3[i],v4[i],v5[i],v6[i],v7[i],v8[i]])

#%%PLOTAR 3D
def plotar3d(exposicao, nivel, angulo = 0, tipo = "", vel = False):
    
    x = []
    y = []
    z = []            
    
    for quad in exposicao:
        
        x.append(quad.x)
        y.append(quad.y)     
        
        if vel == False:
            if quad.quantidade > 0:
                if(tipo == 'media'):
                    if(nivel == 1):
                        z.append(np.mean(quad.falha1_acum)) 
                    elif(nivel == 2):
                        z.append(np.mean(quad.falha2_acum))
                    elif(nivel == 3):
                        z.append(np.mean(quad.falha3_acum))
                elif(tipo == 'mediana'):        
                    if(nivel == 1):
                        z.append(np.median(quad.falha1_acum))
                    elif(nivel == 2):
                        z.append(np.median(quad.falha2_acum))
                    elif(nivel == 3):
                        z.append(np.median(quad.falha3_acum))     
                elif(tipo == ""):
                    z.append(quad.quantidade)
            else:
                z.append(0)        
        else:
            z.append(quad.vw*3.6) 
            
        
    dx = np.ones_like(x)
    dy = np.ones_like(x)
    dz = z
    z = np.zeros_like(dz)        
        
    #style.use('classic')         
    
    colormap = 'turbo'
    cmap = cm.get_cmap(colormap) # Get desired colormap - you can change this!
    max_height = np.max(dz)   # get range of colorbars so we can normalize
    min_height = np.min(dz)
    # scale each z to [0,1], and get their rgb values
    rgba = [cmap((k-min_height)/max_height) for k in dz] 
    
    norm = mpl.colors.Normalize(vmin=np.min(dz),  vmax=np.max(dz))
    
    fig = plt.figure() 
    
    ax1 = fig.add_subplot(111, projection='3d')
    
    ax1.set(facecolor='w')
    fig.set(facecolor='w')
    
    if(tipo == 'media'):
        ax1.set_zlim3d(0,4)
    if(tipo == 'mediana'):
        ax1.set_zlim3d(0,0.4)
    else:
        if vel == False:
            ax1.set_zlim3d(0,25)
        
    ax1.bar3d(x, y, z, dx, dy, dz, shade = True, color = rgba, alpha = 1, edgecolor = 'k', linewidth=0.3)
    if vel == False:
        plt.colorbar(cm.ScalarMappable(norm=norm, cmap = colormap), ax = ax1, label = "Número de Galpões")        
    else:
        plt.colorbar(cm.ScalarMappable(norm=norm, cmap = colormap), ax = ax1, label = "Velocidade [Km/h]")
        
    if(tipo == 'media'):
        plt.title("Média das construções Danificadas - Estado de Dano " +str(nivel)+" - " + str(angulo) + "°") 
    elif(tipo == 'mediana'):        
        plt.title("Mediana das construções Danificadas - Estado de Dano " +str(nivel)+" - " + str(angulo) + "°")                    
    #else:       
        #plt.title("Camada de exposição 3D")
    
        
    plt.show()
    

plotar3d(exposicao,0,angulo = 0, tipo = "", vel = True)

#%% SIMULAÇÕES
rho = 0.87 #Densidade do ar a 3000m de altura (kg/m^3)
lat = math.radians(-30.0277) #Latitude de Porto Alegre
f = 2*math.sin(lat)*7.292*10**-5 #Parâmetro de Coriolis (1/s)
dist_costa = 80000
tempo_inicial = 1 #Tempo até o tornado sair do mar e chegar em Porto Alegre (h)
cont_s = 1
simulacao_falhas1 = []
simulacao_falhas2 = []
simulacao_falhas3 = []
saida_angulo = []
saida_falha = []


t0 = time.time()
#Repetição de trajetória do tornado (angulos)
for trajeto in trajetorias:
    num_desloc = len(trajeto.x)-1
    cont_t = 1
    
    Vt = GerarVt()
    Rm = GerarRm()
    DeltaP0 = GerarDeltaP0()
    e_HollandB = GerarE_HollandB()
    e_a = GerarE_a()
    
    #Nome do arquivo para salvar os dados
    arquivo = dir + '\Angulo_' + str(trajeto.angulo) +'.csv'
    
    #Vetores para salvar no CSV final
    csv_Simulacao=[]
    csv_Vel_max_media=[]
    csv_Vel_media=[]
    csv_Rm=[]
    csv_Vt=[]
    csv_DeltaP0=[]
    csv_Falhas1=[]
    csv_Falhas2=[]
    csv_Falhas3=[]       
    
    #Seta as falhas acumuladas como 0
    for quad in exposicao:
        quad.falha1_acum = []
        quad.falha2_acum = []
        quad.falha3_acum = []
    
    # Repetição para simular N tornados em cada direção
    for j in range(0, num_tornados):
        
        # Cria o objeto tornado com suas propriedades
        tornado = Tornado(Vt[j], Rm[j], DeltaP0[j], 
                                e_HollandB[j], e_a[j], trajeto.angulo)
        tornados.append(tornado)
        
        # Calcula o interalo de tempo para cada deslocamento de cada tornado
        tornado.intervalo_tempo(num_cols/num_desloc)       
        
        t = dist_costa/(tornado.Vt*3600) #Tempo até o tornado sair do mar e chegar em Porto Alegre (h)
        # Repetição para cada deslocamento do tornado
        for posicao in range(0, num_desloc + 1):
            # Calcula a distância do tornado em relação a cada quadrícula
            for quadricula in exposicao:
                #if quadricula.quantidade != 0:
                    X_tornado = trajeto.x[posicao] #(km)
                    Y_tornado = trajeto.y[posicao] #(km)
                    quadricula.distancia(X_tornado, Y_tornado) #(km)

                    #Calculo da diferença de pressão central
                    a = 0.0225 + 0.00167*(tornado.DeltaP0*tornado.Vt/tornado.Rm) + tornado.e_a
                    deltaP = tornado.DeltaP0*math.exp(-a*t) #[mb]               
                    
                    #Holland B parameter
                    B = 1.74425 - 0.007915*lat + 0.0000084*(deltaP)**2 - 0.005024*tornado.Rm + tornado.e_HollandB                
                    quadricula.B = B
                    
                    #Calculo entre o vetor que liga o centro do tornado ao centro da quadrícula e o vetor 
                    #da direção do trajeto do tornado
                    quadricula.angulo_interno(X_tornado, Y_tornado, tornado.angulo)
                    
                    #Velocidade de translação ajustada com base na curvatura
                    W = (tornado.Vt*math.sin(math.radians(quadricula.ang_interno)) - f*quadricula.dist*1000)/2
                    quadricula.W = W
                    
                    #Gradiente de velocidade a 3000m
                    quadricula.Vg =  W + math.sqrt(W**2 + (B*deltaP*100/rho)*((tornado.Rm/quadricula.dist)**B)
                                                  *math.exp(-((tornado.Rm/quadricula.dist)**B)))
                    
                    #Conversao para 300m
                    quadricula.fator_conversao = tornado.converter_vel(quadricula.dist, tornado.Rm)
                    quadricula.v300 = quadricula.Vg*quadricula.fator_conversao
                    
                    #Converte para 10m
                    quadricula.vh = (math.log(10/0.35)/math.log(300/0.35))*quadricula.v300
                    
                    #Converte para velocidade de pico de 3s
                    quadricula.vw = quadricula.vh*1.46
                                         
                    
                    if quadricula.vw > quadricula.vel_max:
                        quadricula.vel_max = quadricula.vw                                             
                                        
                    
                # else:
                #     quadricula.vw = 0        
                #     quadricula.vel_max = 0
                
                
            t = t + tornado.duracao
            
            if tornado.Rm < 10:
                plotar("vel") #Descomentar as velocidades enquanto os tornados passam
                #plotar3d(exposicao,0,angulo = 0, tipo = "", vel = True)
            
        
        
        
        total_falha1 = []
        total_falha2 = []
        total_falha3 = []
        vel_max = 0
        velocidades = []
        
        for quad in exposicao:    
            #Calcula a probabilidade de falha da quadricula
            falha1 = p_falha(v_x_1,v_y_1,quad.vel_max)
            quant_falha1 = falha1*quad.quantidade
            quad.falha1 = quant_falha1
            total_falha1.append(quant_falha1)                 
            
            falha2 = p_falha(v_x_2,v_y_2,quad.vel_max)
            quant_falha2 = falha2*quad.quantidade
            quad.falha2 = quant_falha2
            total_falha2.append(quant_falha2)    
            
            falha3 = p_falha(v_x_3,v_y_3,quad.vel_max)
            quant_falha3 = falha3*quad.quantidade
            quad.falha3 = quant_falha3
            total_falha3.append(quant_falha3)                     
            
            if quad.quantidade > 0:
                quad.falha1_acum.append(quant_falha1)
                quad.falha2_acum.append(quant_falha2)
                quad.falha3_acum.append(quant_falha3)
            
            if vel_max < quad.vel_max:
                vel_max = quad.vel_max*3.6
                velocidades.append(vel_max)
                
            #Reseta as velocidades para os próximos tornados   
            quad.vel_max = 0                
        
        t1 = time.time()
        
        total = t1 - t0
            
        vel_max_media = np.mean(velocidades)
        
        soma1 = np.sum(total_falha1)
        soma2 = np.sum(total_falha2)
        soma3 = np.sum(total_falha3)
        simulacao_falhas1.append(soma1)
        simulacao_falhas2.append(soma2)
        simulacao_falhas3.append(soma3)
        
        #Printa no console para acompanhar
        print("Simulação: ",cont_s, "| Tornado: ",cont_t, "| Angulo: ", 
              tornado.angulo,"° | tempo: ", total )
        
        #Vetores para salvar no CSV final
        csv_Simulacao.append(cont_s)
        csv_Vel_max_media.append(vel_max_media)
        csv_Rm.append(tornado.Rm)
        csv_Vt.append(tornado.Vt*3.6)
        csv_DeltaP0.append(tornado.DeltaP0)
        csv_Falhas1.append(int(soma1))
        csv_Falhas2.append(int(soma2))
        csv_Falhas3.append(int(soma3))
        
        cont_t = cont_t + 1
        cont_s = cont_s + 1
        total_falha1.clear()    
        total_falha2.clear()
        total_falha3.clear()
    
                
    
    plotar3d(exposicao, 1, 280, 'media')
    plotar3d(exposicao, 1, 280, 'mediana')
    plotar3d(exposicao, 2, 280, 'media')
    plotar3d(exposicao, 2, 280, 'mediana')
    plotar3d(exposicao, 3, 280, 'media')
    plotar3d(exposicao, 3, 280, 'mediana')
        
        #plotar("falha")
        
    #Salvar resultados
    # salvar(arquivo, csv_Simulacao, csv_Vel_max_media , csv_Rm, csv_Vt,
    #            csv_DeltaP0, csv_Falhas1, csv_Falhas2,csv_Falhas3)    
    
    #plt.figure()
    #plt.hist(simulacao_falhas,50,color='c', edgecolor='k', alpha=0.65)
    #plt.axvline(np.mean(simulacao_falhas), color='b', linestyle='dashed', linewidth=1)
    #max_xlim, max_ylim = plt.ylim()
    #plt.text(np.mean(simulacao_falhas)*1.1, max_ylim*0.9, 'Média: {:.0f}'.format(np.mean(simulacao_falhas)),color='b')
    
    #plt.axvline(np.median(simulacao_falhas), color='r', linestyle='dashed', linewidth=1)
    #plt.text(np.median(simulacao_falhas)*1.1, max_ylim*0.85,'Mediana: {:.0f}'.format(np.median(simulacao_falhas)),color='r')
    
    #saida_angulo.append(tornado.angulo)
    #saida_falha.append(np.mean(simulacao_falhas))
    
    #simulacao_falhas.clear()
    #plt.show()

plt.figure()
plt.plot(saida_angulo,saida_falha)
plt.show()



    
    
    