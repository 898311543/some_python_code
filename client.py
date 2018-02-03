import socket 
port = 8898
host = '118.89.244.53'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto(b'hello,this is a test info !',(host,port))
data,addr=s.recvfrom(1024)
print('Received:',data,'from',addr)
s.close()

