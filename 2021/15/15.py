import time
from heapq import heappush, heappop

start = time.time()

with open("15.txt") as f:
    rawInput = f.read().splitlines()


# part 1

class Node:

    def __init__(self, X, Y, risk, totalRiskToHere=10 ** 12):
        self.X = X
        self.Y = Y
        self.risk = risk
        self.totalRiskToHere = totalRiskToHere
        self.neighbours = None
        self.removed = False

    def setRisk(self, x):
        self.risk = x

    def getRisk(self):
        return self.risk

    def setNeighbours(self, neighbours):
        self.neighbours = neighbours

    def getNeighbours(self):
        return self.neighbours

    def replaceNeighbour(self, oldNeighbour, newNeighbour):
        self.neighbours.remove(oldNeighbour)
        self.neighbours.add(newNeighbour)

    def setTotalRiskToHere(self, totalRisk):
        self.totalRiskToHere = totalRisk

    def getTotalRiskToHere(self):
        return self.totalRiskToHere

    def setRemoved(self):
        self.removed = True

    def setNotRemoved(self):
        self.removed = False

    def isRemoved(self):
        return self.removed

    def __hash__(self):
        return hash((self.X, self.Y))

    def __eq__(self, other):
        return (self.X == other.X) and (self.Y == other.Y)

    def __lt__(self, other):
        return self.getTotalRiskToHere() <= other.getTotalRiskToHere()


def copyNodeWithNewTotalRisk(node, newTotalRisk):
    newNode = Node(node.X, node.Y, node.getRisk(), newTotalRisk)

    newNode.setNeighbours(node.getNeighbours())
    for neighbour in node.getNeighbours():
        neighbour.replaceNeighbour(node, newNode)

    node.setRemoved()

    return newNode


largestX = len(rawInput[0]) - 1
largestY = len(rawInput) - 1

nodeDict = {}
unvisitedNodes = []

for y, row in enumerate(rawInput):
    for x, risk in enumerate(row):
        nodeDict[(x, y)] = Node(x, y, int(risk))
        heappush(unvisitedNodes, nodeDict[(x, y)])

# set adj nodes

for y, row in enumerate(rawInput):
    for x, risk in enumerate(row):
        curNeighbours = set()

        if (x != 0):
            curNeighbours.add(nodeDict[(x - 1, y)])
        if (x != largestX):
            curNeighbours.add(nodeDict[(x + 1, y)])
        if (y != 0):
            curNeighbours.add(nodeDict[(x, y - 1)])
        if (y != largestY):
            curNeighbours.add(nodeDict[(x, y + 1)])

        nodeDict[(x, y)].setNeighbours(curNeighbours)

newNode = copyNodeWithNewTotalRisk(nodeDict[(0, 0)], 0)
nodeDict[(0, 0)] = newNode
heappush(unvisitedNodes, newNode)

while unvisitedNodes:
    curNode = heappop(unvisitedNodes)
    if not curNode.isRemoved():
        curRisk = curNode.getTotalRiskToHere()

        for neighbour in curNode.getNeighbours().copy():
            alt = curRisk + neighbour.getRisk()

            if (alt < neighbour.getTotalRiskToHere()):
                newNode = copyNodeWithNewTotalRisk(nodeDict[neighbour.X, neighbour.Y], alt)
                nodeDict[(neighbour.X, neighbour.Y)] = newNode
                heappush(unvisitedNodes, newNode)

print("Part 1:", nodeDict[largestX, largestY].getTotalRiskToHere())

# part 2

for x in range(largestX + 1, (largestX + 1) * 5):
    for y in range(0, largestY + 1):
        nodeDict[(x, y)] = Node(x, y, (nodeDict[(x - (largestX + 1), y)].getRisk()) % 9 + 1)

for x in range(0, (largestX + 1) * 5):
    for y in range(largestX + 1, (largestX + 1) * 5):
        nodeDict[(x, y)] = Node(x, y, (nodeDict[(x, y - (largestY + 1))].getRisk()) % 9 + 1)

largestX = ((largestX + 1) * 5) - 1
largestY = ((largestY + 1) * 5) - 1

for y in range(largestY + 1):
    for x in range(largestX + 1):
        curNeighbours = set()

        if (x != 0):
            curNeighbours.add(nodeDict[(x - 1, y)])
        if (x != largestX):
            curNeighbours.add(nodeDict[(x + 1, y)])
        if (y != 0):
            curNeighbours.add(nodeDict[(x, y - 1)])
        if (y != largestY):
            curNeighbours.add(nodeDict[(x, y + 1)])

        curNode = nodeDict[(x, y)]
        curNode.setNeighbours(curNeighbours)
        curNode.setNotRemoved()
        curNode.setTotalRiskToHere(10 ** 12)
        heappush(unvisitedNodes, curNode)

newNode = copyNodeWithNewTotalRisk(nodeDict[(0, 0)], 0)
nodeDict[(0, 0)] = newNode
heappush(unvisitedNodes, newNode)

while unvisitedNodes:
    curNode = heappop(unvisitedNodes)
    if not curNode.isRemoved():
        curRisk = curNode.getTotalRiskToHere()

        for neighbour in curNode.getNeighbours().copy():
            alt = curRisk + neighbour.getRisk()

            if (alt < neighbour.getTotalRiskToHere()):
                newNode = copyNodeWithNewTotalRisk(nodeDict[neighbour.X, neighbour.Y], alt)
                nodeDict[(neighbour.X, neighbour.Y)] = newNode
                heappush(unvisitedNodes, newNode)


print("Part 2:", nodeDict[largestX, largestY].getTotalRiskToHere())

end = time.time()
print(end - start)
