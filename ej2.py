# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 17:54:10 2018

@author: noelp
"""

import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import chain
from func2 import *


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



times = 10000
fraccion = []
fraccion_medida = straight(dolphins)/dolphins.number_of_edges()


for n in range(times):
    dolphins = bend(dolphins, gender, name_attribute='gender')
    fraccion.append(straight(dolphins)/dolphins.number_of_edges())
    


freq, binedges = np.histogram(fraccion, bins=20)
norm = sum(freq)
freq_normed = [i/norm for i in freq]
bincenters = 0.5*(binedges[1:]+binedges[:-1])
lins = {'linestyle': 'None'}

mean = np.mean(fraccion)
stdev = np.std(fraccion)
### El p-val corresponde a la probabilidad de obtener un resultado mayor o igual al obtenido
p_val = pval(freq_normed, binedges, fraccion_medida)

plt.rc('lines', **lins)
plt.axvline(x=fraccion_medida, color='k', linestyle='dashed', linewidth=1)
plt.bar(bincenters,freq_normed, color='orange',edgecolor='black', linewidth=1.2, width = np.diff(binedges))
plt.grid(True)
plt.ylabel('Frecuencia')
plt.xlabel('Fracción de parejas heteronormativas.' )
plt.title('Fracción medida %s. p-val %s. Media de la distribución: %s ±% s ' 
%(round(fraccion_medida,2),round(p_val,2),round(mean,2 ),round(stdev,2) ))
plt.show()



