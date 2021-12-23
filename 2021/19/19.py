import re
import time
from operator import add, sub

start = time.time()

with open("19.txt") as f:
    rawInput = f.read().splitlines()


# part 1

class Vector:

    def __init__(self, allVals):
        allVals = [abs(i) for i in allVals]
        allVals.sort()
        self.abs0, self.abs1, self.abs2 = allVals

    def __eq__(self, other):
        return (self.abs0 == other.abs0) and (self.abs1 == other.abs1) and (self.abs2 == other.abs2)

    def __hash__(self):
        return hash((self.abs0, self.abs1, self.abs2))


def getScannerPos(v1, v2, b1, b2):
    v2Neg = tuple(-i for i in v2)
    v2Abs = tuple(abs(i) for i in v2)

    pos = tuple(v2Abs.index(abs(i)) for i in v1)
    signs = tuple(1 if v1[i] == v2Neg[pos[i]] else -1 for i in (0, 1, 2))
    b2Rel = changeVector(b2, pos, signs)

    return tuple(map(add, b1, b2Rel)), pos, tuple(-i for i in signs)

def changeVector(v, pos, signs):
    newV0 = v[pos[0]] * signs[0]
    newV1 = v[pos[1]] * signs[1]
    newV2 = v[pos[2]] * signs[2]

    return (newV0, newV1, newV2)



class Beacon:

    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.vectorDict = None

    def setVectorDict(self, vectorDict):
        self.vectorDict = vectorDict

    def getVectorDict(self):
        return self.vectorDict

    def getPosition(self):
        return (self.X, self.Y, self.Z)

    def __eq__(self, other):
        return (self.X == other.X) and (self.Y == other.Y) and (self.Z == other.Z)

    def __hash__(self):
        return hash((self.X, self.Y, self.Z))


class Scanner:

    def __init__(self, ID, beaconSet):
        self.ID = ID
        self.beaconSet = beaconSet

    def calculateVectors(self):
        for b1 in self.beaconSet:
            vectorDict = {}
            for b2 in self.beaconSet:
                if b1 != b2:
                    diffV = list(map(sub, b1.getPosition(), b2.getPosition()))
                    vectorDict[Vector(diffV.copy())] = diffV

            b1.setVectorDict(vectorDict)

    def addBeaconSet(self, newBeacons):
        self.beaconSet.update(newBeacons)
        self.calculateVectors()

    def getBeaconSet(self):
        return self.beaconSet


i = 0
scanners = []

while (i < len(rawInput)):
    ID = int(re.findall(r'\d+', rawInput[i])[0])
    i += 1
    beaconSet = set()
    while (i < len(rawInput) and rawInput[i] != ""):
        X, Y, Z = [int(c) for c in re.findall(r'-?\d+', rawInput[i])]
        beaconSet.add(Beacon(X, Y, Z))
        i += 1

    newScanner = Scanner(ID, beaconSet)
    newScanner.calculateVectors()
    scanners.append(newScanner)

    i += 1


def compareScanners(s1, s2):
    for b1 in s1.beaconSet:
        for b2 in s2.beaconSet:
            shared = b1.getVectorDict().keys() & b2.getVectorDict().keys()
            if len(shared) >= 11:
                sharedV = shared.pop()
                v1 = b1.getVectorDict()[sharedV]
                v2 = b2.getVectorDict()[sharedV]

                return getScannerPos(v1, v2, b1.getPosition(), b2.getPosition())

    return False, False, False


def mergeScanners(s1, s2, relPos, pos, signs):
    newBeacons = set()
    for b in s2.beaconSet:
        newBeaconPos = tuple(map(add, relPos, changeVector(b.getPosition(), pos, signs)))
        newBeacons.add(Beacon(*newBeaconPos))

    s1.addBeaconSet(newBeacons)

scannerPositions = set()

while (len(scanners) != 1):
    for s in scanners.copy()[1:]:
        relScannerPos, pos, signs = compareScanners(scanners[0], s)

        if relScannerPos:
            scannerPositions.add(relScannerPos)
            mergeScanners(scanners[0], s, relScannerPos, pos, signs)
            scanners.remove(s)

s = scanners.pop()

print("Part 1:", len(s.getBeaconSet()))

# part 2

longestDist = -1

for s1 in scannerPositions:
    for s2 in scannerPositions:
        curDist = sum(abs(x - y) for x, y in zip(s1, s2))
        longestDist = max(curDist, longestDist)

print("Part 2:", longestDist)

end = time.time()
print(end - start)
