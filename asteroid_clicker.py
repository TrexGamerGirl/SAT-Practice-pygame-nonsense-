import pygame
import sys

# =========================
# INIT
# =========================
pygame.init()

WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Clicker ☄️")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

# =========================
# LOAD IMAGES
# =========================
def load_image(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        print(f"⚠️ Could not load {path}")
        return None

asteroid_img = load_image("asteroid.png", (220, 220))

# fallback if no image
if asteroid_img:
    asteroid_rect = asteroid_img.get_rect(center=(WIDTH//2, HEIGHT//2))
else:
    asteroid_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 100, 200, 200)

upgrade_rect = pygame.Rect(140, 470, 220, 60)

# =========================
# GAME STATE
# =========================
ore = 0
laser_power = 1
upgrade_cost = 15

# click animation scale
click_scale = 1
click_timer = 0

# =========================
# GAME LOOP
# =========================
running = True
while running:
    dt = clock.tick(60) / 1000  # delta time

    screen.fill((10, 10, 25))  # deep space vibe 🌌

    # =========================
    # EVENTS
    # =========================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            # CLICK ASTEROID
            if asteroid_rect.collidepoint(mouse):
                ore += laser_power

                # trigger animation
                click_scale = 1.15
                click_timer = 0.1

            # UPGRADE
            if upgrade_rect.collidepoint(mouse):
                if ore >= upgrade_cost:
                    ore -= upgrade_cost
                    laser_power += 1
                    upgrade_cost = int(upgrade_cost * 1.6)

    # =========================
    # CLICK ANIMATION
    # =========================
    if click_timer > 0:
        click_timer -= dt
    else:
        click_scale = 1

    # =========================
    # DRAW ASTEROID
    # =========================
    if asteroid_img:
        scaled_size = int(220 * click_scale)
        scaled_img = pygame.transform.scale(asteroid_img, (scaled_size, scaled_size))
        rect = scaled_img.get_rect(center=asteroid_rect.center)
        screen.blit(scaled_img, rect)
    else:
        pygame.draw.ellipse(screen, (120, 120, 120), asteroid_rect)

    # =========================
    # DRAW UPGRADE BUTTON
    # =========================
    mouse = pygame.mouse.get_pos()
    hover = upgrade_rect.collidepoint(mouse)

    color = (70, 70, 90) if not hover else (100, 100, 140)
    pygame.draw.rect(screen, color, upgrade_rect, border_radius=8)

    upgrade_text = font.render(
        f"Upgrade Laser ({upgrade_cost})",
        True,
        (255, 255, 255)
    )
    screen.blit(upgrade_text, (upgrade_rect.x + 10, upgrade_rect.y + 15))

    # =========================
    # TEXT HUD
    # =========================
    ore_text = font.render(f"Ore: {ore}", True, (255, 255, 255))
    power_text = font.render(f"Laser Power: {laser_power}", True, (180, 220, 255))

    screen.blit(ore_text, (20, 20))
    screen.blit(power_text, (20, 55))

    # =========================
    # UPDATE
    # =========================
    pygame.display.flip()

pygame.quit()
sys.exit()