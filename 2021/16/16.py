import functools
import operator
import time
from collections import deque

start = time.time()

with open("16.txt") as f:
    rawInput = f.read().splitlines()

# part 1

hexToBinary = {
    '0': "0000",
    '1': "0001",
    '2': "0010",
    '3': "0011",
    '4': "0100",
    '5': "0101",
    '6': "0110",
    '7': "0111",
    '8': "1000",
    '9': "1001",
    'A': "1010",
    'B': "1011",
    'C': "1100",
    'D': "1101",
    'E': "1110",
    'F': "1111"
}


class Packet:

    def __init__(self, version, typeID):
        self.version = version
        self.typeID = typeID

        self.isOperator = None
        self.subPackets = None

        self.literalValue = None
        self.bitsUsed = 6

    def setOperatorWithLength(self):
        self.isOperator = True
        self.subPackets = []
        self.bitsUsed += 16

    def setOperatorWithNumPackets(self):
        self.isOperator = True
        self.subPackets = []
        self.bitsUsed += 12

    def addSubPacket(self, subpacket):
        self.subPackets.append(subpacket)
        self.bitsUsed += subpacket.getBitsUsed()

    def getSubPackets(self):
        return self.subPackets

    def setLiteralValue(self, val, bitsUsed):
        self.isOperator = False
        self.literalValue = val
        self.bitsUsed += bitsUsed

    def getBitsUsed(self):
        return self.bitsUsed

    def getTypeID(self):
        return self.typeID

    def getVal(self):
        return self.literalValue


def popLeftXTimes(X):
    return ''.join([binaryQ.popleft() for _ in range(X)])


binaryQ = deque()

for char in rawInput[0]:
    next4Bits = hexToBinary[char]
    for bit in next4Bits:
        binaryQ.append(bit)


def parsePacket():
    versionSum = version = int(popLeftXTimes(3), 2)
    typeID = int(popLeftXTimes(3), 2)

    packet = Packet(version, typeID)

    if typeID != 4:
        lengthTypeID = int(binaryQ.popleft(), 2)
        if lengthTypeID:
            numPackets = int(popLeftXTimes(11), 2)
            packet.setOperatorWithNumPackets()

            for _ in range(numPackets):
                nextPacket, nextVersion = parsePacket()
                packet.addSubPacket(nextPacket)
                versionSum += nextVersion

        else:
            length = int(popLeftXTimes(15), 2)

            packet.setOperatorWithLength()

            bitsSoFar = 0

            while bitsSoFar < length:
                nextPacket, nextVersion = parsePacket()
                versionSum += nextVersion
                bitsSoFar += nextPacket.getBitsUsed()
                packet.addSubPacket(nextPacket)
    else:
        binaryString = ""
        nextStartBit = binaryQ.popleft()
        bitsUsed = 1

        while nextStartBit == '1':
            binaryString += popLeftXTimes(4)
            nextStartBit = binaryQ.popleft()
            bitsUsed += 5

        binaryString += popLeftXTimes(4)
        bitsUsed += 4

        val = int(binaryString, 2)
        packet.setLiteralValue(val, bitsUsed)

    return packet, versionSum


packet, versionSum = parsePacket()
print("Part 1:", versionSum)


# part 2

def calculateValue(packet):
    match packet.getTypeID():
        case 0:
            return sum(calculateValue(p) for p in packet.getSubPackets())
        case 1:
            return functools.reduce(operator.mul, (calculateValue(p) for p in packet.getSubPackets()))
        case 2:
            return min(calculateValue(p) for p in packet.getSubPackets())
        case 3:
            return max(calculateValue(p) for p in packet.getSubPackets())
        case 4:
            return packet.getVal()
        case 5:
            return 1 if calculateValue(packet.getSubPackets()[0]) > calculateValue(packet.getSubPackets()[1]) else 0
        case 6:
            return 1 if calculateValue(packet.getSubPackets()[0]) < calculateValue(packet.getSubPackets()[1]) else 0
        case 7:
            return 1 if calculateValue(packet.getSubPackets()[0]) == calculateValue(packet.getSubPackets()[1]) else 0


print("Part 2:", calculateValue(packet))

end = time.time()
print(end - start)
