import time
import heapq
from math import inf
from collections import defaultdict
from collections import deque

start = time.time()

with open("16.txt") as f:
    rawInput = f.read().splitlines()

# part 1

xLen = len(rawInput[0])
yLen = len(rawInput)

startingPos = (0, 0)
endPos = (0, 0)
for y in range(0, len(rawInput)):
    for x in range(0, len(rawInput[y])):
        if rawInput[y][x] == "S":
            startingPos = (x, y)
        if rawInput[y][x] == "E":
            endPos = (x, y)

class Graph:
    def __init__(self):
        self.adjacency = {}
    
    def addNode(self, node):
        if node not in self.adjacency:
            self.adjacency[node] = {}
    
    def addEdge(self, fromNode, toNode, weight):
        self.addNode(fromNode)
        self.addNode(toNode)

        self.adjacency[fromNode][toNode] = weight
        self.adjacency[toNode][fromNode] = weight
    
    def getNeighbors(self, node):
        return self.adjacency.get(node, {})
    
    def containsNode(self, node):
        return node in self.adjacency

graph = Graph()

NORTH, EAST, SOUTH, WEST = (0, -1), (1, 0), (0, 1), (-1, 0)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

def getTwo90DegreeTurns(direction):
    if direction == NORTH:
        return [EAST, WEST]
    if direction == EAST:
        return [NORTH, SOUTH]
    if direction == SOUTH:
        return [EAST, WEST]
    if direction == WEST:
        return [NORTH, SOUTH]

startNode = (startingPos[0], startingPos[1], EAST)
nodesToAdd = set([startNode])

while nodesToAdd:
    node = nodesToAdd.pop()
    x, y, direction = node
    dx, dy = direction
    newX, newY = x + dx, y + dy
    if (0 <= newX < xLen and 
        0 <= newY < yLen and 
        rawInput[newY][newX] in [".", "S", "E"]):
        newNode = (newX, newY, direction)
        if not graph.containsNode(newNode):
            nodesToAdd.add(newNode)
        graph.addEdge(node, newNode, 1)
    
    for newDirection in getTwo90DegreeTurns(direction):
        newNode = (x, y, newDirection)
        if not graph.containsNode(newNode):
            nodesToAdd.add(newNode)
        graph.addEdge(node, newNode, 1000)

def findShortestPath(graph, startNode, endNode):
    if not (graph.containsNode(startNode) and graph.containsNode(endNode)):
        return inf

    pq = [(0, startNode)]
    distances = {startNode: 0}
    visited = set()
    
    while pq:
        currentDist, currentNode = heapq.heappop(pq)
        
        if currentNode == endNode:
            return currentDist
            
        if currentNode in visited:
            continue
            
        visited.add(currentNode)
        
        for neighbor, weight in graph.getNeighbors(currentNode).items():
            if neighbor in visited:
                continue
                
            newDist = currentDist + weight
            if newDist < distances.get(neighbor, inf):
                distances[neighbor] = newDist
                heapq.heappush(pq, (newDist, neighbor))
    
    return inf

minScore = inf
for dir in DIRECTIONS:
    minScore = min(minScore, findShortestPath(graph, startNode, (endPos[0], endPos[1], dir)))

print("Part 1:", minScore)

# part 2

def findNodesInShortestPaths(graph, startNode, endNode, shortestDist):
    if not (graph.containsNode(startNode) and graph.containsNode(endNode)):
        return set()
    
    pq = [(0, startNode)]
    distances = defaultdict(lambda: inf)
    distances[startNode] = 0
    nodesInShortestPaths = set()
    predecessors = defaultdict(set)
    visited = set()

    nodesInShortestPaths.add((startNode[0], startNode[1]))
    
    while pq:
        currentDist, currentNode = heapq.heappop(pq)
        
        if currentDist > shortestDist:
            return nodesInShortestPaths
            
        if currentNode in visited:
            continue
            
        visited.add(currentNode)
        currentCoord = (currentNode[0], currentNode[1])
        
        for nextNode, weight in graph.getNeighbors(currentNode).items():
            if nextNode in visited:
                continue
                
            newDist = currentDist + weight
            if newDist > shortestDist:
                continue
            
            neighborCoord = (nextNode[0], nextNode[1])
            
            if newDist <= distances[nextNode]:
                if newDist == distances[nextNode]:
                    predecessors[nextNode].add(currentNode)
                else:
                    distances[nextNode] = newDist
                    predecessors[nextNode] = {currentNode}
                    heapq.heappush(pq, (newDist, nextNode))
                
                if newDist == shortestDist:
                    nodesInShortestPaths.add(currentCoord)
                    nodesInShortestPaths.add(neighborCoord)
                    
                    if nextNode == endNode:
                        queue = deque([currentNode])
                        seen = {currentNode}
                        while queue:
                            node = queue.popleft()
                            nodeCoord = (node[0], node[1])
                            nodesInShortestPaths.add(nodeCoord)
                            for pred in predecessors[node]:
                                if pred not in seen:
                                    seen.add(pred)
                                    queue.append(pred)
    
    return nodesInShortestPaths

nodesInShortestPaths = set()
for dir in DIRECTIONS:
    nodesInShortestPaths |= findNodesInShortestPaths(graph, startNode, (endPos[0], endPos[1], dir), minScore)

print("Part 2:", len(nodesInShortestPaths))

end = time.time()
print(end - start)