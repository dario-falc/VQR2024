import os
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from utility.functions import init_graph

def graph_mincostflow_reduction(G, GRAPH_DATA):    
    n_r = len(GRAPH_DATA["researchers"])
    n_p = len(GRAPH_DATA["papers"])
    
    ## Add source node and sink node
    G.add_node("s", subset = 0)
    G.add_node("t", subset = 3)
    
    # ## Add dummy nodes
    # GRAPH_DATA["dummies"] = []
    # n_dummies = 4*n_r - n_p
    # for i in range(n_dummies):
    #     GRAPH_DATA["dummies"].append(f"D{i}")
    #     G.add_node(f"D{i}", subset = 2)
    
    # ## Add edges from each researcher node to each dummy node
    # for r in GRAPH_DATA["researchers"]:
    #     for d in GRAPH_DATA["dummies"]:
    #         G.add_edge(r, d)
    
    GRAPH_DATA["edge_costs"] = {}
    ## Add edges from source to researchers and from papers to sink
    for r, p in zip(GRAPH_DATA["researchers"], GRAPH_DATA["papers"]):
        G.add_edge("s", r)#, cost = 0)
        GRAPH_DATA["edge_costs"][("s", r)] = 0
        G.add_edge(p, "t")#, cost = 0)
        GRAPH_DATA["edge_costs"][(p, "t")] = 0
        
    ## Add node capacities
    GRAPH_DATA["node_capacities"] = {}
    # Source node
    GRAPH_DATA["node_capacities"]["s"] = 2.5 * n_r

    # Researcher nodes
    for r in GRAPH_DATA["researchers"]:
        GRAPH_DATA["node_capacities"][r] = 4
    
    # Paper nodes
    for p in GRAPH_DATA["papers"]:
        GRAPH_DATA["node_capacities"][p] = 1
    
    # Sink node
    GRAPH_DATA["node_capacities"]["t"] = 2.5 * n_r
    
    
    ## Convert scores into costs for min-cost flow
    max_score = max(GRAPH_DATA["edge_scores"].values())

    for edge, score in GRAPH_DATA["edge_scores"].items():
        cost = max_score - score
        GRAPH_DATA["edge_costs"][edge] = cost
        # print(f"maxV: {max_score}, score: {GRAPH_DATA['edge_scores'][edge]}, cost: {GRAPH_DATA['edge_costs'][edge]}")        
    

def main():
    instance_name = "VQR_50_200_0.30_0_10_4070.dat"
    file_path = os.path.join("data", instance_name)
    G, GRAPH_DATA, GENERATION_PARAMETERS = init_graph(file_path)

    graph_mincostflow_reduction(G, GRAPH_DATA)

    ## Draw graph
    # nx.draw_networkx(
    #     G,
    #     pos = nx.drawing.layout.multipartite_layout(G), 
    #     with_labels = True)
    # plt.show()


if __name__ == "__main__":
    main()
