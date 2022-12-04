import re
import time

start = time.time()

with open("4.txt") as f:
    rawInput = f.read().splitlines()

# part 1

pairs = 0
for line in rawInput:
    nums = [int(x) for x in re.findall(r'\d+', line)]
    if nums[0] <= nums[2] and nums[1] >= nums[3] or nums[0] >= nums[2] and nums[1] <= nums[3]:
        pairs += 1

print(pairs)

# part 2

pairs = 0
for line in rawInput:
    nums = [int(x) for x in re.findall(r'\d+', line)]
    if nums[0] <= nums[2] <= nums[1] or nums[2] <= nums[0] <= nums[3]:
        pairs += 1

print(pairs)

end = time.time()
print(end - start)
