import random
import hashlib


def random_256(): #生成256位随机数
    y = random.randint(pow(2, 255), pow(2, 256))
    return y

def generate_prime():
    p = random_256()
    while not Miller_Rabin(p, 10):
        p = random_256()
    return p

def prime_sieve(x): #素数筛 算法代价太大 不可行
    if x <= 2:
        return False
    if x % 6 != 1 and x % 6 != 5:
        return False
    sqrt = math.sqrt(x)
    i = 5
    while i <= sqrt:
        if x % i == 0 or x % (i+2) == 0:
            return False
        i += 6
    return True


# 快速幂模运算，把b拆分为二进制，遍历b的二进制，当二进制位为0时不计入计算
def quick_pow_mod(a, b, c):
    a = a % c
    ans = 1
    while b != 0:
        if b & 1:
            ans = (ans * a) % c
        b >>= 1
        a = (a % c) * (a % c)
    return ans


def Miller_Rabin(n, iters):
    if n == 2: #2是素数
        return True
    if n & 1 == 0 or n < 2: #偶数和小于2的整数不是素数
        return False
    m, s = n - 1, 0 # n-1 = (2^s)m 费马小定理 可以拆分
    while m & 1 == 0:
        m = m >> 1
        s += 1
    for i in range(iters): #米勒拉宾测试
        b = quick_pow_mod(random.randint(2, n - 1), m, n)
        if b == 1 or b == n - 1:  # x^2=1(mod n) 仅当x=1或x=n-1时成立 可能为素数 继续
            continue
        for j in range(s - 1): # a^((2^s)m)=1(mod n) 且上一位必定为n-1
            b = quick_pow_mod(b, 2, n)
            if b == n - 1: # 有可能为素数
                break # 进行下一轮测试
        else:
            return False
    return True


#gcd(a, b) = gcd(b, a%b)
#Euclidean算法 计算最大公约数
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


#选取公钥e
def select_public_key(phi):
    while True:
        print('e')
        e = random.randint(0, phi)
        if gcd(phi, e) == 1:
            return e


# ax+by=gcd(a,b)
# 模反元素 ed = 1(mod phi)
# d*e-k*phi = 1 = gcd(e,phi)
def ext_euclid(a, b):#扩展Euclidean算法
    if b == 0:
        return 1, 0, a
    else:
        x, y, g = ext_euclid(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, g


# 加密 m是被加密的信息 加密成为c
def encrypt(m, key):
    e = key[0]
    n = key[1]
    c = quick_pow_mod(m, e, n)
    return c

# 解密 c是密文，解密为明文m
def decrypt(c, key):
    d = key[0]
    n = key[1]
    m = quick_pow_mod(c, d, n)
    return m



