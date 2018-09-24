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

k=list(K.keys())    
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
plt.title('Log-Log Scale, Linear Binning',fontsize=10,loc='left')
plt.loglog(k,pk,'.',markersize=3)
applyPlotStyle()

plt.subplots_adjust(wspace=0.4)

#%% Cumulative distribution function

# Calculada usando el método del ranking

sortedk=sorted(listk,reverse=True)
ranking=list(range(1,len(sortedk)+1))

frac=[ranking[i]/N for i in range(len(ranking))]

d=dict()
Pk=[]

for i in k:
    d[i]=[]
for i in range(len(sortedk)):
    d[sortedk[i]].append(ranking[i])
for i in k:
    Pk.append(np.mean(d[i])/N)
    
plt.title('Log-Log Scale, Cumulative',loc='left',fontsize=10)
plt.loglog(sortedk,frac,'.',color='0.9')
plt.loglog(k,np.array(Pk),'.')
applyPlotStyle()
plt.ylabel(r'P$_k$')

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


#%% Estimación exponente de grado con fitteo lineal
from scipy import optimize
    
#Función con la que queremos hacer el fit
fitfunc=lambda p,x: p[0]*x+p[1]

#Parametros iniciales para fitear
p0=[-2,2] 

#Distancia a la función objetivo
errfunc=lambda p,x,y: fitfunc(p,x)-y 

centros1=centros[4:]
pk_log1=pk_log[4:]
x=np.log10(np.array(centros1))
y=np.log10(np.array(pk_log1))

out=optimize.leastsq(errfunc, p0, args=(x,y),full_output=1)
p1=out[0]
covar=out[1]

#Grafico para chequear el fitteo
plt.figure(34)
plt.plot(x, y, "ro", x, fitfunc(p1, x), "k-", linewidth=3)

powerlaw=lambda x, C, a: C*(x**a)
C=10.0**p1[1]
a=p1[0]

print(p1)
print(covar)

a_err = np.sqrt(covar[0][0])

plt.figure(50)
plt.loglog(k,pk,'.',color='0.9')
plt.loglog(centros[4],pk_log[4],marker='d',color='c')
plt.loglog(centros,pk_log,'.')

plt.title(r'$\gamma= %5.2f \pm %5.2f$' %(-a, a_err),loc='right')

abcisa=np.logspace(0,np.log10(kmax+1))
plt.loglog(abcisa,powerlaw(abcisa,C,a),'k:',linewidth=1)
applyPlotStyle()
plt.show()

#%% Estimación exponente de grado con cumulative

k1=k[14:]
Pk1=Pk[14:]
x=np.log10(np.array(k1))
y=np.log10(np.array(Pk1))

out2=optimize.leastsq(errfunc, p0, args=(x,y),full_output=1)
p2=out2[0]
covar2=out2[1]

#Grafico para chequear el fitteo
plt.figure(34)
plt.plot(x, y, "ro", x, fitfunc(p2, x), "k-", linewidth=3)

powerlaw=lambda x, C, a: C*(x**a)
C=10.0**p2[1]
a=p2[0]

print(p2)
print(covar2)

a_err = np.sqrt(covar2[0][0])

plt.figure(50)
plt.loglog(sortedk,frac,'.',color='0.9',markersize=4)
plt.loglog(k[14],Pk[14],marker='d',color='c',markersize=4)
plt.loglog(k,Pk,'.',markersize=4)

plt.title(r'$\gamma= %5.2f \pm %5.2f$' %(-a+1, a_err),loc='right')

abcisa=np.logspace(0,np.log10(kmax+1))
plt.loglog(abcisa,powerlaw(abcisa,C,a),'k--',linewidth=1)
applyPlotStyle()
plt.ylabel(r'P$_k$')
plt.show()


#%% EXPONENTE DE GRADO - FORMA DIFICIL - NO ANDA BIEN

def gamma(listk,N,kmin):
    while N==len(listk):
        suma=0
        for ki in listk:
            suma+=np.log(ki/(kmin-(1/2)))
        return 1+len(listk)/suma
    print('len(k) != N')

def powerlaw(k,gamma,kmin):
    k=np.array(k)
    C=(gamma-1)*kmin**(gamma-1)
    return C*k**(-gamma)

def cumulative(k,gamma,kmin):
    k=np.array(k)
    f1=kmin**(gamma-1)
    f2=k**(-gamma+1)
    return 1-f1*f2


plt.figure(10)
g1=gamma(listk,N,kmin=1)
plt.loglog(k,cumulative(k,g1,kmin=1),'.',label=r'k$_{min}$=1',color='0.8')

g2=gamma(listk,N,kmin=2)
plt.loglog(k,cumulative(k,g2,kmin=2),'.',label=r'k$_{min}$=2',color='0.5')

plt.loglog(k,1-np.array(Pk),'.',label='Data')

plt.legend()
plt.grid(linestyle=':')

plt.figure(11)
plt.loglog(k,pk,'.',color='0.9')
plt.loglog(centros,pk_log,'.')
x=np.linspace(min(k),max(k))
plt.loglog(x,powerlaw(x,g1,kmin=1))
applyPlotStyle()
plt.show()


