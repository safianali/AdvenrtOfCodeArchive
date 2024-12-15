import time
from collections import defaultdict

start = time.time()

with open("10.txt") as f:
    rawInput = f.read().splitlines()

# part 1

rawInput.reverse()

xLen = len(rawInput[0])
yLen = len(rawInput)

def getAdjacent(x, y):
    directions = [(0,1), (0,-1), (-1,0), (1,0)]  # up,down,left,right
    return [(x+dx, y+dy) for dx,dy in directions 
            if 0 <= x+dx < xLen and 0 <= y+dy < yLen]

posToNines = {}

def getReachableNines(x, y, height):
    reqHeight = height + 1
    reachableNines = set()

    for newX, newY in getAdjacent(x, y):
        if int(rawInput[newY][newX]) != reqHeight:
            continue

        if (newX, newY) in posToNines:
            reachableNines |= posToNines[(newX, newY)]
            continue

        if reqHeight == 9: 
            reachableNines.add((newX, newY))
            continue

        reachableNines |= getReachableNines(newX, newY, reqHeight)

    posToNines[(x, y)] = reachableNines

    return reachableNines

scoreSum = 0

for y in range(yLen):
    for x in range(xLen):
        if rawInput[y][x] == "0":
            scoreSum += len(getReachableNines(x, y, 0))

print("Part 1:", scoreSum)

# part 2

posToDistinctRoutes = {}

def getDistinctRoutes(x, y, height):
    reqHeight = height + 1
    routes = 0

    for newX, newY in getAdjacent(x, y):
        if int(rawInput[newY][newX]) != reqHeight:
            continue

        if (newX, newY) in posToDistinctRoutes:
            routes += posToDistinctRoutes[(newX, newY)]
            continue

        if reqHeight == 9: 
            routes += 1
            continue

        routes += getDistinctRoutes(newX, newY, reqHeight)

    posToDistinctRoutes[(x, y)] = routes

    return routes

ratingSum = 0

for y in range(yLen):
    for x in range(xLen):
        if rawInput[y][x] == "0":
            ratingSum += getDistinctRoutes(x, y, 0)

print("Part 2:", ratingSum)

end = time.time()
print(end - start)