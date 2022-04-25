'''
    2 matrices inmatrix1(mxn) and inmatrix2(pxq), create outmatrix such that
        * For each num1 from inmatrix1 at row r1 and col c1:
            - Multiply with each number num2 in inmatrix2 such that num2 is in (r1,r1), (r1,c1), (c1,r1), (c1,c1)
            - Identify and add the product that occurs maximum number of times to outmatrix at (r1,c1)
            - If there are multiple products with maximum number of occurances, then the product with lowest value will be added
            - If both row and column in inmatrix2 doesn't exist for r1 and c1, add -1 to outmatrix.
'''


m = int(input('Enter no_ of rows for 1st matrix: '))
p = int(input('Enter no_ of rows for 2nd matrix: '))
inmatrix1 = []
inmatrix2 = []
for i in range(m):
    ncol = list(int(x) for x in input(f'Enter values for row {i+1} for 1st matrix: ').split())
    inmatrix1.append(ncol)
for i in range(p):
    qcol = list(int(x) for x in input(f'Enter values for row {i+1} for 2nd matrix: ').split())
    inmatrix2.append(qcol)
n = len(inmatrix1[0])
q = len(inmatrix2[0])
outmatrix = []
for i in range(m):
    cols = [0] * n
    outmatrix.append(cols)
for i in range(m):
    for j in range(n):
        product = []
        if i < p and i < q:  
            product.append(inmatrix1[i][j]*inmatrix2[i][i])
        if i < p and j < q:
            product.append(inmatrix1[i][j]*inmatrix2[i][j])
        if j < p and i < q:
            product.append(inmatrix1[i][j]*inmatrix2[j][i])
        if j < p and j < q:
            product.append(inmatrix1[i][j]*inmatrix2[j][j])
        if product != []:
            outmatrix[i][j] += max(sorted(set(product)), key = product.count)
        else:
            outmatrix[i][j] += -1
for i in range(m):
    for j in range(n):
        print(outmatrix[i][j], end=' ')
    print()