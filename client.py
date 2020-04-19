import pygame
import pygame.locals
import random
import time
from sys import exit
import json
import socket


HOSTNAME = input('\033[1;32;40mEnter server IP address: ')  # enter the public ip of your server
print('\033[1;30;40m')


def open_connection():
    global clientsocket, buf
    port = 1234
    buf = 1024
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOSTNAME, port))


def server_send(js_str):
    clientsocket.send(js_str.encode('utf-8'))
    return clientsocket.recv(buf).decode('utf-8')


def close_connection():
    clientsocket.close()


def init():
    global red, blue, yellow, green, white
    global height, width, speedlist, ballspeed
    global myWindow, myCanvas, myFont, score1, score2, score3, score4, myClock, player1y, player2y, player3x, player4x
    global ballx, bally, ballxvar, ballyvar
    global score1display, score1rect, score2display, score2rect, score3display, score3rect, score4display, score4rect
    global clientsocket

    ballspeed = 5

    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)

    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    set_scores()

    height = 800
    width = 800

    pygame.init()
    myWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Коронавирус, уходи! 4P')

    myCanvas = pygame.Surface(myWindow.get_size())
    myCanvas.fill((0, 0, 0))

    myClock = pygame.time.Clock()

    myFont = pygame.font.Font(None, 48)

    score1display = myFont.render(str(score1), True, red)
    score1rect = score1display.get_rect()
    score2display = myFont.render(str(score2), True, blue)
    score2rect = score2display.get_rect()
    score1rect.centerx = 24
    score1rect.centery = 24
    score2rect.centerx = width - 24
    score2rect.centery = 24
    score3display = myFont.render(str(score3), True, yellow)
    score3rect = score3display.get_rect()
    score4display = myFont.render(str(score4), True, green)
    score4rect = score4display.get_rect()
    score3rect.centerx = 24
    score3rect.centery = height - 24
    score4rect.centerx = width - 24
    score4rect.centery = height - 24

    player1y = height / 2 - 100
    player2y = height / 2 - 100
    player3x = width / 2 - 50
    player4x = width / 2 - 50

    ballx = 0
    bally = 0
    set_ball()

    myCanvas.fill((0, 0, 0))
    pygame.draw.rect(myCanvas, red, (0, player1y, 20, 100 + 1),
                     0)
    pygame.draw.rect(myCanvas, blue, (width - 20, player2y, 20, 100
                                      + 2), 0)
    pygame.draw.rect(myCanvas, yellow, (player3x, 0, 100 + 3,
                                        20), 0)
    pygame.draw.rect(myCanvas, green, (player4x, height - 20, 100
                                       + 4, 20), 0)
    pygame.draw.rect(myCanvas, white, (ballx, bally, 20, 20), 0)
    myWindow.blit(myCanvas, (0, 0))
    myWindow.blit(score1display, score1rect)
    myWindow.blit(score2display, score2rect)
    myWindow.blit(score3display, score3rect)
    myWindow.blit(score4display, score4rect)
    pygame.display.flip()
    time.sleep(1)


def receive_server_data(idata):
    return json.loads(server_send(json.dumps(idata)))


def set_player():
    global player_number
    player_number = receive_server_data({'get': True, 'action': 'get_player_number'})['number']


def set_scores():
    global score1, score2, score3, score4
    data = receive_server_data({'get': True, 'action': 'get_scores'})
    score1 = data['score1']
    score2 = data['score2']
    score3 = data['score3']
    score4 = data['score4']


def set_ball():
    global ballx, bally
    data = receive_server_data({'get': True, 'action': 'get_ball'})
    ballx = data['ballx']
    bally = data['bally']


def update(data):
    global player1y, player2y, player3x, player4x
    try:
        player1y = int(data['player1y'])
    except Exception:
        print('Can\'t set player1y')
    try:
        player2y = int(data['player2y'])
    except Exception:
        print('Can\'t set player2y')
    try:
        player3x = int(data['player3x'])
    except Exception:
        print('Can\'t set player3x')
    try:
        player4x = int(data['player4x'])
    except Exception:
        print('Can\'t set player4x')


def main():
    global red, blue, yellow, green, white
    global height, width, speedlist, ballspeed
    global myWindow, myCanvas, myFont, score1, score2, score3, score4, myClock, player1y, player2y, player3x, player4x
    global ballx, bally, ballxvar, ballyvar, player_number
    global score1display, score1rect, score2display, score2rect, score3display, score3rect, score4display, score4rect
    running = True
    set_player()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(
                    '''
                    Final Scores
                    \tP1:''',
                    score1,
                    '\n\tP2:',
                    score2,
                    '\n\tP3:',
                    score3,
                    '\n\tP4:',
                    score4,
                )
                if score1 > score2 and score1 > score3 and score1 > score4:
                    print('P1 wins!')
                if score2 > score3 and score2 > score1 and score2 > score4:
                    print('P2 wins!')
                if score2 < score3 and score3 > score1 and score3 > score4:
                    print('P3 wins!')
                if score4 > score3 and score4 > score1 and score2 < score4:
                    print('P4 wins!')
                receive_server_data({'get': True, 'action': 'quit', 'number': player_number})
                running = False
        myClock.tick(30)
        update(receive_server_data({'get': True, 'action': 'get_updates'}))
        myCanvas.fill((0, 0, 0))
        pygame.draw.rect(myCanvas, red, (0, player1y, 20, 100
                                         + 1), 0)
        pygame.draw.rect(myCanvas, blue, (width - 20, player2y, 20, 100
                                          + 2), 0)
        pygame.draw.rect(myCanvas, yellow, (player3x, 0, 100
                                            + 3, 20), 0)
        pygame.draw.rect(myCanvas, green, (player4x, height - 20, 100
                                           + 4, 20), 0)
        pygame.draw.rect(myCanvas, white, (ballx, bally, 20, 20), 0)
        myWindow.blit(myCanvas, (0, 0))
        myWindow.blit(score1display, score1rect)
        myWindow.blit(score2display, score2rect)
        myWindow.blit(score3display, score3rect)
        myWindow.blit(score4display, score4rect)
        pygame.display.flip()

        # Keeping score
        set_ball()
        set_scores()

        score1display = myFont.render(str(score1), True, red)
        score1rect = score1display.get_rect()
        score2display = myFont.render(str(score2), True, blue)
        score2rect = score2display.get_rect()
        score1rect.centerx = 24
        score1rect.centery = height - 24
        score2rect.centerx = width - 24
        score2rect.centery = 24
        score3display = myFont.render(str(score3), True, yellow)
        score3rect = score3display.get_rect()
        score4display = myFont.render(str(score4), True, green)
        score4rect = score4display.get_rect()
        score3rect.centerx = 24
        score3rect.centery = 24
        score4rect.centerx = width - 24
        score4rect.centery = height - 24

        keys = pygame.key.get_pressed()
        if keys[pygame.locals.K_w]:
            if player_number == 1 and player1y >= 0:
                player1y -= 20
                receive_server_data({'get': False, 'set': 'player1y', 'value': player1y})
            elif player_number == 2 and player2y >= 0:
                player2y -= 20
                receive_server_data({'get': False, 'set': 'player2y', 'value': player2y})
        elif keys[pygame.locals.K_s]:
            if player_number == 1 and player1y <= height - 101:
                player1y += 20
                receive_server_data({'get': False, 'set': 'player1y', 'value': player1y})
            elif player_number == 2 and player2y <= height - 102:
                player2y += 20
                receive_server_data({'get': False, 'set': 'player2y', 'value': player2y})
        elif keys[pygame.locals.K_a]:
            if player_number == 3 and player3x >= 0:
                player3x -= 20
                receive_server_data({'get': False, 'set': 'player3x', 'value': player3x})
            elif player_number == 4 and player4x >= 0:
                player4x -= 20
                receive_server_data({'get': False, 'set': 'player4x', 'value': player4x})
        elif keys[pygame.locals.K_d]:
            if player_number == 3 and player3x <= width - 103:
                player3x += 20
                receive_server_data({'get': False, 'set': 'player3x', 'value': player3x})
            elif player_number == 4 and player4x <= width - 104:
                player4x += 20
                receive_server_data({'get': False, 'set': 'player4x', 'value': player4x})

    close_connection()


open_connection()
init()
main()