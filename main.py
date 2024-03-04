import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 20
NET_WIDTH = 10
NET_HEIGHT = SCREEN_HEIGHT // 2 + 200
BALL_SIZE = 20
PLAYER_SPEED = 5
BALL_SPEED = 5
GRAVITY = 0.5  # Gravity value
PLAYER_AREA = SCREEN_WIDTH // 2  # Define the area where players can move
SCORE_LIMIT = 5  # Score limit to win the game

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, keys, area):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.keys = keys
        self.dy = 0  # Vertical velocity
        self.jump_available = True  # Flag to indicate if the player can jump
        self.area = area  # Define the area where the player can move

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.keys[0]] and self.rect.x > self.area:
            self.rect.x -= PLAYER_SPEED
        if keys[self.keys[1]] and self.rect.x < self.area + PLAYER_AREA:
            self.rect.x += PLAYER_SPEED
        if keys[self.keys[2]] and self.jump_available:
            self.dy = -10  # Jump velocity
            self.jump_available = False

        # Apply gravity
        self.dy += GRAVITY
        self.rect.y += self.dy

        # Boundary checking
        self.rect.x = max(self.area, min(self.area + PLAYER_AREA - PLAYER_WIDTH, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - PLAYER_HEIGHT, self.rect.y))

        # Reset jump availability when player touches the ground
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.jump_available = True


# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.dx = random.choice([-BALL_SPEED, BALL_SPEED])  # Random initial horizontal velocity
        self.dy = BALL_SPEED
        self.serving = True  # Flag to indicate if the ball is being served

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Ball collision with screen borders
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1
        if self.rect.bottom >= SCREEN_HEIGHT:
            if self.rect.left < SCREEN_WIDTH // 2:
                scoreboard.player2_scores()
            else:
                scoreboard.player1_scores()
            self.reset()

        # Ball collision with players
        player_collision = pygame.sprite.spritecollideany(self, players)
        if player_collision:
            if self.rect.bottom >= player_collision.rect.top and self.dy > 0:  # Ball hits the top of player
                self.dy *= -1
            elif self.rect.right >= player_collision.rect.left and self.dx > 0:  # Ball hits left side of player
                self.dx *= -1
            elif self.rect.left <= player_collision.rect.right and self.dx < 0:  # Ball hits right side of player
                self.dx *= -1

        # Ball collision with the net
        if pygame.sprite.collide_rect(self, net):
            if self.rect.bottom >= net.rect.top and self.dy > 0:  # Ball hits the top of the net
                self.dy *= -1

    def serve(self):
        if self.serving:
            self.dy = BALL_SPEED
            self.serving = False

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.dx = random.choice([-BALL_SPEED, BALL_SPEED])  # Random initial horizontal velocity
        self.dy = BALL_SPEED
        self.serving = True


# Net class
class Net(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((NET_WIDTH, NET_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT)  # Place at the bottom


# Scoreboard class
class Scoreboard:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.player1_score = 0
        self.player2_score = 0

    def update(self):
        self.text = f"Player 1: {self.player1_score}  Player 2: {self.player2_score}"
        self.rendered_text = self.font.render(self.text, True, WHITE)
        screen.blit(self.rendered_text, (10, 10))

    def player1_scores(self):
        self.player1_score += 1

    def player2_scores(self):
        self.player2_score += 1


# Sprites
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
ball = Ball()
net = Net()
player1 = Player(
    SCREEN_WIDTH // 4, SCREEN_HEIGHT - PLAYER_HEIGHT, (pygame.K_q, pygame.K_d, pygame.K_z), 0
)
player2 = Player(
    3 * SCREEN_WIDTH // 4,
    SCREEN_HEIGHT - PLAYER_HEIGHT,
    (pygame.K_k, pygame.K_m, pygame.K_o),
    SCREEN_WIDTH // 2,
)
players.add(player1, player2)
all_sprites.add(player1, player2, ball, net)

scoreboard = Scoreboard()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ball.serve()

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)
    scoreboard.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
