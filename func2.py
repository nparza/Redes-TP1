# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 15:01:36 2018

@author: noelp
"""
import numpy as np
import networkx as nx
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
    

def straight(graph,):
    
    ## Devuelve  la fracción que representan las parejas heterosexuales
    ## respecto al total
    
    edges = list(dict(graph.edges))
    hetero = 0
    for n in range(graph.number_of_edges()):
        if graph.nodes[edges[n][0]] != graph.nodes[edges[n][1]]:
            hetero += 1
        else:
            hetero += 0
    return hetero



def grupo(graph,attribute='gender', kind='f'):
    
    ## Te da una lista de los nodos con un cierto atributo 
    
    nodes = list(dict(graph.nodes))
    group = []
    for n in nodes:
        if graph.nodes[n][attribute] == kind:
            group.append(n)
    return group


def subgraph(graph,attribute='gender', kind='f'):
    
    ## Te da una lista de los edges que comparten un atributo
    
    edges = list(dict(graph.edges))
    subgraph = []
    for n in range(graph.number_of_edges()):
        if graph.nodes[edges[n][0]] == graph.nodes[edges[n][1]] and graph.nodes[edges[n][0]]['gender'] == kind :
            subgraph.append(edges[n])
    return subgraph
    
def modularidad(graph, attribute='gender'):
    
    #### Calcula la modularidad de la red
    
    q = 0
    m = (2*graph.number_of_edges())
    for i in range(graph.number_of_nodes()):
        for j in range(graph.number_of_nodes()):
            
            ni = list(dict(graph.nodes()))[i]
            nj = list(dict(graph.nodes()))[j]
            
            if graph.nodes[ni][attribute] == graph.nodes[nj][attribute]:
                ki = graph.degree()[ni]
                kj = graph.degree()[nj]
                aij = nx.adjacency_matrix(graph)[i,j]

                qij = aij - ki*kj/m
            else:
                qij = 0
            q += qij
            
    return q/m
 
    
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
    

## ANDA, PERO NO CALCULA LO QUE QUIERO
# Cunado reasigno los edges, no contemplo que se me pueden armar pares repetidos
# o loops

def recableado(graph):
    
    ## Reasigna los enlaces manteniendo la distribución de grado de cada nodo
    
    half_edges = []
    for n in list(graph.nodes()):
        half_edges.extend([n]*graph.degree()[n])
    
    np.random.shuffle(half_edges)
    
    new_edges = []
    for i in range(0,len(half_edges)-1,2):
        new_edges.append([half_edges[i],half_edges[i+1]])

    # Arreglo posibles loops
#    while i<len(new_edges):
#        if new_edges[i][0] == new_edges[i][1]:
#            # Separo en dos casos por si el último edge es un loop
#            if i == len(new_edges)-1:
#                np.random.shuffle(new_edges)
#                i = -1
#            else:
#                nodo = new_edges[i][0] 
#                new_edges[i][0] = new_edges[i+1][0]
#                new_edges[i+1][0] = nodo
#                i -= 1  
#        i += 1
#    
    # Creo el grafo recableado
    new_graph = nx.Graph()
    new_graph.add_edges_from(new_edges)
    
    #Recupero los géneros del grafo original
    for n in list(graph.nodes()):
        new_graph.nodes[n]['gender'] = graph.nodes[n]['gender']
    
    return new_graph
    
    
            
            
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

