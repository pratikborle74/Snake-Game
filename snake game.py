import turtle
import random
import time

# Constants
WIDTH = 548
HEIGHT = 483
FOOD_SIZE = 10
DELAY = 100  # Milliseconds

# Directional Offsets
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

def reset():
    """Reset the game to the initial state."""
    global snake, snake_direction, food_pos, running
    running = True  
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]  # Initial snake body
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    move_snake()

def move_snake():
    """Move the snake forward and check for collisions."""
    global snake_direction, running

    if not running:
        return  

    try:
        # Calculate new head position
        new_head = [snake[-1][0] + offsets[snake_direction][0], 
                    snake[-1][1] + offsets[snake_direction][1]]

        # Check self-collision
        if new_head in snake:
            game_over()
            return

        snake.append(new_head)

        # Check if food is eaten
        if not food_collision():
            snake.pop(0)  

        # Screen wrapping (Teleport to opposite side)
        for i in range(len(snake)):
            snake[i][0] = (snake[i][0] + WIDTH // 2) % WIDTH - WIDTH // 2
            snake[i][1] = (snake[i][1] + HEIGHT // 2) % HEIGHT - HEIGHT // 2

        # Clear previous snake stamps
        pen.clearstamps()

        # Draw the snake with the head in a different color
        for i, segment in enumerate(snake):
            pen.goto(segment)
            if i == len(snake) - 1:
                pen.color("blue")  # Snake head
            else:
                pen.color("sky blue")  # Snake body
            pen.stamp()

        # Refresh screen and repeat movement
        screen.update()
        turtle.ontimer(move_snake, DELAY)

    except turtle.Terminator:
        print("Game closed. Exiting gracefully.")

def food_collision():
    """Check if the snake has eaten the food."""
    global food_pos
    if get_distance(snake[-1], food_pos) < 15:  # Check if the snake's head is close to the food
        # Align food to the center of the snake's head
        food.goto(snake[-1])  # Move food to the snake's head position
        food_pos = get_random_food_pos()  # Generate a new random position for the next food
        food.goto(food_pos)  # Move food to the new position
        return True
    return False

def get_random_food_pos():
    """Generate a new food position within bounds (ensuring integer values)."""
    x = random.randint(-WIDTH // 2 + FOOD_SIZE, WIDTH // 2 - FOOD_SIZE)
    y = random.randint(-HEIGHT // 2 + FOOD_SIZE, HEIGHT // 2 - FOOD_SIZE)
    return (x, y)

def get_distance(pos1, pos2):
    """Calculate Euclidean distance between two points."""
    return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5

def game_over():
    """Handle game over animation and restart."""
    global running
    running = False
    pen.color("red")
    pen.write("Game Over!", align="center", font=("Arial", 24, "bold"))
    screen.update()
    time.sleep(1)
    pen.clear()
    reset()

def animate_food_eaten():
    """Animate food when eaten to make it more visually appealing."""
    for _ in range(3):
        food.color("white")
        screen.update()
        time.sleep(0.1)
        food.color("red")
        screen.update()
        time.sleep(0.1)

# Direction Control Functions
def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"

def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"

def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"

def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"

# Screen Setup
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Enhanced Snake Game 🐍")
screen.bgcolor("black")
screen.tracer(0)

# Set Background Image
screen.bgpic("bg.gif")  # Turtle supports only .gif format

# Pen Setup (Snake)
pen = turtle.Turtle("square")
pen.penup()

# Food Setup
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(FOOD_SIZE / 20)  
food.penup()

# Game Running Flag
running = True

# Key Bindings
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

# Start the game
reset()
turtle.done()
