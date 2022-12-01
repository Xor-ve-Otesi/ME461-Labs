import socket
from _thread import *

ssid = "AndroidAP3E19"
password = "navq1475"
ThreadCount = 0

health1 = 1
health2 = 1
score1 = 0
score2 = 0
turn = 1
pongspeed = 100

# Open socket
addr = socket.getaddrinfo("192.168.43.139", 1250)[0][-1]
ServerSideSocket = socket.socket()
ServerSideSocket.bind(addr)
ServerSideSocket.listen(5)

print('listening on', addr)

def multi_threaded_client(connection):

    global health1, health2, score1, score2, turn, pongspeed

    while True:
        data = connection.recv(2048)
        response = str(data.decode('utf-8'))


        response = response.split(',')
        print(response)

        if response[0] != str(-1):
            pongspeed = int(response[0])
        if response[1] != str(-1):
            turn = int(response[1])
        if response[2] != str(-1):
            health1 = int(response[2])
        if response[3] != str(-1):
            health2 = int(response[3])
        if response[4] != str(-1):
            score1 = int(response[4])
        try:
            if response[5] != str(-1):
                score2 = int(response[5])
        except:
            if response[5] != "0-1":
                score2 = 0
        if not data:
            break

        gamedata = str(pongspeed) + "," + str(turn) + "," + str(health1) + "," + str(health2) + "," + str(score1) + "," + str(score2)
        print(gamedata)
        connection.sendall(str.encode(gamedata))

    connection.close()

clients = []

while True:

    Client, address = ServerSideSocket.accept()
    clients.append(Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))