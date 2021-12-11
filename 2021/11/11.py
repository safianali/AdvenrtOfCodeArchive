import time

start = time.time()

with open("11.txt") as f:
    rawInput = f.read().splitlines()

# part 1 and part 2

octupi = [[] for i in range(len(rawInput) + 2)]
octupi[0] = [-10 ** 9] * (len(rawInput) + 2)
octupi[len(rawInput) + 1] = [-10 ** 9] * (len(rawInput) + 2)

for x, line in enumerate(rawInput):
    octupi[x + 1].append(-10 ** 9)
    for y, char in enumerate(line):
        octupi[x + 1].append(int(char))
    octupi[x + 1].append(-10 ** 9)

flashes = 0
steps = 0
inSync = False
while not inSync:
    curFlashers = set()
    flashedThisStep = set()

    for x in range(1, len(octupi) - 1):
        for y in range(1, len(octupi[x]) - 1):
            octupi[x][y] += 1
            if octupi[x][y] > 9:
                hasFlashed = True
                curFlashers.add((x, y))

    while curFlashers:
        for octupus in curFlashers.copy():

            x, y = octupus

            incTheseOctupi = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                              (x, y - 1), (x, y + 1),
                              (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

            for incOctupus in incTheseOctupi:
                if incOctupus in flashedThisStep:
                    continue

                incX, incY = incOctupus

                octupi[incX][incY] += 1
                if octupi[incX][incY] > 9:
                    if (incX, incY) not in curFlashers:
                        curFlashers.add((incX, incY))

            curFlashers.remove(octupus)
            flashedThisStep.add(octupus)
            octupi[x][y] = 0
            flashes += 1

    steps += 1

    if steps == 100:
        print("part 1:", flashes)

    if len(flashedThisStep) == (len(octupi) - 2) ** 2:
        inSync = True
        print("part 2:", steps)

end = time.time()
print(end - start)
