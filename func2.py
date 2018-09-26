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
    
    q = 0; qmax = 0
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
                qmaxij = ki*kj
            else:
                qij = 0
                qmaxij = 0
            
            q += qij
            qmax += qmaxij
            
    return q/m, 1-qmax/(m*m)

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
    

       
def switch(edge1,edge2):
    
    ## Switchea los primeros nodos de los los enlaces
    ## Devuelve los dos enlaces intercambiados
    
    nodo = edge1[0]
    edge1[0] = edge2[0]
    edge2[0] = nodo 
    return edge1, edge2

## NO ANDAAA!!!

def recableado(graph):
    
    ## Reasigna los enlaces manteniendo la distribución de grado de cada nodo
    
    half_edges = []
    for n in list(graph.nodes()):
        half_edges.extend([n]*graph.degree()[n])
    
    np.random.shuffle(half_edges)
    
    new_edges = []
    for i in range(0,len(half_edges)-1,2):
        new_edges.append([half_edges[i],half_edges[i+1]])
     
    # Extraigo los self loops y los guardo en una lista
    self_loops = []
    for edge in new_edges:
        if edge[0] == edge[1]:
            new_edges.remove(edge)
            self_loops.append(edge)
    
    # Extraigo los que se repiten más de una vez y los guardo
    repeated = []
    for i in range(len(new_edges)-1):
        for edge in new_edges[i+1:]:
            if new_edges[i][0] in edge and new_edges[i][1] in edge:
                new_edges.remove(edge)
                repeated.append(edge)
    
    for loop in self_loops:
        
        no_go = True
        while no_go:
        
            # Elijo un edge al azar para switchear con mi loop edge
            no_go2 = True
            while no_go2:
                index = np.random.choice(range(0,len(new_edges)))
                if new_edges[index][0] != loop[0] and new_edges[index][1] != loop[0]:
                    edge_elegido = new_edges[index]
                    new_edges.pop(index)
                    no_go2 = False
            
            # Switcheo los edges y me fijo que no se repitan en new_edges  
            edge1, edge2 = switch(loop,edge_elegido)
            if edge1 not in new_edges and edge2 not in new_edges:
                new_edges.append(edge1)
                new_edges.append(edge2)
                no_go = False
            else: new_edges.append(edge_elegido)
            
    for repe in repeated:
        
        no_go = True
        while no_go:
            
            # Elijo un edge al azar para switchear con mi repe edge
            no_go2 = True
            while no_go2:
                index = np.random.choice(range(0,len(new_edges)))
                if set(repe) != set(new_edges[index]):
                    edge_elegido = new_edges[index]
                    new_edges.pop(index)
                    no_go2 = False
            
            # Switcheo los edges y me fijo que no se repitan en new_edges 
            # y que tampoco sean self_loop
            edge1, edge2 = switch(repe,edge_elegido)
            
            self_loop = False
            if edge1[0] == edge1[1] or edge2[0] == edge2[1]:
                self_loop = True
            #no_repeated = edge1 not in new_edges and edge2 not in new_edges
            is_repeated = False
            if edge1 in new_edges or edge2 in new_edges:
                is_repeated = True

            if self_loop == False and is_repeated == False:
                new_edges.append(edge1)
                new_edges.append(edge2)
                no_go = False
            else: new_edges.append(edge_elegido)
          
    
    
    
    
    # Creo el grafo recableado
    new_graph = nx.Graph()
    new_graph.add_edges_from(new_edges)
    
    #Recupero los géneros del grafo original
    for n in list(graph.nodes()):
        new_graph.nodes[n]['gender'] = graph.nodes[n]['gender']
    
    return new_graph
    
    
            
            
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

