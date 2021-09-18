import pygame
import sys
import os

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 500

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'background.jpg_large'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 120

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)

WINNER_FONT = pygame.font.SysFont('comicsans', 85)

pygame.display.set_caption('Ultimate Spaceship Battle')

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

SPEED = 2
BULLET_SPEED = 7

X_WING_COLLISION = pygame.USEREVENT + 1
RED_COLLISION = pygame.USEREVENT + 2

LIMIT = pygame.Rect(WIDTH // 2 - 5, 0, 20, HEIGHT)

x_wing_bullets = []
tie_fighter_bullets = []

X_WING_IMAGE = pygame.image.load(os.path.join('Assets', 'x_wing.png'))
X_WING = pygame.transform.rotate(pygame.transform.scale(X_WING_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

TIE_FIGHTER_IMAGE = pygame.image.load(os.path.join('Assets', 'tie_fighter.png'))
TIE_FIGHTER = pygame.transform.rotate(pygame.transform.scale(TIE_FIGHTER_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def window_display(x_wing, red, x_wing_health, red_health):
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(X_WING, (x_wing.x, x_wing.y))
    WINDOW.blit(TIE_FIGHTER, (red.x, red.y))
    pygame.draw.rect(WINDOW, BLACK, LIMIT)

    x_wing_player_text = HEALTH_FONT.render(f'Health remaining: {x_wing_health} ({round(100 / 15 * x_wing_health)})%', 1, WHITE)
    red_player_text = HEALTH_FONT.render(f'Health remaining: {red_health} ({round(100 / 15 * red_health)})%', 1, WHITE)

    WINDOW.blit(x_wing_player_text, (15, 15))
    WINDOW.blit(red_player_text, (WIDTH - 15 - red_player_text.get_width(), 15))

    handle_x_wing_bullets(red)
    handle_tie_fighter_bullets(x_wing)

    pygame.display.update()

def handle_x_wing_bullets(red):
    for bullet in x_wing_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
        bullet.x += BULLET_SPEED

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_COLLISION))
            x_wing_bullets.remove(bullet)

def handle_tie_fighter_bullets(x_wing):
    for bullet in tie_fighter_bullets:
        pygame.draw.rect(WINDOW, GREEN, bullet)
        bullet.x -= BULLET_SPEED

        if x_wing.colliderect(bullet):
            pygame.event.post(pygame.event.Event(X_WING_COLLISION))
            tie_fighter_bullets.remove(bullet)

def x_wing_key_controls(key, x_wing):
    if key[pygame.K_a] and x_wing.x - SPEED > 0:
        x_wing.x -= SPEED
    if key[pygame.K_d] and x_wing.x + SPEED + x_wing.width < LIMIT.x:
        x_wing.x += SPEED
    if key[pygame.K_w] and x_wing.y - SPEED > 0:
        x_wing.y -= SPEED
    if key[pygame.K_s] and x_wing.y + SPEED + x_wing.height < HEIGHT - 15:
        x_wing.y += SPEED

def red_key_controls(key, red):
    if key[pygame.K_LEFT] and red.x - SPEED - 14 > LIMIT.x + LIMIT.width:
        red.x -= SPEED
    if key[pygame.K_RIGHT] and red.x + SPEED + red.width < WIDTH: 
        red.x += SPEED
    if key[pygame.K_UP] and red.y - SPEED > 0:
        red.y -= SPEED
    if key[pygame.K_DOWN] and red.y + SPEED + red.height < HEIGHT - 15:
        red.y += SPEED

def display_winner(text):
    WINDOW.blit(text, ((WIDTH / 2 - text.get_width() // 2), (HEIGHT - text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    red = pygame.Rect(WIDTH - 40, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    x_wing = pygame.Rect(0, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()

    x_wing_health = 15
    red_health = 15

    winner_text = ''

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(x_wing.x, x_wing.y, 10, 2)
                    x_wing_bullets.append(bullet)

                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x, red.y, 10, 2)
                    tie_fighter_bullets.append(bullet)

            if event.type == X_WING_COLLISION:
                x_wing_health -= 3

            if event.type == RED_COLLISION:
                red_health -= 3

            if x_wing_health <= 0:
                winner_text = WINNER_FONT.render('Tie Fighter Wins!', 1, WHITE)
                
            if red_health <= 0:
                winner_text = WINNER_FONT.render('X Wing Wins!', 1, WHITE)

            if winner_text != '':
                display_winner(winner_text)
                sys.exit()

        keys = pygame.key.get_pressed()
        x_wing_key_controls(keys, x_wing)
        red_key_controls(keys, red)
    
        window_display(x_wing, red, x_wing_health, red_health)

        pygame.display.update()

if __name__ == '__main__':
    main()
