# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 23:05:30 2021

@author: Leo
"""
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d


#%% COLETA DOS DADOS

dir = os.getcwd() + '\Resultados'
angulo_inicial = 140
angulo_final = 320
angulo_incremento = 10
num_simulacoes = 10000

def get_dados(nome):
        csv = dir + nome + '.csv'
        df = pd.read_csv(csv)
        return df
    
resultados = []    
    
for angulo in range(angulo_inicial,angulo_final,angulo_incremento):
    nome = '\Angulo_' + str(angulo)
    resultados.append(get_dados(nome))
    
num_angulos = len(resultados)    

#%%PORCENTAGEM DE DANO
category_names = ['Estado de Dano 3', 'Estado de Dano 2', 'Estado de Dano 1']

list_falhas = []
dados_dict1 = {}
dados_dict2 = {}
dados_dict3 = {}
limite = num_angulos/3
contador = 1

angulo = angulo_inicial
for item in resultados:
    
    #Legendas 
    label_angulo = 'Direção ' + str(angulo) + '°'
    
    #Média das falhas em cada estado de dano   
    media1 = np.round(np.mean(item['Falhas_1']),0)
    media2 = np.round(np.mean(item['Falhas_2']),0)
    media3 = np.round(np.mean(item['Falhas_3']),0)
    

    if contador <= limite:              
        
        # PORCENTAGENS
        # list_falhas = [p_1, p_2, p_3]        
        
        # TOTAL DE FALHAS
        list_falhas = [media3, media2, media1] 
        dados_dict1[label_angulo] = list_falhas
        
    elif contador > limite*2:
        # PORCENTAGENS
        # list_falhas = [p_1, p_2, p_3]        
        
        # TOTAL DE FALHAS
        list_falhas = [media3, media2, media1] 
        dados_dict3[label_angulo] = list_falhas
    else:
        list_falhas = [media3, media2, media1] 
        dados_dict2[label_angulo] = list_falhas             
    
    angulo = angulo + angulo_incremento   
    contador = contador + 1

def survey(results, category_names):
    
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('Reds')(
        np.linspace(0.6, 0.3, data.shape[1]))
    

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.set_title('Estruturas Danificadas', y = -0.07)
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)    
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax

survey(dados_dict1, category_names)
plt.show()

survey(dados_dict2, category_names)
plt.show()

survey(dados_dict3, category_names)
plt.show()

#%% HISTOGRAMAS  

def plot_hist1(falhas_200, falhas_280, nivel):
    plt.figure()
    plt.hist([falhas_200, falhas_280], 30, alpha = 0.5, 
             label=['Direção 200°','Direção 280°'], edgecolor = 'k', color = ['g', 'r'])
    
    plt.yscale('log')
    plt.legend(loc='upper right')
    plt.xlabel('Construções danificadas')
    plt.ylabel('Número de aparições')
    plt.title('Estado de Dano ' + str(nivel))
    
    plt.axvline(np.mean(falhas_200), label = 'Média: {:.0f}'.format(np.mean(falhas_200)), color='g', linestyle='dashed', linewidth=1)
    #max_xlim, max_ylim = plt.ylim()
    #plt.text(np.mean(falhas_200)-100, max_ylim*0.6, 'Média: {:.0f}'.format(np.mean(falhas_200)),color='g')
    
    plt.axvline(np.mean(falhas_280), label = 'Média: {:.0f}'.format(np.mean(falhas_280)), color='r', linestyle='dashed', linewidth=1)
    #max_xlim, max_ylim = plt.ylim()
    #plt.text(np.mean(falhas_280)*1.1, max_ylim*0.5, 'Média: {:.0f}'.format(np.mean(falhas_280)),color='r')
    plt.grid(axis='y', linestyle='dashed', alpha = 0.4)
    plt.legend()
    plt.show()

def plot_hist2(falhas_1, falhas_2, falhas_3, angulo):
    plt.figure()
    plt.hist([falhas_1, falhas_2, falhas_3], 30, alpha = 0.5, 
             label=['Estado de Dano 1','Estado de Dano 2','Estado de Dano 3'], edgecolor = 'k', color = ['g', 'orange', 'r'])
    plt.yscale('log')
    plt.legend(loc='upper right')
    plt.xlabel('Construções danificadas')
    plt.ylabel('Número de aparições')
    plt.title('Direção: ' + str(angulo) + '°')
    plt.grid(axis='y', linestyle='dashed', alpha = 0.4)
    
    plt.axvline(np.mean(falhas_1), label = 'Média: {:.0f}'.format(np.mean(falhas_1)), color='g', linestyle='dashed', linewidth=1)
    plt.axvline(np.mean(falhas_2), label = 'Média: {:.0f}'.format(np.mean(falhas_2)), color='orange', linestyle='dashed', linewidth=1)
    plt.axvline(np.mean(falhas_3), label = 'Média: {:.0f}'.format(np.mean(falhas_3)), color='r', linestyle='dashed', linewidth=1)
    plt.legend()
    plt.show()

angulo = angulo_inicial


# COLETA OS DADOS PARA AS DIREÇÕES DE INTERESSE
for item in resultados:
    
    if angulo == 200:
        falhas_200_1 = item['Falhas_1']
        falhas_200_2 = item['Falhas_2']
        falhas_200_3 = item['Falhas_3']
        v_200 = np.round(item['V_max'])
        
    elif angulo == 280:
        falhas_280_1 = item['Falhas_1']
        falhas_280_2 = item['Falhas_2']
        falhas_280_3 = item['Falhas_3'] 
        v_280 = np.round(item['V_max'])
    
    angulo = angulo + angulo_incremento
    
#CHAMA A FUNÇÃO PARA PLOTAR
plot_hist1(falhas_200_1, falhas_280_1, 1)
plot_hist1(falhas_200_2, falhas_280_2, 2)
plot_hist1(falhas_200_3, falhas_280_3, 3)
plot_hist2(falhas_200_1, falhas_200_2, falhas_200_3, 200)
plot_hist2(falhas_280_1, falhas_280_2, falhas_280_3, 280)


#%% CATEGORIAS

falhas_total_1 = []
falhas_total_2 = []
falhas_total_3 = []
v_total = []
area_cob = 900
custo_cob = 300

for item in resultados:
    for i in range(0,10000):
        falhas_total_1.append(item['Falhas_1'][i])
        falhas_total_2.append(item['Falhas_2'][i])
        falhas_total_3.append(item['Falhas_3'][i])
        v_total.append(item['V_max'][i])
        


#Retorna um vetor com as falhas das simulações separadas por categoria
def dano_categoria(falhas, vel, categoria):
    total_falhas = []
    for i in range(0,10000*num_angulos):
        if categoria == 1:
            if vel[i] >= 119 and vel[i] <=153:
                total_falhas.append(falhas[i])
        if categoria == 2:
            if vel[i] > 153 and vel[i] <=177:
                total_falhas.append(falhas[i])
        if categoria == 3:
            if vel[i] > 177 and vel[i] <=208:
                total_falhas.append(falhas[i])
        if categoria == 4:
            if vel[i] > 208 and vel[i] <=251:
                total_falhas.append(falhas[i])
        if categoria == 5:
            if vel[i] > 251:
                total_falhas.append(falhas[i])                                
    return total_falhas


dano1_nivel1_total = dano_categoria(falhas_total_1, v_total, 1)
dano1_nivel2_total = dano_categoria(falhas_total_2, v_total, 1)
dano1_nivel3_total = dano_categoria(falhas_total_3, v_total, 1)

dano2_nivel1_total = dano_categoria(falhas_total_1, v_total, 2)
dano2_nivel2_total = dano_categoria(falhas_total_2, v_total, 2)
dano2_nivel3_total = dano_categoria(falhas_total_3, v_total, 2)

dano3_nivel1_total = dano_categoria(falhas_total_1, v_total, 3)
dano3_nivel2_total = dano_categoria(falhas_total_2, v_total, 3)
dano3_nivel3_total = dano_categoria(falhas_total_3, v_total, 3)

dano4_nivel1_total = dano_categoria(falhas_total_1, v_total, 4)
dano4_nivel2_total = dano_categoria(falhas_total_2, v_total, 4)
dano4_nivel3_total = dano_categoria(falhas_total_3, v_total, 4)

dano5_nivel1_total = dano_categoria(falhas_total_1, v_total, 5)
dano5_nivel2_total = dano_categoria(falhas_total_2, v_total, 5)
dano5_nivel3_total = dano_categoria(falhas_total_3, v_total, 5)

dano_1_max = [np.mean(dano1_nivel1_total)*custo_cob*area_cob*0.15/1000000,
          np.mean(dano2_nivel1_total)*custo_cob*area_cob*0.15/1000000,
          np.mean(dano3_nivel1_total)*custo_cob*area_cob*0.15/1000000,
          np.mean(dano4_nivel1_total)*custo_cob*area_cob*0.15/1000000,
          np.mean(dano5_nivel1_total)*custo_cob*area_cob*0.15/1000000]

dano_2_max = [np.mean(dano1_nivel2_total)*custo_cob*area_cob*0.5/1000000,
          np.mean(dano2_nivel2_total)*custo_cob*area_cob*0.5/1000000,
          np.mean(dano3_nivel2_total)*custo_cob*area_cob*0.5/1000000,
          np.mean(dano4_nivel2_total)*custo_cob*area_cob*0.5/1000000,
          np.mean(dano5_nivel2_total)*custo_cob*area_cob*0.5/1000000]

dano_3_max = [np.mean(dano1_nivel3_total)*custo_cob*area_cob/1000000,
          np.mean(dano2_nivel3_total)*custo_cob*area_cob/1000000,
          np.mean(dano3_nivel3_total)*custo_cob*area_cob/1000000,
          np.mean(dano4_nivel3_total)*custo_cob*area_cob/1000000,
          np.mean(dano5_nivel3_total)*custo_cob*area_cob/1000000]

dano_1_min = [np.mean(dano1_nivel1_total)*custo_cob*area_cob*0.02/1000000,
          np.mean(dano2_nivel1_total)*custo_cob*area_cob*0.02/1000000,
          np.mean(dano3_nivel1_total)*custo_cob*area_cob*0.02/1000000,
          np.mean(dano4_nivel1_total)*custo_cob*area_cob*0.02/1000000,
          np.mean(dano5_nivel1_total)*custo_cob*area_cob*0.02/1000000]

dano_2_min = [np.mean(dano1_nivel2_total)*custo_cob*area_cob*0.15/1000000,
          np.mean(dano2_nivel2_total)*custo_cob*area_cob*0.15/1000000,
          np.mean(dano3_nivel2_total)*custo_cob*area_cob*0.15/1000000,
          np.mean(dano4_nivel2_total)*custo_cob*area_cob*0.15/1000000,
          np.mean(dano5_nivel2_total)*custo_cob*area_cob*0.15/1000000]

dano_3_min = [np.mean(dano1_nivel3_total)*custo_cob*area_cob*0.5/1000000,
          np.mean(dano2_nivel3_total)*custo_cob*area_cob*0.5/1000000,
          np.mean(dano3_nivel3_total)*custo_cob*area_cob*0.5/1000000,
          np.mean(dano4_nivel3_total)*custo_cob*area_cob*0.5/1000000,
          np.mean(dano5_nivel3_total)*custo_cob*area_cob*0.5/1000000]



def custo(dano_1_min, dano_1_max,dano_2_min, dano_3_min):
    
    c1 = 'g'
    c2 = 'orange'
    c3 = 'r'
    
    a_min = 0.8
    p1_min = '2%'
    p2_min = '15%'
    p3_min = '50%'
    
    a_max = 0.5
    p1_max = '15%'
    p2_max = '50%'
    p3_max = '100%'  
    
    barWidth = 0.25    
        
    r1 = np.arange(len(dano_1_min))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    
    plt.bar(r1, dano_1_min, width = barWidth, label = 'Estado de Dano 1 - Mínimo', edgecolor='black', alpha = a_min, color = c1)
    plt.bar(r1, dano_1_max, width = barWidth, label = 'Estado de Dano 1 - Máximo', edgecolor='black', alpha = a_max, color = c1)
    
    plt.bar(r2, dano_2_min, width = barWidth, label = 'Estado de Dano 2 - Mínimo', edgecolor='black', alpha = a_min, color = c2)
    plt.bar(r2, dano_2_max, width = barWidth, label = 'Estado de Dano 2 - Máximo', edgecolor='black', alpha = a_max, color = c2)
    
    plt.bar(r3, dano_3_min, width = barWidth, label = 'Estado de Dano 3 - Mínimo', edgecolor='black', alpha = a_min, color = c3)
    plt.bar(r3, dano_3_max, width = barWidth, label = 'Estado de Dano 3 - Máximo', edgecolor='black', alpha = a_max, color = c3)
    
    X = ['Categoria 1', 'Categoria 2', 'Categoria 3','Categoria 4', 'Categoria 5']
    Y1_min = dano_1_min
    Y1_max = dano_1_max
    
    Y2_min = dano_2_min
    Y2_max = dano_2_max
    
    Y3_min = dano_3_min
    Y3_max = dano_3_max
    
    plt.xticks([r + barWidth for r in range(len(dano_1_min))], X)
    plt.ylabel('Prejuízo em Milhões de Reais')
    
    #plt.grid(linestyle='-', linewidth=0.3)
    
    for x, y in zip([r  for r in range(len(dano_1_min))], Y1_min):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom', color = c1)
    for x, y in zip([r  for r in range(len(dano_1_max))], Y1_max):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom', color = c1)    
        
    for x, y in zip([r + barWidth for r in range(len(dano_2_min))], Y2_min):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom', color = c2)
    for x, y in zip([r + barWidth for r in range(len(dano_2_max))], Y2_max):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom', color = c2)
        
    for x, y in zip([r + 2*barWidth for r in range(len(dano_3_min))], Y3_min):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom', color = c3)
    for x, y in zip([r + 2*barWidth for r in range(len(dano_3_max))], Y3_max):
        plt.text(x, y, '%.2f' % y, ha='center', va='bottom', color = c3)    
    plt.grid(axis='y', linestyle='dashed', alpha = 0.4)
    plt.legend()
    #plt.title('Prejuízo Médio por Categoria')
    plt.yscale('log')


plt.figure()
custo(dano_1_min, dano_1_max,dano_2_min, dano_3_min)
#custo(dano_1_max, dano_2_max, dano_3_max, 'max')

plt.show()
# #280
# dano1_nivel1_280 = dano_categoria(falhas_280_1, v_280, 1)
# dano1_nivel2_280 = dano_categoria(falhas_280_2, v_280, 1)
# dano1_nivel3_280 = dano_categoria(falhas_280_3, v_280, 1)

# dano2_nivel1_280 = dano_categoria(falhas_280_1, v_280, 2)
# dano2_nivel2_280 = dano_categoria(falhas_280_2, v_280, 2)
# dano2_nivel3_280 = dano_categoria(falhas_280_3, v_280, 2)

# dano3_nivel1_280 = dano_categoria(falhas_280_1, v_280, 3)
# dano3_nivel2_280 = dano_categoria(falhas_280_2, v_280, 3)
# dano3_nivel3_280 = dano_categoria(falhas_280_3, v_280, 3)

# dano4_nivel1_280 = dano_categoria(falhas_280_1, v_280, 4)
# dano4_nivel2_280 = dano_categoria(falhas_280_2, v_280, 4)
# dano4_nivel3_280 = dano_categoria(falhas_280_3, v_280, 4)

# dano5_nivel1_280 = dano_categoria(falhas_280_1, v_280, 5)
# dano5_nivel2_280 = dano_categoria(falhas_280_2, v_280, 5)
# dano5_nivel3_280 = dano_categoria(falhas_280_3, v_280, 5)

# dano_1 = [np.mean(dano1_nivel1_280),
#           np.mean(dano2_nivel1_280),
#           np.mean(dano3_nivel1_280),
#           np.mean(dano4_nivel1_280),
#           np.mean(dano5_nivel1_280)]

# dano_2 = [np.mean(dano1_nivel2_280),
#           np.mean(dano2_nivel2_280),
#           np.mean(dano3_nivel2_280),
#           np.mean(dano4_nivel2_280),
#           np.mean(dano5_nivel2_280)]

# dano_3 = [np.mean(dano1_nivel3_280),
#           np.mean(dano2_nivel3_280),
#           np.mean(dano3_nivel3_280),
#           np.mean(dano4_nivel3_280),
#           np.mean(dano5_nivel3_280)]

# barWidth = 0.25

# r1 = np.arange(len(dano_1))
# r2 = [x + barWidth for x in r1]
# r3 = [x + barWidth for x in r2]

# plt.figure()
# plt.bar(r1, dano_1, width = barWidth, label = 'Estado de Dano 1', edgecolor='black', color = 'g')
# plt.bar(r2, dano_2, width = barWidth, label = 'Estado de Dano 2', edgecolor='black', color = 'orange')
# plt.bar(r3, dano_3, width = barWidth, label = 'Estado de Dano 3', edgecolor='black', color = 'r')

# X = ['Categoria 1', 'Categoria 2', 'Categoria 3','Categoria 4', 'Categoria 5']
# Y1 = dano_1
# Y2 = dano_2
# Y3 = dano_3

# plt.xlabel('Categorias')
# plt.xticks([r + barWidth for r in range(len(dano_1))], X)
# plt.ylabel('Dano')
# plt.legend()
# plt.grid(linestyle='-', linewidth=0.3)

# for x, y in zip([r  for r in range(len(dano_1))], Y1):
#     plt.text(x, y, '%.1f' % y, ha='center', va='bottom', color = 'g')
    
# for x, y in zip([r + barWidth for r in range(len(dano_2))], Y2):
#     plt.text(x, y, '%.1f' % y, ha='center', va='bottom', color = 'orange')
    
# for x, y in zip([r + 2*barWidth for r in range(len(dano_3))], Y3):
#     plt.text(x, y, '%.1f' % y, ha='center', va='bottom', color = 'r')

# plt.title('Direção 280°')
# plt.show()