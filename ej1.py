import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import pandas as pd
from func import *

#%% Importo los datos y creo los grafos

Y2H=ldata('/Users/sofinico/Documents/Exactas/Redes complejas'+
           '/Redes-TP1/tc01_data/yeast_Y2H.txt')

LIT=ldata('/Users/sofinico/Documents/Exactas/Redes complejas'+
           '/Redes-TP1/tc01_data/yeast_LIT.txt')

APMS=ldata('/Users/sofinico/Documents/Exactas/Redes complejas'+
           '/Redes-TP1/tc01_data/yeast_AP-MS.txt')

G_Y2H=nx.Graph(); G_LIT=nx.Graph(); G_APMS=nx.Graph();
G_Y2H.add_edges_from(Y2H); G_LIT.add_edges_from(LIT); G_APMS.add_edges_from(APMS); 

#%% Grafico

f, (ax1,ax2,ax3) = plt.subplots(1,3)

plt.sca(ax1)
nx.draw(G_Y2H, node_size=10)
ax1.set_title('Y2H')

plt.sca(ax2)
nx.draw(G_LIT, node_size=10)
ax2.set_title('LIT')

plt.sca(ax3)
nx.draw(G_APMS, node_size=10)
ax3.set_title('APMS')

f=plt.figure(1)
plt.show()

#%% Calculo valores de la tabla

redes=[G_Y2H,G_LIT,G_APMS]

nodes=[]; edges=[]; kmedio=[]; kmax=[]; kmin=[]; 
clust1=[]; clust2=[]; densidad=[]; diam=[];

pos=0
for red in redes:
    nodes.append(red.number_of_nodes())
    edges.append(red.number_of_edges())
    k=degrees2list(red)
    kmedio.append(np.mean(k))
    kmax.append(max(k))
    kmin.append(min(k))
    densidad.append(edges[pos]/(nodes[pos]*(nodes[pos]-1)/2))
    compgigante=max(nx.connected_component_subgraphs(red),key=len)
    diam.append(nx.diameter(compgigante))
    clust1.append(nx.average_clustering(red))
    clust2.append(nx.transitivity(red))
    pos+=1
    
esdirigida=[False]*3 #Interacción entre proteínas: no dirigido


    
#%% Grafico tabla

caract = pd.DataFrame({ "Red":["Y2H","LIT","APMS"], 
                        "N":nodes,
                        "L":edges,
                        "Dirigida":esdirigida,
                        "<k>":kmedio,
                        "k máx":kmax,
                        "k mín":kmin,
                        "Densidad":densidad,
                        "Clust. <Ci>": clust1,
                        "Clust. global": clust2,
                        "Diametro":[np.inf]*3,
                        "Diam. comp. gigante":diam
                      })
print(caract)

#%%






























