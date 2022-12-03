import time

start = time.time()

with open("1.txt") as f:
    rawInput = f.read().splitlines()

# part 1

maxCalorie = 0
curElfCals = 0
for item in rawInput:
    if item == "":
        maxCalorie = max(curElfCals, maxCalorie)
        curElfCals = 0
    else:
        curElfCals += int(item)

print(maxCalorie)

# part 2

top3Cals = [0, 0, 0]
curElfCals = 0
for item in rawInput:
    if item == "":
        if curElfCals > top3Cals[0]:
            top3Cals = [curElfCals] + top3Cals[0:2]
        elif curElfCals > top3Cals[1]:
            top3Cals = [top3Cals[0]] + [curElfCals] + [top3Cals[1]]
        elif curElfCals > top3Cals[2]:
            top3Cals = top3Cals[0:2] + [curElfCals]

        curElfCals = 0
    else:
        curElfCals += int(item)

print(sum(top3Cals))

end = time.time()
print(end - start)
