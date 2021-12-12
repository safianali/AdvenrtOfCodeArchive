import time
from collections import defaultdict

start = time.time()

with open("12.txt") as f:
    rawInput = f.read().splitlines()

# part 1

caves = {}

for line in rawInput:
    newCaveStrings = line.split('-')

    for string in newCaveStrings:
        caves[string] = set()

for line in rawInput:
    string0, string1 = line.split('-')

    caves[string0].add(string1)
    caves[string1].add(string0)

for k, v in caves.copy().items():
    if k == "end":
        del caves[k]
    else:
        caves[k].discard("start")

pathsFound = 0


def findPaths(cave, smallCavesVisited):
    global pathsFound
    if cave == "end":
        pathsFound += 1
        return

    setCopy = smallCavesVisited.copy()

    for connectedCave in caves[cave]:
        if connectedCave.isupper():
            findPaths(connectedCave, setCopy)
        elif connectedCave not in setCopy:
            setCopy.add(connectedCave)
            findPaths(connectedCave, setCopy)
            setCopy.remove(connectedCave)


findPaths("start", set())

print("Part 1:", pathsFound)

# part 2
pathsFound = 0


def findPathsPart2(cave, smallCavesVisitedDict, smallCaveVisitedTwice):
    global pathsFound
    if cave == "end":
        pathsFound += 1
        return

    setCopy = smallCavesVisitedDict.copy()

    for connectedCave in caves[cave]:
        if connectedCave.isupper():
            findPathsPart2(connectedCave, setCopy, smallCaveVisitedTwice)
        elif setCopy[connectedCave] == 0:
            setCopy[connectedCave] += 1
            findPathsPart2(connectedCave, setCopy, smallCaveVisitedTwice)
            setCopy[connectedCave] -= 1
        elif setCopy[connectedCave] == 1 and not smallCaveVisitedTwice:
            setCopy[connectedCave] += 1
            findPathsPart2(connectedCave, setCopy, True)
            setCopy[connectedCave] -= 1


findPathsPart2("start", defaultdict(int), False)

print("Part 2:", pathsFound)

end = time.time()
print(end - start)
