import time
from collections import defaultdict

start = time.time()

with open("8.txt") as f:
    rawInput = f.read().splitlines()

# part 1

rawInput.reverse()

lettersToPositions = defaultdict(list)

for y, line in enumerate(rawInput):
    for x, char in enumerate(line):
        if char != ".":
            lettersToPositions[char].append((x, y))

xLen = len(rawInput[0])
yLen = len(rawInput)

def getAntinodePositions(pos1, pos2):
    xVec, yVec = pos2[0] - pos1[0], pos2[1] - pos1[1]
    a1 = (pos1[0] - xVec, pos1[1] - yVec)
    a2 = (pos2[0] + xVec, pos2[1] + yVec)

    # return only the antinode positions are within bounds
    if 0 <= a1[0] < xLen and 0 <= a1[1] < yLen:
        yield a1
    if 0 <= a2[0] < xLen and 0 <= a2[1] < yLen:
        yield a2

uniqueAntinodePositions = set()

for char, positions in lettersToPositions.items():
    if len(positions) < 2:
        continue

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            for antinode in getAntinodePositions(positions[i], positions[j]):
                uniqueAntinodePositions.add(antinode)

print("Part 1:", len(uniqueAntinodePositions))

# part 2

def checkPosInBounds(pos):
    return 0 <= pos[0] < xLen and 0 <= pos[1] < yLen

def getAntinodePositionsPart2(pos1, pos2):
    xVec, yVec = pos2[0] - pos1[0], pos2[1] - pos1[1]
    
    inBounds = True
    curX, curY = pos1[0], pos1[1]
    while inBounds:
        curX -= xVec
        curY -= yVec

        if not checkPosInBounds((curX, curY)):
            inBounds = False
        else:
            yield (curX, curY)
    
    inBounds = True
    curX, curY = pos2[0], pos2[1]
    while inBounds:
        curX += xVec
        curY += yVec

        if not checkPosInBounds((curX, curY)):
            inBounds = False
        else:
            yield (curX, curY)

uniqueAntinodePositions = set()

for char, positions in lettersToPositions.items():
    if len(positions) < 2:
        continue

    for position in positions:
        uniqueAntinodePositions.add(position)

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            for antinode in getAntinodePositionsPart2(positions[i], positions[j]):
                uniqueAntinodePositions.add(antinode)

print("Part 2:", len(uniqueAntinodePositions))

end = time.time()
print(end - start)