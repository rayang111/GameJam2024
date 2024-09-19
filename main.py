import pygame
import numpy as np
import heapq

# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize font module

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640
CELL_SIZE = 32

GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE  # 40 cells horizontally
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE  # 20 cells vertically

# Colors
wallColor = (0, 0, 0)
backgroundColor = (91, 113, 134)
playerColor = (192, 192, 192)
enemyColor = (255, 0, 0)
checkPointColor = (0, 0, 255)
codeColor = (255, 255, 0)
red = (255, 0, 0)  # Red for timer text

# Load assets images
star = pygame.image.load("data/star.png")  # Image of the star bonus
brick = pygame.image.load("data/brick.png")
bonus = pygame.image.load("data/bonus.png")  # Image of the bonus
checkpoint = pygame.image.load("data/checkpoint.png")  # Image of the checkpoint
menu_principal = pygame.image.load("data/menu_principal.png")  # Main menu image

guard1Down = pygame.image.load("data/guard1.png")
guard1Up = pygame.transform.rotate(guard1Down, 180)
guard1Left = pygame.transform.rotate(guard1Down, -90)
guard1Right = pygame.transform.rotate(guard1Down, 90)

spyDown = pygame.image.load("data/spy.png")
spyUp = pygame.transform.rotate(spyDown, 180)
spyLeft = pygame.transform.rotate(spyDown, -90)
spyRight = pygame.transform.rotate(spyDown, 90)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Labyrinth Game")

# Define the maze matrix using NumPy
maze_matrix = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,2,1,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1],  # Checkpoint at position (2)
    [1,0,1,0,0,0,0,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,1],
    [1,0,1,1,0,0,0,1,1,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1],
    [1,3,1,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,0,1,1,0,1,0,1,0,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1],
    [1,4,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,0,0,1,0,1,1,0,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1],
    [1,0,0,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,0,0,0,1],
    [1,0,1,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,1,0,0,1,1,0,1,1,0,1,1,0,1,0,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1],
    [1,1,1,0,0,1,0,0,0,0,0,1,1,1,1,0,1,0,0,1,0,1,1,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1],
    [1,0,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,1,1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,1,1,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,0,1,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,0,1,0,1,1,1,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
])

# Timer settings (3 minutes in seconds)
time_limit = 3 * 60  
start_ticks = pygame.time.get_ticks()  # Store the starting time

# Directions for A* (up, down, left, right)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Heuristic function for A* (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* pathfinding algorithm
def a_star(maze, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for direction in DIRECTIONS:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if 0 <= neighbor[0] < maze.shape[0] and 0 <= neighbor[1] < maze.shape[1] and maze[neighbor[0], neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return []  # Return empty path if no path found

# Define the player
class Player:
    def __init__(self, x, y, speed):
        self.x = x  # Grid position x
        self.y = y  # Grid position y
        self.direction = 'right'
        self.speed = speed

    def move(self, dx, dy, maze_matrix):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < maze_matrix.shape[1] and 0 <= new_y < maze_matrix.shape[0]:
            if maze_matrix[new_y, new_x] == 0 or maze_matrix[new_y, new_x] in (2, 3):  # Walk on bonus or checkpoint
                self.x = new_x
                self.y = new_y

                # Remove star or bonus when stepped on
                if maze_matrix[new_y, new_x] == 2:  # Checkpoint
                    maze_matrix[new_y, new_x] = 0
                    return "checkpoint"
                elif maze_matrix[new_y, new_x] == 3:  # Bonus
                    maze_matrix[new_y, new_x] = 0
                    return 'bonus'
                elif maze_matrix[new_y, new_x] == 4:  # Star
                    maze_matrix[new_y, new_x] = 0
                    return 'star'
        return None

# Guard class using A* for pathfinding
class Guard:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed // 4  # Slow down enemies further
        self.chasing_speed = speed // 2  # Chasing speed is faster but still slower than the player
        self.patrol_speed = speed // 4
        self.path = []  # Path found by A*
        self.direction = "down"  # Default direction

    def move(self, player, maze_matrix):
        if abs(self.x - player.x) <= 3 and abs(self.y - player.y) <= 3:
            # Increase speed when within 3 cells of the player
            self.speed = self.chasing_speed
        else:
            self.speed = self.patrol_speed

        # Recalculate path if no path or already reached target
        if not self.path or (self.x, self.y) == self.path[-1]:
            self.path = a_star(maze_matrix, (self.y, self.x), (player.y, player.x))

        # Follow the path
        if self.path:
            next_step = self.path.pop(0)
            # Determine direction based on movement
            if next_step[1] > self.x:
                self.direction = "right"
            elif next_step[1] < self.x:
                self.direction = "left"
            elif next_step[0] > self.y:
                self.direction = "down"
            elif next_step[0] < self.y:
                self.direction = "up"
            self.x, self.y = next_step[1], next_step[0]

    def check_collision(self, player):
        return self.x == player.x and self.y == player.y

# Initialize the player at middle left of the labyrinth
player = Player(1, 1, speed=2)

# Guards initial positions and speed
guards = [
    Guard(16, 4, speed=2),
    Guard(9, 14, speed=2),
    Guard(19, 16, speed=2),
    Guard(28, 12, speed=2)
]

# Initialize checkpoint state storage
checkpoint_state = None
checkpoint_used = False  # Variable to track if the checkpoint has already been used

# Main game loop
clock = pygame.time.Clock()
running = True
game_started = False  # Variable to track if the game has started or not
game_over = False  # Variable to freeze the game when an enemy catches the player
bonus_active = False
bonus_start_time = 0

def render_timer(screen, time_left):
    font = pygame.font.SysFont(None, 48)
    time_text = f"{time_left // 60:02}:{time_left % 60:02}"
    timer_surf = font.render(time_text, True, red)
    screen.blit(timer_surf, (SCREEN_WIDTH - 150, 10))  # Position at top-right corner

while running:
    clock.tick(4)  # Slower FPS for enemies (now adjusted further)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_started:
        # Display the main menu and wait for the player to press ENTER
        screen.blit(menu_principal, (0, 0))
        if keys[pygame.K_RETURN]:
            game_started = True
            start_ticks = pygame.time.get_ticks()  # Reset timer when game starts
    elif not game_over:  # Only move and update if the game is not over
        # Timer countdown
        if not bonus_active:
            seconds_elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
            time_left = max(0, time_limit - seconds_elapsed)  # Calculate time left

        # Handle player movement
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
            player.direction = "left"
        elif keys[pygame.K_RIGHT]:
            dx = 1
            player.direction = "right"
        elif keys[pygame.K_UP]:
            dy = -1
            player.direction = "up"
        elif keys[pygame.K_DOWN]:
            dy = 1
            player.direction = "down"

        if dx != 0 or dy != 0:
            result = player.move(dx, dy, maze_matrix)

            # If the player collected a checkpoint, save the game state
            if result == "checkpoint":
                checkpoint_state = {
                    "player_pos": (player.x, player.y),
                    "guards_pos": [(guard.x, guard.y) for guard in guards]
                }
                checkpoint_used = False  # Reset the checkpoint usage flag

            # If the player collected a bonus, activate the bonus effect
            if result == "bonus":
                bonus_active = True
                bonus_start_time = pygame.time.get_ticks()

        # If the player presses "C" and checkpoint is not yet used, restore the game state
        if keys[pygame.K_c] and checkpoint_state is not None and not checkpoint_used:
            player.x, player.y = checkpoint_state["player_pos"]
            for i, guard in enumerate(guards):
                guard.x, guard.y = checkpoint_state["guards_pos"][i]
            checkpoint_used = True  # Mark the checkpoint as used

        # Move guards and check for collisions with the player
        for guard in guards:
            if not bonus_active:  # Guards only move if bonus is not active
                guard.move(player, maze_matrix)
            if guard.check_collision(player):
                game_over = True  # Freeze the game if a guard catches the player

        # Deactivate the bonus after 10 seconds
        if bonus_active and pygame.time.get_ticks() - bonus_start_time >= 10000:  # 10 seconds
            bonus_active = False
            # Resume the timer correctly after bonus ends
            start_ticks += (pygame.time.get_ticks() - bonus_start_time)

        # Draw the maze
        screen.fill(backgroundColor)
        for y in range(maze_matrix.shape[0]):
            for x in range(maze_matrix.shape[1]):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                image_x = x * CELL_SIZE
                image_y = y * CELL_SIZE
                if maze_matrix[y, x] == 1:
                    screen.blit(brick, (image_x, image_y))
                elif maze_matrix[y, x] == 2:  # Show checkpoint item at this location
                    screen.blit(checkpoint, (image_x, image_y))
                elif maze_matrix[y, x] == 3:  # Show star or bonus at this location
                    screen.blit(bonus, (image_x, image_y))
                elif maze_matrix[y, x] == 4:  # Show star at this location
                    screen.blit(star, (image_x, image_y))

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
            if guard.x < 0 or guard.y < 0 or guard.x >= maze_matrix.shape[1] or guard.y >= maze_matrix.shape[0]:
                continue  # Make sure the guards stay inside the maze
            if guard.direction == "left":
                screen.blit(guard1Left, (guard.x * CELL_SIZE, guard.y * CELL_SIZE))
            elif guard.direction == "right":
                screen.blit(guard1Right, (guard.x * CELL_SIZE, guard.y * CELL_SIZE))
            elif guard.direction == "up":
                screen.blit(guard1Up, (guard.x * CELL_SIZE, guard.y * CELL_SIZE))
            elif guard.direction == "down":
                screen.blit(guard1Down, (guard.x * CELL_SIZE, guard.y * CELL_SIZE))

        # Render the timer on the screen
        if not bonus_active:
            render_timer(screen, time_left)

    # Update the display
    pygame.display.flip()

pygame.quit()
