from anvilcalc import *
from smithpath import *
import copy

items = {}
items["pickaxe"] = Pickaxe()
items["shovel"] = Shovel()
items["axe"] = Axe()
items["sword"] = Sword()
items["helmet"] = Helmet()
items["chestplace"] = Chestplate()
items["leggings"] = Leggings()
items["boots"] = Boots()
items["bow"] = Bow()
items["crossbow"] = Crossbow()
items["trident"] = Trident()
items["fishing rod"] = FishingRod()
items["shears"] = Shears()


s = ""
while s.lower() not in items.keys():
    print("Please type the name of a valid base item:")
    s = input()

plain_base = copy.deepcopy(items[s])
base = items[s]

print("")

s = ""
while not s.isdigit():
    print("Please enter the amount of enchanted books:")
    print("(Assuming each book contains 1 unique enchantment)")
    s = input()

ench_count = int(s)

e_books = []

print("")

while ench_count > 0:
    print("Please give the name of a valid enchantment for the base item:")
    s = input().lower().title()
    if s in enchantments.keys():
        ench = s
        if enchantments[s].maxLevel > 1:
            print("Please enter a valid level for this enchantment:")
            s = input()
            if s.isdigit() and int(s) <= enchantments[ench].maxLevel:
                lvl = int(s)
                new_book = Book()
                new_book.enchant(ench, lvl)
                base.enchant(ench, lvl)
                e_books.append(new_book)
                ench_count -= 1
        else:
            new_book = Book()
            new_book.enchant(ench, 1)
            base.enchant(ench, 1)
            e_books.append(new_book)
            ench_count -= 1

print("-----------------------------------------------------\n")

e_books.append(plain_base)

b,n,c = findPath(e_books, base)

print(b, n, c,"\n")

cp = n.getCreationPath()

for pair in cp:
    print("> Step:\n" + str(pair[0]) + "\n" + str(pair[1]) + "\n")

print("Final Item: " + str(base) + "\nFinal Cost:",c,"\n")

input("Press enter to quit...")
