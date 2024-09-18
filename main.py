import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640
CELL_SIZE = 32

GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE  # 40 cells horizontally
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE  # 20 cells vertically

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 255, 0)  # Green color for the player

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Labyrinth Game")

# Define the maze matrix using NumPy
# 0 represents a path, 1 represents a wall
maze_matrix = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,1],
    [1,0,1,0,0,0,1,1,0,0,0,1,1,1,1,1,1,0,1,0,1,0,0,1,0,1,0,1,1,1,0,0,1,1,0,0,1,0,0,1],
    [1,0,1,1,0,0,0,1,1,0,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,1,0,1,1,0,1,0,1,1,0,1,1,0,1,1],
    [1,0,1,0,0,1,0,1,0,0,1,0,1,1,0,1,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,1,1],
    [1,0,1,0,1,0,0,0,1,0,0,1,1,1,1,1,0,1,1,0,1,0,1,1,0,1,1,1,0,1,0,0,0,0,1,1,0,0,0,1],
    [1,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,1,0,1,1,0,0,1,0,1,0,0,1,1,1,0,1,1,0,0,1,0,0,1],
    [1,0,1,0,1,0,0,0,0,1,1,0,0,0,1,0,1,1,0,1,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1,1,1,1],
    [1,0,1,0,1,1,0,0,1,1,1,1,0,1,1,0,0,0,0,1,0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1,1,1,0,0,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,1,0,1,1,1,0,1,1,1,1,1,1,0,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,1,0,1,0,1,1],
    [1,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,1,1,0,0,1,0,1,0,0,1,1,1,0,0,1,1,1,1,0,1,1,1,0,1],
    [1,0,1,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0,1,1],
    [1,0,1,0,1,1,0,0,1,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1],
    [1,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1,1,0,1,1,0,1,0,1,0,1,0,1,0,1,1],
    [1,0,1,1,0,1,0,1,0,1,1,1,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,1,1,0,0,1,1,1],
    [1,0,0,1,0,1,0,1,0,0,0,1,0,0,1,1,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,0,0,1,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1,1,0,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,1,1,1,0,1,0,1,0,0,1,0,1,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
])

# Resize or pad the matrix if necessary
MAZE_HEIGHT, MAZE_WIDTH = maze_matrix.shape

# Define the player
class Player:
    def __init__(self, x, y):
        self.x = x  # Grid position x
        self.y = y  # Grid position y

    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT:
            if maze_matrix[ny, nx] == 0:
                self.x = nx
                self.y = ny

# Initialize the player at middle left of the labyrinth
player_start_y = MAZE_HEIGHT // 2
# Ensure player_start_y is in a path
for y in range(player_start_y, MAZE_HEIGHT):
    if maze_matrix[y, 1] == 0:
        player_start_y = y
        break

player = Player(1, player_start_y)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # Limit to 60 FPS

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1
    elif keys[pygame.K_UP]:
        dy = -1
    elif keys[pygame.K_DOWN]:
        dy = 1

    if dx != 0 or dy != 0:
        player.move(dx, dy)

    # Draw the maze
    screen.fill(WHITE)
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze_matrix[y, x] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            # Paths are left black (background color)

    # Draw the player
    player_rect = pygame.Rect(player.x * CELL_SIZE, player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Update the display
    pygame.display.flip()

pygame.quit()