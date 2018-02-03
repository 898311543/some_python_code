#-*- coding:utf-8 -*-

import socket
port=53
host='118.89.244.53'
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client=s.connect((host,port))
s.sendall(b'hello,this is a test info !')
