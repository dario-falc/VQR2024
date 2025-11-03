from docplex.mp.model import Model

def main():
    # Model
    milp_model = Model(name="MILP")

    # Variabili
    x = milp_model.binary_var(name="x")
    y = milp_model.continuous_var(name="y")
    z = milp_model.integer_var(name="z")

    # Vincoli
    c1 = milp_model.add_constraint(x+2*y+z<=4, ctname="c1")
    c2 = milp_model.add_constraint(2*z+y<=5, ctname="c2")
    c3 = milp_model.add_constraint(x+y>=1, ctname="c3")
    
    # Funzione obiettivo
    obj_fn = 2*x+y+3*z
    milp_model.set_objective("max", obj_fn)
    milp_model.print_information()
    
    # Soluzione
    milp_model.solve()
    milp_model.print_solution()
    
if __name__ == "__main__":
    main()