import pygame
import random
import sys


pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Harshil Veggie Dodge")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 30)

interval = 250
last_time = pygame.time.get_ticks()


player_width = 60
player_height = 60
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 100
player_speed = 7

# player colour (placeholder for sprites)
player_color = (50, 150, 255)


veggies = []
veggie_width = 40
veggie_height = 40
veggie_speed = 5
spawn_rate = 30  # lower = more frequent

# Veggie colors (placeholder for sprites)
veggie_colors = [
    (0, 200, 0),    # broccoli
    (255, 165, 0),  # carrot
    (255, 0, 0),    # tomato
    (200, 255, 0)   #lettuce
]


score = 0
game_over = False



def draw_player(x, y):
    pygame.draw.rect(screen, player_color, (x, y, player_width, player_height))

def spawn_veggie():
    x = random.randint(0, WIDTH - veggie_width)
    color = random.choice(veggie_colors)
    veggies.append([x, -veggie_height, color])

def draw_veggies():
    for veg in veggies:
        pygame.draw.rect(screen, veg[2], (veg[0], veg[1], veggie_width, veggie_height))

def move_veggies():
    for veg in veggies:
        veg[1] += veggie_speed

    # Remove off-screen veggies and increase score
    veggies[:] = [veg for veg in veggies if veg[1] < HEIGHT]

def check_collision():
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    
    for veg in veggies:
        veg_rect = pygame.Rect(veg[0], veg[1], veggie_width, veggie_height)
        if player_rect.colliderect(veg_rect):
            return True
    return False

def increment_score():
    global score
    score += 1

def draw_score():
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def draw_game_over():
    text = font.render("GAME OVER ", True, (255, 50, 50))
    screen.blit(text, (WIDTH//2 - 100, HEIGHT//2))


while True:
    screen.fill((30, 30, 30))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        # Movement
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # player inside screen stops moving foreward or back
        player_x = max(0, min(WIDTH - player_width, player_x))

        # Spawn veggies
        if random.randint(1, spawn_rate) == 1:
            spawn_veggie()

        # Update veggies
        move_veggies()

        # Collision check
        if check_collision():
            game_over = True

    current_time = pygame.time.get_ticks()
    if current_time - last_time >= interval and not game_over:
        increment_score()
        last_time = current_time

    # Draw everything
    draw_player(player_x, player_y)
    draw_veggies()
    draw_score()


    if game_over:
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)