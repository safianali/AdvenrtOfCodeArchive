from operator import attrgetter

import time
start = time.time()

with open("9.txt") as f:
    input = f.read().splitlines()
    
#part 1

# input = ['2199943210',
# '3987894921',
# '9856789892',
# '8767896789',
# '9899965678']

noOfRows = len(input)
totalRisk = 0

for i in range(noOfRows):
    
    noOfCols = len(input[i])
    
    #top row
    if (i == 0):
        for j in range(noOfCols):
            #first column    
            if (j == 0):
                lowestAdjPoint = min(input[i][j + 1], input[i + 1][j])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
            #last column
            elif (j == noOfCols - 1):
                lowestAdjPoint = min(input[i][j - 1], input[i + 1][j])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
            else:
                lowestAdjPoint = min(input[i][j - 1], input[i][j + 1], input[i + 1][j])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
    #last row
    elif (i == noOfRows - 1):
        for j in range(noOfCols):
            #first column
            if (j == 0):
                lowestAdjPoint = min(input[i - 1][j], input[i][j + 1])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
            #last column
            elif (j == noOfCols - 1):
                lowestAdjPoint = min(input[i - 1][j], input[i][j - 1])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
            else:
                lowestAdjPoint = min(input[i - 1][j], input[i][j - 1], input[i][j + 1])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
    else:
        for j in range(noOfCols):
            #first column
            if (j == 0):
                lowestAdjPoint = min(input[i - 1][j], input[i][j + 1], input[i + 1][j])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
            #last column
            elif (j == noOfCols - 1):
                lowestAdjPoint = min(input[i - 1][j], input[i][j - 1], input[i + 1][j])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
            else:
                lowestAdjPoint = min(input[i - 1][j], input[i][j - 1], input[i][j + 1], input[i + 1][j])
                if input[i][j] < lowestAdjPoint:
                    totalRisk += (1 + int(input[i][j]))
        
print(totalRisk)

#part 2

class Point:
    
    def __init__(self, X, Y, val):
        self.X = X
        self.Y = Y
        self.val = val
        self.adjPoints = None
    
    def setAdjPoints(self, adjPoints):
        self.adjPoints = adjPoints
    
    def isNine(self):
        return self.val == 9
    
    
    def getAdjPoints(self):
        return self.adjPoints
        
    def __hash__(self):
        return hash((self.X, self.Y))

    def __eq__(self, other):
        return (self.X, self.Y) == (other.X, other.Y)

points = []
for i in range(noOfRows):
    pointRow = []
    for j in range(len(input[i])):
        pointRow.append(Point(i, j, int(input[i][j])))
    
    points.append(pointRow)


for i in range(noOfRows):
    for j in range(len(input[i])):
        adjPoints = set()
        
        if (i == 0):
            adjPoints.add(points[i + 1][j])
        elif (i == noOfRows - 1):
            adjPoints.add(points[i - 1][j])
        else:
            adjPoints.add(points[i - 1][j])
            adjPoints.add(points[i + 1][j])
        
        if (j == 0):
            adjPoints.add(points[i][j + 1])
        elif (j == (len(input) - 1)):
            adjPoints.add(points[i][j - 1])
        else:
            adjPoints.add(points[i][j - 1])
            adjPoints.add(points[i][j + 1])
        
        points[i][j].setAdjPoints(adjPoints)

inBasin = set()
basins = []

def expandBasin(basin, point):
    basin.add(point)
    inBasin.add(point)
    adjPointsNotInBasin = point.getAdjPoints() - basin
    for point2 in adjPointsNotInBasin:
        if not point2.isNine():
            expandBasin(basin, point2)
                
            
        
    

for i in range(noOfRows):
    for j in range(len(points[i])):
        point = points[i][j]
        if point not in inBasin:
            if not point.isNine():
                newBasin = set()
                basins.append(newBasin)
                expandBasin(newBasin, point)

longestSets = []

longestSets.append(max(basins, key = len))
basins.remove(longestSets[0])
longestSets.append(max(basins, key = len))
basins.remove(longestSets[1])
longestSets.append(max(basins, key = len))

print(len(longestSets[0]) * len(longestSets[1]) * len(longestSets[2]))

end = time.time()
print(end - start)