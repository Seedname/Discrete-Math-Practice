import random

data1 = []
data2 = []
doors = [True, False, False]


for _ in range(1_000_000):
    random.shuffle(doors)
    chosen_door = random.choice(list(range(len(doors))))

    contestant1 = chosen_door

    wrong_door = random.choice([i for i in range(len(doors)) if not doors[i] and i != chosen_door])
    contestant2 = random.choice([i for i in range(len(doors)) if i != wrong_door and i != chosen_door])

    data1.append(doors[contestant1])
    data2.append(doors[contestant2])

print(f"Samples: {len(data1):,}")
print(f"No Switch Win Rate: {sum(data1)/len(data1)*100}%")
print(f"Switch Win Rate: {sum(data2)/len(data2)*100}%")

