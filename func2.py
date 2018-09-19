# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 15:01:36 2018

@author: noelp
"""
import numpy as np
import networkx as nx
from scipy.optimize import curve_fit
from itertools import chain


def ldata(archive):
    f=open(archive)
    data=[]
    for line in f:
        line=line.strip()
        col=line.split()
        data.append(col)	
    return data

### Cuantificación de homofilia
    
## Devuelve  la fracción que representan las parejas heterosexuales
## respecto al total
def straight(graph):
    edges = list(dict(graph.edges))
    hetero = [ edges[n] if graph.nodes[edges[n][0]] != graph.nodes[edges[n][1]] 
    else '' for n in range(graph.number_of_edges())]
    hetero = list(set(list(hetero)))[1:]
    return len(hetero)


##Reasigna un atributo aleatoriamente manteniendo la proporción
## original de dicho atributo
def bend(graph, attribute, name_attribute='gender'):
    np.random.shuffle(attribute)
    for n,g in zip(graph.nodes,attribute):
        graph.nodes[n][name_attribute] = g               
    return graph 


### Calcula el pval para un cierto estadístico observado
def pval(freq,bines,Tobs):
    bineslef = bines[:-1]
    cumprob = [sum(freq[0:i+1]) for i in range(len(freq))]
    i = 1
    if bineslef[0] >= Tobs:
        return 1
    elif bineslef[-1] < Tobs:
        return 1 - cumprob[-1]
    else:
        while bineslef[i] < Tobs:
            if i < len(bineslef)-1:
                i+=1
            else:
                break
        return 1 - cumprob[i-1] 

