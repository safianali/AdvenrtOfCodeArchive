import re
import time
from collections import defaultdict

start = time.time()

with open("17.txt") as f:
    rawInput = f.read().splitlines()


# this won't work for other inputs, need to change the 'inf' constant on line 113

# part 1

def getValidXVelocities(endGuess, startArea, endArea):
    stepsToGoal = defaultdict(set)

    for x in range(endGuess + 1):
        curPos = steps = 0
        curVel = x
        noLongerApproaching = False

        while not noLongerApproaching:
            curPos += curVel
            steps += 1

            if curVel == 0:
                noLongerApproaching = True
                if (curPos >= startArea) and (curPos <= endArea):
                    stepsToGoal[x].add("inf")
            elif (curPos >= startArea) and (curPos <= endArea):
                stepsToGoal[x].add(steps)

            curVel -= 1

    return stepsToGoal


def getHighestY(endGuess, startArea, endArea):
    bestGuess = None
    bestGuessHighestPos = None

    for x in range(endGuess + 1):
        curPos = 0
        curVel = x
        curHighestPos = 0
        noLongerApproaching = False
        valid = False

        while not noLongerApproaching:
            curPos += curVel
            curVel -= 1

            if (curPos >= startArea) and (curPos <= endArea):
                valid = True
            elif (curPos < startArea) and (curVel <= 0):
                noLongerApproaching = True

            if curPos > curHighestPos:
                curHighestPos = curPos

        if valid:
            if not bestGuess:
                bestGuess = x
                bestGuessHighestPos = curHighestPos
            elif curHighestPos > bestGuessHighestPos:
                bestGuess = x
                bestGuessHighestPos = curHighestPos

    return bestGuess, bestGuessHighestPos


startAreaX, endAreaX, startAreaY, endAreaY = [int(x) for x in re.findall(r'-?\d+', rawInput[0])]

validX = getValidXVelocities(1000, startAreaX, endAreaX)

y, highestPos = getHighestY(1000, startAreaY, endAreaY)

print(y)


# part 2

def getAllY(startGuess, endGuess, startArea, endArea):
    stepsToGoal = defaultdict(set)

    for x in range(startGuess, endGuess + 1):
        curPos = steps = 0
        curVel = x
        noLongerApproaching = False

        while not noLongerApproaching:
            curPos += curVel
            curVel -= 1
            steps += 1

            if (curPos >= startArea) and (curPos <= endArea):
                stepsToGoal[x].add(steps)
            elif (curPos < startArea) and (curVel <= 0):
                noLongerApproaching = True

    return stepsToGoal


allY = getAllY(-1000, 1000, startAreaY, endAreaY)

count = 0
for y in allY.values():
    for x in validX.values():
        if bool(y & x):
            count += 1
        elif 'inf' in x:
            if max(y) > 24:
                count += 1

print(count)

end = time.time()
print(end - start)
