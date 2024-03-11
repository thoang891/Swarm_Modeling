# decay = 0.8
# duration = 6
# timestep = 0.1

# iters = duration/timestep

# sum = 0
# for i in range(int(iters)):
#     val = decay**(1 + i*timestep)*timestep
#     sum += val
#     print(sum)

# print(sum)

list = []
for i in range(10):
    list.append(i)
    print(list)

for i in range(10):
    list.pop(0)
    print(list)