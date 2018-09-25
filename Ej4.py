# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 00:26:20 2018

@author: noelp
"""

import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from scipy import optimize
from func4 import *
#%%

## Load data

netscience = nx.read_gml('c:/users/noelp/Documents/Git'+
           '/Redes-TP1/tc01_data/netscience.gml')
july = nx.read_gml('c:/users/noelp/Documents/Git'+
           '/Redes-TP1/tc01_data/as-22july06.gml')

#%%




knn_net, k_net = nearest_nei(netscience)
knn_july, k_july = nearest_nei(july)


k_netlog = np.log(k_net)
knn_netlog = np.log(knn_net)

# Función con la que queremos hacer el fit
fitfunc = lambda p,x: p[0]*x+p[1]
powerlaw = lambda x, C, a: C*(x**a)

def powerlaw_fit(Xdata,Ydata, p0 = [-2,2]):
        
    # Datos que se van a fittear
    x = np.log10(np.array(Xdata))
    y = np.log10(np.array(Ydata))
    
    # Distancia a la función objetivo
    errfunc = lambda p,x,y: fitfunc(p,x)-y 
    
    # Ajuste con scipy
    out = optimize.leastsq(errfunc, p0, args=(x,y), full_output = 1)
    p = out[0]; covar = out[1]

    # Parámetros de la power-law
    C = 10.0**p[1]
    a = p[0]
    a_err = np.sqrt(covar[0][0])
    
    return C, a, a_err

C_net, a_net, a_err_net = powerlaw_fit(k_net[:9], knn_net[:9], p0 = [-2,2])
C_july, a_july, a_err_july = powerlaw_fit(k_july[1:], knn_july[1:], p0 = [-2,2])

ejex_net = np.linspace(k_net[0],k_net[-1],num=50)
ejex_july = np.linspace(k_july[0],k_july[-1],num=50)

plt.figure(1)
plt.title(r'Netscience: $\gamma= %5.2f \pm %5.2f$' %(-a_net, a_err_net),loc='right',fontsize=10)
plt.loglog(k_net[8],knn_net[8],marker='d',color='c',markersize=7,label=r'$K_{min}$')
plt.loglog(k_net,knn_net,'.',markersize=7,label='Log Scale')
plt.loglog(ejex_net,powerlaw(ejex_net,C_net,a_net),'k--',linewidth=1,label='Ajuste')
plt.legend()
plt.show(1)

plt.figure(2)
plt.title(r'$July: \gamma= %5.2f \pm %5.2f$' %(-a_july, a_err_july),loc='right',fontsize=10)
plt.loglog(k_july[1],knn_july[1],marker='d',color='c',markersize=7,label=r'$K_{min}$')
plt.loglog(k_july,knn_july,'.',markersize=7,label='Log Scale')
plt.loglog(ejex_july,powerlaw(ejex_july,C_july,a_july),'k--',linewidth=1,label='Ajuste')
plt.legend()
plt.show(2)

#%%

bins = np.logspace(np.log10(min(knn_net)), np.log10(max(knn_net)+1), 20)
freq, binedges = np.histogram(knn_net, bins=bins)
norm = sum(freq)
freq_normed = [i/norm for i in freq]
bincenters = 0.5*(binedges[1:]+binedges[:-1])
lins = {'linestyle': 'None'}


plt.figure(3)
plt.rc('lines', **lins)
plt.bar(bincenters,freq_normed, color='orange',edgecolor='black', linewidth=1.2, width = np.diff(binedges))
plt.grid(True)
plt.xlabel('Knn' )
plt.title('Netscience')
plt.show(3)

#%%

bins = np.logspace(0, np.log10(max(knn_july)+1), 60)
freq, binedges = np.histogram(knn_july, bins=bins)
norm = sum(freq)
freq_normed = [i/norm for i in freq]
bincenters = 0.5*(binedges[1:]+binedges[:-1])


plt.figure(3)
plt.plot(bincenters,freq_normed,'.', color='k')
plt.grid(linestyle=':')
plt.xlabel('Knn' )
plt.title('July')
plt.show(3)

