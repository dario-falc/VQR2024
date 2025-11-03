from docplex.mp.model import Model

def main():
    # Modello
    opt_mod = Model(name = "Linear Program")

    # Variabili
    x = opt_mod.continuous_var(name="x", lb=0)
    y = opt_mod.continuous_var(name="y", lb=0)

    # Vincoli
    c1 = opt_mod.add_constraint(x+y>=8, ctname="c1")
    c2 = opt_mod.add_constraint(2*x+y>=10, ctname="c2")
    c3 = opt_mod.add_constraint(x+4*y>=11, ctname="c3")

    # Funzione obiettivo
    obj_fn = 5*x + 4*y
    opt_mod.set_objective("min", obj_fn)

    opt_mod.print_information()

    # Soluzione
    opt_mod.solve()
    opt_mod.print_solution()


if __name__ == "__main__":
    main()