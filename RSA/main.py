# Cryptography and Network Security;2021214265;Huzixuan
import hashlib
import random


class RSA():

    def __init__(self):  # 初始化
        p, q = self.generate_pq()  # 生成p,q
        public_key, private_key = self.generate_key(p, q)  # 计算公钥私钥
        print('\t')
        blocks = self.get_plaintext()  # 获取明文分块并转码为数字
        res = ''
        for i in range(len(blocks)):
            m = blocks[i]
            c = self.quick_pow_mod(m, public_key[0], public_key[1])  # 加密
            print('密文：', c)
            m = self.quick_pow_mod(c, private_key[0], private_key[1])  # 解密
            m = self.decode(m)  # 解码为字符串
            res += m
        print('解密结果：', res.strip('0'))  # 偷懒了 明文开头末尾的零都会被消除
        self.p = p
        self.q = q
        self.public_key = public_key
        self.private_key = private_key

    def get_plaintext(self):  # 获取明文 转换为ascii
        print('请输入明文：')
        text = input()  # 转为比特串
        self.plaintext = text
        print('输入明文二进制长度为：', 8 * len(text), '位')
        blocks = []
        for i in range(len(text) // 63 + 1):
            m = text[63 * i: 63 * (i + 1)]
            print('分块：', i + 1, m)
            m = m.ljust(63, '0').encode('utf-8')
            code = ''
            for j in range(len(m)):
                code += str(hex(m[j])[2:4])  # 转16进制保证每个字符占8位并拼接成一个大数
                j += 1
            blocks.append(int(code, 16))  # 转10进制否则计算出错
        return blocks

    def decode(self, code):  # num2str
        i = 2
        code = str(hex(code))  # 转回16进制才能按位取出对应字符
        text = []
        while i < len(code):
            d = code[i:i + 2]
            text.append(chr(int(d, 16)))  # 转回10进制再转回字符
            i += 2
        return ''.join(i for i in text)

    def quick_pow_mod(self, a, b, c):  # 快速模幂运算 (底 幂 模)
        a = a % c  # 就是在快速幂过程中增加了取模
        ans = 1
        while b != 0:
            if b & 1:  # b为奇数
                ans = (ans * a) % c  # 补上少乘的a 奇数除二省去的余数
            b >>= 1  # 二进制右移一位 除二
            a = (a % c) * (a % c)
        return ans

    def Miller_Rabin(self, n, iters):  # 米勒拉宾素性检验
        if n == 2:  # 2是素数
            return True
        if n & 1 == 0 or n < 2:  # 偶数和小于2的整数不是素数
            return False
        m, s = n - 1, 0  # n-1 = (2^s)m 费马小定理 可以拆分
        while m & 1 == 0:
            m = m >> 1
            s += 1
        for i in range(iters):  # 米勒拉宾测试
            b = self.quick_pow_mod(random.randint(2, n - 1), m, n)
            if b == 1 or b == n - 1:  # x^2=1(mod n) 仅当x=1或x=n-1时成立 可能为素数 继续
                continue
            for j in range(s - 1):  # a^((2^s)m)=1(mod n) 且上一位必定为n-1
                b = self.quick_pow_mod(b, 2, n)
                if b == n - 1:  # 有可能为素数
                    break  # 进行下一轮测试
            else:
                return False
        return True

    # 卢卡斯-莱墨素性检验
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

    def generate_prime(self):  # 生成256位随机素数
        p = random.randint(pow(2, 255), pow(2, 256))
        while self.Miller_Rabin(p, 10):
            return p
        return self.generate_prime()

    def generate_pq(self):  # 生成p和q
        p = self.generate_prime()
        q = self.generate_prime()
        while p != q:
            print('随机大素数p:', p)
            print('随机大素数q:', q)
            return p, q
        return self.generate_prime()

    def gcd(self, a, b):  # Euclidean算法 计算最大公约数
        if b == 0:
            return a
        else:
            return self.gcd(b, a % b)  # gcd(a, b) = gcd(b, a%b)

    def ext_euclid(self, a, b):  # 扩展Euclidean算法
        if b == 0:
            return 1, 0, a
        else:
            x, y, g = self.ext_euclid(b, a % b)  # ax+by=gcd(a,b)
            x, y = y, (x - (a // b) * y)  # 模反元素 ed = 1(mod phi)
            return x, y, g  # d*e-k*phi = 1 = gcd(e,phi)

    def generate_key(self, p, q):
        n = p * q
        phi = (p - 1) * (q - 1)
        e = random.randint(0, phi)
        d = self.ext_euclid(e, phi)[0]
        if self.gcd(phi, e) == 1 and d >= 0:
            print('公钥：', [e, n])
            print('私钥：', [d, n])
            return [e, n], [d, n]
        return self.generate_key(p, q)


if __name__ == "__main__":
    rsa = RSA()

    print('\t')
    Hash = hashlib.md5(rsa.plaintext.encode('utf-8')).hexdigest()
    print('哈希：', Hash)
    signature = rsa.quick_pow_mod(int(Hash, 16), rsa.private_key[0], rsa.private_key[1])
    print('数字签名', signature)
    Hash = rsa.quick_pow_mod(signature, rsa.public_key[0], rsa.public_key[1])
    print('哈希：', hex(Hash)[2:])
