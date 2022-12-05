import time

start = time.time()

with open("5.txt") as f:
    rawInput = f.read().splitlines()

# part 1

stacks = [[] for _ in range(9)]
for line in rawInput:
    if line[1] == "1":
        break

    for stackIdx, crateIdx in enumerate(range(1, 34, 4)):
        if line[crateIdx] != " ":
            stacks[stackIdx].append(line[crateIdx])

for stack in stacks:
    stack.reverse()

for line in rawInput:
    if line == "" or line[0] != "m":
        continue

    splitLine = line.split()
    numCrates, srcStack, dstStack = int(splitLine[1]), int(splitLine[3]) - 1, int(splitLine[5]) - 1

    for _ in range(numCrates):
        stacks[dstStack].append(stacks[srcStack].pop())

print(''.join([stack[-1] for stack in stacks]))

# part 2

stacks = [[] for _ in range(9)]
for line in rawInput:
    if line[1] == "1":
        break

    for stackIdx, crateIdx in enumerate(range(1, 34, 4)):
        if line[crateIdx] != " ":
            stacks[stackIdx].append(line[crateIdx])

for stack in stacks:
    stack.reverse()

for line in rawInput:
    if line == "" or line[0] != "m":
        continue

    splitLine = line.split()
    numCrates, srcStack, dstStack = int(splitLine[1]), int(splitLine[3]) - 1, int(splitLine[5]) - 1

    cratesToMove = stacks[srcStack][-numCrates:]
    for crate in cratesToMove:
        stacks[srcStack].pop()
        stacks[dstStack].append(crate)

print(''.join([stack[-1] for stack in stacks]))

end = time.time()
print(end - start)