from anvilcalc import *

class Node:
    def __init__(self, state = [], cost = float("inf")):
        self.cost = cost
        self.pairs = []
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                self.addPair(state[i], state[j])

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
            print(str(pair[0]) + " / " + str(pair[1]) + " : " + str(pair[2]))
            print("---")
    
    def lowestCostPair(self):
        cheapest = None
        cheapestCost = float("inf")
        for pair in self.pairs:
            if pair[2] < cheapestCost:
                cheapest = pair
        return pair
        
a = Boots()

b = Book()
b.enchant("Blast Protection", 4)

c = Book()
c.enchant("Feather Falling", 3)

d = Book()
d.enchant("Unbreaking", 2)

l = [a, b, c, d]

n = Node(l)

print(n.printPairs())

