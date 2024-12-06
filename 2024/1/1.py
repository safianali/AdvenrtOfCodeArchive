import time
from collections import Counter

start = time.time()

with open("1.txt") as f:
    rawInput = f.read().splitlines()

# part 1

list1, list2 = [], []
for line in rawInput:
    split = line.split()
    list1.append(int(split[0]))
    list2.append(int(split[1]))

list1.sort()
list2.sort()

diff = 0
for num1, num2 in zip(list1, list2):
    diff += abs(num1 - num2)

print("Part 1:", diff)

# part 2

list2counter = Counter(list2)

sim_score = 0
for num1 in list1:
    sim_score += num1 * list2counter[num1]

print("Part 2:", sim_score)

end = time.time()
print(end - start)