import pygame
import sys
import time
import random


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 10

# Window size
window_size_x = 800
window_size_y = 600
GRID_SIZE = 10

# Checks for errors
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_size_x, window_size_y))


# Colors (R, G, B)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
PURPLE = pygame.Color(160,32,240)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_position = [100, 60]
snake_body = [[100, 60], [100-GRID_SIZE, 60], [100-(2*10), 60]]

food_pos = [random.randrange(1, (window_size_x//GRID_SIZE)) * 10, random.randrange(1, (window_size_y//GRID_SIZE)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Game over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_size_x/2, window_size_y/4)
    game_window.fill(BLACK)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, RED, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (window_size_x/10, 15)
    else:
        score_rect.midtop = (window_size_x/2, window_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


#movement
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # prevent oppositve movement
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= GRID_SIZE
    elif direction == 'DOWN':
        snake_position[1] += GRID_SIZE
    elif direction == 'LEFT':
        snake_position[0] -= GRID_SIZE
    elif direction == 'RIGHT':
        snake_position[0] += GRID_SIZE

    # Snake body eating
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == food_pos[0] and snake_position[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food 
    if not food_spawn:
        food_pos = [random.randrange(1, (window_size_x//GRID_SIZE)) * 10, random.randrange(1, (window_size_y//GRID_SIZE)) * 10]
    food_spawn = True


    game_window.fill(BLACK)
    for pos in snake_body:
        # Snake body
        pygame.draw.rect(game_window, PURPLE, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))

    # Snake food
    pygame.draw.rect(game_window, RED, pygame.Rect(food_pos[0], food_pos[1], GRID_SIZE, GRID_SIZE))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_size_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_size_y-10:
        game_over()
    # Touching the body to end game
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, WHITE, 'consolas', 20)
    # Refresh screen
    pygame.display.update()
    # Refresh rate (difficulty adjuster)
    fps_controller.tick(difficulty)