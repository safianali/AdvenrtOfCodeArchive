import time
from collections import Counter

start = time.time()

with open("11.txt") as f:
    rawInput = f.read().splitlines()

# part 1

def getNewStone(stoneNum):
    match stoneNum:
        case 0:
            return [1]
        case n if len(str(n)) % 2 == 0:
            numStr = str(n)
            mid = len(numStr) // 2
            first_half = int(numStr[:mid])
            second_half = int(numStr[mid:])
            return (first_half, second_half)
        case _:
            return [stoneNum * 2024]

stones = Counter(map(int, rawInput[0].split()))
stonesCopy = stones.copy()

for i in range(25):
    newStones = Counter()

    for stone, count in stones.items():
        for newStone in getNewStone(stone):
            newStones[newStone] += count

    stones = newStones

print("Part 1:", stones.total())

# part 2

for i in range(75):
    newStones = Counter()

    for stone, count in stonesCopy.items():
        for newStone in getNewStone(stone):
            newStones[newStone] += count

    stonesCopy = newStones

print("Part 2:", stonesCopy.total())

end = time.time()
print(end - start)