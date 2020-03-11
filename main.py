import readfile

readfile.read()

a=readfile.gen_random_solution()
print(a)
for i in range(1000):
    a=readfile.gen_random_solution()
    print(a)