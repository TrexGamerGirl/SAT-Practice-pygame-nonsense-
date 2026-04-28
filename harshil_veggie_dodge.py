import pygame
import random
import sys
import os

pygame.init()

# ----------------------------
# SETTINGS
# ----------------------------
WIDTH, HEIGHT = 500, 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Harshil Veggie Dodge")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

ASSET_PATH = "assets"

# ----------------------------
# HELPER: LOAD IMAGE SAFELY
# ----------------------------
def load_image(name, size):
    path = os.path.join(ASSET_PATH, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        print(f"Missing asset: {name}")
        return None

# ----------------------------
# PLAYER
# ----------------------------
class Player:
    def __init__(self):
        self.width = 60
        self.height = 60
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 100
        self.speed = 7

        self.image = load_image("harshil.png", (self.width, self.height))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        self.x = max(0, min(WIDTH - self.width, self.x))

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (50,150,255), (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# ----------------------------
# VEGGIE
# ----------------------------
class Veggie:
    def __init__(self, images):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(4, 7)

        self.image = random.choice(images)

    def update(self):
        self.y += self.speed

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0,255,0), (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# ----------------------------
# GAME
# ----------------------------
class Game:
    def __init__(self):
        self.player = Player()

        # Load veggie sprites
        self.veggie_images = [
            load_image("carrot.png", (40,40)),
            load_image("broccoli.png", (40,40)),
            load_image("tomato.png", (40,40)),
        ]

        self.veggies = []
        self.spawn_timer = 0
        self.spawn_delay = 30

        self.score = 0
        self.game_over = False

    def spawn_veggie(self):
        self.veggies.append(Veggie(self.veggie_images))

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys)

        # Spawn system
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_veggie()
            self.spawn_timer = 0

        # Update veggies
        for veg in self.veggies:
            veg.update()

        # Remove off-screen + score
        self.veggies = [v for v in self.veggies if not v.off_screen()]
        self.score += 1

        # Collision
        player_rect = self.player.get_rect()
        for veg in self.veggies:
            if player_rect.colliderect(veg.get_rect()):
                self.game_over = True

    def draw(self):
        screen.fill((30,30,30))

        self.player.draw()

        for veg in self.veggies:
            veg.draw()

        # Score
        score_text = font.render(f"Score: {self.score}", True, (255,255,255))
        screen.blit(score_text, (10,10))

        if self.game_over:
            text = font.render("GAME OVER 😭", True, (255,50,50))
            screen.blit(text, (WIDTH//2 - 100, HEIGHT//2))

# ----------------------------
# MAIN LOOP
# ----------------------------
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.update()
    game.draw()

    pygame.display.flip()
    clock.tick(FPS)