import readfile
import algorithms
import datetime as dt


call7 = 'Call_7_Vehicle_3.txt'
call18 = 'Call_18_Vehicle_5.txt'
call35 = 'Call_035_Vehicle_07.txt'
call80 = 'Call_080_Vehicle_20.txt'
call130 = 'Call_130_Vehicle_40.txt'


start = dt.datetime.now()


readfile.read(call130)

before = readfile.gen_dummy_solution()
score = readfile.objective_function(before)


print("score før : ",score, " solution: ", before)
#print("weights: ", readfile.weighted_calls(before))

#------
etter = algorithms.simulated_annealing_new(before)
#------

score = readfile.objective_function(etter)

print("etter: ", score, " solution: ", etter)
#print("weights: ", readfile.weighted_calls(etter))

end = dt.datetime.now()
total_time = (end - start).total_seconds()
print("Completed in " + "%.6f" % total_time + " seconds.")



def results(filename= 'Call_7_Vehicle_3.txt'):
    readfile.read(filename)
    score_sum = 0
    before = readfile.gen_dummy_solution()
    score_before = readfile.objective_function(before)
    best = before
    best_score = score_before
    time_sum = 0

    for _ in range(10):
        start = dt.datetime.now()
        before = readfile.gen_dummy_solution()
        score_before = readfile.objective_function(before)

        #-------
        after = algorithms.simulated_annealing_new(before)
        #-------


        after_score = readfile.objective_function(after)

        end = dt.datetime.now()
        time = (end - start).total_seconds()

        score_sum += after_score
        time_sum += time

        if after_score < best_score:
            best = after
            best_score = after_score

    average_score = score_sum/10
    average_time = time_sum/10

    improvement = 100 * ((score_before - best_score)/score_before)

    print(f"Avrage objective: {average_score:.2f}")
    print(f"Best objective: {best_score:.2f}")
    print(f"Improvement%: {improvement:.2f}")
    print(f"Running time: {average_time:.2f}")
    print(f"Best solution: {best}")



#results(call130)



