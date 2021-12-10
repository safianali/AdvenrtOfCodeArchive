import os

year = input("Enter year: ")

yearDir = os.path.join(os.getcwd(), year)

os.makedirs(yearDir, exist_ok=True)


def generateTemplate(x):
    return """import time

start = time.time()

with open(\"""" + str(x) + """.txt\") as f:
    rawInput = f.read().splitlines()

# part 1

# part 2

end = time.time()
print(end - start)"""


for i in range(1, 26):
    curYearDir = os.path.join(yearDir, str(i))

    if not os.path.isdir(curYearDir):
        os.makedirs(curYearDir)

        pyFile = os.path.join(curYearDir, str(i) + ".py")
        textFile = os.path.join(curYearDir, str(i) + ".txt")

        file = open(pyFile, 'w+')
        file.write(generateTemplate(i))
        file.close()

        file = open(textFile, 'w+')
        file.close()
