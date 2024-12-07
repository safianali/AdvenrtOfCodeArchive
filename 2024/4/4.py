import time

start = time.time()

with open("4.txt") as f:
    rawInput = f.read().splitlines()

# part 1

xLen = len(rawInput[0])
yLen = len(rawInput)

def getElem(x, y):
    if x < 0 or x >= xLen or y < 0 or y >= yLen:
        return 'O'
    
    return rawInput[y][x]

def getWordsCoords(x, y):
    dirs = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    return [
        [[x + dx*i, y + dy*i] for i in range(4)]
        for dx, dy in dirs
    ]
XMASes = 0
for x in range(xLen):
    for y in range(yLen):
        if rawInput[y][x] != "X":
            continue
        for wordCoords in getWordsCoords(x, y):
            if getElem(*wordCoords[1]) == 'M' and getElem(*wordCoords[2]) == 'A' and getElem(*wordCoords[3]) == 'S':
                XMASes += 1

print("Part 1:", XMASes)

# part 2

def getMASCoords(x, y):
    return [[x, y], [x + 2, y], [x + 1, y + 1], [x, y + 2], [x + 2, y + 2]]

def checkMsAndSs(chars):
    return chars.count('M') == 2 and chars.count('S') == 2

MASes = 0
for x in range(xLen):
    for y in range(yLen):
        if rawInput[y][x] not in "MS":
            continue
            
        coords = getMASCoords(x, y)
        if getElem(*coords[2]) != "A":
            continue

        corners = [getElem(*c) for c in coords[:2] + coords[3:]]
        if not checkMsAndSs(corners) or corners[0] == corners[3]:
            continue

        MASes += 1


print("Part 2:", MASes)

end = time.time()
print(end - start)