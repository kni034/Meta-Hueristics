import readfile
import random
from collections import defaultdict
from math import e
from statistics import mean


def switch(solution, call1, call2):
    temp = list(solution)
    for i,elem in enumerate(temp):
        if elem == call1:
            temp[i]=call2
        if elem == call2:
            temp[i] = call1
    
    return temp


def opt2(solution):
    best = list(solution)
    ex1 = random.choice(solution)
    while ex1 == 0: ex1 = random.choice(solution)

    ex2 = random.choice(solution)
    while ex2 == 0 or ex2 == ex1: ex2 = random.choice(solution)
    
    temp = switch(solution, ex1, ex2)

    if readfile.check_feasibility(temp):
        best = temp
    return best



def opt3(solution):
    best = list(solution)
    ex1 = random.choice(solution)
    while ex1 == 0: ex1 = random.choice(solution)

    ex2 = random.choice(solution)
    while ex2 == 0 or ex2 == ex1: ex2 = random.choice(solution)

    ex3 = random.choice(solution)
    while ex3 == 0 or ex3 == ex2 or ex3 == ex1: ex3 = random.choice(solution)

    order = [ex1,ex2,ex3]
    random.shuffle(order)

    temp = switch(solution, order[0], order[1])
    temp = switch(temp, order[1], order[2])

    if readfile.check_feasibility(temp):
        best = temp

    return best

def car_poss(solution, car_id):
    current_car_num = 1
    possitions = []
    for i,elem in enumerate(solution):
        if current_car_num == car_id:
            possitions.append(i)
        if elem == 0:
            current_car_num += 1
    
    return possitions



def insert1(solution):
    best = list(solution)
    ex1 = random.choice(solution)
    while ex1 == 0: ex1 = random.choice(solution)

    temp = list(solution)

    temp = [x for x in temp if x != ex1]

    car = random.choice(range(1, readfile.num_vehicles + 1))
    cars_possition = car_poss(temp, car)

    temp.insert(random.choice(cars_possition), ex1)
    cars_possition = car_poss(temp, car)
    temp.insert(random.choice(cars_possition), ex1)

    if readfile.check_feasibility(temp):
        best = temp

    return best


def random_search(solution):
    best_solution = solution
    iteration = 0

    for i in range(10000):
        current = readfile.gen_random_solution()

        if not readfile.check_feasibility(current): continue

        if readfile.objective_function(best_solution) > readfile.objective_function(current):
            best_solution = current
            iteration = i
    
    print("iteration: ", iteration)
    return best_solution


def local_search(solution):
    #p of using opt2
    p1 = 0.33
    #p of using opt3
    p2 = 0.33
    iteration = 0

    best = list(solution)
    for i in range(10000):
        rand = random.random()
        if rand >= 0 and rand <= p1:
            temp = opt2(best)
        elif rand > p1 and rand <= p2 + p1:
            temp = opt3(best)
        else:
            temp = insert1(best)

        #print("temp: ", temp, " feasible?: ", readfile.check_feasibility(temp), " temp score: ", readfile.objective_function(temp), "best: ", best)
        
        if readfile.check_feasibility(temp):
            if readfile.objective_function(best) > readfile.objective_function(temp):
                best = temp
                iteration = i

    print("iteration: ", iteration)
    return best


def simulated_annealing(solution):
    #p of using opt2
    p1 = 0.33
    #p of using opt3
    p2 = 0.33

    print("SimAnn")

    init_temperature = 25
    temperature = init_temperature
    cooling = 0.998
    incumbent = list(solution)
    best = list(solution)

    for _ in range(10000):
        rand = random.random()
        rand2 = random.random()
        if rand >= 0 and rand <= p1:
            temp = opt2(incumbent)
        elif rand > p1 and rand <= p2 + p1:
            temp = opt3(incumbent)
        else:
            temp = insert1(incumbent)

        deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

        p_change = e * (-deltaE / temperature)


        if readfile.check_feasibility(temp):
            if deltaE < 0:
                incumbent = temp
                if readfile.objective_function(incumbent) < readfile.objective_function(best):
                    best = list(incumbent)
            
            elif rand2 < p_change:
                incumbent = temp
        temperature *= cooling
    
    return best


#--------------------------------------------------------------------------------------
#new operators and simulated annealing
def insert1_new(solution):
    new = readfile.gen_dummy_solution()
    calls_list = []
    calls_list.extend(range(1, readfile.num_calls+1))
    
    ex1 = random.choices(calls_list, weights=readfile.weighted_calls(solution), k=1)

    ex11 = ex1[0]
    ex1 = ex11

    temp = list(solution)

    temp = [x for x in temp if x != ex1]
    done = False
    i=0
    while not done:
        i+=1

        temp2 = list(temp)
        call_to_cars_results = readfile.call_to_cars(ex1)
        #car = random.choice(readfile.call_to_cars(ex1))
        car_weights = readfile.weighted_cars(solution)
        usable_cars = []
        usable_cars_weights = []
        for j in range(len(car_weights)):
            if j + 1 in call_to_cars_results:
                usable_cars.append(j + 1)
                usable_cars_weights.append(car_weights[j])

        car = random.choices(usable_cars, weights=usable_cars_weights, k=1)
        car1 = car[0]
        car = car1

        cars_possition = car_poss(temp2, car)
        temp2.insert(random.choice(cars_possition), ex1)

        cars_possition = car_poss(temp2, car)
        temp2.insert(random.choice(cars_possition), ex1)

        if readfile.check_feasibility(temp2):
            new = list(temp2)
            done = True

        if i > 6:
            done = True
            new = list(solution)

    return new

def opt3_new(solution):
    new = readfile.gen_dummy_solution()
    calls_list = []
    calls_list.extend(range(1, readfile.num_calls+1))

    i=0
    done = False
    while not done:

        ex = random.choices(calls_list, weights=readfile.weighted_calls(solution), k=3)

        ex1 = ex[0]
        ex2 = ex[1]
        ex3 = ex[2]

        order = [ex1,ex2,ex3]
        random.shuffle(order)

        temp = switch(list(solution), order[0], order[1])
        temp = switch(temp, order[1], order[2])

        if readfile.check_feasibility(temp):
            new = list(temp)
            done = True
        if i > 6:
            new = list(solution)
            done = True

    return new

def opt2_new(solution):
    new = readfile.gen_dummy_solution()
    calls_list = []
    calls_list.extend(range(1, readfile.num_calls+1))
    
    i=0
    done = False
    while not done:
        ex = random.choices(calls_list, weights=readfile.weighted_calls(solution), k=2)

        ex1 = ex[0]
        ex2 = ex[1]

        temp = switch(solution, ex1, ex2)

        if readfile.check_feasibility(temp):
            new = list(temp)
            done = True
        
        if i > 10:
            new = list(solution)
            done = True

    return new


def move1(solution):
    new = readfile.gen_dummy_solution()
    

    car = random.choice(range(readfile.num_vehicles - 1)) + 1
    if len(car_poss(solution,car)) <= 2:
        return solution

    for _ in range(6):
        temp = list(solution)
        car_positions = car_poss(temp, car)
        ex1 = temp.pop(random.choice(car_positions))
        new_car_positions = car_poss(temp, car)
        temp.insert(random.choice(new_car_positions), ex1)

        if temp == solution:
            continue

        if readfile.check_feasibility(temp):
            new = temp
    
    return new



def simulated_annealing_new(solution):
    #p of using opt2
    p1 = 0.25
    #p of using opt3
    p2 = 0.25
    #p of using insert
    p3 = 0.25

    print("SimAnn NEW")

    positive_deltas = []
    init_temperature = int
    temperature = int
    cooling = 0.998
    incumbent = list(solution)
    best = list(solution)
    op_scores = {"opt2": 0, "opt3": 0, "insert": 0, "move1": 0}
    prev_op_scores = {"opt2": 0, "opt3": 0, "insert": 0, "move1": 0}
    op_usage = {"opt2": 0, "opt3": 0, "insert": 0, "move1": 0}
    all_found_solutions = []

    for i in range(10000):
        rand = random.random()
        rand2 = random.random()
        
        if rand >= 0 and rand <= p1:
            temp = opt2_new(incumbent)
            deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

            op_usage["opt2"] += 1
            if readfile.objective_function(temp) < readfile.objective_function(best):
                op_scores["opt2"] += 4
            elif deltaE < 0:
                op_scores["opt2"] += 2
            elif temp not in all_found_solutions:
                op_scores["opt2"] += 1
                all_found_solutions.append(temp)
        

        elif rand > p1 and rand <= p2 + p1:
            temp = opt3_new(incumbent)
            deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

            op_usage["opt3"] += 1
            if readfile.objective_function(temp) < readfile.objective_function(best):
                op_scores["opt3"] += 4
            elif deltaE < 0:
                op_scores["opt3"] += 2
            elif temp not in all_found_solutions:
                op_scores["opt3"] += 1
                all_found_solutions.append(temp)

        elif(rand > p1+ p2 and rand <= p1 + p2 + p3):
            temp = insert1_new(incumbent)
            deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

            op_usage["insert"] += 1
            if readfile.objective_function(temp) < readfile.objective_function(best):
                op_scores["insert"] += 4
            elif deltaE < 0:
                op_scores["insert"] += 2
            elif temp not in all_found_solutions:
                op_scores["insert"] += 1
                all_found_solutions.append(temp)

        else:
            temp = move1(incumbent)
            deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

            op_usage["move1"] += 1
            if readfile.objective_function(temp) < readfile.objective_function(best):
                op_scores["move1"] += 4
            elif deltaE < 0:
                op_scores["move1"] += 2
            elif temp not in all_found_solutions:
                op_scores["move1"] += 1
                all_found_solutions.append(temp)
        
        

        if i == 100:

            print("100 rand: ", rand, " p1: ", p1, " p2: ", p2, " p3: ", p3, " p4: ", (p1+p2+p3))
            print("op usage: ", op_usage, " op scores: ", op_scores)

            if op_usage["opt2"] == 0: op_usage["opt2"] = 1
            if op_usage["opt3"] == 0: op_usage["opt3"] = 1
            if op_usage["insert"] == 0: op_usage["insert"] = 1
            if op_usage["move1"] == 0: op_usage["move1"] = 1


            print("etter 100 rand: ", rand, " p1: ", p1, " p2: ", p2, " p3: ", p3, " p4: ", (p1+p2+p3))
            print("op usage: ", op_usage, " op scores: ", op_scores)


            prev_op_scores = dict(op_scores)
            op_scores = {"opt2": 0, "opt3": 0, "insert": 0, "move1": 0}
            op_usage = {"opt2": 0, "opt3": 0, "insert": 0, "move1": 0}

            

        elif i % 100 == 0 and i != 0:
            print(i," før rand: ", rand, " p1: ", p1, " p2: ", p2, " p3: ", p3, " p4: ", (p1+p2+p3))
            print("op usage: ", op_usage, " op scores: ", op_scores) 

            if op_usage["opt2"] == 0: op_usage["opt2"] = 1
            if op_usage["opt3"] == 0: op_usage["opt3"] = 1
            if op_usage["insert"] == 0: op_usage["insert"] = 1
            if op_usage["move1"] == 0: op_usage["move1"] = 1

            p1 = (0.8 * prev_op_scores["opt2"]) + (0.2 * (op_scores["opt2"] / op_usage["opt2"]))
            p2 = (0.8 * prev_op_scores["opt3"]) + (0.2 * (op_scores["opt3"] / op_usage["opt3"]))
            p3 = (0.8 * prev_op_scores["insert"]) + (0.2 * (op_scores["insert"] / op_usage["insert"]))

            print(i," etter rand: ", rand, " p1: ", p1, " p2: ", p2, " p3: ", p3, " p4: ", (p1+p2+p3))
            print("op usage: ", op_usage, " op scores: ", op_scores)
            
            prev_op_scores = dict(op_scores)
            op_scores = {"opt2": 0, "opt3": 0, "insert": 0, "move1": 0}
            op_usage = {"opt2": 0, "opt3": 0, "insert": 0, "move1": 0}




        if i <= 100:
            p_change = 0.8
            if deltaE > 0:
                positive_deltas.append(deltaE)
        elif i == 101:

            if len(positive_deltas) != 0:
                init_temperature = mean(positive_deltas)
            else:
                init_temperature = 1000
            temperature = init_temperature
            p_change = e * (-deltaE / temperature)
        else:
            p_change = e * (-deltaE / temperature)

        if readfile.check_feasibility(temp):
            if deltaE < 0:
                incumbent = temp
                if readfile.objective_function(incumbent) < readfile.objective_function(best):
                    best = list(incumbent)
            
            elif rand2 < p_change:
                incumbent = temp
        if i > 100:
            temperature *= cooling
    
    return best


