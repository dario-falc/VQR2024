import os
import networkx as nx
from docplex.mp.model import Model
from utility.functions import init_graph, graph_mincostflow_reduction

def solve_instance(instance_name, G, GRAPH_DATA, verbose = False):
    n_r = len(GRAPH_DATA["researchers"])
    n_p = len(GRAPH_DATA["papers"])

    ## Model
    vqr_model_reduction = Model(instance_name)
    
    ## Lists of researchers and papers
    researchers = ["R" + str(i) for i in range(n_r)]
    papers = ["P" + str(i) for i in range(n_p)]
    
    ## Costs
    costs = GRAPH_DATA["edge_costs"]

    ## Scores
    scores = GRAPH_DATA["edge_scores"]

    ## Capacities
    capacities = GRAPH_DATA["node_capacities"]

    ## Variables
    x = vqr_model_reduction.binary_var_dict(G.edges, name="x")

    ## Constraints
    # Flow conservation
    vqr_model_reduction.add_constraints(((sum(x.get((i, j), 0) for j in G.successors(i)) - sum(x.get((k, i), 0) for k in G.predecessors(i)) == capacities.get(i, 0))
                                         for i in G.nodes),
                                        names="flow_conservation")
    
    # for elem in vqr_model_reduction.iter_constraints():
    #     print(elem)

    ## Min Objective function
    # obj_fn = sum(costs.get((r, p), 0) * x.get((r, p), 0) for r in researchers for p in papers)
    # vqr_model_reduction.set_objective("min", obj_fn)

    ## Max Objective function
    obj_fn = sum(scores.get((r, p), 0) * x.get((r, p), 0) for r in researchers for p in papers)
    vqr_model_reduction.set_objective("max", obj_fn)

        
    ## Solution
    vqr_model_reduction.solve()

    if verbose:
        print("INFORMATION:")
        vqr_model_reduction.print_information()    
        
        print("STATUS:")
        print(vqr_model_reduction.solve_details)
            
        print("RESULTS:")
        vqr_model_reduction.print_solution()
    
    
    


def test():
    instance_name = "VQR_50_200_0.30_0_10_4070.dat"
    file_path = os.path.join("data", instance_name)
    G, GRAPH_DATA, GENERATION_PARAMETERS = init_graph(file_path)
    graph_mincostflow_reduction(G, GRAPH_DATA)

    solve_instance(instance_name, G, GRAPH_DATA, verbose = True)


if __name__ == "__main__":
    test()