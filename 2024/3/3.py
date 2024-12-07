import time

start = time.time()

with open("3.txt") as f:
    rawInput = f.read().splitlines()

# part 1

def extractNumber(line, start):
    num = ""
    i = start
    while i < len(line) and line[i].isdigit():
        num += line[i]
        i += 1
    return int(num), i

totalResult = 0
for line in rawInput:
    i = 0
    while i < len(line):
        if i + 4 >= len(line) or line[i:i+4] != "mul(":
            i += 1
            continue
            
        i += 4
        firstNum, i = extractNumber(line, i)
        
        if line[i] != ",":
            continue
            
        i += 1
        secondnum, i = extractNumber(line, i)
        
        if line[i] == ")":
            totalResult += firstNum * secondnum
        i += 1

print("Part 1:", totalResult)

# part 2

def checkDisabled(line, start):
    if i+7 >= len(line) or line[i:i+7] != "don't()":
        return False
    
    return True

totalResult = 0
enabled = True
for line in rawInput:
    i = 0
    while i < len(line):
        if not enabled:
            if i + 4 < len(line) and line[i:i+4] == "do()":
                enabled = True
                i += 4
            else:
                i += 1
            continue
        
        if i + 4 >= len(line) or line[i:i+4] != "mul(":
            enabled = not checkDisabled(line, i)
            i += 7 if not enabled else 1
            continue
        
        i += 4
        firstNum, i = extractNumber(line, i)
        
        if line[i] != ",":
            enabled = not checkDisabled(line, i)
            i += 7 if not enabled else 1
            continue
        
        i += 1
        secondnum, i = extractNumber(line, i)
        
        if line[i] == ")":
            totalResult += firstNum * secondnum
        enabled = not checkDisabled(line, i)
        i += 7 if not enabled else 1

print("Part 2:", totalResult)

end = time.time()
print(end - start)