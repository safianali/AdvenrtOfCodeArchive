import time

start = time.time()

with open("3.txt") as f:
    rawInput = f.read().splitlines()


def getPriority(x):
    ascVal = ord(x)
    if ascVal >= 97:
        return ascVal - 96
    else:
        return ascVal - 38


# part 1

sum = 0
for rucksack in rawInput:
    halfLen = len(rucksack) // 2
    firstHalfChars = set()

    for i in range(halfLen):
        firstHalfChars.add(rucksack[i])

    i = halfLen

    while True:
        if rucksack[i] in firstHalfChars:
            sum += getPriority(rucksack[i])
            break
        else:
            i += 1

print(sum)

# part 2

sum = 0
for i in range(0, len(rawInput), 3):
    elf0 = rawInput[i]
    elf1 = rawInput[i + 1]
    elf2 = rawInput[i + 2]

    set0 = set()
    set1 = set()

    for item in elf0:
        set0.add(item)

    for item in elf1:
        if item in set0:
            set1.add(item)

    for item in elf2:
        if item in set1:
            sum += getPriority(item)
            break

print(sum)

end = time.time()
print(end - start)
