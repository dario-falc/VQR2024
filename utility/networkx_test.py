import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

GENERATION_PARAMETERS = {}
file_path = "data/VQR_50_200_0.30_0_10_4070.dat"
G = nx.Graph()

with open(file_path, "r") as f:
    cur_line=1
    
    # Get data generation parameters (first 10 lines)
    for line in f:
        l = line.strip()
        
        if cur_line <= 10:
            k, v = l.split(": ")
            GENERATION_PARAMETERS[k] = float(v)            
            cur_line+=1
            continue
        
        # Start papers count from #researchers+1 so node names don't overlap between the two subsets
        n_r = GENERATION_PARAMETERS["Researcher"]
        
        # Split file row into researcher, paper and score
        r, p, s = l.split()
        # r = int(r)
        p = str(int(int(p) + n_r + 1))
        s = float(s)
        
        
        ## Add nodes r and p, and edge (r, p) with score s
        # bipartite = 0 indicates that the node belongs to the researchers set
        # bipartite = 1 indicates that the node belongs to the papers set
        G.add_node(r, bipartite = 0)
        G.add_node(p, bipartite = 1)        
        G.add_edge(r, p, weight = s)
        # print(f"{cur_line} - Adding edge ({r}, {p}) with score {s}")
        # cur_line+=1
        

print(G)
# print(nx.is_bipartite(G))
# researchers, papers = bipartite.sets(G)



## Draw graph 
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

