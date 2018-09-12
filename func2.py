# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 15:01:36 2018

@author: noelp
"""
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import chain


def ldata(archive):
    f=open(archive)
    data=[]
    for line in f:
        line=line.strip()
        col=line.split()
        data.append(col)	
    return data


#%%

### Cuantificación de homofilia
    
## Devuelve una lista de las parejas heteros y la fracción que representan
## respecto al total
def straight(graph):
    edges = list(dict(graph.edges))
    hetero = [ edges[n] if graph.nodes[edges[n][0]] == graph.nodes[edges[n][1]] 
    else '' for n in range(graph.number_of_edges())]
    hetero = list(set(list(chain(*hetero))))
    return hetero, len(hetero)

## Toma las parejas heteros y les cambia el sexo aleatoriamente
def bend(graph):
    hetero, len_hetero = straight(graph)   
    for n in hetero:
        if np.random.rand() <0.5:
            if graph.node[n]['gender'] == 'f':
                graph.node[n]['gender'] = 'm'
            else:
                graph.node[n]['gender'] = 'f'               
    return graph    

### Calcula el pval para un cierto estadístico observaado
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