class Point:
    
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        
    def __hash__(self):
        return hash((self.X, self.Y))

    def __eq__(self, other):
        return (self.X, self.Y) == (other.X, other.Y)

#must be x1 <= x2 and y1 <= y2
def generatePoints(x1, x2, y1, y2, isHorizontal):
    points = []
    if isHorizontal:
        for x in range(x1, x2 + 1):
            points.append(Point(x, y1))
    else:
        for y in range(y1, y2 + 1):
            points.append(Point(x1, y))
    
    return points
    

#part 1

input = [line.strip() for line in open("5.txt")]

input = [x.split(" -> ") for x in input]

input = [[x[0].split(","), x[1].split(",")] for x in input]

input = [[[int(x[0][0]), int(x[0][1])], [int(x[1][0]), int(x[1][1])]] for x in input]

onlyStraightLines = [x for x in input if x[0][0] == x[1][0] or x[0][1] == x[1][1]]

#print(onlyStraightLines)

touchedPoints = {}

for line in onlyStraightLines:
    x1 = line[0][0]
    x2 = line[1][0]
    y1 = line[0][1]
    y2 = line[1][1]
    if x1 == x2:
        pointsFromLine = generatePoints(x1, x2, min(y1, y2), max(y1, y2), False)
    else:
        pointsFromLine = generatePoints(min(x1, x2), max(x1, x2), y1, y2, True)
    
    #print(x1, y1)
    #print(x2, y2)
    #print(len(pointsFromLine))
    
    for point in pointsFromLine:
        if point in touchedPoints:
            touchedPoints[point] += 1
        else:
            touchedPoints[point] = 1

print(len([k for k, v in touchedPoints.items() if v > 1]))

#part 2

#must have x1 < x2
def generateDiagonalPoints(x1, x2, y1, y2):
    points = []
    if (y1 < y2):
        for i in range(0, (y2 - y1) + 1):
            points.append(Point(x1 + i, y1 + i))
    else:
        for i in range(0, (y1 - y2) + 1):
            points.append(Point(x1 + i, y1 - i))
    
    return points
            

#not sure why these are lists tbh, i think nearly every usage of lists here could be replaced with sets
#since order is not required
onlyDiagonalLines = [x for x in input if not (x[0][0] == x[1][0] or x[0][1] == x[1][1])]

#print(len(onlyStraightLines))
#print(len(onlyDiagonalLines))

for line in onlyDiagonalLines:
    x1 = line[0][0]
    x2 = line[1][0]
    y1 = line[0][1]
    y2 = line[1][1]
    
    if (x1 < x2):
        pointsFromLine = generateDiagonalPoints(x1, x2, y1, y2)
    else:
        pointsFromLine = generateDiagonalPoints(x2, x1, y2, y1)
        
    for point in pointsFromLine:
        if point in touchedPoints:
            touchedPoints[point] += 1
        else:
            touchedPoints[point] = 1

print(len([k for k, v in touchedPoints.items() if v > 1]))
    
