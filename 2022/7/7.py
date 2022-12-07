import bisect
import re
import time

start = time.time()

with open("7.txt") as f:
    rawInput = f.read().splitlines()

# part 1

class Directory:
    def __init__(self, name, parent):
        # only including files on this level i.e. not child directories
        self.childDirs = {}
        self.name = name
        self.parent = parent
        self.fileSize = 0

    def addChildDir(self, dirName):
        self.childDirs[dirName] = Directory(dirName, self)

    def getChildDir(self, dirName):
        return self.childDirs[dirName]

    def getAllChildDirs(self):
        return self.childDirs.values()

    def addFileSize(self, fileSize):
        self.fileSize += fileSize
    def getFileSize(self):
        return self.fileSize + sum([dir.getFileSize() for dir in self.getAllChildDirs()])

    def getParent(self):
        return self.parent

rootDir = Directory("\\", None)
curDir = rootDir

numLines = len(rawInput)
curLineIdx = 1
while curLineIdx < numLines:
    match rawInput[curLineIdx][0:4]:
        case "$ cd":
            if rawInput[curLineIdx][5] == ".":
                curDir = curDir.getParent()
            else:
                curDir = curDir.getChildDir(rawInput[curLineIdx][5:])

            curLineIdx += 1
        case "$ ls":
            curLineIdx += 1
            fileSize = 0
            while curLineIdx < numLines and rawInput[curLineIdx][0] != "$":
                if rawInput[curLineIdx][0] == "d":
                    curDir.addChildDir(rawInput[curLineIdx][4:])
                else:
                    curDir.addFileSize(int(re.findall('\d+', rawInput[curLineIdx])[0]))
                curLineIdx += 1

def getSumDirsLessThanX(dir, x):
    sm = dir.getFileSize()
    if sm > x:
        sm = 0

    for child in dir.getAllChildDirs():
        sm += getSumDirsLessThanX(child, x)

    return sm

print(getSumDirsLessThanX(rootDir, 100000))

# part 2

def getAllDirSizes(dir):
    dirSizes = []

    for child in dir.getAllChildDirs():
        dirSizes += getAllDirSizes(child)

    dirSizes.append(dir.getFileSize())
    return dirSizes

allDirSizes = getAllDirSizes(rootDir)
allDirSizes.sort()

target = rootDir.getFileSize() - 40000000
print(allDirSizes[bisect.bisect_left(allDirSizes, target)])

end = time.time()
print(end - start)