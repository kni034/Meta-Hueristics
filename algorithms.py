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

    print("ex1: ", ex1)
    temp = list(solution)

    temp = [x for x in temp if x != ex1]
    done = False
    i=0
    while not done:
        i+=1

        temp2 = list(temp)
        print("temp2 før: ", temp2)
        car = random.choice(readfile.call_to_cars(ex1))

        cars_possition = car_poss(temp2, car)
        temp2.insert(random.choice(cars_possition), ex1)
        cars_possition = car_poss(temp2, car)
        temp2.insert(random.choice(cars_possition), ex1)

        print("temp2 etter:", temp2)

        if readfile.check_feasibility(temp2):
            new = temp2
            done = True

        if i > 3:
            done = True
            new = list(solution)
        print("tried for car: ", car, " worked? ", readfile.check_feasibility(temp2) )
    return new

def opt3_new(solution):
    best = list(solution)
    done = False
    while not done:

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
            done = True

    return best

def opt2_new(solution):
    best = list(solution)
    done = False
    while not done:
        ex1 = random.choice(solution)
        while ex1 == 0: ex1 = random.choice(solution)

        ex2 = random.choice(solution)
        while ex2 == 0 or ex2 == ex1: ex2 = random.choice(solution)
        
        temp = switch(solution, ex1, ex2)

        if readfile.check_feasibility(temp):
            best = temp
            done = True

    return best


def simulated_annealing_new(solution):
    #p of using opt2
    p1 = 0
    #p of using opt3
    p2 = 0

    print("SimAnn NEW")

    positive_deltas = []
    init_temperature = int
    temperature = int
    cooling = 0.998
    incumbent = list(solution)
    best = list(solution)

    for i in range(10):
        rand = random.random()
        rand2 = random.random()
        if rand >= 0 and rand <= p1:
            temp = opt2_new(incumbent)
        elif rand > p1 and rand <= p2 + p1:
            temp = opt3_new(incumbent)
        else:
            temp = insert1_new(incumbent)

        deltaE = readfile.objective_function(temp) - readfile.objective_function(incumbent)

        #print("deltaE: ", deltaE)

        if i <= 100:
            p_change = 0.8
            if deltaE > 0:
                positive_deltas.append(deltaE)
        elif i == 101:
            #print(positive_deltas)
            init_temperature = mean(positive_deltas)
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


