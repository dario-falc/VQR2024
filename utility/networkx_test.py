import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import numpy as np

GENERATION_PARAMETERS = {}
file_path = "../data/VQR_50_200_0.30_0_10_4070.dat"

G = nx.Graph()
GRAPH_DATA = {}
GRAPH_DATA["researchers"] = []
GRAPH_DATA["papers"] = []
GRAPH_DATA["scored_edges"] = {}

with open(file_path, "r") as f:
    cur_line=1
    
    # Get data generation parameters (first 10 lines)
    for line in f:
        l = line.strip()
        
        if cur_line <= 10:
            k, v = l.split(": ")
            GENERATION_PARAMETERS[k] = float(v) if k == "RDensity" else int(v)           
            cur_line+=1
            continue
                
        # Split file row into researcher, paper and score
        r, p, s = l.split()
        r = "R" + r
        p = "P" + p
        s = float(s)
        
        GRAPH_DATA["researchers"].append(r) if r not in GRAPH_DATA["researchers"] else None
        GRAPH_DATA["papers"].append(p) if p not in GRAPH_DATA["papers"] else None
        GRAPH_DATA["scored_edges"][(r, p)] = s

print(f"GRAPH_DATA: {GRAPH_DATA}")

G.add_nodes_from(GRAPH_DATA["researchers"], bipartite = 0)      # bipartite = 0 are the researchers
G.add_nodes_from(GRAPH_DATA["papers"], bipartite = 1)           # bipartite = 1 are the papers

for edge, score in GRAPH_DATA["scored_edges"].items():
    G.add_edge(edge[0], edge[1], weight = score)


print(G)
print(nx.is_bipartite(G))
# researchers, papers = bipartite.sets(G)

## Draw graph 
# nx.draw(G, with_labels=True, font_weight='bold')
# plt.show()

