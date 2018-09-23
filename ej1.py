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

def draw_GraphStyle(G):
    nx.draw(G,
            node_size=3, 
            node_color='dodgerblue',
            edge_color='grey'
            )

f, (ax1,ax2,ax3) = plt.subplots(1,3)

plt.sca(ax1)
draw_GraphStyle(G_Y2H)
ax1.set_title('Y2H')

plt.sca(ax2)
draw_GraphStyle(G_LIT)
ax2.set_title('LIT')

plt.sca(ax3)
draw_GraphStyle(G_APMS)
ax3.set_title('APMS')

f=plt.figure(1)
plt.show()

#%% Calculo valores de la tabla

redes=[G_Y2H,G_LIT,G_APMS]

nodes=[]; edges=[]; kmedio=[]; kmax=[]; kmin=[]; 
clustl=[]; clustg=[]; densidad=[]; diam=[];

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
    clustl.append(nx.average_clustering(red))
    clustg.append(nx.transitivity(red))
    pos+=1
    
esdirigida=[False]*3 #Interacción entre proteínas: no dirigido


    
#%% Grafico tabla

caract = pd.DataFrame({ 'red':['Y2H','LIT','APMS'], 
                        'N':nodes,
                        'L':edges,
                        'k_medio':kmedio,
                        'k_max':kmax,
                        'k_min':kmin,
                        'densidad':densidad,
                        'c_local':clustl,
                        'c_global':clustg,
                        'diam_CG':diam
                      })

caract = caract[['red','N','L','k_medio',
                 'k_max','k_min','densidad','c_local',
                 'c_global','diam_CG']]

#Uso cols para copiar y pegar y hacer más rapido la redefinición de lugares
cols=list(caract.columns.values)

print(caract)

#%% Agrego algunos atributos relacionados a los componentes

for red in redes:
    red.graph["comp"]=list(nx.connected_component_subgraphs(red))
    compgigante=max(red.graph["comp"],key=len)
    red.graph["comp"].remove(compgigante)
    nCG=compgigante.number_of_nodes()
    eCG=compgigante.number_of_edges()
    red.graph["dens_CG"]=eCG/(nCG*(nCG-1)/2)
    clustl_comp=[]; clustg_comp=[]; 
    kmedio_comp=[]; dens_comp=[];
    for comp in red.graph["comp"]:
        clustl_comp.append(nx.average_clustering(comp))
        clustg_comp.append(nx.transitivity(comp))
        kcomp=degrees2list(comp)
        kmedio_comp.append(np.mean(kcomp))
        n=comp.number_of_nodes()
        e=comp.number_of_edges()
        if n!=1:
            dens_comp.append(e/(n*(n-1)/2))
        else:
            dens_comp.append(0)
    red.graph["c_local_comp"]=clustl_comp
    red.graph["c_global_comp"]=clustg_comp
    red.graph["k_medio_comp"]=kmedio_comp
    red.graph["densidad_comp"]=dens_comp
    red.graph["c_local_CG"]=nx.average_clustering(compgigante)
    red.graph["c_global_CG"]=nx.transitivity(compgigante)
    

#%% Tablita comparativa sobre los componentes de cada grafo
    
n_comps=[]; n_clustl1=[]; n_clustg1=[]; prom_cl=[]; prom_cg=[];
clustl_CG=[]; clustg_CG=[]; prom_kmedio_comps=[]; prom_dens_comp=[];
dens_cg=[];

for red in redes:
    n_comps.append(len(red.graph["comp"]))
    clustl_comp=red.graph["c_local_comp"]
    clustg_comp=red.graph["c_global_comp"]
    prom_cl.append(np.mean(clustl_comp))
    prom_cg.append(np.mean(clustg_comp))
    n_clustl1.append(sum([int(i==1) for i in clustl_comp]))
    n_clustg1.append(sum([int(i==1) for i in clustg_comp]))
    clustl_CG.append(red.graph["c_local_CG"])
    clustg_CG.append(red.graph["c_global_CG"])
    prom_kmedio_comps.append(np.mean(red.graph["k_medio_comp"]))
    prom_dens_comp.append(np.mean(red.graph["densidad_comp"]))
    dens_cg.append(red.graph["dens_CG"])
    
    
caract2 = pd.DataFrame({ "red":["Y2H","LIT","APMS"],
                         "n_comps":n_comps,
                         "prom_c_local_comp":prom_cl,
                         "prom_c_global_comp":prom_cg,
                         "c_local_CG":clustl_CG,
                         "c_global_CG":clustg_CG,
                         "n_c_local_1":n_clustl1,
                         "n_c_global_1":n_clustg1,
                         "prom_dens_comp":prom_dens_comp,
                         "dens_CG":dens_cg,
                         "prom_kmedio_comps":prom_kmedio_comps
                         })
    
caract2=caract2[['red','n_comps','prom_c_local_comp','prom_c_global_comp',
                 'n_c_local_1','n_c_global_1','c_local_CG','c_global_CG',
                 'prom_kmedio_comps','prom_dens_comp','dens_CG']]
    
print(caract2)






























