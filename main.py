import readfile
import algorithms
import datetime as dt


call7 = 'Call_7_Vehicle_3.txt'
call18 = 'Call_18_Vehicle_5.txt'
call35 = 'Call_035_Vehicle_07.txt'
call80 = 'Call_080_Vehicle_20.txt'
call130 = 'Call_130_Vehicle_40.txt'


#start = dt.datetime.now()


#readfile.read()



#print("funker den?: ", readfile.check_feasibility([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130]))



#before = readfile.gen_dummy_solution()
#score = readfile.objective_function(before)


#print("score før : ",score, " solution: ", before)
#print("weights: ", readfile.weighted_calls(before))

#------
#etter = algorithms.simulated_annealing_new(before)
#------

#score = readfile.objective_function(etter)

#print("etter: ", score, " solution: ", etter)
#print("weights: ", readfile.weighted_calls(etter))

#end = dt.datetime.now()
#total_time = (end - start).total_seconds()
#print("Completed in " + "%.6f" % total_time + " seconds.")



def results(filename= 'Call_7_Vehicle_3.txt'):
    readfile.read(filename)
    score_sum = 0
    before = readfile.gen_dummy_solution()
    score_before = readfile.objective_function(before)
    best = before
    best_score = score_before
    time_sum = 0

    iterations = 1

    for _ in range(iterations):
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

    average_score = score_sum/iterations
    average_time = time_sum/iterations

    improvement = 100 * ((score_before - best_score)/score_before)

    print(f"Avrage objective: {average_score:.2f}")
    print(f"Best objective: {best_score:.2f}")
    print(f"Improvement%: {improvement:.2f}")
    print(f"Running time: {average_time:.2f}")
    print(f"Best solution: {best}")



results(call130)



