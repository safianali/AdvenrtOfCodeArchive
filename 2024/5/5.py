import time
from collections import defaultdict

start = time.time()

with open("5.txt") as f:
    rawInput = f.read().splitlines()

# part 1

i = 0
before = defaultdict(set)
while rawInput[i] != "":
    beforeNum, afterNum = [int(x) for x in rawInput[i].split("|")]
    before[beforeNum].add(afterNum)

    i += 1

i += 1
firstUpdateIdx = i

middleSum = 0
while i < len(rawInput):
    update = [int(x) for x in rawInput[i].split(",")]
    
    seen = set()
    correct = True
    
    for page in update:
        if not correct:
            break

        for beforePage in before[page]:
            if beforePage in seen:
                correct = False
                break
        
        seen.add(page)

    if correct:
        middleSum += update[len(update) // 2]
        
    i += 1

print("Part 1:", middleSum)

# part 2

middleSum = 0
i = firstUpdateIdx
while i < len(rawInput):
    update = [int(x) for x in rawInput[i].split(",")]

    seen = set()
    correctedUpdate = False
    
    for j in range(len(update)):
        seen.add(update[j])
        correctedPage = False
        for beforePage in before[update[j]]:
            if beforePage in seen:
                correctedPage = True
                break

        if correctedPage:
            correctedUpdate = True
            for k in range(len(update)):
                if update[k] in before[update[j]]:
                    update.insert(k, update.pop(j))
                    break

    if correctedUpdate:
        middleSum += update[len(update) // 2]
        
    i += 1
    
print("Part 2:", middleSum)


end = time.time()
print(end - start)