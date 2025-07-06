import pygame
import random
import math
import os
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
player_img = pygame.image.load("assets/player.png")
enemy_img = pygame.image.load("assets/enemy.png")
bullet_img = pygame.image.load("assets/bullet.png")
background_img = pygame.image.load("assets/background.png")
heart_img = pygame.image.load("assets/heart.png.webp") 
heart_img = pygame.transform.scale(heart_img, (30, 30))
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
explosion_img = pygame.image.load("assets/explosion.jpeg")  
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
player_x = 370
player_y = 480
player_x_change = 0

bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"

enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 10
enemy_speed_base = 2

score = 0
level = 1
lives = 3
game_over = False
paused = False
y_scroll = 0
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0
def show_text(text, x, y, size=40, color=(255, 255, 255)):
    fnt = pygame.font.Font(None, size)
    label = fnt.render(text, True, color)
    screen.blit(label, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(ex, ey, bx, by):
    return math.hypot(ex - bx, ey - by) < 27

def reset_enemy(i):
    enemy_x[i] = random.randint(0, 736)
    enemy_y[i] = random.randint(10, 100)

def draw_lives():
    for i in range(lives):
        screen.blit(heart_img, (680 + i * 35, 10))

def draw_background(y_offset):
    screen.blit(background_img, (0, y_offset % HEIGHT))
    screen.blit(background_img, (0, (y_offset % HEIGHT) - HEIGHT))

def spawn_enemies():
    for _ in range(num_enemies):
        enemy_x.append(random.randint(0, 736))
        enemy_y.append(random.randint(10, 100))
        enemy_x_change.append(enemy_speed_base)
        enemy_y_change.append(40)
spawn_enemies()
running = True
while running:
    if not paused:
        y_scroll += 0.5
        draw_background(y_scroll)
    else:
        screen.blit(big_font.render("PAUSED", True, (255, 255, 0)), (300, 250))
        show_text("Press P to Resume", 290, 320)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready" and not paused:
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
            if event.key == pygame.K_r and game_over:
                score = 0
                lives = 3
                level = 1
                bullet_y = 480
                bullet_state = "ready"
                game_over = False
                enemy_x.clear()
                enemy_y.clear()
                enemy_x_change.clear()
                enemy_y_change.clear()
                spawn_enemies()
            if event.key == pygame.K_p:
                paused = not paused

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_x_change = 0

    if not paused and not game_over:
        player_x += player_x_change
        player_x = max(0, min(player_x, 736))
        screen.blit(player_img, (player_x, player_y))

        for i in range(num_enemies):
            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = abs(enemy_x_change[i])
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -abs(enemy_x_change[i])
                enemy_y[i] += enemy_y_change[i]
            if enemy_y[i] > 440:
                lives -= 1
                reset_enemy(i)
                if lives == 0:
                    game_over = True
                    if score > high_score:
                        high_score = score
            if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                explosion_sound.play()
                bullet_y = 480
                bullet_state = "ready"
                score += 1
                reset_enemy(i)
                if score % 10 == 0:
                    level += 1
                    for j in range(num_enemies):
                        enemy_x_change[j] = (enemy_speed_base + level // 2) * (1 if enemy_x_change[j] > 0 else -1)

            screen.blit(enemy_img, (enemy_x[i], enemy_y[i]))

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"
    show_text("Score: " + str(score), 10, 10)
    show_text("Level: " + str(level), 10, 40)
    show_text("High Score: " + str(high_score), 10, 70)
    draw_lives()

    if game_over:
        screen.blit(big_font.render("GAME OVER", True, (255, 0, 0)), (250, 250))
        show_text("Press R to Restart", 270, 339)

    pygame.display.update()
