import pygame
import sys

pygame.init()

# ---------------------------
# WINDOW
# ---------------------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Clicker: Ascension")

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 18)

# ---------------------------
# GAME STATE
# ---------------------------
score = 0
click_power = 1
prestige = 0
prestige_multiplier = 1.0

scroll_offset = 0

# Buildings
buildings = [
    {"name": "Cursor", "cost": 15, "cps": 1, "owned": 0},
    {"name": "Grandma", "cost": 50, "cps": 5, "owned": 0},
    {"name": "Farm", "cost": 150, "cps": 10, "owned": 0},
    {"name": "Mine", "cost": 500, "cps": 25, "owned": 0},
    {"name": "Factory", "cost": 1500, "cps": 75, "owned": 0},
    {"name": "Lab", "cost": 5000, "cps": 200, "owned": 0},
    {"name": "Portal", "cost": 20000, "cps": 500, "owned": 0},
]

# Upgrades
upgrades = [
    {"name": "Better Clicks", "cost": 100, "effect": "click", "value": 2, "bought": False},
    {"name": "Cursor Boost", "cost": 200, "effect": "Cursor", "value": 2, "bought": False},
    {"name": "Grandma Boost", "cost": 500, "effect": "Grandma", "value": 2, "bought": False},
]

# Passive income
PASSIVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PASSIVE_EVENT, 1000)

cookie_rect = pygame.Rect(50, 150, 250, 250)
prestige_btn = pygame.Rect(50, 450, 250, 50)

# ---------------------------
# HELPERS
# ---------------------------
def total_cps():
    total = 0
    for b in buildings:
        total += b["cps"] * b["owned"]
    return total * prestige_multiplier

def reset_game():
    global score, click_power
    score = 0
    click_power = 1
    for b in buildings:
        b["owned"] = 0
        b["cost"] = max(15, b["cost"] // 2)

# ---------------------------
# LOOP
# ---------------------------
while True:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Scroll shop
        if event.type == pygame.MOUSEWHEEL:
            scroll_offset += event.y * 20

        # Passive income
        if event.type == PASSIVE_EVENT:
            score += int(total_cps())

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            # Click cookie
            if cookie_rect.collidepoint(mouse):
                score += int(click_power * prestige_multiplier)

            # Prestige
            if prestige_btn.collidepoint(mouse):
                if score >= 10000:
                    prestige += int(score / 10000)
                    prestige_multiplier = 1 + prestige * 0.1
                    reset_game()

            # Buildings
            for i, b in enumerate(buildings):
                rect = pygame.Rect(350, 50 + i * 80 + scroll_offset, 300, 60)
                if rect.collidepoint(mouse):
                    if score >= b["cost"]:
                        score -= b["cost"]
                        b["owned"] += 1
                        b["cost"] = int(b["cost"] * 1.15)

            # Upgrades
            for i, u in enumerate(upgrades):
                rect = pygame.Rect(700, 50 + i * 70, 180, 60)
                if rect.collidepoint(mouse) and not u["bought"]:
                    if score >= u["cost"]:
                        score -= u["cost"]
                        u["bought"] = True

                        if u["effect"] == "click":
                            click_power *= u["value"]
                        else:
                            for b in buildings:
                                if b["name"] == u["effect"]:
                                    b["cps"] *= u["value"]

    # ---------------------------
    # DRAW COOKIE
    # ---------------------------
    pygame.draw.rect(screen, (150, 75, 0), cookie_rect)

    # Prestige button
    pygame.draw.rect(screen, (200, 50, 200), prestige_btn)
    p_text = font.render("Prestige (10k)", True, (255, 255, 255))
    screen.blit(p_text, (prestige_btn.x + 40, prestige_btn.y + 15))

    # ---------------------------
    # DRAW BUILDINGS (SCROLL)
    # ---------------------------
    for i, b in enumerate(buildings):
        rect = pygame.Rect(350, 50 + i * 80 + scroll_offset, 300, 60)

        if -100 < rect.y < HEIGHT:
            pygame.draw.rect(screen, (100, 100, 255), rect)

            txt = font.render(
                f"{b['name']} | {b['cost']} | Owned: {b['owned']}",
                True,
                (255, 255, 255),
            )
            screen.blit(txt, (rect.x + 10, rect.y + 20))

    # ---------------------------
    # DRAW UPGRADES
    # ---------------------------
    for i, u in enumerate(upgrades):
        rect = pygame.Rect(700, 50 + i * 70, 180, 60)

        color = (50, 200, 50) if not u["bought"] else (80, 80, 80)
        pygame.draw.rect(screen, color, rect)

        txt = font.render(u["name"], True, (0, 0, 0))
        screen.blit(txt, (rect.x + 10, rect.y + 20))

    # ---------------------------
    # UI TEXT
    # ---------------------------
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (20,20))
    screen.blit(font.render(f"CPS: {int(total_cps())}", True, (255,255,255)), (20,50))
    screen.blit(font.render(f"Prestige: {prestige}", True, (255,255,255)), (20,80))
    screen.blit(font.render(f"Multiplier: x{prestige_multiplier:.1f}", True, (255,255,255)), (20,110))

    pygame.display.flip()
    clock.tick(60)