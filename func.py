import networkx as nx

def ldata(archive):
    f=open(archive)
    data=[]
    for line in f:
        line=line.strip()
        col=line.split()
        data.append(col)	
    return data

def directed(lista):
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

def creategraph(lista):
    if directed(lista)==True:
        graph=nx.DiGraph()
    else: 
        graph=nx.Graph()
    graph.add_edges_from(lista)
    return graph
    
        
            
        
        
        
        