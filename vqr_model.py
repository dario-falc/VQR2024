from docplex.mp.model import Model
import networkx as nx

def init_graph(file_path):
    GENERATION_PARAMETERS = {}

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

    G.add_nodes_from(GRAPH_DATA["researchers"], bipartite = 0)      # bipartite = 0 are the researchers
    G.add_nodes_from(GRAPH_DATA["papers"], bipartite = 1)           # bipartite = 1 are the papers

    for edge, score in GRAPH_DATA["scored_edges"].items():
        G.add_edge(edge[0], edge[1], weight = score)

        
    return G, GRAPH_DATA, GENERATION_PARAMETERS


def solve_instance(G, GRAPH_DATA, GENERATION_PARAMETERS):
    n_r = GENERATION_PARAMETERS["Researcher"]
    n_p = GENERATION_PARAMETERS["Papers"]
    
    ## Modello
    vqr_model = Model("VQR assignment")
    
    ## Liste di ricercatori e papers
    researchers = ["R" + str(i) for i in range(n_r)]
    papers = ["P" + str(i) for i in range(n_p)]
    
    ## Dizionario con matrice di adiacenza con scores
    scores = GRAPH_DATA["scored_edges"]
    
    ## Variabili
    # x = vqr_model.binary_var_list(G.edges, name="x")
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
                              names="max_researchers_per_paper")

    # Il dipartimento deve fornire al più 2.5*n_r paper
    alpha = 2.5 * n_r
    vqr_model.add_constraint((sum(x.get((r, p), 0) for r in researchers for p in papers) == alpha))


    ## Funzione obiettivo
    obj_fn = sum(scores.get((r, p), 0) * x.get((r, p), 0) for r in researchers for p in papers)
    vqr_model.set_objective("max", obj_fn)

    vqr_model.print_information()
    
    ## Soluzione
    vqr_model.solve()
    
    print("STATUS:")
    print(vqr_model.solve_details)
    
    vqr_model.print_solution()


def main():
    file_path = "data/VQR_50_200_0.30_0_10_4070.dat"
    G, SCORED_EDGES, GENERATION_PARAMETERS = init_graph(file_path)
    
    solve_instance(G, SCORED_EDGES, GENERATION_PARAMETERS)



if __name__ == "__main__":
    main()