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

G_Y2H=creategraph(Y2H); G_LIT=creategraph(LIT); G_APMS=creategraph(APMS); 

#%% Grafico

f, (ax1,ax2,ax3) = plt.subplots(1,3)

plt.sca(ax1)
nx.draw(G_Y2H, node_size=10,arrowstyle='-|>',width=0.5,arrowsize=3)
ax1.set_title('Y2H')

plt.sca(ax2)
nx.draw(G_LIT, node_size=10)
ax2.set_title('LIT')

plt.sca(ax3)
nx.draw(G_APMS, node_size=10)
ax3.set_title('APMS')

f=plt.figure(1)
plt.show()

#%%

nodes=[G_Y2H.number_of_nodes(),G_LIT.number_of_nodes(),G_APMS.number_of_nodes()]
edges=[G_Y2H.number_of_edges(),G_LIT.number_of_edges(),G_APMS.number_of_edges()]

caract = pd.DataFrame({ "Red":["Y2H","LIT","APMS"], 
                        "N":nodes,
                        "L":edges
                      })
print(caract)






























