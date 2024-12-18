import time
from collections import Counter
import heapq

start = time.time()

with open("14.txt") as f:
    rawInput = f.read().splitlines()

# part 1
xLen = 101
yLen = 103

NE, NW, SE, SW = range(1, 5)

class Robot:
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def __str__(self):
        return f"Position(x={self.pos_x}, y={self.pos_y}, vx={self.vel_x}, vy={self.vel_y}, quadrant={self.getQuadrant()})"
    
    def __repr__(self):
        return self.__str__()
    
    def copy(self):
        return Robot(
            pos_x=self.pos_x,
            pos_y=self.pos_y, 
            vel_x=self.vel_x,
            vel_y=self.vel_y
        )
    
    def move(self):
        self.pos_x = (self.pos_x + self.vel_x) % xLen
        self.pos_y = (self.pos_y + self.vel_y) % yLen

    def getQuadrant(self):
        if self.pos_x == xLen // 2 or self.pos_y == yLen // 2:
            return None
        
        x_right = self.pos_x > xLen // 2
        y_bottom = self.pos_y > yLen // 2
        
        if x_right:
            return SE if y_bottom else NE
        return SW if y_bottom else NW
    
    @classmethod
    def from_string(cls, line):
        pos, vel = line.split()
        pos_x, pos_y = map(int, pos[2:].split(','))
        vel_x, vel_y = map(int, vel[2:].split(','))
        return cls(pos_x, pos_y, vel_x, vel_y)

robots = set()
for line in rawInput:
    robots.add(Robot.from_string(line))
robotsCopy = {robot.copy() for robot in robots}

for i in range(100):
    for robot in robots:
        robot.move()

quadrants = Counter(robot.getQuadrant() for robot in robots if robot.getQuadrant() is not None)
print("Part 1:", quadrants[NE] * quadrants[NW] * quadrants[SE] * quadrants[SW])

# part 2
def printGrid(positions):
    for y in range(yLen):
        for x in range(xLen):
            if (x, y) in positions:
                print('X', end='')
            else:
                print('.', end='')
        print()

def calculate_clumpiness(positions):
    """
    Measures how clumped together positions are by:
    1. Dividing grid into sectors
    2. Counting positions per sector
    3. Calculating variance of counts (higher variance = more clumped)
    """
    # Create 10x10 sectors
    sector_size = 10
    sectors = {}
    
    # Count positions in each sector
    for x, y in positions:
        sector_x = x // sector_size
        sector_y = y // sector_size
        sector = (sector_x, sector_y)
        sectors[sector] = sectors.get(sector, 0) + 1
    
    if not sectors:
        return 0
        
    # Calculate variance of sector counts
    counts = list(sectors.values())
    avg = sum(counts) / len(counts)
    variance = sum((c - avg) ** 2 for c in counts) / len(counts)
    
    return variance

def gridToString(positions, xLen, yLen):
    output = ""
    for y in range(yLen):
        for x in range(xLen):
            output += 'X' if (x, y) in positions else '.'
        output += '\n'
    return output

# Clear the output file
with open('grids.txt', 'w') as f:
    f.write("Starting simulation\n")

clumpiness_data = []

for i in range(10000):
    positions = {(robot.pos_x, robot.pos_y) for robot in robotsCopy}
    
    clumpiness = calculate_clumpiness(positions)
    clumpiness_data.append((clumpiness, i))
    
    with open('grids.txt', 'a') as f:
        f.write(f"\nIteration {i}\n")
        f.write(gridToString(positions, xLen, yLen))
    
    for robot in robotsCopy:
        robot.move()

print("\nPart 2: Cannot be done deterministically, but the most clumpy iteration is likely the answer.")
print("Check grids.txt for the grids of the most clumpy iterations to verify.")


top_clumpy = heapq.nlargest(5, clumpiness_data)
print("\nTop 5 clumpiest iterations:")
for clumpiness, iteration in top_clumpy:
    print(f"Iteration {iteration}: Clumpiness = {clumpiness:.2f}")

end = time.time()
print(end - start)