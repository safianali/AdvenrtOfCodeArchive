import time
from collections import deque

start = time.time()

with open("15.txt") as f:
    rawInput = f.read().splitlines()

# part 1

grid = []
emptyIndex = 0
robotX, robotY = 0, 0
for i in range(len(rawInput)):
    if rawInput[i] == "":
        emptyIndex = i
        break
    if '@' in rawInput[i]:
        robotX = rawInput[i].index('@')
        robotY = i
    grid.append(rawInput[i])

gridCopy = [line[:] for line in grid ]

xLen = len(grid[0])
yLen = len(grid)

def setGridPosition(grid, x, y, value):
    grid[y] = grid[y][:x] + value + grid[y][x + 1:]

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
ROBOT, WALL, BOX, EMPTY = "@", "#", "O", "."

def move(direction):
    x, y = direction
    global robotX, robotY
    nextPos = (robotX + x, robotY + y)
    if grid[nextPos[1]][nextPos[0]] == WALL:
        return
    
    if grid[nextPos[1]][nextPos[0]] == EMPTY:
        setGridPosition(grid, robotX, robotY, EMPTY)
        setGridPosition(grid, nextPos[0], nextPos[1], ROBOT)
        robotX, robotY = nextPos
        return
    
    q = deque(BOX)

    movePossible = False
    while not movePossible and grid[nextPos[1]][nextPos[0]] != WALL:
        nextPos = (nextPos[0] + x, nextPos[1] + y)
        if grid[nextPos[1]][nextPos[0]] == EMPTY:
            movePossible = True
        else:
            q.append(grid[nextPos[1]][nextPos[0]])
    
    if movePossible:
        nextPos = (robotX, robotY)
        robotX, robotY = robotX + x, robotY + y
        q.extend([ROBOT, EMPTY])
        while q:
            setGridPosition(grid, nextPos[0], nextPos[1], q.pop())
            nextPos = (nextPos[0] + x, nextPos[1] + y)


def printGrid(grid):
    for line in grid:
        print(line)

DIRECTION_MAP = {
    "^": UP,
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT
}

for i in range(emptyIndex + 1, len(rawInput)):
    for char in rawInput[i]:
        move(DIRECTION_MAP[char])

boxes = set()

for y in range(yLen):
    for x in range(xLen):
        if grid[y][x] == BOX:
            boxes.add((x, y))

print("Part 1:", sum((100 * y + x) for x, y in boxes))

# part 2

part2Grid = []

part2Conversion = {
    '#': '##',
    'O': '[]',
    '.': '..',
    '@': '@.'
}

for i in range(len(gridCopy)):
    newLine = ""
    for j in range(len(gridCopy[i])):
        char = gridCopy[i][j]
        if char == '@':
            robotX, robotY = j * 2, i
        newLine += part2Conversion[char]
    part2Grid.append(newLine)

NEWBOX = '[]'

def getFullBoxPosition(char, x, y):
    if char == ']':
        return [(x - 1, y), (x, y)]
    
    return [(x, y), (x + 1, y)]

def move2(direction):
    x, y = direction
    global robotX, robotY
    nextPos = (robotX + x, robotY + y)
    if part2Grid[nextPos[1]][nextPos[0]] == WALL:
        return
    
    if part2Grid[nextPos[1]][nextPos[0]] == EMPTY:
        setGridPosition(part2Grid, robotX, robotY, EMPTY)
        setGridPosition(part2Grid, nextPos[0], nextPos[1], ROBOT)
        robotX, robotY = nextPos
        return
    
    # left and right are basically the same as before
    # for up and down, keep track of the positions of each box chcaracter on each row
    # go up/down row by row until wall is hit, using box positions from the last row to determine
    # which boxes on next row should be moved
    if direction in (LEFT, RIGHT):
        q = deque(part2Grid[nextPos[1]][nextPos[0]])

        movePossible = False
        while not movePossible and part2Grid[nextPos[1]][nextPos[0]] != WALL:
            nextPos = (nextPos[0] + x, nextPos[1] + y)
            if part2Grid[nextPos[1]][nextPos[0]] == EMPTY:
                movePossible = True
            else:
                q.append(part2Grid[nextPos[1]][nextPos[0]])

        if movePossible:
            nextPos = (robotX, robotY)
            robotX, robotY = robotX + x, robotY + y
            q.extendleft([ROBOT, EMPTY])
            while q:
                setGridPosition(part2Grid, nextPos[0], nextPos[1], q.popleft())
                nextPos = (nextPos[0] + x, nextPos[1] + y)

        return

    positionsToShiftVertically = deque([(robotX, robotY)])
    wallHit = False
    movePossible = False
    curLevel = [(robotX, robotY)]

    nextLevel = set()
    while not (wallHit or movePossible):
        movePossible = True
        for item in curLevel:
            currentItemPos = (item[0] + x, item[1] + y)

            if part2Grid[currentItemPos[1]][currentItemPos[0]] == EMPTY:
                continue
            
            movePossible = False

            if part2Grid[currentItemPos[1]][currentItemPos[0]] == WALL:
                wallHit = True
                break
            
            nextLevel.update(getFullBoxPosition(part2Grid[currentItemPos[1]][currentItemPos[0]], currentItemPos[0], currentItemPos[1]))
            
        positionsToShiftVertically.extend(nextLevel)
        curLevel = nextLevel
        nextLevel = set()

    if wallHit:
        return
    
    while positionsToShiftVertically:
        curPos = positionsToShiftVertically.pop()
        setGridPosition(part2Grid, curPos[0] + x, curPos[1] + y, part2Grid[curPos[1]][curPos[0]])
        setGridPosition(part2Grid, curPos[0], curPos[1], EMPTY)
    
    robotX, robotY = robotX + x, robotY + y

for i in range(emptyIndex + 1, len(rawInput)):
    for char in rawInput[i]:
        move2(DIRECTION_MAP[char])

boxes = set()
for y in range(yLen):
    for x in range(xLen * 2):
        if part2Grid[y][x] == '[':
            boxes.add((x, y))

print("Part 2:", sum((100 * y + x) for x, y in boxes))

end = time.time()
print(end - start)