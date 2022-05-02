

# Python Version
def binpow(a, b): #递归实现
    if b == 0:
        return 1
    res = binpow(a, b // 2)
    if (b % 2) == 1:
        return res * res * a
    else:
        return res * res

# Python Version
def binpow1(a, b):
    res = 1
    while b > 0:
        if (b & 1): #b为奇数
            res = res * a #是奇数就相当于少乘了一个a嘛 除二的时候余数没了
        a = a * a
        b >>= 1 #二进制右移一位 除二
    return res

def Lucas_Lehmer(num: int) -> bool:  # 快速检验pow(2,m)-1是不是素数
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    s = 4
    Mersenne = pow(2, num) - 1  # pow(2, num)-1是梅森数
    for x in range(1, (num - 2) + 1):  # num-2是循环次数，+1表示右区间开
        s = ((s * s) - 2) % Mersenne
    if s == 0:
        return True
    else:
        return False

def gcd(a, b): # Euclidean算法 计算最大公约数
    if b == 0:
        return a
    else:
        return gcd(b, a % b) # gcd(a, b) = gcd(b, a%b)

p = 65710453376290420600056698994719554088496933342042652691102106023262088660513
q = 74797657896041875753307298013932972972174297845516728337984571221929530647797
e = 788115374667584145215479079779955655347737195727863067647216640602653721320346455671261690037164954969953169903885934051187693913110472397163067075468071
d = 1368864830566932314277950354308417522426416190088362114627919097947093524418226797583740732969267562520194507194892000542202012276096246939215657396398231
phi = (p-1)*(q-1)

# Python Version
def quick_pow_mod(a, b, c):  # 快速模幂运算 (底 幂 模)
    a = a % c  # 就是在快速幂过程中增加了取模
    ans = 1
    while b != 0:
        if b & 1:  # b为奇数
            ans = (ans * a) % c  # 补上少乘的a 奇数除二省去的余数
        b >>= 1  # 二进制右移一位 除二
        a = (a % c) * (a % c)
    return ans

f= quick_pow_mod(e, phi-2, phi)

print((e*f)%phi)
