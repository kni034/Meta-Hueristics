import readfile
import random
from collections import defaultdict
from math import e
from statistics import mean
import datetime as dt


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
def car_poss(solution, car_id):
    current_car_num = 1
    possitions = []
    for i,elem in enumerate(solution):
        if current_car_num == car_id:
            possitions.append(i)
        if elem == 0:
            current_car_num += 1

    return possitions


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

        if i > 5:
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
        if i > 10:
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


def swap_in_car(solution):
    new = readfile.gen_dummy_solution()
    temp = list(solution)
    best = list(new)
    car = random.choice(range(readfile.num_vehicles)) + 1
    car_posstitions = car_poss(temp, car)

    better_number = 0

    car_posstitions.pop()
    if len(car_posstitions) < 4:
        return temp


    for _ in range(100):
        temp = list(solution)

        try:
            ex1 = random.choice(car_posstitions)
            ex2 = random.choice(car_posstitions)

            temp[ex1], temp[ex2] = temp[ex2], temp[ex1]

            if readfile.check_feasibility(temp):

                if readfile.objective_function(temp) < readfile.objective_function(best):

                    best = temp
                    better_number += 1

                    if better_number >= 1:
                        break

        except:
            print("feilet")

    return best


def simulated_annealing_new(solution, max_time):
    function_start = dt.datetime.now()

    print("SimAnn NEW")

    positive_deltas = []
    init_temperature = int
    temperature = int
    cooling = 0.998
    incumbent = list(solution)
    best = list(solution)
    op_scores = {"opt2": 0, "opt3": 0, "insert": 0, "swap": 0}
    prev_op_scores = {"opt2": 0, "opt3": 0, "insert": 0, "swap": 0}
    op_usage = {"opt2": 0, "opt3": 0, "insert": 0, "swap": 0}
    all_found_solutions = []

    #initial weights
    op_weights = [1] * 4
    lookup_list = [0,1,2,3]

    time_opt2 = 0
    time_opt3 = 0
    time_insert = 0
    time_swap = 0
    score_op2 = 0
    score_opt3 = 0
    score_insert = 0
    score_swap = 0


    for i in range(40000):

        op_number_to_op = {0: "opt2", 1:"opt3", 2: "insert", 3: "swap"}
        rand2 = random.random()
        
        current_op = random.choices(lookup_list, weights=op_weights, k=1)
        current_op_temp = current_op[0]
        current_op = current_op_temp
        current_op = op_number_to_op[current_op]

        if current_op == "opt2":
            start = dt.datetime.now()

            temp = opt2_new(incumbent)
            deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

            op_usage["opt2"] += 1
            if readfile.objective_function(temp) < readfile.objective_function(best):
                op_scores["opt2"] += 6
            elif deltaE < 0:
                op_scores["opt2"] += 2
            elif temp not in all_found_solutions:
                op_scores["opt2"] += 1
                all_found_solutions.append(temp)
            
            end = dt.datetime.now()
            time_opt2 += (end - start).total_seconds()

        elif current_op == "opt3":
            start = dt.datetime.now()

            temp = opt3_new(incumbent)
            deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

            op_usage["opt3"] += 1
            if readfile.objective_function(temp) < readfile.objective_function(best):
                op_scores["opt3"] += 6
            elif deltaE < 0:
                op_scores["opt3"] += 2
            elif temp not in all_found_solutions:
                op_scores["opt3"] += 1
                all_found_solutions.append(temp)

            end = dt.datetime.now()
            time_opt3 += (end - start).total_seconds()

        elif current_op == "insert":
            start = dt.datetime.now()

            temp = insert1_new(incumbent)
            deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

            op_usage["insert"] += 1
            if readfile.objective_function(temp) < readfile.objective_function(best):
                op_scores["insert"] += 6
            elif deltaE < 0:
                op_scores["insert"] += 2
            elif temp not in all_found_solutions:
                op_scores["insert"] += 1
                all_found_solutions.append(temp)
            
            end = dt.datetime.now()
            time_insert += (end - start).total_seconds()

        else:
            start = dt.datetime.now()

            temp = swap_in_car(incumbent)
            deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

            op_usage["swap"] += 1
            if readfile.objective_function(temp) < readfile.objective_function(best):
                op_scores["swap"] += 6
            elif deltaE < 0:
                op_scores["swap"] += 2
            elif temp not in all_found_solutions:
                op_scores["swap"] += 1
                all_found_solutions.append(temp)
            end = dt.datetime.now()
            time_swap += (end - start).total_seconds()
        
        

        if i == 100:

            if op_usage["opt2"] == 0: op_usage["opt2"] = 1
            if op_usage["opt3"] == 0: op_usage["opt3"] = 1
            if op_usage["insert"] == 0: op_usage["insert"] = 1
            if op_usage["swap"] == 0: op_usage["swap"] = 1

            prev_op_scores = dict(op_scores)

            score_op2 += op_scores["opt2"]
            score_opt3 += op_scores["opt3"]
            score_insert += op_scores["insert"]
            score_swap += op_scores["swap"]

            op_scores = {"opt2": 0, "opt3": 0, "insert": 0, "swap": 0}
            op_usage = {"opt2": 0, "opt3": 0, "insert": 0, "swap": 0}
            

        elif i % 100 == 0 and i != 0:

            #print(i, " op scores: ", op_scores, " op weights: ", op_weights )

            if op_usage["opt2"] == 0: op_usage["opt2"] = 1
            if op_usage["opt3"] == 0: op_usage["opt3"] = 1
            if op_usage["insert"] == 0: op_usage["insert"] = 1
            if op_usage["swap"] == 0: op_usage["swap"] = 1

            op_weights[0] = (0.8 * prev_op_scores["opt2"]) + (0.2 * (op_scores["opt2"] / op_usage["opt2"]))
            op_weights[1] = (0.8 * prev_op_scores["opt3"]) + (0.2 * (op_scores["opt3"] / op_usage["opt3"]))
            op_weights[2] = (0.8 * prev_op_scores["insert"]) + (0.2 * (op_scores["insert"] / op_usage["insert"]))
            op_weights[3] = (0.8 * prev_op_scores["swap"]) + (0.2 * (op_scores["swap"] / op_usage["swap"]))

            weights_sum = sum(op_weights)
            min_weight = weights_sum * 0.1
            if min_weight < 0.01:
                min_weight = 0.01

            if op_weights[0] < min_weight: op_weights[0] = min_weight
            if op_weights[1] < min_weight: op_weights[1] = min_weight
            if op_weights[2] < min_weight: op_weights[2] = min_weight
            if op_weights[3] < min_weight: op_weights[3] = min_weight

            score_op2 += op_scores["opt2"]
            score_opt3 += op_scores["opt3"]
            score_insert += op_scores["insert"]
            score_swap += op_scores["swap"]
            
            prev_op_scores = dict(op_scores)
            op_scores = {"opt2": 0, "opt3": 0, "insert": 0, "swap": 0}
            op_usage = {"opt2": 0, "opt3": 0, "insert": 0, "swap": 0}



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

        current_time = dt.datetime.now()
        time = (current_time - function_start).total_seconds()
        if time >= max_time:
            return best

    #print("time opt2: ", time_opt2, " time opt3: ", time_opt3, " time insert: ", time_insert, " time swap: ", time_swap)
    #print("scoreopt2: ", score_op2, " scoreopt3: ", score_opt3, " scoreinsert: ", score_insert, "scoreswap: ", score_swap)
    #print("value: ", time_opt2/score_op2, " ", time_opt3/score_opt3, " ", time_insert/score_insert, " ", time_swap/score_swap)
    return best
