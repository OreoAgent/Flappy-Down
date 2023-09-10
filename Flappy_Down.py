import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
BIRD_WIDTH, BIRD_HEIGHT = 40, 40
BIRD_COLOR = (255, 255, 0)
GROUND_COLOR = (0, 255, 0)
PIPE_COLOR = (0, 0, 255)
FPS = 30
GRAVITY = 1
JUMP_STRENGTH = -15
PIPE_WIDTH = 60
PIPE_SPACING = 200
PIPE_SPEED = 5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Going Down")

# Load the bird image
bird_img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_img.fill(BIRD_COLOR)

# Create bird object
bird_rect = bird_img.get_rect()
bird_rect.center = (WIDTH // 2, HEIGHT // 2)
bird_y_velocity = 0

# Create ground
ground_rect = pygame.Rect(0, HEIGHT - 20, WIDTH, 20)

# Create pipes
pipe_top_rect = pygame.Rect(WIDTH // 2, 0, PIPE_WIDTH, random.randint(150, 400))
pipe_bottom_rect = pygame.Rect(WIDTH // 2, pipe_top_rect.height + PIPE_SPACING, PIPE_WIDTH, HEIGHT - pipe_top_rect.height - PIPE_SPACING)

# Fonts
font = pygame.font.Font(None, 36)
score = 0

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2
game_state = START

# Functions
def start_game():
    global game_state, bird_rect, bird_y_velocity, pipe_top_rect, pipe_bottom_rect, score
    game_state = PLAYING
    bird_rect.center = (WIDTH // 2, HEIGHT // 2)
    bird_y_velocity = 0
    pipe_top_rect.x = WIDTH
    pipe_bottom_rect.x = WIDTH
    pipe_top_rect.height = random.randint(150, 400)
    pipe_bottom_rect.y = pipe_top_rect.height + PIPE_SPACING
    score = 0
# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if game_state == START:
            start_game()
        elif game_state == PLAYING:
            bird_y_velocity = JUMP_STRENGTH
        elif game_state == GAME_OVER:
            start_game()  # Restart the game

    if game_state == PLAYING:
        # Bird physics
        bird_y_velocity += GRAVITY
        bird_rect.y += bird_y_velocity

        # Pipe movement
        pipe_top_rect.x -= PIPE_SPEED
        pipe_bottom_rect.x -= PIPE_SPEED

        # Check for collision with the ground
        if bird_rect.colliderect(ground_rect):
            game_state = GAME_OVER

        # Check if bird passed through the pipes
        if pipe_top_rect.right < bird_rect.left:
            score += 1
            pipe_top_rect.x = WIDTH
            pipe_bottom_rect.x = WIDTH
            pipe_top_rect.height = random.randint(150, 400)
            pipe_bottom_rect.y = pipe_top_rect.height + PIPE_SPACING

        # Check for collision with pipes
        if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
            game_state = GAME_OVER

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, PIPE_COLOR, pipe_top_rect)
    pygame.draw.rect(screen, PIPE_COLOR, pipe_bottom_rect)
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect)
    screen.blit(bird_img, bird_rect)

    # Display score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw start/restart button
    if game_state == START:
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(start_text, (WIDTH // 2 - 120, HEIGHT // 2))
    elif game_state == GAME_OVER:
        game_over_text = font.render("Game Over - Press SPACE to Restart", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))

    pygame.display.update()

    # FPS Control
    clock.tick(FPS)

pygame.quit()

