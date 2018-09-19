import networkx as nx
from matplotlib import pyplot as plt
from func import *
import numpy as np

#%% Asignaciones 

sa=nx.read_gml("TC01_data/as-22july06.gml")
listk=degrees2list(sa)
kmax=max(listk)
N=sa.number_of_nodes()

#%% Distribución de grado. Binneado lineal

K=dict()

for i in set(listk):
    K[i]=0

for k in listk:
    K[k]+=1

k=K.keys()    
pk=np.array(list(K.values()))/N

f, (ax1,ax2) = plt.subplots(1,2)

def applyPlotStyle():
    plt.xlabel('k',weight='bold',fontsize=11)
    plt.ylabel(r'p$_k$',weight='bold',fontsize=11)
    plt.grid(linestyle=':')

plt.sca(ax1)
plt.title('Linear Scale, Linear Binning',loc='left',fontsize=10)
plt.plot(k,pk,'.',markersize=3) 
applyPlotStyle()

plt.sca(ax2)
plt.title('Log-Log Scale, Linear Binning',fontsize=10)
plt.loglog(k,pk,'.',markersize=3)
applyPlotStyle()

plt.subplots_adjust(wspace=0.4)

#%% Distribución de grado acumulada

cum=[]
for i in range(len(pk)):
    cum.append(sum(list(K.values())[i:len(pk)]))
    
#plt.loglog(k,pk,'.',color='0.9')
plt.loglog(k,cum,'.')
plt.loglog(cum,'.')
applyPlotStyle()

plt.show()

#%% Binneado logaritmico

n=14
bins=np.logspace(0,np.log10(kmax+1),n)
h,bins=np.histogram(listk,bins)

centros=[]
for i in range(len(bins)-1):
    c=(bins[i]+bins[i+1])/2
    centros.append(c)

A=[]
for i in range(len(h)):
    A.append(h[i]/(bins[i+1]-bins[i]))
pk_log=A/sum(A)

plt.loglog(k,pk,'.',color='0.9')
plt.loglog(centros,pk_log,'.')
applyPlotStyle()
plt.show()

#%% Grafico comparativo linear/log scale

f, (ax1,ax2) = plt.subplots(1,2)

plt.sca(ax1)
plt.title('Linear Scale, Log Binning',loc='left',fontsize=10)
plt.plot(k,pk,'.',color='0.9')
plt.plot(centros,pk_log,'.')
applyPlotStyle()

plt.sca(ax2)
plt.title('Log-Log Scale, Log Binning',loc='left',fontsize=10)
plt.loglog(k,pk,'.',color='0.9')
plt.loglog(centros,pk_log,'.')
applyPlotStyle()

plt.subplots_adjust(wspace=0.4)

#%%   

#%% Binneado lineal

nbins=kmax
bins=np.linspace(min(listk),kmax,abs(nbins))

#Calculo los centros de los binnes
centros=[]
for i in range(len(bins)-1):
    c=(bins[i]+bins[i+1])/2
    centros.append(c)

#Armo el histograma. Tiene que pasar bins2==bins p c elemento.
h,bins2=np.histogram(listk,bins); pk=h/N;

#Ploteo función de distribución
plt.loglog(centros,pk,'.')

#Ploteo función de distribución acumulada
Pk=[]
for i in range(len(h)):
    Pk.append(sum(h[i:len(h)])/N)

plt.loglog(centros,Pk,'.',label='Cumulative')
plt.legend()


plt.ylabel(r'p$_k$',fontsize=10)
plt.xlabel('k')  
plt.title('Linear Binning',loc='left')
plt.show()   

  


