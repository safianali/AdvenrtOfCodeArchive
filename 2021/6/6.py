input = [line.split(",") for line in open("6.txt")]

#input = [[3, 4, 3, 1, 2]]

#part 1
fishDays = [0] * 9
for fish in input[0]:
    fishDays[int(fish)] += 1
    
#print(fishDays)

noOfDays = 0

while (noOfDays < 80):
    newFishDays = [0] * 9
    newFishDays[8] = fishDays[0]
    newFishDays[6] = fishDays[0]
    
    for i in range(1, len(fishDays)):
        newFishDays[i - 1] += fishDays[i]
        
    fishDays = newFishDays
    noOfDays += 1
        
print(sum(fishDays))

#part 2
fishDays = [0] * 9
for fish in input[0]:
    fishDays[int(fish)] += 1
    
#print(fishDays)

noOfDays = 0

while (noOfDays < 256):
    newFishDays = [0] * 9
    newFishDays[8] = fishDays[0]
    newFishDays[6] = fishDays[0]
    
    for i in range(1, len(fishDays)):
        newFishDays[i - 1] += fishDays[i]
        
    fishDays = newFishDays
    noOfDays += 1
        
print(sum(fishDays))
    
    
        
        
    
