import networkx as nx
from matplotlib import pyplot as plt
from func import *

#%%

sa=nx.read_gml("TC01_data/as-22july06.gml")
listk=degrees2list(sa)
N=sa.number_of_nodes()

#Tiene del orden de 23k nodos

#%% Esto por el momento no es muy util, ir a la otra celda
import numpy as np

#Creo un dict K cuyos keys sean grados y los values la cantidad de nodos con ese grado

K=dict()

for i in range(min(listk),max(listk)+1):
    K[i]=0

"""Si no, se puede hacer 
for i in set(listk): 
    K[i]=0
y de esa manera no tengo keys vacías."""

for k in listk:
    K[k]+=1


#%%

nbins=np.sqrt(N)
bins=np.logspace(0,4.38,nbins)

centros=[]
for i in range(len(bins)-1):
    c=(bins[i]+bins[i+1])/2
    centros.append(c)

h=np.histogram(listk,bins)
plt.loglog(centros,h[0],'.')
plt.show()

    


