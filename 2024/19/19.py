import time

start = time.time()

with open("19.txt") as f:
    rawInput = f.read().splitlines()

# part 1

smallWords = rawInput[0].split(", ")
targetWords = [word for word in rawInput[2:]]

def canBeMade(smallWords, target):
    dp = [False] * (len(target) + 1)
    dp[0] = True
    
    for i in range(len(target)):
        if dp[i]:
            for word in smallWords:
                if target.startswith(word, i):
                    dp[i + len(word)] = True
    
    return dp[len(target)]

print("Part 1:", sum(1 for target in targetWords if canBeMade(smallWords, target)))

# part 2

def countHowManyWaysItCanBeMade(smallWords, target):
    dp = [0] * (len(target) + 1)
    dp[0] = 1
    
    for i in range(len(target)):
        if dp[i]:
            for word in smallWords:
                if target.startswith(word, i):
                    dp[i + len(word)] += dp[i]
    
    return dp[len(target)]

print("Part 2:", sum(countHowManyWaysItCanBeMade(smallWords, target) for target in targetWords))

end = time.time()
print(end - start)