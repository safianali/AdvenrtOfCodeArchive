import copy

#part 1
with open("3.txt") as f:
    length = len(f.readline().strip())

noOfLines = 0
countOnes = dict.fromkeys(range(length), 0)

with open("3.txt") as f:
    for line in f:
        for i, char in enumerate(line.strip()):
            if char == "1":
                countOnes[i] += 1
        
        noOfLines += 1

threshold = noOfLines // 2

gamma = ""
epsilon = ""

for key in sorted(countOnes):
    if countOnes[key] > threshold:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"
        

print(int(gamma, 2) * int(epsilon, 2))

#part 2
#a better way to do this would be to make 2 copies of the countOnes dict
#and update it as items are removed from each list, rather than recalculating 
#the most common bit length times

oxygen = [line.strip() for line in open("3.txt")]

co2 = copy.copy(oxygen)

i = 0
while (len(oxygen) != 1):
    count = 0
    
    for num in oxygen:
        if num[i] == "1":
            count += 1
    mc = "1" if (count * 2 >= len(oxygen)) else "0"
    
    for num in list(oxygen):
        if num[i] != mc and len(oxygen) > 1:
            oxygen.remove(num)
    i += 1
            
i = 0
while (len(co2) != 1):
    count = 0
    
    for num in co2:
        if num[i] == "1":
            count += 1
    lc = "0" if (count * 2 >= len(co2)) else "1"
    
    for num in list(co2):
        if num[i] != lc and len(co2) > 1:
            co2.remove(num)
    
    i += 1

print(int(oxygen[0], 2) * int(co2[0], 2))

        




            
    

