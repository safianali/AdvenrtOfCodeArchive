import time
from multiprocessing import Pool
import itertools

start = time.time()

with open("6.txt") as f:
    rawInput = f.read().splitlines()

# part 1

rawInput.reverse()

xLen = len(rawInput[0])
yLen = len(rawInput)

xPos = None
yPos = None
for y in range(yLen):
    if xPos is not None:
        break
    for x in range(xLen):
        if rawInput[y][x] == "^":
            xPos, yPos = x, y
            break

startXPos = xPos
startYPos = yPos

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def getCurrentDirection(directionIdx):
    return directions[directionIdx]

def turnRight(directionIdx):
    return (directionIdx + 1) % 4

positionsSeen = set()
directionIdx = 0
while True:
    positionsSeen.add((xPos, yPos))
    
    curDirection = getCurrentDirection(directionIdx)
    nextXPos = xPos + curDirection[0]
    nextYPos = yPos + curDirection[1]

    if not (0 <= nextXPos < xLen and 0 <= nextYPos < yLen):
        break

    if rawInput[nextYPos][nextXPos] == "#":
        directionIdx = turnRight(directionIdx)
    else:
        xPos = nextXPos
        yPos = nextYPos

print("Part 1:", len(positionsSeen))

# part 2
def checkGuardEscapes(grid):
    global xLen, yLen
    directionIdx = 0

    xPos = startXPos
    yPos = startYPos

    positionsAndDirectionsSeen = set()
    while True:
        positionsAndDirectionsSeen.add((xPos, yPos, directionIdx))

        curDirection = getCurrentDirection(directionIdx)
        nextXPos = xPos + curDirection[0]
        nextYPos = yPos + curDirection[1]

        if not (0 <= nextXPos < xLen and 0 <= nextYPos < yLen):
            return True

        if grid[nextYPos][nextXPos] == "#":
            directionIdx = turnRight(directionIdx)
        else:
            xPos = nextXPos
            yPos = nextYPos

        if (nextXPos, nextYPos, directionIdx) in positionsAndDirectionsSeen:
            return False

rawInput = [list(row) for row in rawInput]

def check_position(args):
    y, x, raw_input = args
    if raw_input[y][x] == ".":
        grid_copy = [row[:] for row in raw_input]
        grid_copy[y][x] = "#"

        if not checkGuardEscapes(grid_copy):
            return 1
        
    return 0

positions = [(y, x, rawInput) for y in range(yLen) 
            for x in range(xLen) if rawInput[y][x] == "."]

with Pool(16) as pool:
    results = pool.map(check_position, positions)
    numPositions = sum(results)

print("Part 2:", numPositions)

end = time.time()
print(end - start)