# coding: UTF-8
import socket
import sys
import _thread
import binascii
import queue
import datetime
import time
import threading
import MySQLdb
import subprocess

Host = ''
port = 8899

def clientThread(conn):
    while True:
            data = conn.recv(1024)
            try:
                data = data.decode('ascii')
            except UnicodeDecodeError as e:
                print('bad request')
                return 1
            print('The recived data is '+data)
            try:
                data_s = data.split(',')
                insert_value(data_s)
                if(int(data_s[1]) > 60):
                    code = subprocess.call(["python3", "mail.py"])
                    if(not code):
                        sys.stderr.write('发送成功')
                    else:
                        sys.stderr.write('发送失败')
                    
            except Exception as e:
                print(e)
            if not data:
                print('client is hung up...waiting for reconnect')
                break
            conn.sendall(b'OK')
            queue_lock.acquire()
            if console_queue.empty() == False:
                cmd = console_queue.get()
                conn.sendall(cmd)
                print('command: %s'%cmd)
            queue_lock.release()
    conn.close()
#command return_
def socket_control(conn):
    conn.send(b'control server has benn connected:')
    print('Control client is connecting...')
    while True:
            mutex = 0
            data = conn.recv(1024)
            print('The recived data is '+data.decode('ascii'))
            if not data :
                break
            console_queue.put(data)
def db_init():
    conn = MySQLdb.connect(host="172.17.0.1",user="root",passwd="shubin",db='envireoment_detection',charset='utf8')
    cursor = conn.cursor()
    return conn,cursor
def insert_value(value):
    global conn_db,cursor
    date_t = (time.strftime("date-%Y%m%d",time.localtime(time.time())))
    sql = "insert into `"+date_t+"` values(NULL,current_timestamp(),%s,%s,%s,%s,%s,%s,NULL)"
    param=(value[0],value[1],value[2],value[4],value[5],value[6])
    try:
        n = cursor.execute(sql,param)
        conn_db.commit()
    except MySQLdb.Error as error:
        print(error.args[0])
        if(error.args[0] == 1146):
            sql_c = "CREATE TABLE `"+date_t+"` (\
              `id` int(11) NOT NULL AUTO_INCREMENT,\
              `time` varchar(45) NOT NULL,\
              `temp` int(11) DEFAULT NULL,\
               `humidity` int(11) DEFAULT NULL,\
               `pm2.5` DECIMAL(5,2) DEFAULT NULL,\
               `illumination` DECIMAL(5,2) NULL DEFAULT -1,\
               `weather` INT(11) NULL DEFAULT -1,\
	       `field1` DECIMAL(5,2) NULL DEFAULT -1,\
	       `field2` INT(11) NULL DEFAULT -1 ,\
               PRIMARY KEY (`id`)\
               ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;";
            n = cursor.execute(sql_c)
        if(error.args[0] == 2006):
            conn_db,cursor = db_init()
            n = 0
    return n
conn_db,cursor = db_init()
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
console_queue = queue.Queue(20)
queue_lock = threading.Lock() 
print("socket created")
ip_array = []
for i in range(1,255):
    ip_array.append("172.17.0.%s"%i)
try:
    s.bind((Host,port))
except socket.error as msg:
    print('Bind failed.Eroor code: '+str(msg[0])+' Messsage: '+msg[1])
    sys.exit()
print('Socket bind completed')
s.listen(10)
print('socket now listening')
while True:
    conn,addr=s.accept()
    print( time.asctime()+' Connected with '+addr[0]+' '+str(addr[1]))
    if(addr[0] not in ip_array):
            _thread.start_new_thread(clientThread,(conn,))
    else:
            _thread.start_new_thread(socket_control,(conn,))
s.close()
