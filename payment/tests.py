soni = int(input("to'nkalar soni: "))
balandliklari = input("Balandliklari: ").split(',')
son = []
for i in balandliklari:
    son.append(int(i))

umumiy_balandlik = sum(son)

if umumiy_balandlik % soni == 0:
    print("Yes")
else:
    print("No")
