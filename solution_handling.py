import readfile
import random


def gen_random_solution():
    solution = []
    num_vehicles_left = readfile.num_vehicles 
    num_iterations = (readfile.num_calls * 2) + readfile.num_vehicles
    chance_of_changing_car = (readfile.num_vehicles/readfile.num_calls) * 100
    finished_calls = [0] * readfile.num_calls
    unfinished_calls = []
    unfinished_calls.extend(range(1, readfile.num_calls+1))

    while len(solution) < num_iterations:

        change_car = False
        #roll random 1/n chance to change car
        if num_vehicles_left > 0:
            change_car_check = random.randrange(0,101)
            if change_car_check <= chance_of_changing_car:
                change_car = True
            else:
                change_car = False

        #if we want to change car we have to deliver all packages that has been picked up by that car first
        if change_car:
            undelivered_calls = []
            for call_id, interaction_number in enumerate(finished_calls):
                if interaction_number == 1: 
                    undelivered_calls.append(call_id + 1) 
  
            #loop through and deliver packages that has been picked up
            while len(undelivered_calls) > 0:
                next_elem = random.choice(undelivered_calls)
                undelivered_calls.remove(next_elem)
                solution.append(next_elem)

                finished_calls[next_elem - 1] += 1
                unfinished_calls.remove(next_elem)

            num_vehicles_left -= 1
            solution.append(0)

        #add node to solution normaly
        else:
            
            #if all nodes are placed but there are more unused cars:
            if len(unfinished_calls) == 0: 
                solution.append(0)
                continue
            
            #pick random call that is not finished
            next_call = random.choice(unfinished_calls)

            solution.append(next_call)
            finished_calls[next_call - 1] += 1

            #call is done if visited 2 times
            if finished_calls[next_call - 1] == 2:
                unfinished_calls.remove(next_call)

    return solution


def check_feasibility(solution):
    test = True
