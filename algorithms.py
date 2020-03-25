import readfile
import random
from collections import defaultdict

def opt2(solution):
    best = solution
    call_to_change = random.choice(solution)
    if call == 0:
        call_to_change = random.choice(solution)

    call_index = defaultdict(list)
    for i, call in solution:
        if call != 0:
            call_index[call].append(i)
    
    for i in solution:
        temp = list(solution)
        temp[call_index[i][0]] =call_index[call_to_change][0]
        temp[call_index[i][1]] = call_index[call_to_change][1]



def opt3(solution):
    best = solution
    for i, call1 in enumerate(solution):
        for j,call2 in enumerate(solution):
            for k,call3 in enumerate(solution):
                temp = list(solution)
                temp[i] = call3
                temp[j] = call1
                temp[k] = call2

                #print("i: ", i, " j: ",j ," k: ",k, " temp: ",temp, " best: ", best)

                if readfile.check_feasibility(temp):
                    if readfile.objective_function(best) > readfile.objective_function(temp):
                        best = temp

    return best


def insert1(solution):
    best = solution
    for i in solution:
        for j in solution:
            temp = list(solution)
            elem = temp.pop(i)
            temp.insert(j, elem)

            if readfile.check_feasibility(temp):
                if readfile.objective_function(best) > readfile.objective_function(temp):
                    best = temp
    return best


def random_search(solution):
    best_solution = solution

    for _ in range(10000):
        current = readfile.gen_random_solution()

        if not readfile.check_feasibility(current): continue

        if readfile.objective_function(best_solution) > readfile.objective_function(current):
            best_solution = current
    
    return best_solution


def local_search(solution):
    #p of using opt2
    p1 = 0.33
    #p of using opt3
    p2 = 0.33
    #p of using insert1
    p3 = (1-p1 - p2)
    
    best = solution
    for _ in range(10000):
        rand = random.random()
        if rand >= 0 and rand <= p1:
            temp = opt2(solution)
        if rand > p1 and rand <= p2:
            temp = opt3(solution)
        else:
            temp = insert1(solution)
        
        if readfile.check_feasibility(temp):
            if readfile.objective_function(best) > readfile.objective_function(temp):
                best = temp
    
    return best