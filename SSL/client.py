#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：ssl 
@File    ：client.py
@IDE     ：PyCharm 
@Author  ：HuGe
@Date    ：2022/4/20 10:52 
'''
import socket
import datetime
from RSA import *
from AES import *

'''
提出请求
'''
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('124.70.30.109', 10600)  # 服务器地址
# server_address = ('127.0.0.1', 10600)
client_socket.connect(server_address)  # 与服务端建立连接
print(f'{datetime.datetime.now()} send certification request to server')
msg = "request certificates".encode("utf-8")  # 发送消息请求认证
client_socket.send(msg)

'''
验证证书
'''
certificates = client_socket.recv(1024).decode('utf-8')  # 接收服务端返回的消息
print(f"{datetime.datetime.now()} receive certificates from server : {certificates}")
_, crypto_type, _, e, n, _, signiture = certificates.split()
public_key = [int(e.strip('[').strip(',')),int(n.strip(']'))]
signiture = int(signiture.strip('[').strip(']'))
hash1 = rsa.quick_pow_mod(signiture, public_key[0], public_key[1])  # 解密
hash1 = rsa.decode(hash1).strip('0')

#计算文件哈希
msg = f"{crypto_type},{public_key}".encode("utf-8")
hash2 = hashlib.md5(msg).hexdigest()

'''
发送密钥
'''
if hash1 == hash2:
    print(f'\n{datetime.datetime.now()} certification success, send key to server')
    rsa = RSA()
    key = 'abcdefghijklmnop'
    crypted_key = rsa.encrypt(public_key, key)  # 加密传输密钥
    msg = f"key {crypted_key}".encode("utf-8")
    client_socket.send(msg)
    connect = True
else:
    print(f'\n{datetime.datetime.now()} certification failure, connect will close')
    connect = False

'''
加密通信
'''
aes=AES(key)
msg = 'Cryptography and Network Security;2021214265;HuZiXuan'
msg = aes.block_encrypt(msg).encode('utf-8')
client_socket.send(msg)
msg = client_socket.recv(1024).decode("utf-8")
print(f"{datetime.datetime.now()} receive ciphertext from server : {msg}")
msg = aes.block_decrypt(msg)
print(f"{datetime.datetime.now()} plaintext {msg}")


url = 'www.qq.com'
url = aes.block_encrypt(url).encode('utf-8')
client_socket.send(url)

html = client_socket.recv(65536).decode("utf-8")
print(html)


