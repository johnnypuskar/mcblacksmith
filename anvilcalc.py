import copy

class Enchantment:
    def __init__(self, name, maxLevel, im, bm):
        self.name = name
        self.maxLevel = maxLevel
        self.itemMultiplier = im
        self.bookMultiplier = bm
        self.incompatible = []

    def makeIncompatible(self, other):
        self.incompatible.append(other)
        other.incompatible.append(self)

enchantments = {}
enchantments["Protection"] = Enchantment("Protection", 4, 1, 1)
enchantments["Fire Protection"] = Enchantment("Fire Protection", 4, 2, 1)
enchantments["Feather Falling"] = Enchantment("Feather Falling", 4, 2, 1)
enchantments["Blast Protection"] = Enchantment("Blast Protection", 4, 4, 2)
enchantments["Projectile Protection"] = Enchantment("Projectile Protection", 4, 2, 1)
enchantments["Thorns"] = Enchantment("Thorns", 3, 8, 4)
enchantments["Respiration"] = Enchantment("Respiration", 3, 4, 2)
enchantments["Depth Strider"] = Enchantment("Depth Strider", 3, 4, 2)
enchantments["Aqua Affinity"] = Enchantment("Aqua Affinity", 1, 4, 2)
enchantments["Sharpness"] = Enchantment("Sharpness", 5, 1, 1)
enchantments["Smite"] = Enchantment("Smite", 5, 2, 1)
enchantments["Bane of Arthropods"] = Enchantment("Bane of Arthropods", 5, 2, 1)
enchantments["Knockback"] = Enchantment("Knockback", 2, 2, 1)
enchantments["Fire Aspect"] = Enchantment("Fire Aspect", 2, 4, 2)
enchantments["Looting"] = Enchantment("Looting", 3, 4, 2)
enchantments["Efficiency"] = Enchantment("Efficiency", 5, 1, 1)
enchantments["Silk Touch"] = Enchantment("Silk Touch", 1, 8, 4)
enchantments["Unbreaking"] = Enchantment("Unbreaking", 3, 2, 1)
enchantments["Fortune"] = Enchantment("Fortune", 3, 4, 2)
enchantments["Power"] = Enchantment("Power", 5, 1, 1)
enchantments["Punch"] = Enchantment("Punch", 2, 4, 2)
enchantments["Flame"] = Enchantment("Flame", 1, 4, 2)
enchantments["Infinity"] = Enchantment("Infinity", 1, 8, 4)
enchantments["Luck of the Sea"] = Enchantment("Luck of the Sea", 3, 4, 2)
enchantments["Lure"] = Enchantment("Lure", 3, 4, 2)
enchantments["Frost Walker"] = Enchantment("Frost Walker", 2, 4, 2)
enchantments["Mending"] = Enchantment("Mending", 1, 4, 2)
enchantments["Curse of Binding"] = Enchantment("Curse of Binding", 1, 8, 4)
enchantments["Curse of Vanishing"] = Enchantment("Curse of Vanishing", 1, 8, 4)
enchantments["Sweeping Edge"] = Enchantment("Sweeping Edge", 3, 4, 2)
enchantments["Impaling"] = Enchantment("Impaling", 5, 3, 2)
enchantments["Riptide"] = Enchantment("Riptide", 3, 4, 2)
enchantments["Loyalty"] = Enchantment("Loyalty", 3, 1, 1)
enchantments["Channeling"] = Enchantment("Channelling", 1, 8, 4)
enchantments["Multishot"] = Enchantment("Multishot", 1, 4, 2)
enchantments["Piercing"] = Enchantment("Piercing", 4, 1, 1)
enchantments["Quick Charge"] = Enchantment("Quick Charge", 3, 2, 1)
enchantments["Soul Speed"] = Enchantment("Soul Speed", 3, 4, 2)

enchantments["Protection"].makeIncompatible(enchantments["Fire Protection"])
enchantments["Protection"].makeIncompatible(enchantments["Blast Protection"])
enchantments["Protection"].makeIncompatible(enchantments["Projectile Protection"])
enchantments["Fire Protection"].makeIncompatible(enchantments["Blast Protection"])
enchantments["Fire Protection"].makeIncompatible(enchantments["Projectile Protection"])
enchantments["Blast Protection"].makeIncompatible(enchantments["Projectile Protection"])

enchantments["Silk Touch"].makeIncompatible(enchantments["Fortune"])

enchantments["Sharpness"].makeIncompatible(enchantments["Smite"])
enchantments["Sharpness"].makeIncompatible(enchantments["Bane of Arthropods"])
enchantments["Smite"].makeIncompatible(enchantments["Bane of Arthropods"])

enchantments["Depth Strider"].makeIncompatible(enchantments["Frost Walker"])

enchantments["Infinity"].makeIncompatible(enchantments["Mending"])

enchantments["Riptide"].makeIncompatible(enchantments["Loyalty"])
enchantments["Riptide"].makeIncompatible(enchantments["Channeling"])
enchantments["Loyalty"].makeIncompatible(enchantments["Channeling"])

enchantments["Multishot"].makeIncompatible(enchantments["Piercing"])


class Item:
    def __init__(self, priorWorks = 0, damaged = False, priorEnchantments = []):
        self.priorWorks = priorWorks
        self.legalEnchantments = {}
        self.enchantments = {}
        self.isBook = False
        self.isDamaged = damaged
        self.defineEnchantments()
        if len(priorEnchantments) > 0:
            self.setEnchantments(priorEnchantments)

    def addLegalEnchantment(self, enchantment):
        self.legalEnchantments[enchantment] = enchantments[enchantment]
    
    def defineEnchantments(self):
        self.addLegalEnchantment("Mending")
        self.addLegalEnchantment("Unbreaking")
        self.addLegalEnchantment("Curse of Vanishing")

    def enchant(self, name, level = 1):
        self.enchantments[name] = level

    def disenchant(self, name = None):
        if name == None:
            self.enchantments = {}
        else:
            del self.enchantments[name]

    def getOptimalCost(self, other):
        if self.isBook and not other.isBook:
            return other.getCombineCost(self)
        elif not self.isBook and other.isBook:
            return self.getCombineCost(other)
        return min(self.getCombineCost(other), other.getCombineCost(self))
    
    def getCombineCost(self, other):
        totalCost = 0
        if self.isDamaged:
            totalCost += 2
        for enchName in other.enchantments:
            ench = enchantments[enchName]
            if ench.name in self.legalEnchantments:
                hasConflicting = False
                for conflicting in ench.incompatible:
                    if conflicting.name in self.enchantments:
                        hasConflicting = True
                        break
                if not hasConflicting:
                    multiplier = 1
                    if other.isBook:
                        multiplier = ench.bookMultiplier
                    else:
                        multiplier = ench.itemMultiplier
                    if ench.name not in self.enchantments:
                        totalCost += other.enchantments[ench.name] * multiplier
                    elif self.enchantments[ench.name] == enchantments[ench.name].maxLevel:
                        totalCost += self.enchantments[ench.name] * multiplier
                    elif other.enchantments[ench.name] == self.enchantments[ench.name]:
                        totalCost += (self.enchantments[ench.name] + 1) * multiplier
                    else:
                        totalCost += max(self.enchantments[ench.name], other.enchantments[ench.name]) * multiplier
                        
                else:
                    totalCost += 1
        totalCost += (2**self.priorWorks-1) + (2**other.priorWorks-1)
        return totalCost
            
    def orderMatters(self, other):
        for enchName in self.enchantments:
            ench = enchantments[enchName]
            for incompatible in ench.incompatible:
                if incompatible.name in other.enchantments:
                    return True
        return False

    def combinable(self, other):
        if isinstance(self, Book) and not isinstance(other, Book):
            return False
        for ench in other.enchantments:
            if ench in self.legalEnchantments:
                hasIncompatibility = False
                for incompatible in enchantments[ench].incompatible:
                    if incompatible.name in self.enchantments:
                        hasIncompatibility = True
                if not hasIncompatibility:
                    return self.getCombineCost(other) < 40
            
    
    def combine(self, other):
        result = copy.deepcopy(self)
        for enchName in other.enchantments:
            ench = enchantments[enchName]
            if ench.name in self.enchantments:
                if self.enchantments[ench.name] < other.enchantments[ench.name]:
                    result.enchantments[ench.name] = other.enchantments[ench.name]
                elif self.enchantments[ench.name] == other.enchantments[ench.name]:
                    result.enchantments[ench.name] += 1
            elif ench.name in self.legalEnchantments:
                hasConflicting = False
                for incompatible in ench.incompatible:
                    if incompatible.name in self.enchantments:
                        hasConflicting = True
                        break
                if not hasConflicting:
                    result.enchantments[ench.name] = other.enchantments[ench.name]
        result.priorWorks = max(self.priorWorks, other.priorWorks) + 1
        return result

    def enchantmentString(self):
        enchList = [(k, v) for k, v in self.enchantments.items()]
        enchList.sort(key = lambda i: (i[0], i[1]))
        toReturn = ""
        for e in enchList:
            toReturn += e[0] + str(e[1])
        return toReturn
        
    
    def equals(self, other):
        if len(self.enchantments) != len(other.enchantments) or type(self) is not type(other):
            return False
        for ench in other.enchantments:
            if ench not in self.enchantments:
                return False
            elif self.enchantments[ench] != other.enchantments[ench]:
                return False
        return True

    def __str__(self):
        if len(self.enchantments.keys()) == 0:
            return type(self).__name__.upper()
        toReturn = type(self).__name__ + "{"
        for ench in self.enchantments.keys():
            toReturn += ench
            if self.enchantments[ench] > 1:
                toReturn += " " + str(self.enchantments[ench])
            toReturn += ", "
        return (toReturn[:-2] + "}").upper()
        

class Armor(Item):
    def defineEnchantments(self):
        Item.defineEnchantments(self)
        self.addLegalEnchantment("Protection")
        self.addLegalEnchantment("Fire Protection")
        self.addLegalEnchantment("Blast Protection")
        self.addLegalEnchantment("Projectile Protection")
        self.addLegalEnchantment("Thorns")
        self.addLegalEnchantment("Curse of Binding")

class Helmet(Armor):
    def defineEnchantments(self):
        Armor.defineEnchantments(self)
        self.addLegalEnchantment("Respiration")
        self.addLegalEnchantment("Aqua Affinity")

class Boots(Armor):
    def defineEnchantments(self):
        Armor.defineEnchantments(self)
        self.addLegalEnchantment("Feather Falling")
        self.addLegalEnchantment("Depth Strider")
        self.addLegalEnchantment("Soul Speed")

class Chestplate(Armor):
    pass

class Leggings(Armor):
    pass

class Tool(Item):
    def defineEnchantments(self):
        Item.defineEnchantments(self)
        self.addLegalEnchantment("Efficiency")
        self.addLegalEnchantment("Silk Touch")
        self.addLegalEnchantment("Fortune")

class Pickaxe(Tool):
    pass

class Shovel(Tool):
    pass

class Weapon(Item):
    def defineEnchantments(self):
        Item.defineEnchantments(self)
        self.addLegalEnchantment("Sharpness")
        self.addLegalEnchantment("Bane of Arthropods")
        self.addLegalEnchantment("Smite")

class Sword(Weapon):
    def defineEnchantments(self):
        Weapon.defineEnchantments(self)
        self.addLegalEnchantment("Fire Aspect")
        self.addLegalEnchantment("Looting")
        self.addLegalEnchantment("Knockback")
        self.addLegalEnchantment("Sweeping Edge")

class Trident(Item):
    def defineEnchantments(self):
        Item.defineEnchantments(self)
        self.addLegalEnchantment("Impaling")
        self.addLegalEnchantment("Channeling")
        self.addLegalEnchantment("Loyalty")
        self.addLegalEnchantment("Riptide")

class Bow(Item):
    def defineEnchantments(self):
        Item.defineEnchantments(self)
        self.addLegalEnchantment("Power")
        self.addLegalEnchantment("Punch")
        self.addLegalEnchantment("Flame")
        self.addLegalEnchantment("Infinity")

class Crossbow(Item):
    def defineEnchantments(self):
        Item.defineEnchantments(self)
        self.addLegalEnchantment("Quick Charge")
        self.addLegalEnchantment("Piercing")
        self.addLegalEnchantment("Multishot")

class FishingRod(Item):
    def defineEnchantments(self):
        Item.defineEnchantments(self)
        self.addLegalEnchantment("Lure")
        self.addLegalEnchantment("Luck of the Sea")

class Axe(Tool, Weapon):
    def defineEnchantments(self):
        Tool.defineEnchantments(self)
        Weapon.defineEnchantments(self)

class Shears(Item):
    def defineEnchantments(self):
        Item.defineEnchantments(self)
        self.addLegalEnchantment("Efficiency")

class Book(Item):
    def __init__(self):
        Item.__init__(self)
        self.isBook = True
        self.isDamaged = False
    
    def defineEnchantments(self):
        for ench in enchantments.keys():
            self.addLegalEnchantment(ench)

