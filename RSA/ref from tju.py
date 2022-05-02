import random
import Prime
import time


# encryption ,according to the formula:m^e = c (mod n) , calculate c ,c == secret,m == message
def encryption(plaintext, puk):
    return Prime.quick_pow_mod(plaintext, puk[1], puk[0])


# decryption ,according to the formula:c^d = m (mod n),  calculate m ,
def decryption(ciphertext, prk):
    return Prime.quick_pow_mod(ciphertext, prk[1], prk[0])


def get_RSAKey():
    RSAKey = {}

    start = time.perf_counter()
    prime_arr = Prime.get_rand_prime_arr(2)
    p = prime_arr[0]
    q = prime_arr[1]
    while p == q:
        q = random.choice(prime_arr)
    end = time.perf_counter()

    n = p * q
    s = (p - 1) * (q - 1)
    a = 65537
    b = Prime.mod_inverse(a, s)

    print("随机生成的素数p =", p)
    print("随机生成的素数q =", q)
    print('素数生成的时间为：', end - start, 's')

    print("n = pq =", n)
    print("利用Euclidean算法生成的私钥a =", a)
    print("利用扩展Euclidean算法生成的公钥b =", b)

    puk = [n, a]
    prk = [n, b]
    RSAKey['puk'] = puk
    RSAKey['prk'] = prk
    return RSAKey


if __name__ == '__main__':
    RSAKey = get_RSAKey()
    # print("Enter a number less and shorter than ", len(str(RSAKey['puk'][0])), ",", RSAKey['puk'][0], ":")
    print('请输入明文：')
    # only encrypt a number type
    m = int(input())
    c = encryption(m, RSAKey['puk'])
    print("RSA加密后的密文为:", c)
    # print(len(str(c)))
    m1 = decryption(c, RSAKey['prk'])
    print("RSA解密后的密文为:", m1)
    # print(len(str(m1)))
    # 检验解密的正确性
    if m == m1:
        print('解密成功')
    # 记录10组明文的RSA加密和解密时间
    sumEnTime = 0
    sumDeTime = 0
    for i in range(10):
        print('请输入明文：')
        # only encrypt a number type
        m = int(input())

        # RSA加密
        start = time.perf_counter()
        c = encryption(m, RSAKey['puk'])
        end = time.perf_counter()
        sumEnTime = sumEnTime + (end - start)
        print("RSA加密后的密文为:", c)
        # print(len(str(c)))

        # RSA解密
        start = time.perf_counter()
        m1 = decryption(c, RSAKey['prk'])
        end = time.perf_counter()
        sumDeTime = sumDeTime + (end - start)
        print("RSA解密后的密文为:", m1)
    print('10组明文的RSA加密时间为：', sumEnTime)
    print('10组明文的RSA解密时间为：', sumDeTime)