import collections
import copy
import sys
from typing import Dict

#sorry this code is really terrible, i was working quickly

MAX_FLOOR = 3

class Item:

    def __init__(self, id, isMicrochip):
        self.id = id
        self.isMicrochip = isMicrochip

class Node:
    
    def __init__(self, personFloor, floorItemLists):
        self.personFloor = personFloor
        self.floorItemLists = floorItemLists
        
    def possibleNodes(self):
        itemsOnFloor = self.copyOfFloorItemLists()[self.personFloor]
        possibleNodes = []
        
        if (self.personFloor == MAX_FLOOR):
            for i in range(len(itemsOnFloor)):
                newNode = self.moveDownOneItem(i)
                if newNode:
                    possibleNodes.append(newNode)
                if (len(itemsOnFloor) > 1):
                    for j in range(i + 1, len(itemsOnFloor)):
                        newNode = self.moveDownTwoItems(i, j)
                        if newNode:
                            possibleNodes.append(newNode)
        elif (self.personFloor == 0):
            for i in range(len(itemsOnFloor)):
                newNode = self.moveUpOneItem(i)
                if newNode:
                    possibleNodes.append(newNode)
                if (len(itemsOnFloor) > 1):
                    for j in range(i + 1, len(itemsOnFloor)):
                        newNode = self.moveUpTwoItems(i, j)
                        if newNode:
                            possibleNodes.append(newNode)
        else:
            for i in range(len(itemsOnFloor)):
                newNode = self.moveUpOneItem(i)
                if newNode:
                    possibleNodes.append(newNode)
                
                newNode = self.moveDownOneItem(i)
                if newNode:
                    possibleNodes.append(newNode)
                
                if (len(itemsOnFloor) > 1):
                    for j in range(i + 1, len(itemsOnFloor)):
                        newNode = self.moveUpTwoItems(i, j)
                        if newNode:
                            possibleNodes.append(newNode)
                        
                        newNode = self.moveDownTwoItems(i, j)
                        if newNode:
                            possibleNodes.append(newNode)
        
        return [x for x in possibleNodes if x.isValid()]
            
                
    def moveUpOneItem(self, i):
        newFloorItemLists = self.copyOfFloorItemLists()
        item = newFloorItemLists[self.personFloor].pop(i)
        
        if not self.isRemovalValid(item):
            return None
        
        newFloorItemLists[self.personFloor + 1].append(item)
        return Node(self.personFloor + 1, newFloorItemLists)
    
    def moveDownOneItem(self, i):
        newFloorItemLists = self.copyOfFloorItemLists()
        item = newFloorItemLists[self.personFloor].pop(i)
        
        if not self.isRemovalValid(item):
            return None
        
        newFloorItemLists[self.personFloor - 1].append(item)
        return Node(self.personFloor - 1, newFloorItemLists)
    
    def moveUpTwoItems(self, i, j):
        newFloorItemLists = self.copyOfFloorItemLists()
        item1 = newFloorItemLists[self.personFloor].pop(i)
        item2 = newFloorItemLists[self.personFloor].pop(j - 1)
        
        if not self.isMultipleRemovalValid(item1, item2):
            return None
        
        newFloorItemLists[self.personFloor + 1].append(item1)
        newFloorItemLists[self.personFloor + 1].append(item2)
        return Node(self.personFloor + 1, newFloorItemLists)
    
    def moveDownTwoItems(self, i, j):
        newFloorItemLists = self.copyOfFloorItemLists()
        item1 = newFloorItemLists[self.personFloor].pop(i)
        item2 = newFloorItemLists[self.personFloor].pop(j - 1)
        
        if not self.isMultipleRemovalValid(item1, item2):
            return None
        
        newFloorItemLists[self.personFloor - 1].append(item1)
        newFloorItemLists[self.personFloor - 1].append(item2)
        return Node(self.personFloor - 1, newFloorItemLists)
    
    def copyOfFloorItemLists(self):
        newList = []
        
        for i in range(MAX_FLOOR + 1):
            newList.append(copy.copy(self.floorItemLists[i]))
        
        return newList
         

    def isRemovalValid(self, item):
        if (item.isMicrochip):
            return True
        
        floor = self.floorItemLists[self.personFloor]
        
        for itemMatch in floor:
            if (not itemMatch.isMicrochip):
                if (itemMatch.id != item.id):
                    for itemMatch2 in floor:
                        if (item.isMicrochip):
                            if (itemMatch2.id == item.id):
                                return False
                        
                    return True
        
        return True
    
    def isMultipleRemovalValid(self, item1, item2):
        if (item1.id == item2.id):
            return True
        
        return self.isRemovalValid(item1) and self.isRemovalValid(item2)
        
        
    
    def isValid(self):
        items = self.floorItemLists[self.personFloor]
            
        generators = set()
        chips = set()
        
        for item in items:
            if (item.isMicrochip):
                chips.add(item.id)
            else:
                generators.add(item.id)
        
        if (len(generators) == 0):
            return True
        
        for chip in chips:
            if chip not in generators:
                return False
        
        return True
    
    def isDone(self):
        for i in range(MAX_FLOOR):
            if (len(self.floorItemLists[i]) != 0):
                return False

        return True
    
    def __eq__(self, __o: object) -> bool:
        
        # if not self.personFloor == __o.personFloor:
        #     return False
        
        # for i in range(len(self.floorItemLists)):
        #     if not hash(frozenset(self.floorItemLists[i])) == hash(frozenset(__o.floorItemLists[i])):
        #         return False
            
        # return True
        
        if (self.personFloor != __o.personFloor):
            print("False")
            return False
        
        chips = dict()
        generators = dict()
        
        for i in range(len(self.floorItemLists)):
            for item in self.floorItemLists[i]:
                if (item.isMicrochip):
                    chips[item.id] = i
                else:
                    generators[item.id] = i
                    
        newState = []
        
        for i in range(len(self.floorItemLists)):
            newFloor = []
            for item in self.floorItemLists[i]:
                if (item.isMicrochip):
                    newFloor.append(generators[item.id])
                else:
                    newFloor.append(chips[item.id])
            newState.append(newFloor)
            
        chips = dict()
        generators = dict()
        
        for i in range(len(__o.floorItemLists)):
            for item in __o.floorItemLists[i]:
                if (item.isMicrochip):
                    chips[item.id] = i
                else:
                    generators[item.id] = i
        
        for i in range(len(__o.floorItemLists)):
            otherFloor = []
            for item in __o.floorItemLists[i]:
                if (item.isMicrochip):
                    otherFloor.append(generators[item.id])
                else:
                    otherFloor.append(chips[item.id])
            if collections.Counter(otherFloor) != collections.Counter(newState[i]):
                print("False")
                return False
            
            
        #print("True")    
        return True
            
            
        
            
        
                
            
    
    def __hash__(self):
        # hashh = 0
        # for i in range(len(self.floorItemLists)):
        #     hashh += (hash(frozenset(self.floorItemLists[i])) + (i ** 2))
        
        # hashh += hash(self.personFloor ** 3)
        
        # return hashh
        
        chips = dict()
        generators = dict()
        
        for i in range(len(self.floorItemLists)):
            for item in self.floorItemLists[i]:
                if (item.isMicrochip):
                    chips[item.id] = i
                else:
                    generators[item.id] = i
                    
        newState = []
        
        for i in range(len(self.floorItemLists)):
            newFloor = []
            for item in self.floorItemLists[i]:
                if (item.isMicrochip):
                    newFloor.append(generators[item.id])
                else:
                    newFloor.append(chips[item.id])
            newFloor.sort()
            newState.append(newFloor)
        
        #return hash(tuple(hash(tuple(tuple(x) for x in newState)), hash(self.personFloor)))
        return hash((tuple(tuple(x) for x in newState), hash(self.personFloor)))
            
        
                
                            
        
                    
        
                
PlC = Item(1, True)
PlG = Item(1, False)

PrC = Item(2, True)
PrG = Item(2, False) 

RuC = Item(3, True)
RuG = Item(3, False)

StC = Item(4, True)
StG = Item(4, False)

ThC = Item(5, True)
ThG = Item(5, False)

ElC = Item(6, True)
ElG = Item(6, False)

DiC = Item(7, True)
DiG = Item(7, False)

Floor0 = [ThG, ThC, PlG, StG, ElC, ElG, DiC, DiG]
Floor1 = [PlC, StC]
Floor2 = [PrG, PrC, RuG, RuC]
Floor3 = []

FloorItemList = [Floor0, Floor1, Floor2, Floor3]

startNode = Node(0, FloorItemList)

movesMade = 0
done = False

currentNodes = [startNode]
nextNodes = []

seenNodes = set()
seenNodes.add(startNode)

while (not done):
    for node in currentNodes:
        if node.isDone():
            print("Done! in " + str(movesMade) + " moves")
            done = True
            sys.exit()
    
    for node in currentNodes:
        potentialNewNodes = node.possibleNodes()
        
        for node in potentialNewNodes:
            if (node not in seenNodes):
                nextNodes.append(node)
                seenNodes.add(node)
    
    movesMade += 1
    print(movesMade, len(currentNodes))
    
    currentNodes = nextNodes
    
    nextNodes = []
    
    
    

    
    