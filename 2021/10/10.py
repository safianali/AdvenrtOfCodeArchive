import time
import bisect

start = time.time()

with open("10.txt") as f:
    rawInput = f.read().splitlines()

# part 1

closingCharScores = {')': 3, ']': 57, '}': 1197, '>': 25137}
closingCharMatches = {')': '(', ']': '[', '}': '{', '>': '<'}
totalError = 0
for line in rawInput:
    i = 0
    stack = []

    while i < len(line):
        curChar = line[i]

        if curChar in closingCharMatches:
            if stack and (stack[-1] == closingCharMatches[curChar]):
                stack.pop()
            else:
                totalError += closingCharScores[curChar]
                break
        else:
            stack.append(curChar)

        i += 1

print(totalError)

# part 2

closingCharMatches = {')': '(', ']': '[', '}': '{', '>': '<'}
incompleteStacks = []
for line in rawInput:
    i = 0
    corruptCharFound = False
    stack = []

    while (i < len(line)) and not corruptCharFound:
        curChar = line[i]

        if curChar in closingCharMatches:
            if stack and (stack[-1] == closingCharMatches[curChar]):
                stack.pop()
            else:
                corruptCharFound = True
        else:
            stack.append(curChar)

        i += 1

    if not corruptCharFound:
        incompleteStacks.append(stack[::-1])

openingCharMatches = {v: k for k, v in closingCharMatches.items()}
closingChars = []
for stack in incompleteStacks:
    closingChars.append([openingCharMatches[x] for x in stack])

# print(incompleteStacks)
# print(closingChars)

closingStringScores = []
closingCharScores = {')': 1, ']': 2, '}': 3, '>': 4}

for closingString in closingChars:
    curScore = 0
    for char in closingString:
        curScore *= 5
        curScore += closingCharScores[char]

    bisect.insort(closingStringScores, curScore)

# print(closingStringScores)
print(closingStringScores[len(closingStringScores) // 2])

end = time.time()
print(end - start)
