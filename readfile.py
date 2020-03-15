import random

num_nodes = int
num_vehicles = int
vehicle_start = {}
num_calls = int
calls = {}
travel_times_and_cost = {}
node_time_and_cost = {}

def read(filename = 'Call_7_Vehicle_3.txt'):

    with open(filename, encoding="utf8", errors='ignore') as f:
        f.readline()

        #number of nodes
        global num_nodes
        num_nodes = int(f.readline().rstrip('\n'))
        f.readline()

        #number of vehicles
        global num_vehicles
        num_vehicles = int(f.readline().rstrip('\n'))
        f.readline()

        #adds all vehicles start node to a dictionary with lists
        #vehicle_start = { vehicle index:[(0)home node, (1)starting time, (2)capacity]}
        global vehicle_start
        for _ in range(num_vehicles):
            line = f.readline().rstrip('\n')
            temp = line.split(",")
            temp = list(map(int, temp))
            first_elem = temp.pop(0)
            vehicle_start[first_elem] = temp

        f.readline()

        #number of calls
        global num_calls
        num_calls = int(f.readline().rstrip('\n'))
        f.readline()

        #list of calls each vehicle can do
        #vehicle_calls = {vehicle number:[call]}
        #call = (0)vehicle index, 
        # (1)list of calls that can be transported using that vehicle
        vehicle_calls={}
        for _ in range(num_vehicles):
            line = f.readline().rstrip('\n')
            temp = line.split(",")
            temp = list(map(int, temp))
            first_elem = temp.pop(0)
            vehicle_calls[first_elem] = temp

        f.readline()

        #adds all calls to a list containing the callinfo in a dictionary
        #calls = {call_index : [call]}
        #call = (0)call index, (1)origin node, (2)destination node, (3)size, 
        # (4)cost of not transporting, (5)lowerbound timewindow for pickup, 
        # (6)upper_timewindow for pickup, (7)lowerbound timewindow for delivery, 
        # (8)upper_timewindow for delivery
        global calls
        for _ in range(num_calls):
            line = f.readline().rstrip('\n')
            temp = line.split(",")
            temp = list(map(int, temp))
            first_elem = temp[0]
            calls[first_elem] = temp

        f.readline()

        #travel times and cost in a dict with tupel as key
        #travel_times_and_cost = 
        # {(vehicle number, origin node, destinaton node) : [(0)travel time, (1)travel cost]} 
        global travel_times_and_cost
        for _ in range(num_nodes*num_nodes*num_vehicles):
            line = f.readline().rstrip('\n')
            temp = line.split(",")
            temp = list(map(int, temp))
            first_elem = temp.pop(0)
            secound_elem = temp.pop(0)
            third_elem = temp.pop(0)
            temp_key = (first_elem, secound_elem, third_elem)
            travel_times_and_cost[temp_key] = temp

        f.readline()

        #time and cost of picking up and dropping packages in a call
        # node_time_and_cost = 
        # {(vechicle number, call) : 
        # ((0)origin node time, (1)origin node cost, (2)destination node time, (3)destination node cost)}
        global node_time_and_cost
        for _ in range(num_calls * num_vehicles):
            line = f.readline().rstrip('\n')
            temp = line.split(",")
            temp = list(map(int, temp))
            first_elem = temp.pop(0)
            secound_elem = temp.pop(0)
            temp_key = (first_elem, secound_elem)
            node_time_and_cost[temp_key] = temp



def gen_random_solution():

    solution = []
    num_vehicles_left = num_vehicles
    num_iterations = (num_calls * 2) + num_vehicles
    chance_of_changing_car = (num_vehicles/num_calls) * 100
    finished_calls = [0] * num_calls
    unfinished_calls = []
    unfinished_calls.extend(range(1, num_calls+1))

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


def test():
    car_id = 1
    time = vehicle_start[car_id][1]
    print(time)


def check_feasibility(solution):

    car_id = 1
    car_weight = 0
    time = vehicle_start[car_id][1]
    unfinished_calls = []
    unfinished_calls.extend(range(1, num_calls+1))
    cars_storage = []
    last_node = vehicle_start[car_id][0]


    if len(solution) is not (num_calls * 2) + num_vehicles:
        print("solution har feil lengde")
        return False

    for call in solution:
        #check for undelivered calls and change and reset active cars stats
        if call == 0:
            
            if len(cars_storage) is not 0:
                return False

            car_id += 1
            car_weight = 0
            time = vehicle_start[car_id][1]
            last_node = vehicle_start[car_id][0]

        #number is not 0 so it is a call and not a change of car
        else:
            #check if a call is 'visited' more than 2 times
            try:
                if call in cars_storage:
                    cars_storage.remove(call)
                    unfinished_calls.remove(call)
                    
                    car_weight += calls[call][3]



                else:
                    cars_storage.append(call)

                    car_weight -= calls[call][3]
                
            except:
                print("fler enn 2 av samme call")
                return False

            #check if package exceeds cars capacity

            if car_weight >= vehicle_start[car_id][2]:
                print("over papasitet for bil nr.", car_id, " på call: ", call)
                return False

            #calculate and check time usage
            

            
            #check if car can do call

    return True
            
