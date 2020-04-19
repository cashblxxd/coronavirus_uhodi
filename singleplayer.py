import pygame
import pygame.locals
import random
import time
from sys import exit
import json
import socket

coronaimage = pygame.image.load('virus.png')
coronaimage = pygame.transform.scale(coronaimage, (20, 20))
ballspeed = 5
speedlist = [ballspeed, -1 * ballspeed, ballspeed / 2, -1 * (ballspeed / 2)]
ballxvar = random.choice(speedlist)
ballyvar = random.choice(speedlist)
player_number = random.randrange(1, 5)

def update_ball():
    global ballx, bally, player1y, player2y, player3x, player4x, ballxvar, ballyvar
    global score1, score2, score3, score4

    if ballx <= 20 and (bally >= player1y and bally <= (player1y + (80 + 1)) or player_number != 1):
        ballx = 20
        ballxvar = ballxvar * -1.1
        ballyvar = ballyvar * 1.1

    if ballx >= (width - 40) and (bally >= player2y and bally <= (player2y + (80 + 2)) or player_number != 2):
        ballx = width - 40
        ballxvar = ballxvar * -1.1
        ballyvar = ballyvar * 1.1

    if bally <= 20 and (ballx >= player3x and ballx <= (player3x + (80 + 3)) or player_number != 3):
        bally = 20
        ballyvar = ballyvar * -1.1
        ballxvar = ballxvar * 1.1

    if bally >= (height - 40) and (ballx >= player4x and ballx <= (player4x + (4 + 80)) or player_number != 4):
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


def init():
    print(1)
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

    ballx = 400
    bally = 400

    myCanvas.fill((0, 0, 0))
    pygame.draw.rect(myCanvas, red, (0, player1y, 20, 100 + 1),
                     0)
    pygame.draw.rect(myCanvas, blue, (width - 20, player2y, 20, 100
                                      + 2), 0)
    pygame.draw.rect(myCanvas, yellow, (player3x, 0, 100 + 3,
                                        20), 0)
    pygame.draw.rect(myCanvas, green, (player4x, height - 20, 100
                                       + 4, 20), 0)
    myWindow.blit(myCanvas, (0, 0))
    myWindow.blit(score1display, score1rect)
    myWindow.blit(score2display, score2rect)
    myWindow.blit(score3display, score3rect)
    myWindow.blit(score4display, score4rect)
    myWindow.blit(coronaimage, (ballx, bally))
    pygame.display.flip()
    time.sleep(1)


def set_ball():
    update_ball()


def main():
    global red, blue, yellow, green, white
    global height, width, speedlist, ballspeed
    global myWindow, myCanvas, myFont, score1, score2, score3, score4, myClock, player1y, player2y, player3x, player4x
    global ballx, bally, ballxvar, ballyvar, player_number
    global score1display, score1rect, score2display, score2rect, score3display, score3rect, score4display, score4rect
    running = True
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
                #receive_server_data({'get': True, 'action': 'quit', 'number': player_number})
                running = False
        myClock.tick(30)
        #update(receive_server_data({'get': True, 'action': 'get_updates'}))
        myCanvas.fill((0, 0, 0))
        pygame.draw.rect(myCanvas, red, (0, player1y, 20, 100
                                         + 1), 0)
        pygame.draw.rect(myCanvas, blue, (width - 20, player2y, 20, 100
                                          + 2), 0)
        pygame.draw.rect(myCanvas, yellow, (player3x, 0, 100
                                            + 3, 20), 0)
        pygame.draw.rect(myCanvas, green, (player4x, height - 20, 100
                                           + 4, 20), 0)
        myWindow.blit(myCanvas, (0, 0))
        myWindow.blit(score1display, score1rect)
        myWindow.blit(score2display, score2rect)
        myWindow.blit(score3display, score3rect)
        myWindow.blit(score4display, score4rect)
        myWindow.blit(coronaimage, (ballx, bally))
        pygame.display.flip()

        # Keeping score
        set_ball()
        #set_scores()

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
        print(1)
        if keys[pygame.locals.K_w]:
            if player_number == 1 and player1y >= 0:
                player1y -= 20
                #receive_server_data({'get': False, 'set': 'player1y', 'value': player1y})
            elif player_number == 2 and player2y >= 0:
                player2y -= 20
                #receive_server_data({'get': False, 'set': 'player2y', 'value': player2y})
        elif keys[pygame.locals.K_s]:
            if player_number == 1 and player1y <= height - 101:
                player1y += 20
                #receive_server_data({'get': False, 'set': 'player1y', 'value': player1y})
            elif player_number == 2 and player2y <= height - 102:
                player2y += 20
                #receive_server_data({'get': False, 'set': 'player2y', 'value': player2y})
        elif keys[pygame.locals.K_a]:
            if player_number == 3 and player3x >= 0:
                player3x -= 20
                #receive_server_data({'get': False, 'set': 'player3x', 'value': player3x})
            elif player_number == 4 and player4x >= 0:
                player4x -= 20
                #receive_server_data({'get': False, 'set': 'player4x', 'value': player4x})
        elif keys[pygame.locals.K_d]:
            if player_number == 3 and player3x <= width - 103:
                player3x += 20
                #receive_server_data({'get': False, 'set': 'player3x', 'value': player3x})
            elif player_number == 4 and player4x <= width - 104:
                player4x += 20
                #receive_server_data({'get': False, 'set': 'player4x', 'value': player4x})

    #close_connection()


#open_connection()
init()
main()