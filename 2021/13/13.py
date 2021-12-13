import time

start = time.time()

with open("13.txt") as f:
    rawInput = f.read().splitlines()

# part 1

emptyStringReached = False
i = 0
origXY = set()
largestX = 0
largestY = 0
while not emptyStringReached:
    if rawInput[i] != '':
        x, y = [int(k) for k in rawInput[i].split(',')]
        origXY.add((x, y))
        largestX = x if x > largestX else largestX
        largestY = y if y > largestY else largestY
    else:
        emptyStringReached = True

    i += 1

foldInstructions = rawInput[i:]


def countDots(paper, largestX, largestY):
    dots = 0
    for y in range(largestY + 1):
        for x in range(largestX + 1):
            if paper[y][x] == 1:
                dots += 1

    return dots


paper = [[False] * (largestX + 1) for i in range(largestY + 1)]

for coords in origXY:
    x, y = coords
    paper[y][x] = True

firstInstruction = foldInstructions[0].removeprefix('fold along ').split('=')

foldAt = int(firstInstruction[1])

for y in range(0, largestY + 1):
    for x in range(1, 1 + largestX - foldAt):
        paper[y][foldAt - x] |= paper[y][foldAt + x]

largestX = foldAt - 1

print("part 1:", countDots(paper, largestX, largestY))

# part 2

instructions = map(lambda x: x.removeprefix('fold along ').split('='), foldInstructions[1:])

for curIns in instructions:
    foldAt = int(curIns[1])

    if curIns[0] == 'x':
        for y in range(0, largestY + 1):
            for x in range(1, 1 + largestX - foldAt):
                paper[y][foldAt - x] |= paper[y][foldAt + x]

        largestX = foldAt - 1
    else:
        for y in range(1, 1 + largestY - foldAt):
            for x in range(0, largestX + 1):
                paper[foldAt - y][x] |= paper[foldAt + y][x]

        largestY = foldAt - 1


def printPaper(paper, largestX, largestY):
    for y in range(largestY + 1):
        for x in range(largestX + 1):
            if paper[y][x]:
                print('█', end='')
            else:
                print(' ', end='')

        print('')


print("part 2: ")
printPaper(paper, largestX, largestY)

end = time.time()
print(end - start)
