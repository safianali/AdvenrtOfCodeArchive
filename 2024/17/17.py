import time
import heapq

start = time.time()

with open("17.txt") as f:
    rawInput = f.read().splitlines()

# part 1

regA = int(rawInput[0].split(": ")[1])
regB = int(rawInput[1].split(": ")[1])
regC = int(rawInput[2].split(": ")[1])

program = [int(x) for x in rawInput[4].split(": ")[1].split(",")]

def runProgram(program, input_A, input_B, input_C):
    A = input_A
    B = input_B
    C = input_C
    pointerIdx = 0
    output = []

    def getComboValue(operand):
        # if operand is between 0 and 3
        if operand < 4:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C

    while True:
        if pointerIdx >= len(program):
            break
        opcode = program[pointerIdx]
        operand = program[pointerIdx + 1]

        if opcode == 0:
            A = A // (2 ** getComboValue(operand))
            pointerIdx += 2
        elif opcode == 1:
            B = B ^ operand
            pointerIdx += 2
        elif opcode == 2:
            B = getComboValue(operand) % 8
            pointerIdx += 2
        elif opcode == 3:
            if A != 0:
                pointerIdx = operand
            else:
                pointerIdx += 2
        elif opcode == 4:
            B = B ^ C
            pointerIdx += 2
        elif opcode == 5:
            output.append(getComboValue(operand) % 8)
            pointerIdx += 2
        elif opcode == 6:
            B = A // (2 ** getComboValue(operand))
            pointerIdx += 2
        elif opcode == 7:
            C = A // (2 ** getComboValue(operand))
            pointerIdx += 2
    
    return output
    
print("Part 1:", ",".join(str(x) for x in runProgram(program, regA, regB, regC)))

# part 2

# following code was used to find the pattern in the output
# it's of no use now

# lastThreeDigitsInOutputs = []
# for candidateA in range(10000):
#     output = runProgram(program, candidateA, regB, regC)
#     print("Candidate A:", candidateA, "Output:", output)
#     last_three = (tuple(output[-3:]) if len(output) >= 3 else 
#                  (None, *tuple(output)) if len(output) == 2 else
#                  (None, None, output[-1]) if output else 
#                  (None, None, None))
#     lastThreeDigitsInOutputs.append((last_three, len(output)))

# newDigitsInOutputs = [(0, lastThreeDigitsInOutputs[0][0], lastThreeDigitsInOutputs[0][1])]
# for i in range(1, len(lastThreeDigitsInOutputs)):
#     if lastThreeDigitsInOutputs[i][0] != lastThreeDigitsInOutputs[i - 1][0]:
#         newDigitsInOutputs.append((i, lastThreeDigitsInOutputs[i][0], lastThreeDigitsInOutputs[i][1]))

# print("\nChanges in output pattern:")
# print(f"{'A Value':<15} | {'Last Three Digits':<20} | {'Output Length':<12}")
# print("-" * 51)
# for idx, (a_val, last_digits, output_len) in enumerate(newDigitsInOutputs):
#     diff = f" (+{a_val - newDigitsInOutputs[idx-1][0]})" if idx > 0 else ""
#     last_digits_str = f"{last_digits[0]},{last_digits[1]},{last_digits[2]}" if last_digits[0] is not None else f"None,{last_digits[1]},{last_digits[2]}"
#     print(f"{a_val}{diff:<15} | {last_digits_str:<20} | {output_len:<12}")

def getLengthWithA(A):
    return [len(runProgram(program, A, regB, regC)), len(runProgram(program, A + 1, regB, regC))]

desiredLength = len(program)

def getFirstAWithLength(desiredLength):
    low = 0
    high = 10**20

    while low < high:
        mid = (low + high) // 2
        curLength = getLengthWithA(mid)
        if curLength[0] <= desiredLength - 1 and curLength[1] != desiredLength:
            low = mid + 1
        else:
            high = mid
    
    return low + 1

print("First A with length", desiredLength, ":", getFirstAWithLength(desiredLength))
print("First A with length", desiredLength + 1, ":", getFirstAWithLength(desiredLength + 1))

def checkIfOutputMatches(A, expectedOutput, lastXDigits):
    actualOutput = runProgram(program, A, regB, regC)
    return actualOutput[-lastXDigits:] == expectedOutput[-lastXDigits:]

# value = (0 < x0 <= 8) * 8^15 + (0 < x1 <= 8) * 8^13 + (0 < x2 <= 8) * 8^12 ...
# where x0 affects the last digit in the output, x1 affects the second last digit and so on
# need to do BFS

def convertToA(digits):
    return sum([digits[i] * 8 ** (desiredLength - 1 - i) for i in range(len(digits))])

# currentA is a list of up to 16 integers. This list can be converted to a guess for A by
# calculating sum([currentA[i] * 8 ** (15 - i) for i in range(16)])
def getValue(currentADigits, desiredOutput):
    currentLevel = len(currentADigits)
    if currentLevel == len(desiredOutput):
        currentA = convertToA(currentADigits)
        return currentA if checkIfOutputMatches(currentA, desiredOutput, len(desiredOutput)) else None
    
    children = []
    for i in range(16):
        if checkIfOutputMatches(convertToA(currentADigits + [i]), desiredOutput, currentLevel + 1):
            heapq.heappush(children, currentADigits + [i])
    
    while children:
        child = heapq.heappop(children)
        result = getValue(child, desiredOutput)
        if result:
            return result
    
    return None

print("Part 2:", getValue([], program))

end = time.time()
print(end - start)