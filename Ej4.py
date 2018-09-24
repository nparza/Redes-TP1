# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 00:26:20 2018

@author: noelp
"""

import numpy as np
import networkx as nx

#%%

## Load data

netscience = nx.read_gml('c:/users/noelp/Documents/Git'+
           '/Redes-TP1/tc01_data/netscience.gml')
july = nx.read_gml('c:/users/noelp/Documents/Git'+
           '/Redes-TP1/tc01_data/as-22july06.gml')

#%%


degree = list(dict(netscience.degree).values())
k_vecinos = []
for n in netscience.nodes():
    for k in range(len(netscience.edges(nbunch= n ))):
        