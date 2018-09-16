# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 17:54:10 2018

@author: noelp
"""

import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import chain


#%%

## Load data

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
nx.draw_shell(dolphins, 
        with_labels=True,
        node_color= ['blue' if g=="m" else "r" for g in nx.get_node_attributes(dolphins, "gender").values()] , 
        node_size=10, nlist=[range(5,10), range(5)])
#%%



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




