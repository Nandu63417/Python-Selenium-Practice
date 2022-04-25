m = int(input())
s = 1
n = 1 
res = 0
itr = 0
def solve(s, n, m):
    global res,itr
    if s > m + 1:
        return
    if s == m:
        res+=1
        print(s,n,m,res,itr)
    itr+=1
    solve(s+n,2*n,m)
    if s > 0:
        itr+=1
        solve(s-1,n,m)
solve(s,n,m)
print(res)