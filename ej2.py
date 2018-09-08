# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 17:54:10 2018

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


dolphins = nx.read_gml('c:/users/noelp/Documents/Git'+
           '/Redes-TP1/tc01_data/dolphins.gml')
gender = ldata('c:/users/noelp/Documents/Git'+
           '/Redes-TP1/tc01_data/dolphinsGender.txt')
gender = [gender[n][1] for n in range(len(gender))]

for n,g in zip(dolphins.nodes,gender):
    dolphins.nodes[n]["gender"] = g

#%%

### Layout

nx.draw(dolphins, 
        with_labels=True,
        node_color= ['blue' if g=="m" else "r" for g in nx.get_node_attributes(dolphins, "gender").values()] , 
        node_size=10)


#%%

def straight(graph):
    edges = list(dict(graph.edges))
    hetero = [ edges[n] if graph.nodes[edges[n][0]] == graph.nodes[edges[n][1]] 
    else '' for n in range(graph.number_of_edges())]
    hetero = list(set(list(chain(*hetero))))
    return hetero, len(hetero)


def bend(graph):
    hetero, len_hetero = straight(graph)   
    for n in hetero:
        if np.random.rand() <0.5:
            if graph.node[n]['gender'] == 'f':
                graph.node[n]['gender'] = 'm'
            else:
                graph.node[n]['gender'] = 'f'               
    return graph    

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

times = 5000
fraccion = []
fraccion_medida = straight(dolphins)[1]/dolphins.number_of_nodes()


for n in range(times):
    dolphins = bend(dolphins)
    fraccion.append(straight(dolphins)[1]/dolphins.number_of_nodes())
    

freq, binedges = np.histogram(fraccion, bins=20)
norm = sum(freq)
freq_normed = [i/norm for i in freq]
bincenters = 0.5*(binedges[1:]+binedges[:-1])
pval = pval(freq_normed, binedges, fraccion_medida)
lins = {'linestyle': 'None'}

plt.rc('lines', **lins)
plt.bar(bincenters,freq_normed, color='orange',edgecolor='black', linewidth=1.2, width = np.diff(binedges))
plt.grid(True)
plt.ylabel('Frecuencia')
plt.xlabel('Fracción de parejas heteronormativas. Valor medido %s. p-val %s' %(round(fraccion_medida,2),round(pval,2) ))
plt.show()





