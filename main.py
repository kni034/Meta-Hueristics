import readfile
import algorithms

a = [0,3 ,3 ,0, 1, 1, 0, 5, 6, 2, 7, 7, 6, 4, 2, 4, 5]
b = [3, 3, 0, 0, 7, 7, 1, 1, 0, 5, 4, 6, 2, 5, 6, 4, 2]
c = [7, 7, 0, 1, 1, 0, 5, 5, 6, 6, 0, 3, 2, 3, 4, 2, 4] 
d = [0, 7, 7, 3, 3, 0, 5, 5, 0, 1, 4, 1, 2, 6, 2, 6, 4]
e = [1, 1, 0, 7, 7, 0, 2, 2, 0, 3, 4, 5, 6, 4, 5, 3, 6] 
f = [3, 3, 0, 7, 1, 7, 1, 0, 5, 5, 0, 2, 2, 4, 4, 6, 6]

readfile.read()

score = readfile.objective_function(f)

print("score før randomsearch: ",score)

ny = algorithms.random_search(f)

score = readfile.objective_function(ny)
print("etter: ", score)

