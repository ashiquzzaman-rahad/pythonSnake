import pygame
import os
import random

pygame.mixer.init()
pygame.init()


#colours
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

#game window
screen_height = 500
screen_width = 700
gameWindow = pygame.display.set_mode((screen_width,screen_height))
bgimg = pygame.image.load("backimg2.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()
bgimg2 = pygame.image.load("welcomeimg.jpg")
bgimg2 = pygame.transform.scale(bgimg2,(screen_width,screen_height)).convert_alpha()
bgimg3 = pygame.image.load("game-over-wallpaper.png")
bgimg3 = pygame.transform.scale(bgimg3,(screen_width,screen_height)).convert_alpha()
pygame.display.set_caption("Snake with Rahad")
pygame.display.update()
#clock
clock = pygame.time.Clock()
#score update on screen
font = pygame.font.SysFont(None,35)

def text_score(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

#snake plotting
def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x,y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(bgimg2,(0,0))
        text_score("Welcome To Snake Game!", black,int(screen_width/4),int(screen_height/2.3))
        text_score("Press Space To Play!", black,int(screen_width/3.5),int(screen_height/1.8))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("Back.mp3")
                    pygame.mixer.music.play()
                    game_loop()
        pygame.display.update()
        clock.tick(40)

def game_loop():
    # game variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    init_velocity = 4
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    food_x = random.randint(20, int(screen_width / 1.5))
    food_y = random.randint(20, int(screen_height / 1.5))
    score = 0
    snake_size = 20
    fps = 40

#check if file exists
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")

    with open("hiscore.txt","r") as f:
        hiscore = f.read()

    #game loop
    while not exit_game:
        if game_over:
            with open("hiscore.txt","w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(bgimg3,(0,0))
            text_score("Press Enter To Continue",red,int(screen_width/4),int(screen_height/1.2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score += 10
                    if event.key == pygame.K_c:
                        hiscore = 0


            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 18 and abs(snake_y - food_y) < 18:
                score += 10
                snk_length += 5
                if score > int(hiscore):
                   hiscore = score
                food_x = random.randint(20, int(screen_width / 1.5))
                food_y = random.randint(20, int(screen_height / 1.5))

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_score("Score:"+str(score)+" High Score:"+str(hiscore),red,5,5)
            pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()

            plot_snake(gameWindow,black,snk_list,snake_size)
            #pygame.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size])
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()
