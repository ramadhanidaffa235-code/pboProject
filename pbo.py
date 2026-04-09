import pygame
import random

pygame.init()
pygame.mixer.init()  # aktifkan sound

# layar
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tembak naga")

clock = pygame.time.Clock()

# =====================
# LOAD GAMBAR
# =====================
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# 🔊 LOAD SOUND
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# =====================
# CLASS
# =====================

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Player(GameObject):
    def __init__(self):
        super().__init__(WIDTH//2 - 25, HEIGHT - 100, 50, 50)
        self.speed = 5
        self.image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(self.image, (120, 120))

    def move(self, key_input):
        if key_input[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if key_input[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class Enemy(GameObject):
    def __init__(self):
        x = random.randint(0, WIDTH - 40)
        super().__init__(x, 0, 40, 40)
        self.speed = random.randint(3, 6)
        self.image = pygame.image.load("enemy.png")
        self.image = pygame.transform.scale(self.image, (120, 120))

    def fall(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH - 40)

    def draw(self):
        screen.blit(self.image, self.rect)

# 🔫 CLASS PELURU
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = 7

    def move(self):
        self.rect.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)

# =====================
# SETUP
# =====================
player = Player()
enemy = Enemy()
bullets = []

score = 0
lives = 3
game_over = False

font = pygame.font.SysFont(None, 23)

# =====================
# LOOP
# =====================
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 🔫 TEMBAK
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))
                shoot_sound.play()  # suara tembak

        # restart
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player = Player()
                    enemy = Enemy()
                    bullets = []
                    score = 0
                    lives = 3
                    game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)

        enemy.fall()
        score += 1

        # musuh makin cepat
        enemy.speed = 3 + score // 200

        # gerak peluru
        for bullet in bullets:
            bullet.move()

        # hapus peluru keluar layar
        bullets = [b for b in bullets if b.rect.y > 0]

        # 💥 collision peluru vs musuh
        for bullet in bullets:
            if bullet.rect.colliderect(enemy.rect):
                hit_sound.play()  # suara kena musuh
                bullets.remove(bullet)
                enemy = Enemy()
                score += 50

        # collision player vs musuh
        if player.rect.colliderect(enemy.rect):
            lives -= 1
            enemy = Enemy()

            if lives <= 0:
                game_over = True

    # gambar
    screen.blit(bg, (0, 0))
    player.draw()
    enemy.draw()

    for bullet in bullets:
        bullet.draw()

    # score
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # nyawa
    life_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    screen.blit(life_text, (10, 30))

    # GAME OVER
    if game_over:
        go_text = font.render("GAME OVER", True, (255, 0, 0))
        go_rect = go_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(go_text, go_rect)

        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
        screen.blit(restart_text, restart_rect)

    pygame.display.update()

pygame.quit()