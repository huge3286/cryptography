#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：ssl 
@File    ：server.py
@IDE     ：PyCharm 
@Author  ：HuGe
@Date    ：2022/4/20 10:51 
'''
import socket
import datetime
from RSA import *
from AES import *


# 参数AF_INET表示该socket网络层使用IP协议
# 参数SOCK_STREAM表示该socket传输层使用tcp协议
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket实例
# server_socket.bind(('192.168.0.225', 10600))  # 绑定IP和端口
server_socket.bind(('', 10600))
server_socket.listen(5)  # 至多listen五个client

'''
接收请求
'''
client_socket, client_address = server_socket.accept() #获取客户的请求
msg = client_socket.recv(1024).decode("utf-8")
print(f'{datetime.datetime.now()} receive request from client {client_address}：{msg}')

'''
生成并返回证书
'''
rsa = RSA()  # 生成类的实例
crypto_type = 'RSA'
public_key = rsa.public_key
private_key = rsa.private_key

msg = f"{crypto_type},{public_key}".encode("utf-8")
hash = hashlib.md5(msg).hexdigest()
signiture = rsa.encrypt(private_key, hash)

certificates = f"crypto_type: {crypto_type} public_key(e,n): {public_key} signiture: {signiture}".encode("utf-8")
client_socket.send(certificates)
print(f'{datetime.datetime.now()} send certificates to server')

'''
接收密钥
'''
msg = client_socket.recv(1024).decode("utf-8")
_, key = msg.split()
key = rsa.quick_pow_mod(int(key.strip('[').strip(']')), private_key[0], private_key[1])  # 解密
key = rsa.decode(key).strip('0')
print(f"{datetime.datetime.now()} receive key from client {client_address}：{key}")

'''
加密通信
'''
aes = AES(key)
msg = client_socket.recv(1024).decode("utf-8")
print(f"{datetime.datetime.now()} receive ciphertext from client {client_address}：{msg}")
msg = aes.block_decrypt(msg)
print(f"{datetime.datetime.now()} plaintext {msg}")
msg = 'Cryptography and Network Security;2021214258;WangZiZhuo'
msg = aes.block_encrypt(msg).encode('utf-8')
client_socket.send(msg)


html = ''
url = client_socket.recv(1024).decode("utf-8")
url = aes.block_decrypt(url)
head = 'GET / HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n' % url
url_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url_socket.connect((url, 80))
url_socket.send(head.encode())
# 循环接收返回数据
while True:
    data = url_socket.recv(65536)
    if data:
        try:
            data = data.decode('UTF-8')
            html += data
        except:
            pass
        continue
    break
# 分离报文头部和报文主体
# html = html.split('\r\n\r\n')
client_socket.send(html.encode('utf-8'))