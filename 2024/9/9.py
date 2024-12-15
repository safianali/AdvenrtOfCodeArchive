import time
from collections import deque

start = time.time()

with open("9.txt") as f:
    rawInput = f.read().splitlines()

# part 1

fileMap = []
listOfNoneIndexes = deque()

for i, char in enumerate(rawInput[0]):
    if i % 2 == 0:
        for j in range(int(char)):
            fileMap.append(i // 2)
    else:
        for j in range(int(char)):
            fileMap.append(None)
            listOfNoneIndexes.append(len(fileMap) - 1)

ogFileMap = fileMap.copy()
ogListOfNoneIndexes = listOfNoneIndexes.copy()

curIndex = len(fileMap) - 1

while len(listOfNoneIndexes) > 0 and curIndex > listOfNoneIndexes[0]:
    if fileMap[curIndex] is not None:
        fileMap[listOfNoneIndexes.popleft()] = fileMap[curIndex]

    del fileMap[curIndex]
    curIndex -= 1

checksum = 0

for pos, fileID in enumerate(fileMap):
    if fileID is not None:
        checksum += pos * fileID

print("Part 1:", checksum)

# part 2

def moveFileIfPossible(fileMap, startIndex, endIndex, ogListOfNoneIndexes):
    lengthRequired = endIndex - startIndex + 1

    for i in range(len(ogListOfNoneIndexes)):
        if ogListOfNoneIndexes[i] > startIndex:
            break

        if ogListOfNoneIndexes[i] + lengthRequired - 1 == ogListOfNoneIndexes[i + lengthRequired - 1]:
            for j in range(lengthRequired):
                fileMap[ogListOfNoneIndexes[i] + j] = fileMap[startIndex + j]
            
            for j in range(endIndex, startIndex - 1, -1):
                fileMap[j] = None

            for j in range(lengthRequired):
                del ogListOfNoneIndexes[i]

            return

curChar = None
count = 0
for i in range(len(ogFileMap) - 1, -1, -1):
    if curChar is None and ogFileMap[i] is not None:
        curChar = ogFileMap[i]
        count = 1
    elif curChar is not None and ogFileMap[i] == curChar:
        count += 1
    elif curChar is not None and ogFileMap[i] != curChar:
        moveFileIfPossible(ogFileMap, i + 1, i + count, ogListOfNoneIndexes)

        if ogFileMap[i] is None:
            curChar = None
            count = 0
        else:
            curChar = ogFileMap[i]
            count = 1

checksum = 0

for pos, fileID in enumerate(ogFileMap):
    if fileID is not None:
        checksum += pos * fileID

print("Part 2:", checksum)

end = time.time()
print(end - start)