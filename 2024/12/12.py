import sys
import time

start = time.time()

with open("12.txt") as f:
    rawInput = f.read().splitlines()

# part 1

rawInput.reverse()

remainingPositions = set()

for y, line in enumerate(rawInput):
    for x, char in enumerate(line):
        remainingPositions.add((x, y))

remainingPositionsCopy = remainingPositions.copy()

xLen = len(rawInput[0])
yLen = len(rawInput)

def getAdjacent(x, y):
    return [(x + dx, y + dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
            if 0 <= x + dx < xLen and 0 <= y + dy < yLen]

# instead of returning the valid positions, here just return the difference in coordinates
def getAdjacentIncludingDiagonals(x, y):
    return [(dx, dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
            if 0 <= x + dx < xLen and 0 <= y + dy < yLen]

# returns the number in the 3x3 grid that corresponds to the position
# 0 1 2
# 3 4 5
# 6 7 8
# where 4 is (0, 0)
posToGridPosition = {
    (-1, 1): 0,
    (0, 1): 1,
    (1, 1): 2,
    (-1, 0): 3,
    (0, 0): 4,
    (1, 0): 5,
    (-1, -1): 6,
    (0, -1): 7,
    (1, -1): 8
}

def getPerimeterAndArea(x, y, region):
    plant = rawInput[y][x]
    
    area = 1
    perimeter = 4
    
    newPositions = [pos for pos in getAdjacent(x, y) if rawInput[pos[1]][pos[0]] == plant and pos in remainingPositions]

    while newPositions:
        curPos = newPositions.pop()
        if curPos in region:
            continue
        region.add(curPos)
        remainingPositions.remove(curPos)

        potentialNewPositions = [pos for pos in getAdjacent(curPos[0], curPos[1]) if rawInput[pos[1]][pos[0]] == plant]
        alreadyNeighbourCount = 0
        for pos in potentialNewPositions:
            if pos in region:
                alreadyNeighbourCount += 1
            elif pos in remainingPositions:
                newPositions.append(pos)
        
        area += 1

        match alreadyNeighbourCount:
            case 0:
                sys.exit("Error: plant is not connected")
            case 1:
                perimeter += 2
            case 3:
                perimeter -= 2
            case 4:
                perimeter -= 4
        
    return perimeter, area

totalPrice = 0

while remainingPositions:
    x, y = remainingPositions.pop()
    perimeter, area = getPerimeterAndArea(x, y, {(x, y)})

    totalPrice += perimeter * area

print("Part 1:", totalPrice)

# part 2

def calculateSides(positions):
    grid = [positions[0:3], positions[3:6], positions[6:9]]
    edges = set()
    
    # Collect all edges
    for i in range(3):
        for j in range(3):
            if grid[i][j]:
                # North edge
                if i == 0 or not grid[i-1][j]:
                    edges.add((j,i,'N'))
                # South edge
                if i == 2 or not grid[i+1][j]:
                    edges.add((j,i,'S'))
                # West edge
                if j == 0 or not grid[i][j-1]:
                    edges.add((j,i,'W'))
                # East edge
                if j == 2 or not grid[i][j+1]:
                    edges.add((j,i,'E'))
    
    # Group connected edges into sides
    sides = []
    used = set()
    
    for edge in edges:
        if edge in used:
            continue
            
        # Start new side
        current_side = {edge}
        used.add(edge)
        changed = True
        
        # Keep adding connected edges
        while changed:
            changed = False
            for other in edges:
                if other in used:
                    continue
                    
                # Check if connects to current side
                for e in current_side:
                    if (
                        # Same direction
                        other[2] == e[2] and
                        # Adjacent coordinates
                        abs(other[0] - e[0]) + abs(other[1] - e[1]) == 1
                    ):
                        current_side.add(other)
                        used.add(other)
                        changed = True
                        break
                        
        sides.append(current_side)
    
    return len(sides)

def getAreaAndSides(x, y, region):
    plant = rawInput[y][x]
    
    area = 1
    sides = 4
    
    newPositions = [pos for pos in getAdjacent(x, y) if rawInput[pos[1]][pos[0]] == plant and pos in remainingPositionsCopy]

    while newPositions:
        curPos = newPositions.pop()
        if curPos in region:
            continue
        region.add(curPos)
        remainingPositionsCopy.remove(curPos)

        potentialNewPositions = [pos for pos in getAdjacent(curPos[0], curPos[1]) if rawInput[pos[1]][pos[0]] == plant]
        for pos in potentialNewPositions:
            if pos not in region and pos in remainingPositionsCopy:
                newPositions.append(pos)
        
        currentGrid = [False] * 9
        for pos in getAdjacentIncludingDiagonals(curPos[0], curPos[1]):
            if (pos[0] + curPos[0], pos[1] + curPos[1]) in region:
                currentGrid[posToGridPosition[pos]] = True
        
        currentSides = calculateSides(currentGrid)
        currentGrid[4] = True
        sides += calculateSides(currentGrid) - currentSides

        area += 1
        
    return area, sides

totalPrice = 0
while remainingPositionsCopy:
    x, y = remainingPositionsCopy.pop()
    area, sides = getAreaAndSides(x, y, {(x, y)})

    totalPrice += area * sides

print("Part 2:", totalPrice)

end = time.time()
print(end - start)