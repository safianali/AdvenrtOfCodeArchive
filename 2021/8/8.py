with open("8.txt") as f:
    input = f.read().splitlines()

#part 1

outputCount = [0] * 10

for line in input:
    signals, outputs = line.split(" | ")
    
    signals = signals.split(" ")
    outputs = outputs.split(" ")
    
    for output in outputs:
        currentCharSet = set()
        for char in output:
            currentCharSet.add(char)
        
        if len(currentCharSet) == 2:
            outputCount[0] += 1
        elif len(currentCharSet) == 4:
            outputCount[3] += 1
        elif len(currentCharSet) == 3:
            outputCount[6] += 1
        elif len(currentCharSet) == 7:
            outputCount[7] += 1
    
print(sum(outputCount))

#part 2

outputSum = 0

for line in input:
    signals, outputs = line.split(" | ")
    
    signals = signals.split(" ")
    outputs = outputs.split(" ")
    
    charDict = {}
    unknownCharSet = set()
    for signal in signals:
        currentCharSet = set()
        for char in signal:
            currentCharSet.add(char)
        
        if len(currentCharSet) == 2:
            charDict[1] = frozenset(currentCharSet)
        elif len(currentCharSet) == 4:
            charDict[4] = frozenset(currentCharSet)
        elif len(currentCharSet) == 3:
            charDict[7] = frozenset(currentCharSet)
        elif len(currentCharSet) == 7:
            charDict[8] = frozenset(currentCharSet)
        else:
            unknownCharSet.add(frozenset(currentCharSet))
    
    
    for val in set(unknownCharSet):
        if val.issuperset(charDict[4]):
            if len(val) == 6:
                charDict[9] = val
                unknownCharSet.remove(val)
    
    for val in set(unknownCharSet):
        if val.issuperset(charDict[7]):
            if len(val) == 5:
                charDict[3] = val
                unknownCharSet.remove(val)
            elif len(val) == 6:
                charDict[0] = val
                unknownCharSet.remove(val)
    
    for val in set(unknownCharSet):
        if len(val) == 6:
            charDict[6] = val
            unknownCharSet.remove(val)
    
    for val in set(unknownCharSet):
        if val.issubset(charDict[6]):
            charDict[5] = val
            unknownCharSet.remove(val)
        else:
            charDict[2] = val
            unknownCharSet.remove(val)
    
    outputString = ''
    for output in outputs:
        currentCharSet = set()
        for char in output:
            currentCharSet.add(char)
        
        for k, v in charDict.items():
            if v == currentCharSet:
                outputString += str(k)
    
    outputSum += int(outputString)
    
print(outputSum)