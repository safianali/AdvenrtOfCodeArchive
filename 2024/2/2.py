import time

start = time.time()

with open("2.txt") as f:
    rawInput = f.read().splitlines()

# part 1

# returns -1 if the report is valid, otherwise returns the index of the second
# number in the first invalid pair
def checkReport(levels):
    if levels[1] - levels[0] in [1, 2, 3]:
        increasing = True
    elif levels[1] - levels[0] in [-1, -2, -3]:
        increasing = False
    else:
        return 1

    allowed_diffs = [1, 2, 3] if increasing else [-1, -2, -3]
    for i in range(2, len(levels)):
        if levels[i] - levels[i - 1] not in allowed_diffs:
            return i
    
    return -1

numSafe = 0
for report in rawInput:
    levels = [int(level) for level in report.split(" ")]
    numSafe += 1 if checkReport(levels) == -1 else 0

print("Part 1:", numSafe)       

# part 2

numSafe = 0
for report in rawInput:
    levels = [int(level) for level in report.split(" ")]
    idx = checkReport(levels)
    
    if idx == -1:
        numSafe += 1
        continue
    
    # if the pair (idx-1, idx) aren't working, then it's possible that levels
    # could work if either idx, idx-1, or idx-2 are removed
    for i in range(idx, max(idx-3, -1), -1):
        test_levels = levels.copy()
        test_levels.pop(i)
        if checkReport(test_levels) == -1:
            numSafe += 1
            break

print("Part 2:", numSafe)

end = time.time()
print(end - start)