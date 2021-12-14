import time
from collections import Counter, defaultdict
from math import ceil

start = time.time()

with open("14.txt") as f:
    rawInput = f.read().splitlines()

# part 1

curTemplate = list(rawInput[0])

rules = {}
for rule in rawInput[2:]:
    k, v = rule.split(" -> ")
    rules[k] = v

for _ in range(10):
    newCurTemplate = []

    for i in range(len(curTemplate) - 1):
        char1 = curTemplate[i]
        char2 = curTemplate[i + 1]
        newCurTemplate.append(char1)
        newCurTemplate.append(rules[char1 + char2])

    newCurTemplate.append(curTemplate[-1])
    curTemplate = newCurTemplate

# counting chars as you go along in a dict is definitely better but     i forgot
elemCount = Counter(curTemplate).most_common()
mostCommonMinusLeastCommon = elemCount[0][1] - elemCount[-1][1]

print("Part 1:", mostCommonMinusLeastCommon)

# part 2

rulesPart2 = {}

for k, v in rules.items():
    rulesPart2[k] = [k[0] + v, v + k[1]]

curPairCount = defaultdict(int)
for i in range(len(curTemplate) - 1):
    curPairCount[curTemplate[i] + curTemplate[i + 1]] += 1

for _ in range(30):
    newPairCount = defaultdict(int)
    for k, v in curPairCount.items():
        i1, i2 = rulesPart2[k]
        newPairCount[i1] += v
        newPairCount[i2] += v

    curPairCount = newPairCount

elemCount = defaultdict(int)

for k, v in curPairCount.items():
    elemCount[k[0]] += v
    elemCount[k[1]] += v

for k in elemCount.keys():
    elemCount[k] = ceil(elemCount[k] / 2)

elemCount = Counter(elemCount).most_common()
mostCommonMinusLeastCommon = elemCount[0][1] - elemCount[-1][1]

print("Part 2:", mostCommonMinusLeastCommon)

end = time.time()
print(end - start)
