# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 12:43:28 2018

@author: noelp
"""
import numpy as np
import networkx as nx


def degrees(grafo, node = 'All'):
    if node == 'All':
        lista=list(dict(grafo.degree).values())
    else:
        lista= grafo.degree(node)
    return lista

def knn(graph):
    knn = list(nx.k_nearest_neighbors(graph).values())
    k = list(nx.k_nearest_neighbors(graph).keys())
    return knn, k

def nearest_nei(graph):
    k_vecinos = []                      #Grado medio de los vecinos para un k
    k = []                              #Grados de los nodos
    deg = 1                             #Grado de los nodos que recorro
    while deg <= max(degrees(graph, node='All')):
        
        mismo_k = 0                     #Grado medio acumulado para un k
        m = 0                           #Número de nodos con ese k
        
        for n in list(graph.nodes()):
            
            if degrees(graph, node=n) == deg:
                deg_n = 0               #Grado medio acumulado para un nodo
                ed = list(graph.neighbors(n))  #Lista de vecinos de un nodo
                
                for i in ed:
                    deg_n += degrees(graph, node=i)
                    
                deg_n =deg_n/deg        #Valor medio del grado para un nodo
                mismo_k += deg_n        #Suma ese valor medio al grado acumulado para un k
                m+=1                    #Cuenta el nodo como perteneciente a cierto k
                
        #Recorre la lista de nodos, si hay nodos con ese grado, los appendea.
        if m != 0:
            k_vecinos.append(mismo_k/m)
            k.append(deg)           #Guardo el grado de los nodos
                
        #Cambia de grado
        deg += 1
    return k_vecinos, k

def powerlaw_fit(Xdata,Ydata, p0 = [-2,2]):
    
    fitfunc = lambda p,x: p[0]*x+p[1]
    powerlaw = lambda x, C, a: C*(x**a)    
    
    # Datos que se van a fittear
    x = np.log10(np.array(Xdata))
    y = np.log10(np.array(Ydata))
    
    # Distancia a la función objetivo
    errfunc = lambda p,x,y: fitfunc(p,x)-y 
    
    # Ajuste con scipy
    out = optimize.leastsq(errfunc, p0, args=(x,y), full_output = 1)
    p = out[0]; covar = out[1]

    # Parámetros de la power-law
    C = 10.0**p[1]
    a = p[0]
    a_err = np.sqrt(covar[0][0])
    
    return C, a, a_err


def asort_Newman(graph):
    S1 = np.sum([ degrees(graph, node='All') ])
    S2 = np.sum([i**2 for i in degrees(graph, node='All')])
    S3 = np.sum([i**3 for i in degrees(graph, node='All')])
    Se = 0
    for n in list(graph.nodes()):
        kn = degrees(graph,node=n)
        ed = list(graph.neighbors(n))
        deg_ed = np.sum([degrees(graph, node=i)*kn for i in ed])
        Se += deg_ed
    Se = Se/2
    r = (S1*Se-S2**2)/(S1*S3-S2**2)
    return r
        
        
        
        

