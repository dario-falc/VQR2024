import os
import json
import networkx as nx
from docplex.mp.model import Model
from utility.functions import sorted_alphanumeric

def init_graph(file_path):
    GENERATION_PARAMETERS = {}

    G = nx.Graph()
    GRAPH_DATA = {}
    GRAPH_DATA["researchers"] = []
    GRAPH_DATA["papers"] = []
    GRAPH_DATA["scored_edges"] = {}

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
            GRAPH_DATA["scored_edges"][(r, p)] = s

    G.add_nodes_from(GRAPH_DATA["researchers"], bipartite = 0)      # bipartite = 0 are the researchers
    G.add_nodes_from(GRAPH_DATA["papers"], bipartite = 1)           # bipartite = 1 are the papers

    for edge, score in GRAPH_DATA["scored_edges"].items():
        G.add_edge(edge[0], edge[1], weight = score)

        
    return G, GRAPH_DATA, GENERATION_PARAMETERS


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
    

def solve_instance(instance_name, G, GRAPH_DATA, GENERATION_PARAMETERS):
    RESULTS = {}
    
    n_r = GENERATION_PARAMETERS["Researcher"]
    n_p = GENERATION_PARAMETERS["Papers"]
    
    ## Modello
    vqr_model = Model(instance_name)
    
    ## Liste di ricercatori e papers
    researchers = ["R" + str(i) for i in range(n_r)]
    papers = ["P" + str(i) for i in range(n_p)]
    
    ## Dizionario con matrice di adiacenza con scores
    scores = GRAPH_DATA["scored_edges"]
    
    ## Variabili
    x = vqr_model.binary_var_dict(G.edges, name="x")
    
    ## Vincoli
    # Ad ogni ricercatore deve essere assegnato almeno 1 paper
    vqr_model.add_constraints((sum(x.get((r, p), 0) for p in papers) >= 1
                               for r in researchers),
                              names = "min_papers_per_researcher")
    
    # Ad ogni ricercatore possono essere assegnati massimo 4 paper
    vqr_model.add_constraints((sum(x.get((r, p), 0) for p in papers) <= 4
                               for r in researchers),
                              names = "max_papers_per_researcher")

    # Ogni paper può essere assegnato massimo ad solo ricercatore
    vqr_model.add_constraints((sum(x.get((r, p), 0) for r in researchers) <= 1
                               for p in papers),
                              names = "max_researchers_per_paper")

    # Il dipartimento deve fornire al più 2.5*n_r paper
    alpha = 2.5 * n_r
    vqr_model.add_constraint((sum(x.get((r, p), 0) for r in researchers for p in papers) == alpha))


    ## Funzione obiettivo
    obj_fn = sum(scores.get((r, p), 0) * x.get((r, p), 0) for r in researchers for p in papers)
    vqr_model.set_objective("max", obj_fn)


    ## Soluzione
    vqr_model.solve()


    # print("INFORMATION:")
    # vqr_model.print_information()    
    
    # print("STATUS:")
    # print(vqr_model.solve_details)
        
    # print("RESULTS:")
    # vqr_model.print_solution()

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


# def main():
#     instance_name = "VQR_50_200_0.30_0_10_4070.dat"
#     file_path = os.path.join("data", instance_name)
#     G, GRAPH_DATA, GENERATION_PARAMETERS = init_graph(file_path)
#     solve_instance(instance_name, G, GRAPH_DATA, GENERATION_PARAMETERS)


def main():
    all_results = {}
    
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    solutions_dir = "solutions"
    if not os.path.exists(solutions_dir):
        os.makedirs(solutions_dir)

    ## Data directory
    data_dir = "data"                       # nuove istanze
    # data_dir = "old_data_converted"       # vecchie istanze
    
    
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
    main()