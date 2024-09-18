import pygame
import numpy as np
import random
import sys

# Initialize Pygame
pygame.init()

# Colors
wallColor = (0, 0, 0)
backgroundColor = (91, 113, 134)
playerColor = (192, 192, 192)
enemyColor = (255, 0, 0)
checkPointColor = (0, 0, 255)
codeColor = (255, 255, 0)

# Load assets images
brick = pygame.image.load("data/brick.png")
bonus = pygame.image.load("data/bonus.png")
checkpoint = pygame.image.load("data/checkpoint.png")
metalBlock = pygame.image.load("data/metalBlock.png")
menu_principal = pygame.image.load("data/menu_principal.png")  # Image du menu principal

guard1Down = pygame.image.load("data/guard1.png")
guard1Up = pygame.transform.rotate(guard1Down, 180)
guard1Left = pygame.transform.rotate(guard1Down, -90)
guard1Right = pygame.transform.rotate(guard1Down, 90)

spyDown = pygame.image.load("data/spy.png")
spyUp = pygame.transform.rotate(spyDown, 180)
spyLeft = pygame.transform.rotate(spyDown, -90)
spyRight = pygame.transform.rotate(spyDown, 90)

# SCREEN_WIDTH = 1536
# SCREEN_HEIGHT = 640
# 48
# 20

# Define the maze matrix using NumPy
maze_matrix1 = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,0,0,0,1,1,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,0,1,1,0,1,0,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1],
    [1,0,0,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,1,1,0,1,1,0,1,1,0,1,0,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,1,0,0,0,0,0,1,1,1,1,0,1,0,0,1,0,1,1,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,1,1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,0,1,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
])

MAZE_HEIGHT, MAZE_WIDTH = maze_matrix1.shape
# Screen dimensions
CELL_SIZE = 32
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ChronoSpy")

# Guards initial positions
guardsMap1 = [
    [16, 4, "guard1", "left"],
    [9, 14, "guard1", "left"],
    [19, 16, "guard1", "left"],
    [28, 12, "guard1", "left"]
]

# Place the bonus at a random 0 cell in the maze
bonus_position = (7, 12)  # Example of a random position (7th row, 12th column)
maze_matrix1[bonus_position[0], bonus_position[1]] = 3  # Set the bonus value to 3

# Font
font = pygame.font.SysFont("Arial", 74)
pauseText = font.render('Pause', True, (0, 0, 0))
pauseText_width, pauseText_height = pauseText.get_size()

# Define the player
class Player:
    def __init__(self, x, y, speed):
        self.x = x  # Grid position x
        self.y = y  # Grid position y
        self.direction = 'right'
        self.speed = speed

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            if maze_matrix1[new_y, new_x] == 0 or maze_matrix1[new_y, new_x] in (2, 3):  # Walk on bonus or checkpoint:
                self.x = new_x
                self.y = new_y
                
                # Remove bonus or checkpoint if player steps on it
                if maze_matrix1[new_y, new_x] == 2:  # Checkpoint
                    maze_matrix1[new_y, new_x] = 0
                    return "checkpoint"
                elif maze_matrix1[new_y, new_x] == 3:  # Bonus
                    maze_matrix1[new_y, new_x] = 0
                    return "bonus"
        return None

# Guard class
class Guard:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            if dx == -1:
                self.direction = "left"
            elif dx == 1:
                self.direction = "right"
            elif dy == -1:
                self.direction = "up"
            elif dy == 1:
                self.direction = "down"
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze_matrix1[new_y, new_x] == 0:
                self.x = new_x
                self.y = new_y
                break

# Initialize the player at middle left of the labyrinth
player_start_y = MAZE_HEIGHT // 2
for y in range(player_start_y, MAZE_HEIGHT):
    if maze_matrix1[y, 1] == 0:
        player_start_y = y
        break

player = Player(1, player_start_y, speed=1)

# Initialize guards
guards = [Guard(x, y, direction) for x, y, _, direction in guardsMap1]

# Initialize checkpoint state storage
checkpoint_state = None
checkpoint_used = False  # Variable to track if the checkpoint has already been used

# Main game loop
clock = pygame.time.Clock()
running = True
# "start" -> start of the game
# "pause" -> pause of the game
# "play" -> play the game
gameStatus = "start"

while running:
    clock.tick(7)  # Limit to 8 FPS

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if gameStatus == "pause":
                    gameStatus = "play"
                elif gameStatus == "play":
                    gameStatus = "pause"
            elif event.key == pygame.K_RETURN and gameStatus == "start":
                gameStatus = "play"
            
    if gameStatus == "play":
        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            dx = -1
            player.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
            player.direction = "right"
        elif keys[pygame.K_UP] or keys[pygame.K_z]:
            dy = -1
            player.direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            player.direction = "down"

        if dx != 0 or dy != 0:
            result = player.move(dx, dy)
            
            # If the player collected a checkpoint, save the game state
            if result == "checkpoint":
                checkpoint_state = {
                    "player_pos": (player.x, player.y),
                    "guards_pos": [(guard.x, guard.y) for guard in guards]
                }
                checkpoint_used = False  # Reset the checkpoint usage flag
        
        # If the player presses "C" and checkpoint is not yet used, restore the game state
        if keys[pygame.K_c] and checkpoint_state is not None and not checkpoint_used:
            player.x, player.y = checkpoint_state["player_pos"]
            for i, guard in enumerate(guards):
                guard.x, guard.y = checkpoint_state["guards_pos"][i]
            checkpoint_used = True  # Mark the checkpoint as used
        
        # Move guards
        for guard in guards:
            guard.move()
    
    if gameStatus == "play" or gameStatus == "pause":
        # Draw the maze
        screen.fill(backgroundColor)
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                image_x = x * CELL_SIZE
                image_y = y * CELL_SIZE
                if maze_matrix1[y, x] == 1:
                    screen.blit(brick, (image_x, image_y))
                elif maze_matrix1[y, x] == 2:  # Afficher l'item checkpoint à cet emplacement
                    screen.blit(checkpoint, (image_x, image_y))
                elif maze_matrix1[y, x] == 3:  # Afficher l'item bonus à cet emplacement
                    screen.blit(bonus, (image_x, image_y))

        # Draw the player
        if player.direction == "left":
            screen.blit(spyLeft, (player.x * CELL_SIZE, player.y * CELL_SIZE))
        elif player.direction == "right":
            screen.blit(spyRight, (player.x * CELL_SIZE, player.y * CELL_SIZE))
        elif player.direction == "up":
            screen.blit(spyUp, (player.x * CELL_SIZE, player.y * CELL_SIZE))
        elif player.direction == "down":
            screen.blit(spyDown, (player.x * CELL_SIZE, player.y * CELL_SIZE))

        # Draw the guards
        for guard in guards:
            if guard.direction == "left":
                screen.blit(guard1Left, (guard.x * CELL_SIZE, guard.y * CELL_SIZE))
            elif guard.direction== "right":
                screen.blit(guard1Right, (guard.x * CELL_SIZE, guard.y * CELL_SIZE))
            elif guard.direction == "up":
                screen.blit(guard1Up, (guard.x * CELL_SIZE, guard.y * CELL_SIZE))
            elif guard.direction == "down":
                screen.blit(guard1Down, (guard.x * CELL_SIZE, guard.y * CELL_SIZE))
                
        # Draw pause text
        if gameStatus == "pause":
            x = (SCREEN_WIDTH-pauseText_width)/2
            y = (SCREEN_HEIGHT-pauseText_height)/2
            screen.blit(pauseText, (x, y))
    
    elif gameStatus == "start":
        screen.blit(menu_principal, (0, 0))
    
    # Update the display
    pygame.display.flip()

pygame.quit()