import os
import json
import math
import networkx as nx
from docplex.mp.model import Model
from utility.functions import sorted_alphanumeric, init_graph, solution_to_txt


def solve_instance(instance_name, G, GRAPH_DATA, verbose = False):
    RESULTS = {}
    
    # n_r = GENERATION_PARAMETERS["Researcher"]
    # n_p = GENERATION_PARAMETERS["Papers"]
    n_r = len(GRAPH_DATA["researchers"])
    n_p = len(GRAPH_DATA["papers"])
    
    ## Model
    vqr_model = Model(instance_name)
    
    ## Lists of researchers and papers
    researchers = ["R" + str(i) for i in range(n_r)]
    papers = ["P" + str(i) for i in range(n_p)]
    
    ## Scores
    scores = GRAPH_DATA["edge_scores"]
    
    ## Variables
    x = vqr_model.binary_var_dict(G.edges, name="x")
    
    ## Constraints
    # Minimum number of papers per researcher
    vqr_model.add_constraints((sum(x.get((r, p), 0) for p in papers) >= 1
                               for r in researchers),
                              names = "min_papers_per_researcher")
    
    # Maximum number of papers per researcher
    vqr_model.add_constraints((sum(x.get((r, p), 0) for p in papers) <= 4
                               for r in researchers),
                              names = "max_papers_per_researcher")

    # Maximum number of researchers per paper
    vqr_model.add_constraints((sum(x.get((r, p), 0) for r in researchers) <= 1
                               for p in papers),
                              names = "max_researchers_per_paper")

    # Required number of assignments
    alpha = math.floor(2.5 * n_r)
    vqr_model.add_constraint((sum(x.get((r, p), 0) for r in researchers for p in papers) == alpha))


    ## Objective function
    obj_fn = sum(scores.get((r, p), 0) * x.get((r, p), 0) for r in researchers for p in papers)
    vqr_model.set_objective("max", obj_fn)


    ## Solution
    vqr_model.solve()

    if verbose:
        print("INFORMATION:")
        vqr_model.print_information()    
        
        print("STATUS:")
        print(vqr_model.solve_details)
            
        print("RESULTS:")
        vqr_model.print_solution()

    # solution_variables = ""
    solution_variables = []
    for v in vqr_model.iter_binary_vars():
        if v.solution_value > 0.9:
            # solution_variables += v.name + ", " 
            solution_variables.append(v.name) 


    # RESULTS["graph"] = G
    RESULTS["n_researchers"] = n_r
    RESULTS["n_papers"] = n_p
    RESULTS["num_var"] = vqr_model.number_of_variables
    RESULTS["status"] = vqr_model.solve_details.status
    RESULTS["time"] = vqr_model.solve_details.time                                  # wall clock time (in seconds)
    RESULTS["deterministic_time"] = vqr_model.solve_details.deterministic_time      # CPU time (in ticks)
    RESULTS["objective_value"] = vqr_model.objective_value

    return RESULTS, solution_variables


def test():
    instance_name = "VQR_50_200_0.30_0_10_4070.dat"
    file_path = os.path.join("data", instance_name)
    G, GRAPH_DATA, GENERATION_PARAMETERS = init_graph(file_path)
    solve_instance(instance_name, G, GRAPH_DATA, verbose = True)


def main():
    all_results = {}
    
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    solutions_dir = "solutions"
    if not os.path.exists(solutions_dir):
        os.makedirs(solutions_dir)

    ## Data directory
    data_dir = "data"                       # new instances
    # data_dir = "old_data_converted"       # old instances
    
    
    problem_instances = sorted_alphanumeric(os.listdir(data_dir))
    for instance_name in problem_instances:
        print(f"Evaluating instance: {instance_name}")
        file_path = os.path.join(data_dir, instance_name)
        
        G, GRAPH_DATA, GENERATION_PARAMETERS = init_graph(file_path)
        
        all_results[instance_name], solution_variables = solve_instance(instance_name, G, GRAPH_DATA, GENERATION_PARAMETERS)
    
        with open(os.path.join(results_dir, data_dir + "_results.json"), "w") as f:
            json.dump(all_results, f, indent=3, separators=(',', ': '))

        solution_to_txt(data_dir, solutions_dir, instance_name, solution_variables)



if __name__ == "__main__":
    # main()
    test()