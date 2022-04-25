n = int(input())
p = list(int(num) for num in input().strip().split())[:n]
# print(p)
flag = False
breakPoint = 0
firstPart = []
lastPart = []
new_p = []

for x in range(n):
    if x == 0:
        continue
    if p[x-1] > p[x]:
        if flag == False:
            flag = True
            breakPoint += x
            # print(breakPoint)
            for y in range(breakPoint):
                firstPart.append(p[y])
            # print(firstPart)
            for y in range(breakPoint, n):
                lastPart.append(p[y])
            # print(lastPart)
            new_p = lastPart + firstPart
            # print(new_p)
            if sorted(new_p) != new_p:
                print("No")
                break
        else:
            print("No")
            break
else:
    print("Yes")