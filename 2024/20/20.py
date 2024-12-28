import time
import sys
import heapq
from collections import Counter

start = time.time()

with open("20.txt") as f:
    rawInput = f.read().splitlines()

# Both parts are very inefficient, solution will take a while to run, around 2 minutes

# part 1

xLen = len(rawInput[0])
yLen = len(rawInput)

s = e = None 
for y in range(len(rawInput)):
    for x in range(len(rawInput[y])):
        if rawInput[y][x] == 'S':
            s = (x, y)
        if rawInput[y][x] == 'E':
            e = (x, y)
    if s and e:
        break

def findShortestPaths(startPoint, endPoint, grid):
    distanceMap = {startPoint: 0}
    predecessors = {startPoint: []}
    priorityQueue = [(0, startPoint)]
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while priorityQueue:
        currentDist, (x, y) = heapq.heappop(priorityQueue)
        if currentDist > distanceMap[(x, y)]:
            continue

        for dx, dy in directions:
            newX, newY = x + dx, y + dy
            if (
                0 <= newX < xLen
                and 0 <= newY < yLen
                and grid[newY][newX] != '#'
            ):
                newDist = currentDist + 1
                newPoint = (newX, newY)
                if newPoint not in distanceMap or newDist < distanceMap[newPoint]:
                    distanceMap[newPoint] = newDist
                    predecessors[newPoint] = [(x, y)]
                    heapq.heappush(priorityQueue, (newDist, newPoint))
                elif newDist == distanceMap[newPoint]:
                    predecessors[newPoint].append((x, y))

    if endPoint not in distanceMap:
        return None

    allPaths = []
    def buildPaths(current, path):
        if current == startPoint:
            allPaths.append(path[::-1])
            return
        for pred in predecessors[current]:
            buildPaths(pred, path + ([current] if current != endPoint else []))

    buildPaths(endPoint, [endPoint])
    return allPaths

def findShortestPath(s, e, grid):
    distances = {s: 0}
    queue = [(0, s)]
    while queue:
        dist, (x, y) = heapq.heappop(queue)
        if (x, y) == e:
            return dist
        if dist > distances[(x, y)]:
            continue
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < xLen and 
                0 <= ny < yLen and 
                grid[ny][nx] != '#'):
                ndist = dist + 1
                if (nx, ny) not in distances or ndist < distances[(nx, ny)]:
                    distances[(nx, ny)] = ndist
                    heapq.heappush(queue, (ndist, (nx, ny)))
    return None

def findAdjacentWalls(x, y, grid):
    walls = set()
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        wallX, wallY = x+dx, y+dy
        if 1 <= wallX < xLen-1 and 1 <= wallY < yLen-1 and grid[wallY][wallX] == '#':
            # Check horizontal connection
            if (grid[wallY][wallX-1] in '.SE' and grid[wallY][wallX+1] in '.SE') or \
               (wallY > 0 and grid[wallY-1][wallX] in '.SE' and wallY < yLen-1 and grid[wallY+1][wallX] in '.SE'):
                walls.add((wallX, wallY))
    return walls

sys.setrecursionlimit(10000)
shortestPaths = findShortestPaths(s, e, rawInput)
shortestPathLength = len(shortestPaths[0])
shortestPathWalls = {wall for path in shortestPaths for x,y in path for wall in findAdjacentWalls(x,y, rawInput)}

picosecondsSaved = Counter()
for i, wall in enumerate(shortestPathWalls):
    oldGrid = rawInput[wall[1]]
    rawInput[wall[1]] = oldGrid[:wall[0]] + '.' + oldGrid[wall[0]+1:]
    if (saved := shortestPathLength - findShortestPath(s, e, rawInput)) > 0:
        picosecondsSaved[saved] += 1
    rawInput[wall[1]] = oldGrid
    if i % 100 == 0:
        print(f"Processed {i} walls of {len(shortestPathWalls)}")

print("Part 1:",  sum(picosecondsSaved[ps] for ps in picosecondsSaved if ps >= 100))

# part 2

def manhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def getPointsWithinManhattanDistance(start, distance, xMax, yMax):
    reachablePoints = {}
    x0, y0 = start
    
    for dy in range(-distance, distance + 1):
        y = y0 + dy
        if y < 0 or y >= yMax:
            continue            

        x_spread = distance - abs(dy)
        x_min = max(0, x0 - x_spread)
        x_max = min(xMax - 1, x0 + x_spread)

        for x in range(x_min, x_max + 1):
            if rawInput[y][x] != '#':
                reachablePoints[(x, y)] = manhattanDistance(start, (x, y))
    
    return reachablePoints

distanceFromS = {s: 0, e: shortestPathLength}
for y in range(yLen):
    for x in range(xLen):
        if rawInput[y][x] == '.':
            distanceFromS[(x, y)] = findShortestPath(s, (x, y), rawInput)

distanceToE = {e: 0, s: shortestPathLength}
for y in range(yLen):
    for x in range(xLen):
        if rawInput[y][x] == '.':
            distanceToE[(x, y)] = findShortestPath(e, (x, y), rawInput)

picosecondsSaved = Counter()
for point1, dist1 in distanceFromS.items():
    for point2, dist2 in getPointsWithinManhattanDistance(point1, 20, xLen, yLen).items():
        saved = shortestPathLength - (dist1 + dist2 + distanceToE[point2])
        if saved > 0:
            picosecondsSaved[saved] += 1

print("Part 2:", sum(picosecondsSaved[ps] for ps in picosecondsSaved if ps >= 100))

end = time.time()
print(end - start)