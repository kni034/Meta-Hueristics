with open('Call_7_Vehicle_3.txt', encoding="utf8", errors='ignore') as f:
    f.readline()

    #number of nodes
    num_nodes = int(f.readline().rstrip('\n'))
    f.readline()

    #number of vehicles
    num_vehicles = int(f.readline().rstrip('\n'))
    f.readline()

    #adds all vehicles start node to a dictionary with lists
    #vehicle_start = {vehicle index:[home node, starting time, capacity]}
    vehicle_start = {}
    for i in range(num_vehicles):
        line = f.readline().rstrip('\n')
        temp = line.split(",")
        temp = list(map(int, temp))
        first_elem = temp.pop(0)
        vehicle_start[first_elem] = temp

    f.readline()

    #number of calls
    num_calls = int(f.readline().rstrip('\n'))
    f.readline()

    #list of calls each vehicle can do
    #vehicle_calls = {vehicle number:[call1, call3...]}
    vehicle_calls={}
    for i in range(num_vehicles):
        line = f.readline().rstrip('\n')
        temp = line.split(",")
        temp = list(map(int, temp))
        first_elem = temp.pop(0)
        vehicle_calls[first_elem] = temp

    f.readline()

    #adds all calls to a list containing the callinfo in a dictionary
    #calls = {call_index : [call]}
    calls = {}
    for i in range(num_calls):
        line = f.readline().rstrip('\n')
        temp = line.split(",")
        temp = list(map(int, temp))
        first_elem = temp[0]
        calls[first_elem] = temp

    f.readline()

    #travel times and cost in a dict with tupel as key
    #travel_times_and_cost = 
    # {(vehicle number, origin node, destinaton node) : [travel time, travel cost]} 
    travel_times_and_cost = {}
    for i in range(num_nodes*num_nodes*num_vehicles):
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
    # (origin node time, origin node cost, destination node time, destination node cost)}
    node_time_and_cost = {}
    for i in range(num_calls * num_vehicles):
        line = f.readline().rstrip('\n')
        temp = line.split(",")
        temp = list(map(int, temp))
        first_elem = temp.pop(0)
        secound_elem = temp.pop(0)
        temp_key = (first_elem, secound_elem)
        node_time_and_cost[temp_key] = temp


def printVars():
    #print variables
    print(f"num nodes: {num_nodes}\n")
    print(f"num vehicles: {num_vehicles}\n")
    print(f"vehicle start: {vehicle_start}\n")
    print(f"num calls {num_calls}\n")
    print(f"vehicle calls: {vehicle_calls}\n")
    print(f"calls: {calls}\n")
    print(f"travel time and cost: {travel_times_and_cost}\n")
    print(f"node time and cost: {node_time_and_cost}\n")

