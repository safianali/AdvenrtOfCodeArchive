import time

start = time.time()

with open("20.txt") as f:
    rawInput = f.read().splitlines()

#only works if algo[0] is #

# part 1

algo = rawInput[0]
rawImage = rawInput[2:]

ogLen = len(rawImage[0])
ogHeight = len(rawImage)
paddedLen = ogLen + 6

paddedImage = []

for _ in range(3):
    paddedImage.append('.' * paddedLen)

for row in rawImage:
    newRow = "..."
    newRow += row
    newRow += "..."
    paddedImage.append(newRow)

for _ in range(3):
    paddedImage.append('.' * paddedLen)

newImage = []


def getChar(b):
    val = 0
    for idx, char in enumerate(b[::-1]):
        val += (2 ** idx) if char == '#' else 0

    return algo[val]


for _ in range(2):
    newImage.append('#' * paddedLen)

for i in range(2, ogLen + 4):
    newRow = "##"
    for j in range(2, ogLen + 4):
        string = paddedImage[i - 1][j - 1] + paddedImage[i - 1][j] + paddedImage[i - 1][j + 1] \
                 + paddedImage[i][j - 1] + paddedImage[i][j] + paddedImage[i][j + 1] \
                 + paddedImage[i + 1][j - 1] + paddedImage[i + 1][j] + paddedImage[i + 1][j + 1]

        newRow += getChar(string)

    newRow += "##"
    newImage.append(newRow)

for _ in range(2):
    newImage.append('#' * paddedLen)

finalImage = ['.' * paddedLen]

for i in range(1, ogLen + 5):
    newRow = "."
    for j in range(1, ogLen + 5):
        string = newImage[i - 1][j - 1] + newImage[i - 1][j] + newImage[i - 1][j + 1] \
                 + newImage[i][j - 1] + newImage[i][j] + newImage[i][j + 1] \
                 + newImage[i + 1][j - 1] + newImage[i + 1][j] + newImage[i + 1][j + 1]

        newRow += getChar(string)

    newRow += "."
    finalImage.append(newRow)

count = 0

for row in finalImage:
    for char in row:
        if char == '#':
            count += 1

print("Part 1:", count)

# part 2

padLen = 51
paddedLen = ogLen + (padLen * 2)

curImage = []

for _ in range(padLen):
    curImage.append('.' * paddedLen)

for row in rawImage:
    newRow = "." * padLen
    newRow += row
    newRow += "." * padLen
    curImage.append(newRow)

for _ in range(padLen):
    curImage.append('.' * paddedLen)

curPadChar = '.'
padLen -= 1

for n in range(50):
    newImage = []

    if curPadChar == '.':
        curPadChar = '#'
    else:
        curPadChar = '.'

    for _ in range(padLen - n):
        newImage.append(curPadChar * paddedLen)

    for i in range(padLen - n, ogLen + padLen + 2 + n):
        newRow = curPadChar * (padLen - n)
        for j in range(padLen - n, ogLen + padLen + 2 + n):
            string = curImage[i - 1][j - 1] + curImage[i - 1][j] + curImage[i - 1][j + 1] \
                     + curImage[i][j - 1] + curImage[i][j] + curImage[i][j + 1] \
                     + curImage[i + 1][j - 1] + curImage[i + 1][j] + curImage[i + 1][j + 1]

            newRow += getChar(string)

        newRow += curPadChar * (padLen - n)
        newImage.append(newRow)

    for _ in range(padLen - n):
        newImage.append(curPadChar * paddedLen)

    curImage = newImage

count = 0

for row in curImage:
    for char in row:
        if char == '#':
            count += 1

print("Part 2:", count)

end = time.time()
print(end - start)
