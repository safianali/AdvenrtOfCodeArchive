class Board:
    
    def __init__(self, boardNo, allNums):
        self.boardNo = boardNo
        self.allNums = allNums
        self.rowList = [set() for i in range(5)]
        self.columnList = [set() for i in range(5)]
        self.populateSets()
        
    def populateSets(self):
        for i in range(5):
            for j in range(5):
                self.rowList[i].add(self.allNums[i][j])
                self.columnList[j].add(self.allNums[i][j])
    
    def removeNumber(self, num):
        for row in self.rowList:
            row.discard(num)
        
        for column in self.columnList:
            column.discard(num)
            
    def sumOfRemainingNums(self):
        return sum(sum(x) for x in self.rowList)       
    
    def hasWon(self):
        for row in self.rowList:
            if len(row) == 0:
                return True
        
        for column in self.columnList:
            if len(column) == 0:
                return True
        
        return False


#part 1

fullInput = [line.strip() for line in open("4.txt")]

bingoNums = [int(x) for x in fullInput[0].split(",")]

boards = set()
boardNo = 0
for i in range(2, len(fullInput), 6):
    allNums = []
    
    for j in range(i, i + 5):
        nextRow = fullInput[j].split(" ")
        nextRow = [int(x) for x in nextRow if x]
        allNums.append(nextRow)
    
    newBoard = Board(boardNo, allNums)
    boards.add(newBoard)
    boardNo += 1

winnerFound = False
winningBoard = None

i = 0
while (not winnerFound):
    for board in boards:
        board.removeNumber(bingoNums[i])
        if board.hasWon():
            winningBoard = board
            winnerFound = True
    
    i += 1
    
print(winningBoard.sumOfRemainingNums() * bingoNums[i - 1])

#part 2

i = 0
while(len(boards) > 1):
    for board in boards.copy():
        board.removeNumber(bingoNums[i])
        if board.hasWon():
            boards.remove(board)
    
    i += 1
    
finalBoard = boards.pop()

while(not finalBoard.hasWon()):
    finalBoard.removeNumber(bingoNums[i])
    i += 1

print(finalBoard.sumOfRemainingNums() * bingoNums[i - 1])

