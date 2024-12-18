import time

start = time.time()

with open("13.txt") as f:
    rawInput = f.read().splitlines()

# part 1
coordSets = [(int(a.split('+')[1].split(',')[0]), int(a.split('+')[2]),
               int(b.split('+')[1].split(',')[0]), int(b.split('+')[2]),
               int(p.split('=')[1].split(',')[0]), int(p.split('=')[2]))
              for a, b, p in zip(rawInput[::4], rawInput[1::4], rawInput[2::4])]

def binarySearch(numA, ax, bx, targetX):
    low = 0
    high = 100
    
    startingX = numA * ax
    while low < high:
        mid = (low + high) // 2
        res = (startingX + mid * bx) - targetX

        if res < 0:
            low = mid + 1
        elif res == 0:
            return mid
        else:
            high = mid
    
    return False
        

def solve(coord_set):
    tokenSpend = None

    ax, ay, bx, by, px, py = coord_set
    XSolutions = set()

    for numA in range(100, -1, -1):
        numB = binarySearch(numA, ax, bx, px)
        if numB:
            XSolutions.add((numA, numB))
    
    XYsolutions = set()
    for numA, numB in XSolutions:
        if numA * ay + numB * by == py:
            XYsolutions.add((numA, numB))
    
    for numA, numB in XYsolutions:
        curSpend = 3 * numA + numB
        if tokenSpend is None or curSpend < tokenSpend:
            tokenSpend = curSpend
    
    return tokenSpend


minTokenSpend = 0

for coordSet in coordSets:
    tokenSpend = solve(coordSet)
    if tokenSpend:
        minTokenSpend += tokenSpend

print("Part 1:", minTokenSpend)

# part 2

# add 10000000000000 to each px and py in coordSets
coordSets = [(ax, ay, bx, by, px + 10000000000000, py + 10000000000000) for ax, ay, bx, by, px, py in coordSets]

def solveSystem(a1, a2, b1, b2, c1, c2):
    """Solves system of two linear equations:
    a1*x + b1*y = c1
    a2*x + b2*y = c2
    where x,y must be non-negative integers
    
    Parameters:
        a1,b1,c1: Coefficients and constant of first equation
        a2,b2,c2: Coefficients and constant of second equation
    
    Returns:
        Tuple (x,y) if non-negative integer solution exists, None otherwise
    """
    det = a1*b2 - a2*b1
    if det == 0:
        return None
        
    # Check if solutions would be integers
    if (c1*b2 - c2*b1) % det != 0 or (a1*c2 - a2*c1) % det != 0:
        return None
        
    x = (c1*b2 - c2*b1) // det
    y = (a1*c2 - a2*c1) // det
    
    return (x, y) if x >= 0 and y >= 0 else None

tokenSpend = 0
for coordSet in coordSets:
    res = solveSystem(*coordSet)
    if res:
        tokenSpend += 3 * res[0] + res[1]

print("Part 2:", tokenSpend)

end = time.time()
print(end - start)