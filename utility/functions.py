import re
import os
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)


def solution_to_txt(data_dir, solutions_dir, instance_name, solution_variables):
    assignments = {}
    pairs = []
    for v in solution_variables:
        r, p = v[2:].split("_")
        pairs.append((r, p))

    for r, p in pairs:
        if r not in assignments:
            assignments[r] = []
        assignments[r].append(p)


    with open(os.path.join(solutions_dir, data_dir + "_solutions.txt"), "a") as f:
        f.write(instance_name + "\n")
        
        for r, p in assignments.items():
            f.write(f"{r}: {', '.join(p)}\n")
        f.write("\n")


def draw_simple_graph(G):
    ## Draw graph
    nx.draw_networkx(
        G,
        pos = nx.drawing.draw(G, with_labels=True), 
        with_labels = True)
    plt.show()


def draw_bipratite_graph(G):
    researchers, papers = bipartite.sets(G)

    ## Draw graph
    nx.draw_networkx(
        G,
        pos = nx.drawing.layout.bipartite_layout(G, researchers), 
        with_labels = True)
    plt.show()


def draw_multipartite_graph(G):
    ## Draw graph
    nx.draw_networkx(
        G,
        pos = nx.drawing.layout.multipartite_layout(G), 
        with_labels = True)
    plt.show()


def init_graph(file_path):
    GENERATION_PARAMETERS = {}

    G = nx.DiGraph()
    GRAPH_DATA = {}
    GRAPH_DATA["researchers"] = []
    GRAPH_DATA["papers"] = []
    GRAPH_DATA["edge_scores"] = {}

    cur_line=1
    with open(file_path, "r") as f:
        
        # Get data generation parameters (first 10 lines)
        for line in f:
            l = line.strip()
            
            if cur_line <= 10:
                k, v = l.split(": ")
                if v == "None":
                    GENERATION_PARAMETERS[k] = None
                
                else:
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
            GRAPH_DATA["edge_scores"][(r, p)] = s

            cur_line += 1
            ##### ELIMINARE #####
            # if cur_line > 30:
            #     break
            #####################

    G.add_nodes_from(GRAPH_DATA["researchers"], subset = 1)     # subset = 1 are the researchers
    G.add_nodes_from(GRAPH_DATA["papers"], subset = 2)          # subset = 2 are the papers

    for edge, score in GRAPH_DATA["edge_scores"].items():
        G.add_edge(edge[0], edge[1])#, score = score)
        
    return G, GRAPH_DATA, GENERATION_PARAMETERS


def graph_mincostflow_reduction(G, GRAPH_DATA):
    n_r = len(GRAPH_DATA["researchers"])
    n_p = len(GRAPH_DATA["papers"])
    

    ## Add source node and sink node
    G.add_node("s", subset = 0)
    G.add_node("t", subset = 3)
    
        
    ## Separate researcher slots
    for r in GRAPH_DATA["researchers"][:]:
        for i in range(1, 4):
            r_i = r + "'"*i
            
            G.add_node(r_i, subset = 1)
            GRAPH_DATA["researchers"].append(r_i)

            ## Connect each slot to the same papers the original researcher is connected to
            for succ in G.successors(r):
                G.add_edge(r_i, succ)
                
                ## Edge (ri, succ) gets the same score as edge (r, p)
                GRAPH_DATA["edge_scores"][(r_i, succ)] = GRAPH_DATA["edge_scores"][(r, succ)]

    ## Duplicate paper nodes for yes/no assignments
    # for p in GRAPH_DATA["papers"][:]:
    #     p_star = p + "*"
        
    #     G.add_node(p_star, subset = 2)
    #     GRAPH_DATA["papers"].append(p_star)
        
    #     ## Connect each duplicate to the same researchers the original paper is connected to
    #     for pred in G.predecessors(p):
    #         G.add_edge(pred, p_star)
            
    #         ## Edge (pred, p) gets the same score as edge (r, p)
    #         GRAPH_DATA["edge_scores"][(pred, p_star)] = GRAPH_DATA["edge_scores"][(pred, p)]



    ## Add dummy nodes
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
        GRAPH_DATA["node_capacities"][r] = 0
    
    # Paper nodes
    for p in GRAPH_DATA["papers"]:
        GRAPH_DATA["node_capacities"][p] = 0
    
    # Sink node
    GRAPH_DATA["node_capacities"]["t"] = -2.5 * n_r
    
    
    ## Convert scores into costs for min-cost flow
    max_score = max(GRAPH_DATA["edge_scores"].values())

    for edge, score in GRAPH_DATA["edge_scores"].items():
        cost = max_score - score
        GRAPH_DATA["edge_costs"][edge] = cost
        # print(f"maxV: {max_score}, score: {GRAPH_DATA['edge_scores'][edge]}, cost: {GRAPH_DATA['edge_costs'][edge]}")

    # draw_multipartite_graph(G)
    # print(GRAPH_DATA)
