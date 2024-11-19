result = 1
n = 23
for i in range(2, n+1):
    result *= (367 - i) / 366
result = 1 - result
print(f"Probability of two people sharing the same birthday in a room with {n} people: \n{100*result:.3f}%")