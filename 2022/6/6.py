import collections
import time

start = time.time()

with open("6.txt") as f:
    rawInput = f.read().splitlines()


# part 1
def isSOP(x):
    charSet = set(x)
    return len(charSet) == len(x)


def findMarker(message, numUnique):
    curIdx = numUnique
    initChars = [x for x in message[0:curIdx]]
    buffer = collections.deque(initChars)
    found = False

    for char in message[curIdx:]:
        if isSOP(buffer):
            print(curIdx)
            found = True
            break

        curIdx += 1
        buffer.popleft()
        buffer.append(char)

    if not found:
        print(curIdx)


findMarker(rawInput[0], 4)

# part 2

findMarker(rawInput[0], 14)

end = time.time()
print(end - start)
