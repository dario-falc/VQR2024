import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

# Create example graph
G = nx.Graph()


## Draw simple graph
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()


### Draw bipartite graph (per immagini tesi)
## METODO 1
# nx.draw_networkx(
#     G,
#     pos = nx.drawing.layout.bipartite_layout(G, researchers), 
#     with_labels = True)
# plt.show()


## METODO 2
# pos = dict()
# researchers, papers = bipartite.sets(G)
# pos.update( (n, (1, i)) for i, n in enumerate(researchers) ) # put nodes from X at x=1
# pos.update( (n, (2, i)) for i, n in enumerate(papers) ) # put nodes from Y at x=2
# nx.draw(G, pos=pos, with_labels=True)
# plt.show()
