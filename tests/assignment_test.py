from docplex.mp.model import Model
import numpy as np

def main():
    # Costi
    cost = np.random.randint(1, 10, (4, 4))

    # Modello
    assignment_model = Model(name="Assignment")
    
    # Variabili
    x = assignment_model.binary_var_matrix(cost.shape[0],
                                           cost.shape[1],
                                           name="x")

    # Vincoli
    assignment_model.add_constraints((sum(x[i, j] for i in range(cost.shape[0])) <= 1
                                      for j in range(cost.shape[1])),
                                     names="work_load")
    assignment_model.add_constraints((sum(x[i, j] for j in range(cost.shape[1])) == 1
                                      for i in range(cost.shape[0])),
                                     names="task_completion")
    
    # Funzione obiettivo
    obj_fn = sum(cost[i, j]*x[i, j] for i in range(cost.shape[0]) for j in range(cost.shape[1]))
    assignment_model.set_objective("min", obj_fn)

    assignment_model.print_information()
    # print(assignment_model.export_as_lp_string())
    
    # Soluzione
    assignment_model.solve()
    assignment_model.print_solution()

    print("="*60)
    
    ## Rilassamento del vincolo di interezza
    # Modello
    assignment_model2 = Model(name="Assignment2")
    
    # Variabili
    y = assignment_model2.continuous_var_matrix(cost.shape[0],
                                                cost.shape[1],
                                                lb=0, ub=1,
                                                name="y")

    # Vincoli
    assignment_model2.add_constraints((sum(y[i, j] for i in range(cost.shape[0])) <= 1
                                      for j in range(cost.shape[1])),
                                     names="work_load")
    assignment_model2.add_constraints((sum(y[i, j] for j in range(cost.shape[1])) == 1
                                      for i in range(cost.shape[0])),
                                     names="task_completion")
    
    # Funzione obiettivo
    obj_fn = sum(cost[i, j]*y[i, j] for i in range(cost.shape[0]) for j in range(cost.shape[1]))
    assignment_model2.set_objective("min", obj_fn)

    assignment_model2.print_information()
    # print(assignment_model2.export_as_lp_string())
    
    # Soluzione
    assignment_model2.solve()
    assignment_model2.print_solution()
    
    

if __name__ == "__main__":
    main()