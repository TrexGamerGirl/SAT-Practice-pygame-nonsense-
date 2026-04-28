import pygame
import random
import math

pygame.init()

# WINDOW
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shape Roguelike")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# PLAYER
player_pos = [WIDTH//2, HEIGHT//2]
player_speed = 5
player_radius = 15
player_hp = 100

# COMBAT
bullets = []
bullet_speed = 8
bullet_damage = 10
attack_cooldown = 500
last_shot = pygame.time.get_ticks()

# ENEMIES
enemies = []
spawn_delay = 1000
last_spawn = pygame.time.get_ticks()

# PROGRESSION
xp = 0
level = 1
xp_needed = 10

def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        return [random.randint(0, WIDTH), 0]
    if side == "bottom":
        return [random.randint(0, WIDTH), HEIGHT]
    if side == "left":
        return [0, random.randint(0, HEIGHT)]
    if side == "right":
        return [WIDTH, random.randint(0, HEIGHT)]

def shoot():
    global last_shot
    now = pygame.time.get_ticks()
    if now - last_shot > attack_cooldown:
        if enemies:
            target = min(enemies, key=lambda e: math.hypot(e[0]-player_pos[0], e[1]-player_pos[1]))
            dx = target[0] - player_pos[0]
            dy = target[1] - player_pos[1]
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx/dist, dy/dist
                bullets.append([player_pos[0], player_pos[1], dx, dy])
        last_shot = now

def level_up():
    global level, xp, xp_needed, bullet_damage, attack_cooldown
    level += 1
    xp = 0
    xp_needed += 5

    upgrade = random.choice(["damage", "speed"])

    if upgrade == "damage":
        bullet_damage += 5
    elif upgrade == "speed":
        attack_cooldown = max(100, attack_cooldown - 50)

running = True
while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # MOVEMENT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos[1] -= player_speed
    if keys[pygame.K_s]: player_pos[1] += player_speed
    if keys[pygame.K_a]: player_pos[0] -= player_speed
    if keys[pygame.K_d]: player_pos[0] += player_speed

    # SHOOTING
    shoot()

    # SPAWN ENEMIES
    if pygame.time.get_ticks() - last_spawn > spawn_delay:
        enemies.append(spawn_enemy())
        last_spawn = pygame.time.get_ticks()

    # UPDATE ENEMIES
    for enemy in enemies[:]:
        dx = player_pos[0] - enemy[0]
        dy = player_pos[1] - enemy[1]
        dist = math.hypot(dx, dy)

        if dist != 0:
            enemy[0] += dx/dist * 2
            enemy[1] += dy/dist * 2

        # HIT PLAYER
        if dist < player_radius + 10:
            player_hp -= 1

    # UPDATE BULLETS
    for bullet in bullets[:]:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed

        for enemy in enemies[:]:
            if math.hypot(enemy[0]-bullet[0], enemy[1]-bullet[1]) < 10:
                enemies.remove(enemy)
                bullets.remove(bullet)
                xp += 1
                break

    # LEVEL UP CHECK
    if xp >= xp_needed:
        level_up()

    # DRAW PLAYER
    pygame.draw.circle(screen, (0, 200, 255), (int(player_pos[0]), int(player_pos[1])), player_radius)

    # DRAW ENEMIES
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 50, 50), (*enemy, 20, 20))

    # DRAW BULLETS
    for bullet in bullets:
        pygame.draw.circle(screen, (255, 255, 0), (int(bullet[0]), int(bullet[1])), 5)

    # UI
    screen.blit(font.render(f"HP: {player_hp}", True, (255,255,255)), (10, 10))
    screen.blit(font.render(f"XP: {xp}/{xp_needed}", True, (255,255,255)), (10, 40))
    screen.blit(font.render(f"Level: {level}", True, (255,255,255)), (10, 70))

    pygame.display.flip()

pygame.quit()