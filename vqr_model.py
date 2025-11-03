from docplex.mp.model import Model
import networkx as nx
import numpy as np

def init_graph(file_path):
    GENERATION_PARAMETERS = {}
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

            p = str(int(int(p) + n_r + 1))
            s = float(s)            
            
            ## Add nodes r and p, and edge (r, p) with score s
            # bipartite = 0 indicates that the node belongs to the researchers set
            # bipartite = 1 indicates that the node belongs to the papers set
            G.add_node(r, bipartite = 0)
            G.add_node(p, bipartite = 1)        
            G.add_edge(r, p, weight = s)
            
    return G, GENERATION_PARAMETERS


def main():
    file_path = "data/VQR_50_200_0.30_0_10_4070.dat"
    G, GENERATION_PARAMETERS = init_graph(file_path)
    
    n_r = GENERATION_PARAMETERS["Researcher"]
    n_p = GENERATION_PARAMETERS["Papers"]
    
    ## Modello
    vqr_model = Model("VQR assignment")
    
    ## Variabili
    x = vqr_model.binary_var_matrix(n_r,
                                    n_p,
                                    name="x")

    ## Vincoli
    # Ad ogni soggetto deve essere assegnato almeno 1 prodotto
    vqr_model.add_constraints((sum(x[i,j] for i in range(n_p)) >= 1
                               for j in range(n_r)),
                              names="min_papers_per_researcher")

    # Ad ogni soggetto possono essere assegnati massimo 4 prodotti
    vqr_model.add_constraints((sum(x[i,j] for i in range(n_p)) <= 4
                               for j in range(n_r)),
                              names="max_papers_per_researcher")

    # Ogni prodotto può essere assegnato massimo ad solo soggetto
    vqr_model.add_constraints((sum(x[i,j] for j in range(n_r)) <= 1
                               for i in range(n_p)),
                              names="max_researchers_per_paper")

    # Il dipartimento deve fornire al più 2.5*n_r paper
    alpha = 2.5 * n_r
    vqr_model.add_constraint((sum(x[i,j] for i in range(n_p) for j in range(n_r)) == alpha))


    ## Funzione obiettivo
    obj_fn = sum(s[i,j] * x[i,j] for i in range(n_p) for j in range(n_r))
    vqr_model.set_objective("max", obj_fn)

    vqr_model.print_information()
    
    ## Soluzione
    vqr_model.solve()
    
    print("STATUS:")
    print(vqr_model.solve_details)
    
    vqr_model.print_solution()

if __name__ == "__main__":
    main()