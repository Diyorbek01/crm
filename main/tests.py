# from django.test import TestCase
#
# # Create your tests here.
# kocha = "Bog'bon"
# mahalla = "Sag'bon"
#
# natija = f"{kocha} ko'chasi, {mahalla} mahallasi ..."
# print(natija)


# son = int(input("son: "))
# juft = []
# toq = []
#
# for i in range(0, son,2):
#     juft.append(i)
#
# for i in range(1, son,2):
#     toq.append(i)
#
# print(juft, "juft sonlar")
# print(toq, "toq sonlar")


son = int(input("son: "))

tubb=[]
for i in range(1, son):
    tub = 0
    for n in range(2, i):
        if i % n == 0:
            tub = 1
            break

    if tub == 0:
        tubb.append(i)
        print(i)
print(f"Opshi {len(tubb)} ta tub son")