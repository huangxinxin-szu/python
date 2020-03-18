#!/usr/bin/python3
import socket
import sys

json_file_path = "/home/admin-kn1/nscc/scripts/data/startlight_err_data.json"
port = 12345

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()

serversocket.bind(("0.0.0.0", port))
serversocket.listen(5)

while True:
	clientsocket,addr = serversocket.accept() 
	json_file = open(json_file_path, mode='r')
	json_date = json_file.readline()
	data_send = clientsocket.sendall(json_date.encode('utf-8'))  # 发送数据
	json_file.close()
	clientsocket.close()
	print("{} bytes data had been sent".format(data_send))

serversocket.close()
