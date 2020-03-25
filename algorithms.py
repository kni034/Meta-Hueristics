import readfile

def random_search(solution):
    best_solution = solution

    for _ in range(10000):
        current = readfile.gen_random_solution()

        if not readfile.check_feasibility(current): continue

        if readfile.objective_function(best_solution) > readfile.objective_function(current):
            best_solution = current
    
    return best_solution