import networkx as nx

def ldata(archive):
    f=open(archive)
    data=[]
    for line in f:
        line=line.strip()
        col=line.split()
        data.append(col)	
    return data

def repeated_edge(lista):
    i=0
    isdirected=False
    while i<len(lista) and isdirected==False:
        par=lista[i]
        j=i+1
        while j<len(lista) and isdirected==False:
            if par[0] in lista[j] and par[1] in lista[j]:
                isdirected=True
            j+=1
        i+=1
    return isdirected

def degrees2list(grafo):
    lista=list(dict(grafo.degree).values())
    return lista

        
            
        
        
        
        