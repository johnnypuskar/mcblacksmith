from anvilcalc import *

class Node:
    def __init__(self, state = [], cost = float("inf"), creationPair = None, previousNode = None):
        self.cost = cost
        self.state = state
        self.pairs = []
        self.creationPair = creationPair
        self.previousNode = previousNode
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                self.addPair(state[i], state[j])
        self.state.sort(key = lambda i: (i.priorWorks, i.enchantmentString()))

    def addPair(self, a, b):
        if type(a) is type(b):
            if a.combinable(b):
                if a.orderMatters(b):
                    self.pairs.append((a, b, a.getCombineCost(b)))
                    self.pairs.append((b, a, b.getCombineCost(a)))
                else:
                    ab = a.getCombineCost(b)
                    ba = b.getCombineCost(a)
                    if ab <= ba:
                        self.pairs.append((a, b, ab))
                    else:
                        self.pairs.append((b, a, ba))
        elif a.isBook or b.isBook:
            if a.isBook and b.combinable(a):
                self.pairs.append((b, a, b.getCombineCost(a)))
            elif b.isBook and a.combinable(b):
                self.pairs.append((a, b, a.getCombineCost(b)))

    def printPairs(self):
        for pair in self.pairs:
            print(str(pair[0]) + " +\n" + str(pair[1]) + " : " + str(pair[2]))
            print("---")

    def expand(self):
        newNodes = []
        for pair in self.pairs:
            newState = copy.copy(self.state)
            newState.remove(pair[0])
            newState.remove(pair[1])
            newState.append(pair[0].combine(pair[1]))
            n = Node(newState,pair[2]+self.cost,pair,self)
            newNodes.append(n)
        return newNodes
    
    def lowestCostPair(self):
        cheapest = None
        cheapestCost = float("inf")
        for pair in self.pairs:
            if pair[2] < cheapestCost:
                cheapest = pair
        return pair

    def containsItem(self, item):
        for i in self.state:
            if i.equals(item):
                return True
        return False

    def equals(self, other):
        if len(self.state) != len(other.state):
            return False
        for i in range(len(self.state)):
            if not self.state[i].equals(other.state[i]):
                return False
        return True

    def getCreationPath(self):
        path = [self.creationPair]
        if self.previousNode.creationPair != None:
            path = self.previousNode.getCreationPath() + path
        return path
    
    def __str__(self):
        toReturn = "NODE (COST=" + str(self.cost) + ")["
        for item in self.state:
            toReturn += str(item) + ", "
        return toReturn[:-2] + "]"


class Graph:
    def __init__(self):
        self.nodes = []

    def addNode(self, node):
        i = 0
        while i < len(self.nodes) and node.cost > self.nodes[i].cost:
            i += 1
        self.nodes.insert(i,node)

    def getSimilarNode(self, node):
        for n in self.nodes:
            if node.equals(n):
                return n
        return None

    def __str__(self):
        toReturn = "GRAPH [\n-- "
        for n in self.nodes:
            toReturn += str(n) + "\n-- "
        return toReturn[:-3] + "]"
                

def findPath(start, end):
    g = Graph()
    g.addNode(Node(start, 0))
    index = 0
    while index < len(g.nodes) and not g.nodes[index].containsItem(end):
        node = g.nodes[index]
        expanded = node.expand()
        for n in expanded:
            similar = g.getSimilarNode(n)
            if similar == None:
                g.addNode(n)
            elif n.cost < similar.cost:
                similar.cost = n.cost
                similar.previousNode = node
                similar.creationPair = n.creationPair
        index += 1
    if index == len(g.nodes):
        return False, None, -1
    else:
        return True, g.nodes[index], g.nodes[index].cost

def printList(l):
    for i in l:
        print(i)

def enchantedBook(enchantment, level):
    a = Book()
    a.enchant(enchantment, level)
    return a

a = Axe()

#l = [Boots(), enchantedBook("Protection", 4), enchantedBook("Depth Strider", 3), enchantedBook("Feather Falling", 4), enchantedBook("Soul Speed", 3), enchantedBook("Mending", 1), enchantedBook("Unbreaking", 3)]

#final = Boots()
#final.enchant("Protection",4)
#final.enchant("Depth Strider",3)
#final.enchant("Feather Falling",4)
#final.enchant("Soul Speed", 3)
#final.enchant("Mending")
#final.enchant("Unbreaking",3)
#b,n,c = findPath(l,final)

#print(b, n, c)

#cp = n.getCreationPath()

#for pair in cp:
#    print("> Step:\n" + str(pair[0]) + "\n" + str(pair[1]) + "\n")

#print("Final Item: " + str(final) + "\nFinal Cost:",c)
