from generate import generate_prime, select_public_key, \
    ext_euclid, encrypt, decrypt, quick_pow_mod, gcd
import time

start = time.perf_counter()
p = generate_prime()
q = generate_prime()
while p == q: #防止重复
    q = generate_prime()
end = time.perf_counter()
print('p:', p)
print('q:', q)
print('大素数生成时间:%s毫秒' % ((end - start) * 1000))

n = p * q
phi = (p-1) * (q-1)
e = select_public_key(phi)
d = ext_euclid(e, phi)[0]


while d <= 0: #e有问题会无限循环。。。
    print('d')
    d = ext_euclid(e, phi)[0]


public_key = [e, n]
private_key = [d, n]

print('公钥：', public_key)
print('私钥：', private_key)

m = 89237598273589723857023059720935672903650
print('明文：', m)
c = encrypt(m, public_key)
print('密文：', c)
m = decrypt(c, private_key)
print('解密：', m)




