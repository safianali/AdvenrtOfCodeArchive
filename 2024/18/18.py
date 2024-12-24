import time

start = time.time()

with open("18.txt") as f:
    rawInput = f.read().splitlines()

# part 1

xLen = 7
yLen = 7
numBytesToRead = 12

# for real/non-sample input
# xLen = 71
# yLen = 71
# numBytesToRead = 1024

grid = [['.' for x in range(xLen)] for y in range(yLen)]

for i in range(numBytesToRead):
    x, y = map(int, rawInput[i].split(','))
    grid[y][x] = '#'

def isValidMove(grid, newX, newY):
    return 0 <= newX < xLen and 0 <= newY < yLen and grid[newY][newX] == '.'

def findShortestPath(grid, start, end):
    distances = {start: 0}
    unvisited = {start}
    visited = set()
    
    while unvisited:
        current = min(unvisited, key=lambda x: distances[x])
        
        if current == end:
            return distances[current]
            
        unvisited.remove(current)
        visited.add(current)
        
        x, y = current
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newX, newY = x + dx, y + dy
            neighbor = (newX, newY)
            if isValidMove(grid, newX, newY) and neighbor not in visited:
                new_distance = distances[current] + 1
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    unvisited.add(neighbor)
    
    return float('inf')

print("Part 1:", findShortestPath(grid, (0, 0), (xLen - 1, yLen - 1)))

# part 2

i = numBytesToRead - 1
while True:
    i += 1
    x, y = map(int, rawInput[i].split(','))
    grid[y][x] = '#'

    if findShortestPath(grid, (0, 0), (xLen - 1, yLen - 1)) == float('inf'):
        print(f"Part 2: {x},{y}")
        break

end = time.time()
print(end - start)