import json
from statistics import median

if __name__ == "__main__":
    with open("results.json", "r") as f:
        data = json.load(f)
        
    for file_name, results in data.items():
        for res in data[file_name]:
            print(f"Instance: {file_name}")
            print(f"Time: {round(res['time'], 4)} sec.    ({round(res['deterministic_time'], 4)} ticks)")
            print(f"n_r: {res['n_researchers']}, n_p: {res['n_papers']}, num_var: {res['num_var']}")
            print()
        