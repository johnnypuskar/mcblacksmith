from anvilcalc import *

class Node:
    def __init__(self, item = None, cost = 0):
        self.cost = 0
        self.item = item
        self.creationTargetNode = None
        self.creationSacrificeNode = None

    def setCreationNodes(self, target, sacrifice):
        self.creationTargetNode = target
        self.creationSacrificeNode = sacrifice

def addItemToNodeList(nodes, first, second):
    

def lowestCombination(nodes):
    
    for node in nodes:
        for otherNode in nodes:
            if node != otherNode:
                ab = node.item.combine(otherNode.item)
                ba = otherNode.item.combine(otherNode.item)
                

def findPath(nodes, goal):
    
