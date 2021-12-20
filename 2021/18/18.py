import time
from collections import deque
from math import ceil

start = time.time()

with open("18.txt") as f:
    rawInput = f.read().splitlines()


# part 1

class Pair:

    def __init__(self, nestLevel, parent):
        self.nestLevel = nestLevel
        self.parent = parent
        self.left = None
        self.right = None

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def incrementLevel(self):
        self.nestLevel += 1

        if type(self.left) is Pair:
            self.left.incrementLevel()
        if type(self.right) is Pair:
            self.right.incrementLevel()

    def checkDeepestLevel(self):
        if type(self.left) is Pair:
            if type(self.right) is Pair:
                return max(self.left.checkDeepestLevel(), self.right.checkDeepestLevel())
            else:
                return self.left.checkDeepestLevel()
        elif type(self.right) is Pair:
            return self.right.checkDeepestLevel()
        else:
            return self.nestLevel

    def setParent(self, parent):
        self.parent = parent

    def incrementLeft(self, value):
        if type(self.left) is Pair:
            self.left.incrementRightRecursive(value)
        else:
            self.left += value

    def incrementRightRecursive(self, value):
        if type(self.right) is Pair:
            self.right.incrementRightRecursive(value)
        else:
            self.right += value

    def incrementRight(self, value):
        if type(self.right) is Pair:
            self.right.incrementLeftRecursive(value)
        else:
            self.right += value

    def incrementLeftRecursive(self, value):
        if type(self.left) is Pair:
            self.left.incrementLeftRecursive(value)
        else:
            self.left += value


def parsePair(q, nestLevel, parent):
    pair = Pair(nestLevel, parent)

    q.popleft()
    nextChar = q[0]

    if (nextChar == '['):
        pair.setLeft(parsePair(q, nestLevel + 1, pair))
    elif (nextChar.isdigit()):
        q.popleft()
        pair.setLeft(int(nextChar))
    else:
        print("ERROR")

    q.popleft()

    nextChar = q[0]

    if (nextChar == '['):
        pair.setRight(parsePair(q, nestLevel + 1, pair))
    elif (nextChar.isdigit()):
        q.popleft()
        pair.setRight(int(nextChar))
    else:
        print("ERROR")

    q.popleft()

    return pair


def addPair(num1, num2):
    addedPair = Pair(0, None)
    num1.incrementLevel()
    num2.incrementLevel()

    num1.setParent(addedPair)
    num2.setParent(addedPair)

    addedPair.setLeft(num1)
    addedPair.setRight(num2)

    return addedPair


def explodePairLeft(pair):
    parent = pair.parent
    num = pair.left

    found = False
    while (parent is not None) and not found:
        if pair == parent.right:
            found = True
            parent.incrementLeft(num)
        else:
            pair = parent
            parent = pair.parent


def explodePairRight(pair):
    parent = pair.parent
    num = pair.right

    found = False
    while (parent is not None) and not found:
        if pair == parent.left:
            found = True
            parent.incrementRight(num)
        else:
            pair = parent
            parent = pair.parent


def explodePair(pair):
    explodePairLeft(pair)
    explodePairRight(pair)

    if pair.parent.right == pair:
        pair.parent.right = 0
    else:
        pair.parent.left = 0


def findLevel4Pair(pair):
    if pair.nestLevel == 4:
        return pair
    else:
        if type(pair.left) is Pair:
            leftPair = findLevel4Pair(pair.left)
            if leftPair:
                return leftPair
            else:
                if type(pair.right) is Pair:
                    return findLevel4Pair(pair.right)
                else:
                    return None
        else:
            if type(pair.right) is Pair:
                return findLevel4Pair(pair.right)
            else:
                return None


def findPairToSplit(pair):
    if type(pair.left) is Pair:
        leftPair = findPairToSplit(pair.left)
        if leftPair:
            return leftPair

        if type(pair.right) is Pair:
            return findPairToSplit(pair.right)
        if pair.right >= 10:
            return pair

        return None

    else:
        if pair.left >= 10:
            return pair
        if type(pair.right) is Pair:
            return findPairToSplit(pair.right)
        else:
            if pair.right >= 10:
                return pair
            else:
                return None


def splitPair(pair):
    if type(pair.left) is not Pair and pair.left >= 10:
        newPair = Pair(pair.nestLevel + 1, pair)
        newPair.setLeft(pair.left // 2)
        newPair.setRight(ceil(pair.left / 2))
        pair.setLeft(newPair)
        return
    else:
        newPair = Pair(pair.nestLevel + 1, pair)
        newPair.setLeft(pair.right // 2)
        newPair.setRight(ceil(pair.right / 2))
        pair.setRight(newPair)


def reducePair(pair):
    pairtoExplode = findLevel4Pair(pair)
    while (pairtoExplode):
        explodePair(pairtoExplode)
        pairtoExplode = findLevel4Pair(pair)

    pairToSplit = findPairToSplit(pair)
    if pairToSplit:
        splitPair(pairToSplit)
        reducePair(pair)


def calcMag(pair):
    if type(pair.left) is int:
        leftMag = pair.left
    else:
        leftMag = calcMag(pair.left)

    if type(pair.right) is int:
        rightMag = pair.right
    else:
        rightMag = calcMag(pair.right)

    return (3 * leftMag) + (2 * rightMag)


line1 = deque(rawInput[0])
addedNum = parsePair(line1, 0, None)

for line in rawInput[1:]:
    lineQ = deque(line)
    lineNum = parsePair(lineQ, 0, None)

    addedNum = addPair(addedNum, lineNum)

    reducePair(addedNum)

print(calcMag(addedNum))

# part 2

largestMagSoFar = -1


def MagFrom2NumSum(str1, str2):
    num1 = parsePair(deque(str1), 0, None)
    num2 = parsePair(deque(str2), 0, None)

    addedNum = addPair(num1, num2)
    reducePair(addedNum)

    return calcMag(addedNum)


for i in range(len(rawInput)):
    for j in range(i + 1, len(rawInput)):
        curMag1 = MagFrom2NumSum(rawInput[i], rawInput[j])
        curMag2 = MagFrom2NumSum(rawInput[j], rawInput[i])

        largestMagSoFar = max(largestMagSoFar, curMag1, curMag2)

print(largestMagSoFar)

end = time.time()
print(end - start)
