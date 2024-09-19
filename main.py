import pygame
import numpy as np
import random
import heapq

# Initialize Pygame
pygame.init()

# Colors
wallColor = (0, 0, 0)
backgroundColor = (91, 113, 134)
playerColor = (192, 192, 192)
enemyColor = (255, 0, 0)
checkPointColor = (0, 0, 255)
codeColor = (255, 255, 0)
red = (255, 0, 0)  # Red for timer text

# Load assets images
# star = pygame.image.load("data/star.png")  # Image of the star bonus
brick = pygame.image.load("data/brick.png")
bonus = pygame.image.load("data/bonus.png")
checkpoint = pygame.image.load("data/checkpoint.png")
portail = pygame.image.load("data/portail.png")
metalBlock = pygame.image.load("data/metalBlock.png")
menu_principal = pygame.image.load("data/menu_principal.png")
code = pygame.image.load("data/code.png")
gameover = pygame.image.load("data/gameover.png")
win = pygame.image.load("data/win.png")
bomb = pygame.image.load("data/bomb.png")

portail_bottom = pygame.image.load("data/portail/portail_bottom.png") # 13
portail_left_angle = pygame.image.load("data/portail/portail_left_angle.png") # 6
portail_left_bootom_angle = pygame.image.load("data/portail/portail_left_bootom_angle.png") # 10
portail_left = pygame.image.load("data/portail/portail_left.png") # 9
portail_right = pygame.image.load("data/portail/portail_right_.png") # 11
portail_right_bottom_angle = pygame.image.load("data/portail/portail_right_bottom_angle.png") # 12
portail_right_top_angle = pygame.image.load("data/portail/portail_right_top_angle.png") # 8
portail_top = pygame.image.load("data/portail/portail_top.png") # 7
portail_center = pygame.image.load("data/portail/portail-center.png") # 14

guard1Down = pygame.image.load("data/guard1.png")
guard1Up = pygame.transform.rotate(guard1Down, 180)
guard1Left = pygame.transform.rotate(guard1Down, -90)
guard1Right = pygame.transform.rotate(guard1Down, 90)

spyDown = pygame.image.load("data/spy.png")
spyUp = pygame.transform.rotate(spyDown, 180)
spyLeft = pygame.transform.rotate(spyDown, -90)
spyRight = pygame.transform.rotate(spyDown, 90)

# Screen_width = 1536
# Screen_height = 640
# 48
# 20

# Define the maze matrix using NumPy
maze_matrix1 = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,6,7,7,7,7,7,8,1],
    [1,0,1,0,0,0,0,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,1,0,0,0,1,1,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,3,0,1,0,0,0,0,1,0,1,0,0,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,0,1,1,0,1,0,1,0,1,1,1,1,0,1,1,1,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,1,1,1,1,0,0,1,0,1,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,1,1,9,14,14,14,14,14,11,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,0,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,0,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,0,1,1,0,1,1,0,1,1,0,1,0,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,9,14,14,14,14,14,11,1],
    [1,1,1,0,0,1,0,0,0,0,0,1,1,1,1,0,1,0,0,1,0,1,1,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,9,14,14,14,14,14,11,1],
    [1,0,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,1,1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,1,1,1,9,14,14,14,14,14,11,1],
    [1,0,1,1,0,1,3,1,1,1,1,1,0,0,1,0,1,0,1,1,0,0,1,1,0,1,0,3,0,0,0,1,0,1,1,1,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,10,13,13,13,13,13,12,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
])

maze_matrix2 = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,7,7,7,7,7,8,1],
    [1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,1,1,1,1,1,0,0,1,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,9,14,14,14,14,14,11,1],
    [1,0,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,0,0,0,1,0,0,1,1,1,0,1,1,0,0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,1,1,0,1,0,0,0,1,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,1,1,0,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,0,0,0,0,1,1,1,0,1,0,1,0,0,1,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,1,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,1,1,1,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,0,0,0,0,1,0,1,1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,1,0,1,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,9,14,14,14,14,14,11,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,10,13,13,13,13,13,12,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
])

# maze_height, maze_width = maze_matrix1.shape
# # Screen dimensions
# CELL_SIZE = 32
# Screen_width = maze_width * CELL_SIZE
# Screen_height = maze_height * CELL_SIZE

current_level= 1
current_maze = maze_matrix1
CELL_SIZE = 32
maze_height, maze_width = current_maze.shape
Screen_width = maze_width * CELL_SIZE
Screen_height = maze_height * CELL_SIZE

def update_current_maze():
    global current_maze, maze_height, maze_width, Screen_width, Screen_height
    if current_level==1:
        current_maze = maze_matrix1
    elif current_level==2:
        current_maze = maze_matrix2
    maze_height, maze_width = current_maze.shape
    # Screen dimensions
    Screen_width = maze_width * CELL_SIZE
    Screen_height = maze_height * CELL_SIZE


# Create the screen
screen = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption("ChronoSpy")

# Guards initial positions
guardsMap1 = [
    [16, 4, "guard1", "left"],
    [9, 14, "guard1", "left"],
    [19, 16, "guard1", "left"],
    [28, 12, "guard1", "left"]
]

# Timer settings (3 minutes in seconds)
time_limit = 2 * 60  
checkpoint_time_left = None  # To store the time left at the checkpoint
start_ticks = pygame.time.get_ticks() # Store the starting time

# Directions for A* (up, down, left, right)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# # Place the bonus at a random 0 cell in the maze
# bonus_position = (7, 12)  # Example of a random position (7th row, 12th column)
# current_maze[bonus_position[0], bonus_position[1]] = 3  # Set the bonus value to 3

# Place the code!
# code_position = (10, 2)
# current_maze[code_position[0], code_position[1]] = 15

# Font
font = pygame.font.SysFont("Arial", 74)
pauseText = font.render('Pause', True, (0, 0, 0))
pauseText_width, pauseText_height = pauseText.get_size()

# Position of the code ( random )
codePositionX = 0
codePositionY = 0
while(codePositionX == 0 and codePositionY==0):
    new_x = random.randint(33, 39)
    new_y = random.randint(1, 19)
    if current_maze[new_y, new_x]!=1:
        codePositionX = new_x
        codePositionY = new_y

if current_level==1:
    if codePositionX>1 and codePositionX<maze_width and codePositionY>1 and codePositionY<maze_height: 
        current_maze[codePositionY,codePositionX] = 15

# Chasing
chasing = False

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

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if 0 <= new_x < maze_width and 0 <= new_y < maze_height:
            if current_maze[new_y, new_x] == 0 or current_maze[new_y, new_x] in (2, 3, 4, 5, 15):  # Walk on bonus or checkpoint:
                self.x = new_x
                self.y = new_y
                
                # Remove bonus or checkpoint if player steps on it
                if current_maze[new_y, new_x] == 2:  # Checkpoint
                    current_maze[new_y, new_x] = 5
                    return "checkpoint"
                elif current_maze[new_y, new_x] == 3:  # Bonus
                    current_maze[new_y, new_x] = 0
                    return "bonus"
                elif current_maze[new_y, new_x] == 4:  # Star
                    current_maze[new_y, new_x] = 0
                    return 'star'
                elif current_maze[new_y, new_x] == 15:  # Code
                    current_maze[new_y, new_x] = 0
                    return "code"
        return None

# Guard class
class Guard:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.speed = speed // 4  # Slow down enemies further
        self.path = []  # Path found by A*
        self.direction = "down"  # Default direction

    def move(self, player, maze_matrix, chasing):
        self.isChasing = chasing
        
        if self.isChasing:
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
        else:
            random.shuffle(DIRECTIONS)
            for dx, dy in DIRECTIONS:
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
                if 0 <= new_x < maze_width and 0 <= new_y < maze_height and current_maze[new_y, new_x] == 0:
                    self.x = new_x
                    self.y = new_y
                    break
            
    def check_collision(self, player):
        return self.x == player.x and self.y == player.y

# Initialize the player at middle left of the labyrinth
player_start_y = maze_height // 2
for y in range(player_start_y, maze_height):
    if current_maze[y, 1] == 0:
        player_start_y = y
        break

player = Player(1, player_start_y, speed=1)

# Guards initial positions and speed
guards = [
    Guard(16, 4, "left", speed=2),
    Guard(9, 14, "left", speed=2),
    Guard(19, 16, "left", speed=2),
    Guard(28, 12, "left", speed=2)
]

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
bonus_active = False
bonus_start_time = 0
code_gathered = False

def render_timer(screen, time_left):
    font = pygame.font.SysFont(None, 48)
    time_text = f"{time_left // 60:02}:{time_left % 60:02}"
    timer_surf = font.render(time_text, True, red)
    screen.blit(timer_surf, (Screen_width - 150, 10))  # Position at top-right corner

while running:
    clock.tick(5)  # Slower FPS for enemies (now adjusted further)
    update_current_maze()
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
                start_ticks = pygame.time.get_ticks()  # Reset timer when game starts
    
    if gameStatus == "play" and not bonus_active:  # Only move and update if the game is not over or pause state
        # Timer countdown
        if not bonus_active:
            seconds_elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
            time_left = max(0, time_limit - seconds_elapsed)  # Calculate time left
        
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
                    "guards_pos": [(guard.x, guard.y) for guard in guards],
                }
                checkpoint_ticks = pygame.time.get_ticks()
                checkpoint_time_left = time_left
                checkpoint_used = False  # Reset the checkpoint usage flag

            # If the player collected a bonus, activate the bonus effect
            if result == "bonus":
                bonus_active = True
                bonus_start_time = pygame.time.get_ticks()
                
            if result == "code":
                code_gathered = True
                current_level = 2
                update_current_maze()
                player.x = 1
                player.y = player_start_y

        # If the player presses "C" and checkpoint is not yet used, restore the game state
        if keys[pygame.K_c] and checkpoint_state is not None and not checkpoint_used:
            player.x, player.y = checkpoint_state["player_pos"]
            for i, guard in enumerate(guards):
                guard.x, guard.y = checkpoint_state["guards_pos"][i]
                guard.path = []
            if checkpoint_time_left is not None:
                start_ticks = pygame.time.get_ticks() - (time_limit - checkpoint_time_left) * 1000  # 
            
            checkpoint_used = True  # Mark the checkpoint as used
            pygame.time.wait(50)
        
        guardPos = []
        # Check if the guard see the player and if so, chase the player
        for guard in guards:
            guardX = guard.x
            guardY = guard.y
            direction = guard.direction
            if (guard.y-player.y)>0 and direction=="up":
                while(current_maze[guardY,guardX]!=1):
                    guardY = guardY-1
                    guardPos.append([guardX,guardY])
            elif (guard.y-player.y)<0 and direction=="down":
                while(current_maze[guardY,guardX]!=1):
                    guardY = guardY+1
                    guardPos.append([guardX,guardY])
            elif (guard.x-player.x)>0 and direction=="left":
                while(current_maze[guardY,guardX]!=1):
                    guardX = guardX-1
                    guardPos.append([guardX,guardY])
            elif (guard.x-player.x)<0 and direction=="right":
                while(current_maze[guardY,guardX]!=1):
                    guardX = guardX+1
                    guardPos.append([guardX,guardY])
        
        for guardP in guardPos:
            if guardP[0] == player.x and guardP[1] == player.y or guardP[0] == player.x and guardP[1] == player.y:
                chasing = True
        
        # Move guards and check for collisions with the player
        for guard in guards:
            if not bonus_active:  # Guards only move if bonus is not active
                guard.move(player, current_maze, chasing)
            if guard.check_collision(player):
                gameStatus = "gameover"  # Freeze the game if a guard catches the player
        
        # Deactivate the bonus after 10 seconds
        if bonus_active and pygame.time.get_ticks() - bonus_start_time >= 10000:  # 10 seconds
            bonus_active = False
            # Resume the timer correctly after bonus ends
            start_ticks += (pygame.time.get_ticks() - bonus_start_time)
    
    if gameStatus == "play" or gameStatus == "pause" or gameStatus=="gameover":
        # Draw the maze
        screen.fill(backgroundColor)
        for y in range(maze_height):
            for x in range(maze_width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                image_x = x * CELL_SIZE
                image_y = y * CELL_SIZE
                if current_maze[y, x] == 1:
                    screen.blit(brick, (image_x, image_y))
                elif current_maze[y, x] == 2:  # Afficher l'item checkpoint à cet emplacement
                    screen.blit(checkpoint, (image_x, image_y))
                elif current_maze[y, x] == 3:  # Afficher l'item bonus à cet emplacement
                    screen.blit(bonus, (image_x, image_y))
                # elif current_maze[y, x] == 4:  # Show star at this location
                #     screen.blit(star, (image_x, image_y))
                elif current_maze[y, x] == 5:  # Afficher le checkpoint sauvegarde
                    screen.blit(portail, (image_x, image_y))
                # Afficher l'arriere plan
                elif current_maze[y, x] == 6:
                    screen.blit(portail_left_angle, (image_x, image_y))
                elif current_maze[y, x] == 7:
                    screen.blit(portail_top, (image_x, image_y))
                elif current_maze[y, x] == 8:
                    screen.blit(portail_right_top_angle, (image_x, image_y))
                elif current_maze[y, x] == 9:
                    screen.blit(portail_left, (image_x, image_y))
                elif current_maze[y, x] == 10:
                    screen.blit(portail_left_bootom_angle, (image_x, image_y))
                elif current_maze[y, x] == 11:
                    screen.blit(portail_right, (image_x, image_y))
                elif current_maze[y, x] == 12:
                    screen.blit(portail_right_bottom_angle, (image_x, image_y))
                elif current_maze[y, x] == 13:
                    screen.blit(portail_bottom, (image_x, image_y))
                elif current_maze[y, x] == 14:
                    screen.blit(portail_center, (image_x, image_y))
                elif current_maze[y, x] == 15:  # Afficher l'item code à cet emplacement
                    screen.blit(code, (image_x, image_y))
                elif current_maze[y, x] == 15:  # Afficher l'item de la bombe
                    screen.blit(code, (image_x, image_y))
        
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
        
        # Render the timer on the screen
        render_timer(screen, time_left)
        
        # Draw pause text
        if gameStatus == "pause":
            x = (Screen_width-pauseText_width)/2
            y = (Screen_height-pauseText_height)/2
            screen.blit(pauseText, (x, y))
    
    elif gameStatus == "start":
        screen.blit(menu_principal, (0, 0))
    elif gameStatus == "gameover":
        screen.blit(gameover, (0, 0))
    elif gameStatus == "win":
        screen.blit(win, (0, 0))
    
    # Update the display
    pygame.display.flip()

pygame.quit()