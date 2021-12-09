file = open("2.txt", "r")

##part 1

finalH = 0
finalD = 0

for line in file:
    split = line.split()
    
    if (split[0] == "forward"):
        finalH += int(split[1])
    elif(split[0] == "down"):
        finalD += int(split[1])
    elif(split[0] == "up"):
        finalD -= int(split[1])

print(finalH * finalD)

##part 2

finalH = 0
finalD = 0
aim = 0

file.seek(0)
for line in file:
    split = line.split()
    
    if (split[0] == "forward"):
        finalH += int(split[1])
        finalD += (aim * int(split[1])) 
    elif(split[0] == "down"):
        aim += int(split[1])
    elif(split[0] == "up"):
        aim -= int(split[1])
        
print(finalH * finalD)


        