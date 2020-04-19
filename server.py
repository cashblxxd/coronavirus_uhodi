from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SOCK_DGRAM
import _thread
import json
import random
from urllib.request import urlopen
import time


def get_local_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    h = s.getsockname()[0]
    s.close()
    return h


HOSTNAME = get_local_ip()
print('Public IP for clients:\033[1;32;40m', json.load(urlopen('http://jsonip.com'))['ip'], '\033[1;30;40m')


def start_server():
    global serversocket, clients, numbers_pool, ballspeed, height, width, speedlist
    port = 1234

    addr = (HOSTNAME, port)

    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversocket.bind(addr)
    serversocket.listen(10)
    numbers_pool = {1, 2, 3, 4}
    ballspeed = 5
    height = 800
    width = 800
    speedlist = [ballspeed, -1 * ballspeed, ballspeed / 2, -1 * (ballspeed / 2)]
    clients = {serversocket}


def update_ball():
    global ballx, bally, player1y, player2y, player3x, player4x, ballxvar, ballyvar
    global score1, score2, score3, score4

    if ballx <= 20 and bally >= player1y and bally <= (player1y + (80 + 1)):
        ballx = 20
        ballxvar = ballxvar * -1.1
        ballyvar = ballyvar * 1.1

    if ballx >= (width - 40) and bally >= player2y and bally <= (player2y + (80 + 2)):
        ballx = width - 40
        ballxvar = ballxvar * -1.1
        ballyvar = ballyvar * 1.1

    if bally <= 20 and ballx >= player3x and ballx <= (player3x + (80 + 3)):
        bally = 20
        ballyvar = ballyvar * -1.1
        ballxvar = ballxvar * 1.1

    if bally >= (height - 40) and ballx >= player4x and ballx <= (player4x + (4 + 80)):
        bally = height - 40
        ballyvar = ballyvar * -1.1
        ballxvar = ballxvar * 1.1

    if ballx <= 0 or ballx >= width - 20 or bally <= 0 or bally >= height - 20:
        if ballx <= 0:
            score2 += 1
            score4 += 1
            score3 += 1
        if ballx >= width - 20:
            score1 += 1
            score3 += 1
            score4 += 1
        if bally <= 0:
            score4 += 1
            score1 += 1
            score2 += 1
        if bally >= height - 20:
            score1 += 1
            score2 += 1
            score3 += 1
        player1y = height / 2 - (100 + 1)
        player2y = height / 2 - (100 + 2)
        player3x = width / 2 - (50 + 3)
        player4x = width / 2 - (50 + 4)
        ballx = random.randint(300, width - 300)
        bally = random.randint(300, height - 300)
        ballxvar = random.choice(speedlist)
        ballyvar = random.choice(speedlist)

    ballx += ballxvar
    bally += ballyvar


def processing(data):
    global player1y, player2y, player3x, player4x
    if data['get']:
        if data['action'] == 'get_ball':
            return {
                'ballx': ballx,
                'bally': bally,
            }
        elif data['action'] == 'get_player_number':
            if len(numbers_pool) == 0:
                return {'number': 0}
            else:
                return {'number': numbers_pool.pop()}
        elif data['action'] == 'get_updates':
            return {
                'player1y': player1y,
                'player2y': player2y,
                'player3x': player3x,
                'player4x': player4x
            }
        elif data['action'] == 'get_scores':
            return {
                'score1': score1,
                'score2': score2,
                'score3': score3,
                'score4': score4,

            }
        elif data['action'] == 'quit':
            numbers_pool.add(data['number'])
            return 'exit'
    else:
        if data['set'] == 'player1y':
            player1y = data['value']
        elif data['set'] == 'player2y':
            player2y = data['value']
        elif data['set'] == 'player3x':
            player3x = data['value']
        elif data['set'] == 'player4x':
            player4x = data['value']
        return {'success': True}


def handler(clientsocket, clientaddr):
    print("Accepted connection from: ", clientaddr)
    running = True
    while running:
        data = clientsocket.recv(1024).decode('utf-8')
        data = json.loads(data)
        update_ball()
        response = json.dumps(processing(data))
        if response != 'exit':
            clientsocket.send(f'{response}'.encode('utf-8'))
        else:
            running = False
    clients.remove(clientsocket)
    clientsocket.close()


def updater_hull(n):
    while len(clients) != 0:
        update_ball()
        time.sleep(30)


def main():
    global player1y, player2y, player3x, player4x, ballx, bally, ballxvar, ballyvar
    global score1, score2, score3, score4
    height = 600
    width = 800
    ballx = random.randint(300, width - 300)
    bally = random.randint(300, height - 300)
    ballxvar = random.choice(speedlist)
    ballyvar = random.choice(speedlist)
    player1y = height / 2 - (100 + 1)
    player2y = height / 2 - (100 + 2)
    player3x = width / 2 - (50 + 3)
    player4x = width / 2 - (50 + 4)
    score1, score2, score3, score4 = 0, 0, 0, 0
    _thread.start_new_thread(updater_hull, (1,))
    while True:
        try:
            print("Server is listening for connections\n")
            clientsocket, clientaddr = serversocket.accept()
            clients.add(clientsocket)
            _thread.start_new_thread(handler, (clientsocket, clientaddr))
        except KeyboardInterrupt:
            print("Closing server socket...")
            serversocket.close()


start_server()
main()