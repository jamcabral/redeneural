

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 09:56:00 2019

@author: jammesson
"""


import numpy as np

#SAIDAS ORIGINAIS COM NUMEROS DE 0 A 4
#ONDE 0 = AZUL , 1 = VERDE , 2 = AMARELO , 3 = VERMELHO
#saidas = np.array([[1],[3],[2],[2],[2],[2],[2],[2],[2],[1],[2],[2],[1],[1],[1],[1],[2],[2],[1],[3],[3],[1],[1],[2],[2],[2],[1],[2],[1],[2],[2],[3],[0],[1],[2],[1],[3],[3],[2],[2],[1],[3],[2],[1],[1],[2],[2],[1],[1],[3],[2],[0],[3],[2],[3],[3],[3],[2],[3],[3],[2],[1],[0],[2],[2],[2],[3],[1],[0],[1],[3],[3],[3],[2],[2],[2],[1],[3],[1],[2],[3],[2],[2],[1],[3],[2],[2],[3],[2],[2],[1],[2],[1],[2],[2],[1],[3],[3],[3],[2]])

pesos0 = 2*np.random.random((24,14)) - 1

pesos1 = 2*np.random.random((14,4)) - 1

epocas = 10000
taxaAprendizagem = 0.1
momento = 1

taxaDeAcerto = 1
cr_vermelho = np.array(np.around([1., 0., 0., 0.]))
cr_amarelo = np.array(np.around([0., 1., 0., 0.]))
cr_verde = np.array(np.around([0., 0., 1., 0.]))
cr_azul = np.array(np.around([0., 0., 0., 1.]))
cont_erro = 0
cont_acerto = 0
##https://stackoverflow.com/questions/10626134/derivative-of-sigmoid
def sigmoid(soma):
    return 1 / (1 + np.exp(-soma))
#https://stackoverflow.com/questions/10626134/derivative-of-sigmoid
def sigmoidDerivada(sig):
    return sig * (1 - sig)

entradas = np.array([[0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#1
                     [0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#2
                     [0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#3
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],#4
                     [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,4],#5
                     [0,0,0,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,3],#6
                     [0,0,0,0,0,0,0,0,5,0,0,4,0,0,0,0,0,0,0,0,1,0,0,3],#7
                     [0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,4],#8
                     [0,0,0,0,0,0,0,4,0,0,0,3,0,0,0,1,0,0,0,0,0,0,0,1],#9
                     [0,0,0,0,0,0,0,0,1,0,0,3,0,0,0,0,0,0,0,0,0,0,0,2],#10
                     [0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#11
                     [0,0,0,0,0,0,0,1,0,0,0,4,0,1,0,0,0,0,0,0,0,0,0,1],#12
                     [0,0,0,2,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#13
                     [0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,2],#14
                     [0,0,0,3,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#15
                     [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],#16
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],#17
                     [0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,3],#18
                     [0,0,1,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],#19
                     [0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1],#20
                     [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],#21
                     [0,0,0,1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#22
                     [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#23
                     [0,0,0,2,0,0,0,3,1,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],#24
                     [0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#25
                     [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],#26
                     [0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#27
                     [0,0,1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#28
                     [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#29
                     [0,0,1,0,0,0,0,4,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,4],#30
                     [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#31
                     [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],#32
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2],#33
                     [0,0,1,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#34 
                     [0,0,0,3,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1],#35
                     [0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#36
                     [0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0],#37
                     [0,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#38
                     [0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0],#39
                     [0,0,1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],#40
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#41
                     [0,0,1,0,0,0,0,4,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0],#42
                     [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2],#43
                     [0,0,0,1,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#44
                     [0,0,0,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,3],#45
                     [0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0],#46
                     [0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0],#47
                     [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],#48
                     [0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,3],#49
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],#50
                     [0,0,1,0,0,1,0,4,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],#51
                     [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2],#52
                     [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],#53
                     [0,0,0,0,0,0,0,3,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],#54
                     [0,0,1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],#55
                     [0,0,1,0,0,1,0,4,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,1],#56
                     [0,0,1,0,0,0,0,4,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0],#57
                     [0,0,1,0,0,0,0,4,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1],#58
                     [0,0,1,0,1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],#59
                     [0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,2],#60
                     [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,2],#61
                     [0,0,0,2,0,0,0,4,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],#62
                     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#63
                     [0,1,0,4,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#64
                     [0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0],#65
                     [0,0,0,0,0,0,0,4,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1],#66
                     [0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],#67
                     [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#68
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],#69
                     [1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,4],#70
                     [0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],#71
                     [0,0,0,0,0,0,0,4,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0],#72
                     [0,0,0,0,1,0,0,4,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],#73
                     [0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#74
                     [0,0,0,1,0,0,0,4,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],#75
                     [0,0,1,0,1,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0],#76
                     [0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#77
                     [0,0,1,0,1,0,0,3,0,0,0,3,0,1,0,0,0,0,0,0,0,0,0,0],#78
                     [0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],#79
                     [0,0,0,4,0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,1],#80
                     [0,1,0,0,1,0,0,3,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],#81
                     [0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],#82
                     [0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,3],#83
                     [0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#84
                     [0,0,1,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,0,0,0,0],#85
                     [0,0,0,1,0,0,0,4,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0],#86
                     [0,0,1,0,0,0,0,0,0,0,0,4,0,1,0,1,0,0,0,0,0,0,0,0],#87
                     [0,0,0,0,0,0,0,4,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0],#88
                     [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1],#89
                     [0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#90
                     [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0],#91
                     [0,0,0,1,0,0,0,4,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0],#92
                     [0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],#93
                     [0,0,0,1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#94
                     [0,1,0,0,0,1,0,4,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],#95
                     [0,0,0,0,0,0,0,4,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],#96
                     [0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],#97
                     [0,0,0,0,1,0,0,4,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0],#98
                     [0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],#99
                     [0,0,0,0,0,1,0,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#100
                     #[0,0,1,0,0,0,0,4,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0],#101
                     #[0,0,1,0,0,0,0,4,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],#102
                     #[0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#103
                     #[0,0,0,0,1,0,0,3,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],#104
                     #[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],#105
                     #[0,0,1,0,0,0,0,3,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],#106
                     #[0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0],#107
                     #[1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#108
                     #[0,0,1,0,0,0,0,0,0,3,0,0,1,1,0,0,0,0,0,0,0,0,0,1],#109
                     ])

saidas = np.array([[0,0,1,0],#1
                   [1,0,0,0],#2
                   [0,1,0,0],#3
                   [0,1,0,0],#4
                   [0,1,0,0],#5
                   [0,1,0,0],#6
                   [0,1,0,0],#7
                   [0,1,0,0],#8
                   [0,1,0,0],#9
                   [0,0,1,0],#10
                   [0,1,0,0],#11
                   [0,1,0,0],#12
                   [0,0,1,0],#13
                   [0,0,1,0],#14
                   [0,0,1,0],#15
                   [0,0,1,0],#16
                   [0,1,0,0],#17
                   [0,1,0,0],#18
                   [0,0,1,0],#19
                   [1,0,0,0],#20
                   [1,0,0,0],#21
                   [0,0,1,0],#22
                   [0,0,1,0],#23
                   [0,1,0,0],#24
                   [0,1,0,0],#25
                   [0,1,0,0],#26
                   [0,0,1,0],#27
                   [0,1,0,0],#28
                   [0,0,1,0],#29
                   [0,1,0,0],#30
                   [0,1,0,0],#31
                   [1,0,0,0],#32
                   [0,0,0,1],#33
                   [0,0,1,0],#34
                   [0,1,0,0],#35
                   [0,0,1,0],#36
                   [1,0,0,0],#37
                   [1,0,0,0],#38
                   [0,1,0,0],#39
                   [0,1,0,0],#40
                   [0,0,1,0],#41
                   [1,0,0,0],#42
                   [0,1,0,0],#43
                   [0,0,1,0],#44
                   [0,0,1,0],#45
                   [0,1,0,0],#46
                   [0,1,0,0],#47
                   [0,0,1,0],#48
                   [0,0,1,0],#49
                   [1,0,0,0],#50
                   [0,1,0,0],#51
                   [0,0,0,1],#52
                   [1,0,0,0],#53
                   [0,1,0,0],#54
                   [1,0,0,0],#55
                   [1,0,0,0],#56
                   [1,0,0,0],#57
                   [0,1,0,0],#58
                   [1,0,0,0],#59
                   [1,0,0,0],#60
                   [0,1,0,0],#61
                   [0,0,1,0],#62
                   [0,0,0,1],#63
                   [0,1,0,0],#64
                   [0,1,0,0],#65
                   [0,1,0,0],#66
                   [1,0,0,0],#67
                   [0,0,1,0],#68
                   [0,0,0,1],#69
                   [0,0,1,0],#70
                   [1,0,0,0],#71
                   [1,0,0,0],#72
                   [1,0,0,0],#73
                   [0,1,0,0],#74
                   [0,1,0,0],#75
                   [0,1,0,0],#76
                   [0,0,1,0],#77
                   [1,0,0,0],#78
                   [0,0,1,0],#79
                   [0,1,0,0],#80
                   [1,0,0,0],#81
                   [0,1,0,0],#82
                   [0,1,0,0],#83
                   [0,0,1,0],#84
                   [1,0,0,0],#85
                   [0,1,0,0],#86
                   [0,1,0,0],#87
                   [1,0,0,0],#88
                   [0,1,0,0],#89
                   [0,1,0,0],#90
                   [0,0,1,0],#91
                   [0,1,0,0],#92
                   [0,0,1,0],#93
                   [0,1,0,0],#94
                   [0,1,0,0],#95
                   [0,0,1,0],#96
                   [1,0,0,0],#97
                   [1,0,0,0],#98
                   [1,0,0,0],#99
                   [0,1,0,0],#100
                   #[0,1,0,0],#101
                   #[0,0,1,0],#102
                   #[0,0,0,1],#103
                   #[1,0,0,0],#104
                   #[0,0,0,1],#105
                   #[0,0,0,1],#106
                   #[0,1,0,0],#107
                   #[0,0,1,0],#108
                   #[1,0,0,0],#109
                   ])
    

for j in range(epocas):
    camadaEntrada = entradas
    somaSinapse0 = np.dot(camadaEntrada, pesos0)
    camadaOculta = sigmoid(somaSinapse0)
    
    somaSinapse1 = np.dot(camadaOculta, pesos1)
    camadaSaida = sigmoid(somaSinapse1)
    
    erroCamadaSaida = saidas - camadaSaida
    mediaAbsoluta = np.mean(np.abs(erroCamadaSaida))
    print("Erro: " + str(mediaAbsoluta))
    
    derivadaSaida = sigmoidDerivada(camadaSaida)
    deltaSaida = erroCamadaSaida * derivadaSaida
    
    pesos1Transposta = pesos1.T
    deltaSaidaXPeso = deltaSaida.dot(pesos1Transposta)
    deltaCamadaOculta = deltaSaidaXPeso * sigmoidDerivada(camadaOculta)
    
    camadaOcultaTransposta = camadaOculta.T
    pesosNovo1 = camadaOcultaTransposta.dot(deltaSaida)
    pesos1 = (pesos1 * momento) + (pesosNovo1 * taxaAprendizagem)
    
    camadaEntradaTransposta = camadaEntrada.T
    pesosNovo0 = camadaEntradaTransposta.dot(deltaCamadaOculta)
    pesos0 = (pesos0 * momento) + (pesosNovo0 * taxaAprendizagem)
    
    

taxaDeAcerto = (taxaDeAcerto - mediaAbsoluta) * 100
print("A taxa de acerto da Rede é de : " + str(taxaDeAcerto) + " % \n" )
    

producao_entradas = np.array([
                    #[0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#1
                    #[0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#2
                    #[0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#3
                    #[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],#4
                    #[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,4],#5
                    #[0,0,0,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,3],#6
                    #[0,0,0,0,0,0,0,0,5,0,0,4,0,0,0,0,0,0,0,0,1,0,0,3],#7
                    #[0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,4],#8
                    #[0,0,0,0,0,0,0,4,0,0,0,3,0,0,0,1,0,0,0,0,0,0,0,1],#9
                    #[0,0,0,0,0,0,0,0,1,0,0,3,0,0,0,0,0,0,0,0,0,0,0,2],#10
                    #[0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#11
                    #[0,0,0,0,0,0,0,1,0,0,0,4,0,1,0,0,0,0,0,0,0,0,0,1],#12
                    #[0,0,0,2,0,0,0,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#13
                    #[0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,2],#14
                    #[0,0,0,3,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#15
                    #[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],#16
                    #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],#17
                    #[0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,3],#18
                    #[0,0,1,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],#19
                    #[0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1],#20
                    #[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],#21
                    #[0,0,0,1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#22
                    #[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#23
                    #[0,0,0,2,0,0,0,3,1,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],#24
                    #[0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#25
                    #[0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],#26
                    #[0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#27
                    #[0,0,1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#28
                    #[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#29
                    #[0,0,1,0,0,0,0,4,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,4],#30
                    #[1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#31
                    #[0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],#32
                    #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2],#33
                    #[0,0,1,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],#34 
                    #[0,0,0,3,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1],#35
                    #[0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#36
                    #[0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0],#37
                    #[0,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],#38
                    #[0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0],#39
                    #[0,0,1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],#40
                    #[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#41
                    #[0,0,1,0,0,0,0,4,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0],#42
                    #[1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,2],#43
                    #[0,0,0,1,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#44
                    #[0,0,0,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,3],#45
                    #[0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0],#46
                    #[0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0],#47
                    #[0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],#48
                    #[0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,3],#49
                    #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],#50
                    #[0,0,1,0,0,1,0,4,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],#51
                    #[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2],#52
                    #[0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],#53
                    #[0,0,0,0,0,0,0,3,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],#54
                    #[0,0,1,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],#55
                    #[0,0,1,0,0,1,0,4,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,1],#56
                    #[0,0,1,0,0,0,0,4,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0],#57
                    #[0,0,1,0,0,0,0,4,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1],#58
                    #[0,0,1,0,1,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],#59
                    #[0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,2],#60
                    #[0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,2],#61
                    #[0,0,0,2,0,0,0,4,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],#62
                    #[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#63
                    #[0,1,0,4,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#64
                    #[0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0],#65
                    #[0,0,0,0,0,0,0,4,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1],#66
                    #[0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],#67
                    #[0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#68
                    #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],#69
                    #[1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,4],#70
                    #[0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],#71
                    #[0,0,0,0,0,0,0,4,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0],#72
                    #[0,0,0,0,1,0,0,4,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],#73
                    #[0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#74
                    #[0,0,0,1,0,0,0,4,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],#75
                    #[0,0,1,0,1,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0],#76
                    #[0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#77
                    #[0,0,1,0,1,0,0,3,0,0,0,3,0,1,0,0,0,0,0,0,0,0,0,0],#78
                    #[0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],#79
                    #[0,0,0,4,0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,1],#80
                    #[0,1,0,0,1,0,0,3,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],#81
                    #[0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],#82
                    #[0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,3],#83
                    #[0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,2],#84
                    #[0,0,1,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,0,0,0,0],#85
                    #[0,0,0,1,0,0,0,4,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0],#86
                    #[0,0,1,0,0,0,0,0,0,0,0,4,0,1,0,1,0,0,0,0,0,0,0,0],#87
                    #[0,0,0,0,0,0,0,4,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0],#88
                    #[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1],#89
                    #[0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#90
                    #[1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0],#91
                    #[0,0,0,1,0,0,0,4,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0],#92
                    #[0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],#93
                    #[0,0,0,1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#94
                    #[0,1,0,0,0,1,0,4,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],#95
                    #[0,0,0,0,0,0,0,4,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],#96
                    #[0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],#97
                    #[0,0,0,0,1,0,0,4,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0],#98
                    #[0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],#99
                    #[0,0,0,0,0,1,0,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],#100
                    [0,0,1,0,0,0,0,4,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0],#101
                    [0,0,1,0,0,0,0,4,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],#102
                    [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#103
                    [0,0,0,0,1,0,0,3,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],#104
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],#105
                    [0,0,1,0,0,0,0,3,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],#106
                    [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0],#107
                    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],#108
                    [0,0,1,0,0,0,0,0,0,3,0,0,1,1,0,0,0,0,0,0,0,0,0,1],#109
                     ])

producao_saidas = np.array([
                    #[0,0,1,0],#1
                    #[1,0,0,0],#2
                    #[0,1,0,0],#3
                    #[0,1,0,0],#4
                    #[0,1,0,0],#5
                    #[0,1,0,0],#6
                    #[0,1,0,0],#7
                    #[0,1,0,0],#8
                    #[0,1,0,0],#9
                    #[0,0,1,0],#10
                    #[0,1,0,0],#11
                    #[0,1,0,0],#12
                    #[0,0,1,0],#13
                    #[0,0,1,0],#14
                    #[0,0,1,0],#15
                    #[0,0,1,0],#16
                    #[0,1,0,0],#17
                    #[0,1,0,0],#18
                    #[0,0,1,0],#19
                    #[1,0,0,0],#20
                    #[1,0,0,0],#21
                    #[0,0,1,0],#22
                    #[0,0,1,0],#23
                    #[0,1,0,0],#24
                    #[0,1,0,0],#25
                    #[0,1,0,0],#26
                    #[0,0,1,0],#27
                    #[0,1,0,0],#28
                    #[0,0,1,0],#29
                    #[0,1,0,0],#30
                    #[0,1,0,0],#31
                    #[1,0,0,0],#32
                    #[0,0,0,1],#33
                    #[0,0,1,0],#34
                    #[0,1,0,0],#35
                    #[0,0,1,0],#36
                    #[1,0,0,0],#37
                    #[1,0,0,0],#38
                    #[0,1,0,0],#39
                    #[0,1,0,0],#40
                    #[0,0,1,0],#41
                    #[1,0,0,0],#42
                    #[0,1,0,0],#43
                    #[0,0,1,0],#44
                    #[0,0,1,0],#45
                    #[0,1,0,0],#46
                    #[0,1,0,0],#47
                    #[0,0,1,0],#48
                    #[0,0,1,0],#49
                    #[1,0,0,0],#50
                    #[0,1,0,0],#51
                    #[0,0,0,1],#52
                    #[1,0,0,0],#53
                    #[0,1,0,0],#54
                    #[1,0,0,0],#55
                    #[1,0,0,0],#56
                    #[1,0,0,0],#57
                    #[0,1,0,0],#58
                    #[1,0,0,0],#59
                    #[1,0,0,0],#60
                   #[0,1,0,0],#61
                   #[0,0,1,0],#62
                   #[0,0,0,1],#63
                   #[0,1,0,0],#64
                   #[0,1,0,0],#65
                   #[0,1,0,0],#66
                   #[1,0,0,0],#67
                   #[0,0,1,0],#68
                   #[0,0,0,1],#69
                   #[0,0,1,0],#70
                   #[1,0,0,0],#71
                   #[1,0,0,0],#72
                   #[1,0,0,0],#73
                   #[0,1,0,0],#74
                   #[0,1,0,0],#75
                   #[0,1,0,0],#76
                   #[0,0,1,0],#77
                   #[1,0,0,0],#78
                   #[0,0,1,0],#79
                   #[0,1,0,0],#80
                   #[1,0,0,0],#81
                   #[0,1,0,0],#82
                   #[0,1,0,0],#83
                   #[0,0,1,0],#84
                   #[1,0,0,0],#85
                   #[0,1,0,0],#86
                   #[0,1,0,0],#87
                   #[1,0,0,0],#88
                   #[0,1,0,0],#89
                   #[0,1,0,0],#90
                   #[0,0,1,0],#91
                   #[0,1,0,0],#92
                   #[0,0,1,0],#93
                   #[0,1,0,0],#94
                   #[0,1,0,0],#95
                   #[0,0,1,0],#96
                   #[1,0,0,0],#97
                   #[1,0,0,0],#98
                   #[1,0,0,0],#99
                   #[0,1,0,0],#100
                   [0,1,0,0],#101
                   [0,0,1,0],#102
                   [0,0,0,1],#103
                   [1,0,0,0],#104
                   [0,0,0,1],#105
                   [0,0,0,1],#106
                   [0,1,0,0],#107
                   [0,0,1,0],#108
                   [1,0,0,0],#109
                   ])
    
    


#testando uma classificação de risco já com os pesos ajustados.    
testecamadaEntrada = np.array(producao_entradas)
testesomaSinapse0 = np.dot(testecamadaEntrada, pesos0)
testecamadaOculta = sigmoid(testesomaSinapse0)
testesomaSinapse1 = np.dot(testecamadaOculta, pesos1)
testecamadaSaida = sigmoid(testesomaSinapse1)
round_off_values = np.around(testecamadaSaida) 




for k in range(9):
    if np.array_equal(round_off_values[k], producao_saidas[k]) == True:
        print("Valor da classificação é: " + str(round_off_values[k]) + "A rede Neural Acertou" + str(k))
        #print("A rede Neural Acertou" + str(k))
        cont_acerto = cont_acerto + 1
    
    
    if np.array_equal(round_off_values[k], producao_saidas[k]) == False:
        print("Valor da classificação é: " + str(round_off_values[k]) + "A rede Neural Errou" + str(k))
        #print("A rede Neural Errou" + str(k))
        cont_erro = cont_erro + 1

print("Quantidade de Acertos" + str(cont_acerto))
print("Quantidade de Erros" + str(cont_erro))


"""
if np.array_equal(round_off_values, cr_vermelho) == True:
    print("A Classificação deste paciente é VERMELHA")
    
if np.array_equal(round_off_values, cr_amarelo) == True:
    print("A Classificação deste paciente é AMARELO")

if np.array_equal(round_off_values, cr_verde) == True:
    print("A Classificação deste paciente é VERDE")
    
if np.array_equal(round_off_values, cr_azul) == True:
    print("A Classificação deste paciente é AZUL")
    
"""
