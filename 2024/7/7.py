import time

start = time.time()

with open("7.txt") as f:
    rawInput = f.read().splitlines()

# part 1

processed_lines = []
for line in rawInput:
    first, second = line.split(':')
    numbers = [int(first)] + [int(x) for x in second.split()]
    processed_lines.append(numbers)

def getBinaryPermutations(length):
    width = len(line) - 1
    nums = []
    for i in range(2 ** width):
        nums.append(bin(i)[2:].zfill(width))
    
    return nums

def checkMatch(line, permutation):
    result = line[1]
    for operator, num in enumerate(line[2:]):
        if permutation[operator] == '1':
            result *= num
        else:
            result += num
    
    return result == line[0]

        
totalResult = 0
for line in processed_lines:
    for permutation in getBinaryPermutations(len(line) - 2):
        if checkMatch(line, permutation):
            totalResult += line[0]
            break

print("Part 1:", totalResult)
   
# part 2

def ter(decimal):
    if decimal == 0:
        return "0"
    ternary = ""
    while decimal > 0:
        ternary = str(decimal % 3) + ternary
        decimal //= 3
    return ternary

def getTernaryPermutations(length):
    width = len(line) - 1
    nums = []
    for i in range(3 ** width):
        nums.append(ter(i).zfill(width))
    
    return nums

def checkTernaryMatch(line, permutation):
    result = line[1]
    for operator, num in enumerate(line[2:]):
        if permutation[operator] == '2':
            result = int(str(result) + str(num))
        elif permutation[operator] == '1':
            result *= num
        else:
            result += num
    
    return result == line[0]

totalResult = 0
for line in processed_lines:
    for permutation in getTernaryPermutations(len(line) - 2):
        if checkTernaryMatch(line, permutation):
            totalResult += line[0]
            break

print("Part 2:", totalResult)

end = time.time()
print(end - start)