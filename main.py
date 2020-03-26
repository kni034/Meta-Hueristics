import readfile
import algorithms
import datetime as dt



start = dt.datetime.now()

readfile.read('Call_130_Vehicle_40.txt')
#readfile.read()

before = readfile.gen_dummy_solution()
score = readfile.objective_function(before)

print("score før localsearch: ",score, " solution: ", before)

#------
etter = algorithms.local_search(before)
#------

score = readfile.objective_function(etter)

print("etter: ", score, " solution: ", etter)

end = dt.datetime.now()
total_time = (end - start).total_seconds()
print("Completed in " + "%.6f" % total_time + " seconds.")

