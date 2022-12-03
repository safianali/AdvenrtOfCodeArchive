import time

start = time.time()

with open("2.txt") as f:
    rawInput = f.read().splitlines()

# part 1

scoreDict1 = {
    "A X": 4,
    "B X": 1,
    "C X": 7,
    "A Y": 8,
    "B Y": 5,
    "C Y": 2,
    "A Z": 3,
    "B Z": 9,
    "C Z": 6
}

totalScore = 0
for game in rawInput:
    totalScore += scoreDict1[game]

print(totalScore)

# part 2

scoreDict2 = {
    "A X": 3,
    "B X": 1,
    "C X": 2,
    "A Y": 4,
    "B Y": 5,
    "C Y": 6,
    "A Z": 8,
    "B Z": 9,
    "C Z": 7
}

totalScore = 0
for game in rawInput:
    totalScore += scoreDict2[game]

print(totalScore)

end = time.time()
print(end - start)
