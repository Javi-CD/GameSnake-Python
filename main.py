
#*Librerias
import pygame 
from pygame.math import Vector2
from random import randrange
import os
import config

#*Configurar pantalla
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_SIZE, config.SCREEN_SIZE))

clock = pygame.time.Clock() 

#*Funciones
def read_best_score():
    if os.path.exists(best_score_file):
        with open(best_score_file, 'r') as file:
            return int(file.read())
    return 0

def save_best_score(score):
    with open(best_score_file, 'w') as file:
        file.write(str(score))

#*Archivo de mejor puntaje
best_score_file = 'best_score.txt'

best_score = read_best_score()
current_score = 0

#*Variables
running = True
begin = True
bait = True

time = None
snake_rect = None
snake_length = None
snake_parts = None
snake_direction = None

food_rect = None

while running:
    
    #*Iniciar el juego
    if begin:
        begin = False
        time = pygame.time.get_ticks()
        
        #*Posicion de la serpiente
        snake_rect = pygame.rect.Rect(
            [randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE), 
             randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE), 
             config.SNAKE_PART_SIZE,
             config.SNAKE_PART_SIZE])
        
        #*caracteristicas de la serpiente 
        snake_length = 1
        snake_parts = []
        snake_direction = Vector2(0,0)
    
    #*Posicion de la comida
    if bait:
        bait = False
        food_rect = pygame.rect.Rect(
            [randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE), 
             randrange(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE), 
             config.FOOD_SIZE,
             config.FOOD_SIZE])
    
    #*Eventos
    for event in pygame.event.get():
        
        #*Salir del juego
        if (event.type == pygame.QUIT or 
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running = False
        
        #*Mover la serpiente con las flechas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not snake_direction.y:
                snake_direction = Vector2(0, -config.SNAKE_MOVE_LENGTH)
            if event.key == pygame.K_DOWN and not snake_direction.y:
                snake_direction = Vector2(0, config.SNAKE_MOVE_LENGTH)
            if event.key == pygame.K_LEFT and not snake_direction.x:
                snake_direction = Vector2(-config.SNAKE_MOVE_LENGTH, 0)
            if event.key == pygame.K_RIGHT and not snake_direction.x:
                snake_direction = Vector2(config.SNAKE_MOVE_LENGTH, 0)
    
    time_now = pygame.time.get_ticks()
    
    #*Color de fondo
    screen.fill(config.COLOR_BG)
    
    #*Dibujar cuadricula
    for i in range(0, config.SCREEN_SIZE, config.GRID_CELL_SIZE):
        pygame.draw.line(screen, config.COLOR_GRID, (i, 0), (i, config.SCREEN_SIZE))
        pygame.draw.line(screen, config.COLOR_GRID, (0, i), (config.SCREEN_SIZE, i))
    
    #*Mover la serpiente
    if time_now - time > config.DELAY:
        
        time = time_now
        snake_rect.move_ip(snake_direction)
        snake_parts.append(snake_rect.copy())
        snake_parts = snake_parts[-snake_length:]
    
    #*Dibujar la comida
    pygame.draw.rect(screen, config.FOOD_COLOR, food_rect, 0, 10)
    
    #*Dibujar la serpiente
    [pygame.draw.rect(screen, config.SNAKE_COLOR, snake_part, 4, 1) 
     for snake_part in snake_parts]
    
    #*Colisiones
    if (snake_rect.left < 0 or snake_rect.right > config.SCREEN_SIZE or
            snake_rect.top < 0 or snake_rect.bottom > config.SCREEN_SIZE or
            snake_rect.collidelist(snake_parts[:-1]) != -1):
        begin = True
    
    #*Puntaje
    pygame.display.set_caption(f'Snake | Score: {snake_length - 1}')
    
    #*Mejor puntaje
    if snake_length - 1 > best_score:
        best_score = snake_length - 1
        save_best_score(best_score)
    
    #*Mostrar mejor puntaje
    pygame.display.set_caption(f'Snake | Score: {snake_length - 1} | Best Score: {best_score}')
    
    #*Comer la comida
    if snake_rect.colliderect(food_rect):
        bait = True
        snake_length += 1 
    
    #*Actualizar la pantalla
    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()