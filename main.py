import readfile
import algorithms
import datetime as dt

a = [0,3 ,3 ,0, 1, 1, 0, 5, 6, 2, 7, 7, 6, 4, 2, 4, 5]
b = [3, 3, 0, 0, 7, 7, 1, 1, 0, 5, 4, 6, 2, 5, 6, 4, 2]
c = [7, 7, 0, 1, 1, 0, 5, 5, 6, 6, 0, 3, 2, 3, 4, 2, 4] 
d = [0, 7, 7, 3, 3, 0, 5, 5, 0, 1, 4, 1, 2, 6, 2, 6, 4]
e = [1, 1, 0, 7, 7, 0, 2, 2, 0, 3, 4, 5, 6, 4, 5, 3, 6] 
f = [3, 3, 0, 7, 1, 7, 1, 0, 5, 5, 0, 2, 2, 4, 4, 6, 6]

bad = [0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7]

start = dt.datetime.now()

readfile.read()



score = readfile.objective_function(bad)

print("score før localsearch: ",score, " solution: ", bad)

ny = algorithms.local_search(bad)

score = readfile.objective_function(ny)
print("etter: ", score, " solution: ", ny)

end = dt.datetime.now()
total_time = (end - start).total_seconds()
print("Completed in " + "%.6f" % total_time + " seconds.")

