import pygame
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

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
PIPE_SPEED = 5
TOP_SCORE_FILE = "top_score.txt"

# Music
musoff = False  # Change to True if you want it to start without music
#AudioPath = os.path.dirname(os.path.abspath(__file__))
#AudioPath = AudioPath + "\\Audio\\"
#ColisionSFX = pygame.mixer.Sound(AudioPath + "WindshieldHitWithBar.mp3")
ColisionSFX = pygame.mixer.Sound("Audio\\WindshieldHitWithBar.mp3")
newmu = False

#Add volume feature

# Initialize top score
top_score = 0

# Function to load top score from a file
def load_top_score():
    if os.path.exists(TOP_SCORE_FILE):
        with open(TOP_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

# Function to save top score to a file
def save_top_score(score):
    with open(TOP_SCORE_FILE, "w") as file:
        file.write(str(score))

# Initialize top score
top_score = load_top_score()

#bgmusic = None

#preload music
#bgmusic2 = pygame.mixer.Sound(AudioPath + "IttyBitty8Bit-Kevin MacLeod.mp3")
#bgmusic3 = pygame.mixer.Sound(AudioPath + "Powerup!-JeremyBlake.mp3")
#bgmusic4 = pygame.mixer.Sound(AudioPath + "MAZE-Density&Time.mp3")
#bgmusic5 = pygame.mixer.Sound(AudioPath + "FloatingAlso-William Rosati.mp3")

bgmusic2 = pygame.mixer.Sound("Audio\\IttyBitty8Bit-Kevin MacLeod.mp3")
bgmusic3 = pygame.mixer.Sound("Audio\\Powerup!-JeremyBlake.mp3")
bgmusic4 = pygame.mixer.Sound("Audio\\MAZE-Density&Time.mp3")
bgmusic5 = pygame.mixer.Sound("Audio\\FloatingAlso-William Rosati.mp3")

# Function to start playing music
def play_music():
    global bgmusic
    if not pygame.mixer.get_busy(): # or newmu:
        #pygame.mixer.Sound.stop(bgmusic)
        bgmusic1 = random.randint(1, 4)
        if bgmusic1 == 1:
            bgmusic = bgmusic2 # = pygame.mixer.Sound("Flappy_Down4\Audio\IttyBitty8Bit-Kevin MacLeod.mp3")
            bgmusic.play(-1)
            bgmusic.set_volume(0.4)
        elif bgmusic1 == 2:
            bgmusic = bgmusic3 # = pygame.mixer.Sound("Flappy_Down4\Audio\Powerup!-JeremyBlake.mp3")
            bgmusic.play(-1)
            bgmusic.set_volume(0.4)
        elif bgmusic1 == 3:
            bgmusic = bgmusic4 # = pygame.mixer.Sound("Flappy_Down4\Audio\MAZE-Density&Time.mp3")
            bgmusic.play(-1)
            bgmusic.set_volume(0.4)
        elif bgmusic1 == 4:
            bgmusic = bgmusic5 # = pygame.mixer.Sound("Flappy_Down4\Audio\FloatingAlso-William Rosati.mp3")
            bgmusic.play(-1)
            bgmusic.set_volume(0.4)

# Function to stop playing music
def stop_music():
    global bgmusic
    pygame.mixer.Sound.stop(bgmusic)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Down - Going Down")

# Load the bird image
bird_img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_img.fill(BIRD_COLOR)

# Create bird object
bird_rect = bird_img.get_rect()
bird_rect.center = (WIDTH // 2, HEIGHT // 2)
bird_y_velocity = 0

# Create ground
ground_rect = pygame.Rect(0, HEIGHT - 20, WIDTH, 20)

# Create ceiling
ceiling_rect = pygame.Rect(0, 0, WIDTH, 20)

# Create pipes
pipe_top_rect = pygame.Rect(WIDTH // 2, 0, PIPE_WIDTH, random.randint(150, HEIGHT - 350))
pipe_bottom_rect = pygame.Rect(WIDTH // 2, pipe_top_rect.height + 200, PIPE_WIDTH, HEIGHT - pipe_top_rect.height - 100)

# Fonts
font = pygame.font.Font(None, 36)
score = 0

# Function to start the game
def start_game():
    global game_state, bird_rect, bird_y_velocity, pipe_top_rect, pipe_bottom_rect, score
    game_state = PLAYING
    bird_rect.center = (WIDTH // 2, HEIGHT // 2)
    bird_y_velocity = 0
    pipe_top_rect.x = WIDTH
    pipe_bottom_rect.x = WIDTH
    pipe_top_rect.height = random.randint(150, HEIGHT - 350)
    pipe_bottom_rect.y = pipe_top_rect.height + 200
    score = 0

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2
game_state = START

# Variables for key debouncing
space_pressed = False

# Game loop
clock = pygame.time.Clock()
running = True

# Initial music play
play_music()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_F2]:
        musoff = True  # Stop the music
        stop_music()
    elif keys[pygame.K_F1]:
        musoff = False  # Start the music
        play_music()
    elif keys[pygame.K_F3]:
        newmu = True  # Request new music and stop current
        stop_music()
        play_music()

    # Handle spacebar key press with debouncing
    if keys[pygame.K_SPACE] and game_state == START and not space_pressed:
        start_game()
        space_pressed = True
    elif keys[pygame.K_SPACE] and game_state == PLAYING and not space_pressed:
        bird_y_velocity = JUMP_STRENGTH
        space_pressed = True
    elif keys[pygame.K_SPACE] and game_state == GAME_OVER and not space_pressed:
        start_game()
        space_pressed = True
    elif not keys[pygame.K_SPACE]:
        space_pressed = False  # Reset the space_pressed flag

    if keys[pygame.K_ESCAPE]:
        running = False

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
            ColisionSFX.play()

        # Check if bird passed through the pipes
        if pipe_top_rect.right < bird_rect.left:
            score += 1
            if score > top_score:
                top_score = score
                save_top_score(top_score)
            pipe_top_rect.x = WIDTH
            pipe_bottom_rect.x = WIDTH
            pipe_top_rect.height = random.randint(150, HEIGHT - 350)
            pipe_bottom_rect.y = pipe_top_rect.height + 200

        # Check for collision with pipes
        if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
            game_state = GAME_OVER
            ColisionSFX.play()
        
        # Check for ceiling collisions
        if bird_rect.colliderect(ceiling_rect):
            game_state = GAME_OVER
            ColisionSFX.play()

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 0), ceiling_rect)
    pygame.draw.rect(screen, PIPE_COLOR, pipe_top_rect)
    pygame.draw.rect(screen, PIPE_COLOR, pipe_bottom_rect)
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect)
    screen.blit(bird_img, bird_rect)

    # Display score and top score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    top_score_text = font.render("Top Score: " + str(top_score), True, (255, 255, 255))
    screen.blit(top_score_text, (WIDTH - 200, 10))

    # Draw game over text
    if game_state == GAME_OVER:
        game_over_text = font.render("GAME OVER", True, (255, 255, 255))
        restart_text = font.render("Click SPACE to Restart", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - 140, HEIGHT // 2 + 20))

    pygame.display.update()

    # FPS Control
    clock.tick(FPS)

pygame.quit()
