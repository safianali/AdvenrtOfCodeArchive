from collections import defaultdict

#part 1
input = [line.split(",") for line in open("7.txt")][0]

inputDict = defaultdict(int)

for val in input:
    inputDict[int(val)] += 1

minFuelUsed = 10**9

for pos in range(min(inputDict), max(inputDict) + 1):
    fuelUsedAtPos = 0
    for k, v in inputDict.items():
        fuelUsedAtPos += abs(pos - k) * v
    
    if fuelUsedAtPos < minFuelUsed:
        minFuelUsed = fuelUsedAtPos

print(minFuelUsed)

#part 2
minFuelUsed = 10**9

for pos in range(min(inputDict), max(inputDict) + 1):
    fuelUsedAtPos = 0
    for k, v in inputDict.items():
        #https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF
        n = abs(pos - k)
        fuelUsedAtPos += int((n * (n + 1) * v) / 2)
    
    if fuelUsedAtPos < minFuelUsed:
        minFuelUsed = fuelUsedAtPos

print(minFuelUsed)