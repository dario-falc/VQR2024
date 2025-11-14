import os
from utility.functions import sorted_alphanumeric

def change_format(file_path, instance_name):
    GRAPH_DATA = {}
    full_string = ""
    
    with open(file_path, "r") as f:    
        seed_line = f.readline().strip("\n")
        
        for line in f:
            l = line.strip("\n")
            full_string += l
    
    instance_data = full_string.split(";")
    
    GRAPH_DATA["Seed"] = seed_line.split(": ")[1]
    GRAPH_DATA["Researcher"] = instance_data[0].split("= ")[1]
    GRAPH_DATA["Papers"] = instance_data[1].split("= ")[1]
    GRAPH_DATA["Edges"] = None
    GRAPH_DATA["RDensity"] = None
    GRAPH_DATA["minScore"] = 0
    GRAPH_DATA["maxScore"] = 10
    GRAPH_DATA["maxResearcherForPaper"] = None
    GRAPH_DATA["maxPaperForResearcher"] = None
    GRAPH_DATA["ToAssign"] = instance_data[2].split("= ")[1]
    
    
    # Edge cleaning
    edges = instance_data[3]
    from_idx = edges.find("{")
    to_idx = edges.find("}")
    edges = edges[from_idx+1:to_idx].strip(" ").split(", ")
    
    
    # Score cleaning
    scores = instance_data[4]
    from_idx = scores.find("[")
    to_idx = scores.find("]")
    scores = scores[from_idx+1:to_idx].strip(" ").split(", ")

    GRAPH_DATA["Edges"] = len(edges)


    # Create new dir
    if not os.path.exists("./old_data_converted"):
        os.makedirs("./old_data_converted")

    new_file_name = "new_" + instance_name
    new_file_path = os.path.join("old_data_converted", new_file_name)

    # Write to file
    with open(new_file_path, "a") as f:
        f.write(f"Seed: {GRAPH_DATA['Seed']}\n")
        f.write(f"Researcher: {GRAPH_DATA['Researcher']}\n")
        f.write(f"Papers: {GRAPH_DATA['Papers']}\n")
        f.write(f"Edges: {GRAPH_DATA['Edges']}\n")
        f.write(f"RDensity: {GRAPH_DATA['RDensity']}\n")
        f.write(f"minScore: {GRAPH_DATA['minScore']}\n")
        f.write(f"maxScore: {GRAPH_DATA['maxScore']}\n")
        f.write(f"maxResearcherForPaper: {GRAPH_DATA['maxResearcherForPaper']}\n")
        f.write(f"maxPaperForResearcher: {GRAPH_DATA['maxPaperForResearcher']}\n")
        f.write(f"ToAssign: {GRAPH_DATA['ToAssign']}\n")

        for edge, score in zip(edges, scores):
            r, p = edge.strip().strip("<").strip(">").split(",")
            # Sottraggo 1 agli ID dei ricercatori e dei paper per seguire il formato delle nuove istanze
            f.write(f"{int(r)-1} {int(p)-1} {score}\n")

if __name__ == "__main__":    
    problem_instances = sorted_alphanumeric(os.listdir("old_data"))
    for instance_name in problem_instances:
        print(f"Converting instance: {instance_name}")
        file_path = os.path.join("old_data", instance_name)
    
        change_format(file_path, instance_name)