import itertools
def findsubsets(s,n):
    return list(itertools.combinations(s, n))
def print_factors(x):
    fact=[]
    for i in range(2, x):
       if x % i == 0:
           fact.append(i)
    return fact
def check_prime_factors(fact):
    for i in fact:
        if i == 2:
            continue
        if i % 2 == 0:
            return False
        for j in range(3,i//2,2):
            if i % j == 0:
                return False
    return True
def isPrime(i):
    if i == 2:
        return True
    if i % 2 == 0:
        return False
    for j in range(3,i//2,2):
        if i % j == 0:
            return False
    return True

t = int(input())
for _ in range(t):
    n = int(input())
    l = [int(x) for x in input().split()]
    ml = []
    count = 0
    for i in l:
        fact = print_factors(i)
        if check_prime_factors(fact):
            ml.append(i)
    subsets = [] 
    for x in range(1,len(ml)+1):
        subsetlist = findsubsets(ml,x)
        for y in subsetlist:
            subsets.append(y)
    # print(subsets)
    for x in subsets:
        product = 1
        for y in x:
            product *= y
        fact = print_factors(product)
        if check_prime_factors(fact):
            count += 1
    print(count)