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

#%% Calculo valores de la tabla

nodes=[G_Y2H.number_of_nodes(),G_LIT.number_of_nodes(),G_APMS.number_of_nodes()]
edges=[G_Y2H.number_of_edges(),G_LIT.number_of_edges(),G_APMS.number_of_edges()]
esdirigida=[directed(Y2H),directed(LIT),directed(APMS)]
grado_medio=[np.mean(list(dict(G_Y2H.degree).values())), 
             np.mean(list(dict(G_LIT.degree).values())),
             np.mean(list(dict(G_APMS.degree).values()))]
gradoin=[np.mean(list(dict(G_Y2H.in_degree).values())), 
         np.mean(list(dict(G_LIT.in_degree).values())),
         np.NaN]
gradoout=[np.mean(list(dict(G_Y2H.out_degree).values())), 
         np.mean(list(dict(G_LIT.out_degree).values())),
         np.NaN]
gradomax=[max(list(dict(G_Y2H.degree).values())), 
          max(list(dict(G_LIT.degree).values())),
          max(list(dict(G_APMS.degree).values()))]
gradomin=[min(list(dict(G_Y2H.degree).values())), 
          min(list(dict(G_LIT.degree).values())),
          min(list(dict(G_APMS.degree).values()))]
densidad=[]
for i in range(3):
    densidad.append(edges[i]/(nodes[i]*(nodes[i]-1)/2))
densidad[2]=densidad[2]*2

    


#%% Grafico tabla

caract = pd.DataFrame({ "Red":["Y2H","LIT","APMS"], 
                        "N":nodes,
                        "L":edges,
                        "Es dirigida":esdirigida,
                        "<k>":grado_medio,
                        "<k in>":gradoin,
                        "<k out>":gradoout,
                        "k máx":gradomax,
                        "k mín":gradomin,
                        "Densidad":densidad
                      })
print(caract)






























