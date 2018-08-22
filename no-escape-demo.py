import pygame, time, random

pygame.init()

height = 600
width = 600
gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Survive')
clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
red = (190,0,0)

playerImg = pygame.image.load('player.png')
bombImg = pygame.image.load('bomb.png')
loseImg = pygame.image.load('LOSS.png')

imgHeight, imgWidth = 55, 48

bombs = []
high_score = 0

def message_display(message):
    font = pygame.font.Font("freesansbold.ttf", 28)
    TextSurf = font.render(message, True, red)
    TextBounds = TextSurf.get_rect()
    TextBounds.center = (300, 275)
    loss()
    gameDisplay.blit(TextSurf, TextBounds)
    pygame.display.update()
    bombs.clear()
    time.sleep(2)
    game_loop()

def score_display(score):
    font = pygame.font.Font("freesansbold.ttf", 20)
    TextSurf = font.render("Score: " + str(score), True, black)
    TextBounds = TextSurf.get_rect()
    TextBounds.center = (60, 20)
    gameDisplay.blit(TextSurf, TextBounds)

def high_score_display(high):
    font = pygame.font.Font("freesansbold.ttf", 20)
    TextSurf = font.render("High Score: " + str(high), True, black)
    TextBounds = TextSurf.get_rect()
    TextBounds.center = (520, 20)
    gameDisplay.blit(TextSurf, TextBounds)
    
    
def player(x,y):
    gameDisplay.blit(playerImg, (x,y))
    
def bomb(x,y):
    gameDisplay.blit(bombImg, (x,y))

def loss():
    gameDisplay.blit(loseImg, (0,0))
    

def place_new_bomb(playerCol, playerRow):
    outOfBounds = True
    (x,y) = (0,0)
    count = 0
    while outOfBounds:
        rand = random.randint(1,4)        
        if (rand == 1) and (playerCol > 1):
            (x,y) = grid_pos(playerCol-1, playerRow)
        elif (rand == 2) and (playerRow > 1):
            (x,y) = grid_pos(playerCol, playerRow-1)
        elif (rand == 3) and (playerCol < 5):
            (x,y) = grid_pos(playerCol+1, playerRow)    
        elif (rand == 4) and (playerRow < 5):
            (x,y) = grid_pos(playerCol, playerRow+1)
        if (x,y) != (0,0):
            outOfBounds = False
    if (x,y) in bombs:
        (x,y) = place_new_bomb(playerCol, playerRow)
    return (x,y)

    

def place_bombs():
    for coordinate in bombs:
        bomb(coordinate[0], coordinate[1])

def grid_pos(column, row):
    x_coordinate = (119*(column-1)) + 119/2 - imgWidth/2
    y_coordinate = (119*(row-1)) + 63 - imgHeight/2
    return (x_coordinate, y_coordinate)
    

def game_loop():    
    gameExit = False
    curX = 3
    curY = 3
    score = 0
    global high_score
    playerPos = grid_pos(curX,curY)
    square_size = 119
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and curX < 5:
                    curX += 1
                    bombs.append(place_new_bomb(curX, curY))
                    score += 1                    
                if event.key == pygame.K_LEFT and curX > 1:
                    curX -= 1
                    bombs.append(place_new_bomb(curX, curY))
                    score += 1                    
                if event.key == pygame.K_UP and curY > 1:
                    curY -= 1
                    bombs.append(place_new_bomb(curX, curY))
                    score += 1                    
                if event.key == pygame.K_DOWN and curY < 5:
                    curY += 1
                    bombs.append(place_new_bomb(curX, curY))
                    score += 1
        gameDisplay.fill(black)
        ##############
        for row in range(5):
            for column in range(5):
                square = pygame.Rect(row*(square_size+1),
                                     column*(square_size+1),
                                     square_size, square_size)
                pygame.draw.rect(gameDisplay, white, square)
        ##############
        playerPos = grid_pos(curX,curY)
        place_bombs()
        player(playerPos[0], playerPos[1])
        score_display(score)
        high_score_display(high_score)
        for coordinate in bombs:
            if ((playerPos[0] == coordinate[0]) and
            (playerPos[1] == coordinate[1])):
                if score > high_score:
                    high_score = score-1
                    
                message_display("You stepped on a trap! Final score: " + str(score-1))
        pygame.display.update()
        clock.tick(60)

game_loop()
