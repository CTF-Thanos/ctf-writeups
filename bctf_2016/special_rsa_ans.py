
import os, sys
# from key import k, random_r
import msgpack
import string
import gmpy

sys.setrecursionlimit(1000000)

N = 23927411014020695772934916764953661641310148480977056645255098192491740356525240675906285700516357578929940114553700976167969964364149615226568689224228028461686617293534115788779955597877965044570493457567420874741357186596425753667455266870402154552439899664446413632716747644854897551940777512522044907132864905644212655387223302410896871080751768224091760934209917984213585513510597619708797688705876805464880105797829380326559399723048092175492203894468752718008631464599810632513162129223356467602508095356584405555329096159917957389834381018137378015593755767450675441331998683799788355179363368220408879117131L

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    assert g == 1
    # if g != 1: return None
    # return x+m #x % m
    return x%m

def pad_even(x):
    return ('', '0')[len(x)%2] + x

def encrypt(ms, k):
    out = [] 
    for i in range(0, len(ms), 256):
        m = ms[i:i+256]
        m = int(m.encode('hex'), 16)
        out.append(m)
        # r = random_r()  # public key
        # r_s = pad_even(format(r, 'x')).decode('hex')
        # assert m < N
        # c = (pow(k, r, N) * m) % N
        # c_s = pad_even(format(c, 'x')).decode('hex')
        # out.append((r_s, c_s))
    # return msgpack.packb(out)
    return out

def decrypt(c, k):
    out = ''
    res = []
    for r_s, c_s in msgpack.unpackb(c):
        r = int(r_s.encode('hex'), 16)
        c = int(c_s.encode('hex'), 16)
        res.append([r, c])
        # k_inv = modinv(k, N)
        # out += pad_even(format(pow(k_inv, r, N) * c % N, 'x')).decode('hex')
    # return out
    return res

msg = "msg.txt"
enc = "msg.enc"
flag = "flag.enc"

res1 = encrypt(open(msg).read(), 1)
res2 = decrypt(open(enc).read(), 1)
res3 = decrypt(open(flag).read(), 1)

### setp 1
# now pow(k_inv, r, N) * c = m (mod N)
# if set pow(k_inv, r, N) is n, so n*c = m (mod N)
# n*c*c_inv = m*c_inv (mod N)
# n = t (mod N) , m*c_inv = t (mod N)
# we can do a test like below: 
# c = res2[0][1]
# m = res1[0]
# c_inv = modinv(c, N)  
# t = (m * c_inv) % N 
# assert (t*c)%N == m
# print t

lst = []
for i in range(2):
    m = res1[i]
    r, c = res2[i]
    c_inv = modinv(c, N) 
    t = (m * c_inv) % N
    lst.append([t, r])

### setp 2
# now we have : 
#   k_inv^r1 = t1 (mod N) 
#   k_inv^r2 = t2 (mod N)
# do some change: 
#   k_inv^(r0+r2) = t1 (mod N) if r0+r2 equal r1
#   k_inv^r0 * k_inv^r2 = t1 (mod N)
# and we can calc the Multiplicative inverse modulo of k_inv^r2 
#   n = modinv(t2, N)
# as the Multiplicative inverse modulo's character:
#   n*k_inv^r2 = 1 (mod N)
# do some change:
#   k_inv^r0 * k_inv^r2 * n = t1 * n (mod N)
#   k_inv^r0 = t1 * n (mod N)

### setp 3
# we can see gcd(r1, r2) is 1, check as below：
#   print gmpy.gcd(res2[0][0], res2[1][0]) == 1
# so we can get the k_inv by Euclidean algorithm

def my_gcd(t1, r1, t2, r2): 
    assert r1 > r2   
    r = 1     
    while r:
        r = r1 % r2
        a = r1 / r2       
        r1 = r2         
        r2 = r
        t2_inv = modinv(t2, N)
        t = t2 
        t2 = (t1*pow(t2_inv, a, N)) % N
        t1 = t 
    # print t1, r1 
    # print t2, r2 
    return t1
    
t1, r1 = lst[0]
t2, r2 = lst[1]
if r1 >= r2:
    print "first"
    k_inv = my_gcd(t1, r1, t2, r2)
else:
    print "second"
    k_inv = my_gcd(t2, r2, t1, r1)

r, c = res3[0]
print pad_even(format(pow(k_inv, r, N) * c % N, 'x')).decode('hex')
