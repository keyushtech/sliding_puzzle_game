
# Importing required packages

import turtle
import random
import time
import tkinter as tk
from tkinter import messagebox
import copy
import math

def fireworks():
    fire = turtle.Turtle(visible=False)
    fire.speed(0)
    fire.color("red", "yellow")
    for radius in range(20, 120, 10):
        fire.clear()
        for angle in range(0, 360, 30):
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            fire.penup()
            fire.goto(x, y)
            fire.dot(10)
        screen.update()
        time.sleep(0.1)
    fire.clear()

GAME_ASCII_ART = """                     ░██████    ░██ ░██       ░██ ░██                          ░█████████                                   ░██ 
                     ░██   ░██  ░██           ░██                              ░██     ░██                                  ░██ 
                     ░██        ░██ ░██ ░████████ ░██ ░████████   ░████████    ░██     ░██ ░██    ░██ ░█████████ ░█████████ ░██  ░███████  
                     ░████████  ░██ ░██ ░██   ░██ ░██ ░██    ░██ ░██    ░██    ░█████████  ░██    ░██      ░███       ░███  ░██ ░██    ░██ 
                            ░██ ░██ ░██ ░██   ░██ ░██ ░██    ░██ ░██    ░██    ░██         ░██    ░██    ░███       ░███    ░██ ░█████████ 
                     ░██   ░██  ░██ ░██ ░██   ░██ ░██ ░██    ░██ ░██   ░███    ░██         ░██   ░███  ░███       ░███      ░██ ░██        
                     ░██████    ░██ ░██ ░█████░██ ░██ ░██    ░██  ░█████░██    ░██          ░█████░██ ░█████████ ░█████████ ░██  ░███████
                                                                        ░██
                                                                   ░███████"""
print(GAME_ASCII_ART)
# Game Title
GAME_TITLE = "The Ultimate Sliding Puzzle Challenge!"

print("The Ultimate Sliding Puzzle Challenge!")
print("EASY:")
print("Solve the classic 4x4 sliding puzzle using numbers 1 through 15.\
The grid lines are clearly visible, providing distinct boundaries for each tile.\
This mode is ideal for beginners to understand the game mechanics and practice their moves!")
print("MEDIUM:")
print("Piece together a picture on the 4x4 grid. \
The grid lines are still visible,offering a helpful guide. A good challenge for those familiar with the puzzle.")
print("HARD:")
print("Reconstruct a seamless picture on the 4x4 grid. The grid lines are hidden,making it much harder to distinguish tile boundaries.\
Only for expert puzzlers seeking the ultimate challenge!")

difficulty_level = input("Choose your difficulty! Type easy, medium, or hard: ").lower()


# Game Board Configuration

BOARD_SIZE = 600
CELL = BOARD_SIZE // 4
half = BOARD_SIZE // 2

# Counter

moves = 0
leaderboard = [
    ("Obul", 105),  # Example: 15 moves + 10 sec = 25 pts
    ("Keyush Sai", 150),  # Example: 20 moves + 12 sec = 32 pts
    ("Abhishek", 190),  # Example: 18 moves + 10 sec = 28 pts
    ("Saumitra", 234)  # Example: 30 moves + 15 sec = 45 pts
]
moves_history = []   # store each move
checkpoint_state = None  # to store a snapshot (grid + moves + timer)

# Turtle screen setup

screen = turtle.Screen()
screen.setup(700, 700)
screen.title(f"Sliding Puzzle ({difficulty_level.capitalize()})")
screen.bgcolor("black")
screen.tracer(0)
screen.tracer(0)

# Instruction banner
instruction_turtle = turtle.Turtle(visible=False)
instruction_turtle.penup()
instruction_turtle.color("yellow")
instruction_turtle.goto(0, -330)
instruction_turtle.write("Press 's' to save, 'r' to resume",
                          align="center", font=("Arial", 20, "bold"))


if difficulty_level in ("medium", "hard"):
    try:
        # Medium tiles (load from medium_set/)
        for i in range(1, 16):
            screen.addshape(f"medium_set/medium_tile_{i}.gif")
        screen.addshape("medium_set/medium_blank_tile.gif")

        # Hard tiles (load from hard_set/)
        for i in range(1, 16):
            screen.addshape(f"hard_set/hard_tile_{i}.gif")
        screen.addshape("hard_set/hard_blank_tile.gif")

        screen.bgcolor("black")
    except turtle.TurtleGraphicsError as e:
        print("Image registration error:", e)
        print("Make sure medium_set/ and hard_set/ folders exist with the GIFs.")


# Setting the Timer

start_time = None
timer_running = False

# Physical appearance of timer and move counter

timer_turtle = turtle.Turtle(visible=False)
timer_turtle.penup()
timer_turtle.color("orange")
timer_turtle.goto(200, 320)
moves_turtle = turtle.Turtle(visible=False)
moves_turtle.penup()
moves_turtle.color("orange")
moves_turtle.goto(-200, 320)

# Leaderboard setup

message_turtle = turtle.Turtle(visible=False)
message_turtle.penup()
message_turtle.hideturtle()
message_turtle.color("orange")
message_turtle.goto(0, 320)

# Background for Leaderboard

bg_turtle = turtle.Turtle(visible=False)
bg_turtle.penup()
bg_turtle.hideturtle()

# Function to keep timer running

def start_timer():
    global start_time, timer_running
    start_time = time.time()
    timer_running = True
    update_timer()

def update_timer():
    if timer_running:
        elapsed = int(time.time() - start_time )
        mins, secs = divmod(elapsed, 60)
        timer_turtle.clear()
        timer_turtle.write(f"Time: {mins:02d}:{secs:02d}",
                           align="center", font=("Arial", 16, "normal"))
        screen.ontimer(update_timer, 1000)


# Function to keep move counter running

def update_moves():
    moves_turtle.clear()
    moves_turtle.write(f"Moves: {moves}",
                       align="center", font=("Arial", 16, "normal"))


# Function to clear message that pops up after invalid move

def clear_message():
    message_turtle.clear()

# Checkpoint Function
def checkpoint():
    global checkpoint_state
    checkpoint_state = {
        "grid": copy.deepcopy(grid),
        "moves": moves,
        "history": moves_history.copy(),
        "time": time.time() - start_time if start_time else 0
    }
    # show on screen
    message_turtle.clear()
    message_turtle.goto(0, -280)
    message_turtle.color("yellow")
    message_turtle.write("✅ Checkpoint Saved!", align="center", font=("Arial", 16, "bold"))
    screen.ontimer(clear_message, 1500)  # clear after 1.5s

def resume():
    global grid, moves, moves_history, start_time, timer_running
    if checkpoint_state:
        grid = copy.deepcopy(checkpoint_state["grid"])
        moves = checkpoint_state["moves"]
        moves_history = checkpoint_state["history"].copy()
        start_time = time.time() - checkpoint_state["time"]
        timer_running = True
        draw_tiles()
        update_moves()
        # show on screen
        message_turtle.clear()
        message_turtle.goto(0, -280)
        message_turtle.color("green")
        message_turtle.write("🔄 Resumed from Checkpoint!", align="center", font=("Arial", 16, "bold"))
        screen.ontimer(clear_message, 1500)  # clear after 1.5s
    else:
        message_turtle.clear()
        message_turtle.goto(0, -280)
        message_turtle.color("red")
        message_turtle.write("⚠️ No Checkpoint Available", align="center", font=("Arial", 16, "bold"))
        screen.ontimer(clear_message, 1500)



# Grid drawing

pen = turtle.Turtle(visible=False)
pen.speed(0)
if difficulty_level == "hard":
    pen.color("black")  # hide grid in hard mode
else:
    pen.color("orange")
pen.pensize(2)

pen.penup()
pen.goto(-half, half)
pen.pendown()
for _ in range(4):
    pen.forward(BOARD_SIZE)
    pen.right(90)

for i in range(1, 4):
    pen.penup()
    pen.goto(-half + i * CELL, half)
    pen.pendown()
    pen.goto(-half + i * CELL, -half)
    pen.penup()
    pen.goto(-half, half - i * CELL)
    pen.pendown()
    pen.goto(half, half - i * CELL)

# Setting up Logic states of Grid

solved_grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, None]
]
grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, None]
]

# Setting up required prerequisites for drawing style

t = turtle.Turtle(visible=False)
t.penup()
t.speed(0)

# Locating coordinates on basis of row and column

def cell_to_xy(row, col):
    x = -half + col * CELL + CELL // 2
    y = half - row * CELL - CELL // 2
    return x, y

# Drawing tiles

def draw_tiles():
    t.clearstamps()
    t.clear()
    for r in range(4):
        for c in range(4):
            v = grid[r][c]
            x, y = cell_to_xy(r, c)
            if v is not None:
                if difficulty_level == "easy":
                    t.color("orange")
                    t.goto(x, y - 15)
                    t.write(str(v), align="center", font=("Arial", 48, "bold"))
                else:
                    if difficulty_level == "medium":
                        img = f"medium_set/medium_tile_{v}.gif" if v else "medium_set/medium_blank_tile.gif"
                    else:
                        img = f"hard_set/hard_tile_{v}.gif" if v else "hard_set/hard_blank_tile.gif"

                    t.shape(img)
                    t.goto(x, y)
                    t.stamp()
    screen.update()

# Leaderboard defn and changing state at end

def display_leaderboard():
    global leaderboard
    message_turtle.clear()
    bg_turtle.clear()
    bg_turtle.penup()
    bg_turtle.goto(-250, 220)
    bg_turtle.color("black")
    bg_turtle.begin_fill()
    bg_turtle.pendown()
    bg_turtle.goto(250, 220)
    bg_turtle.goto(250, -200)
    bg_turtle.goto(-250, -200)
    bg_turtle.goto(-250, 220)
    bg_turtle.end_fill()

    leaderboard.sort(key=lambda x: x[1])
    message_turtle.goto(-200, 180)
    message_turtle.color("white")
    message_turtle.write("LEADERBOARD", align="left", font=("Arial", 24, "bold"))

    y_pos = 140
    for i, entry in enumerate(leaderboard[:10]):
        name, score = entry
        message_turtle.goto(-200, y_pos)
        message_turtle.write(f"{i + 1}. {name}: {score} pts", align="left", font=("Arial", 16, "normal"))
        y_pos -= 30
    screen.update()

# Function to shuffle board properly so as to avoid impossible configurations

def shuffle(n):
    """Shuffles the puzzle grid by making 'n' random valid moves."""
    for _ in range(n):
        # Find the blank tile's current position
        r1, c1 = -1, -1
        for r in range(4):
            for c in range(4):
                if grid[r][c] is None:
                    r1, c1 = r, c
                    break
            if r1 != -1:
                break

        neighbours = []
        # Determine valid adjacent cells for swapping
        if r1 > 0: neighbours.append("up")
        if r1 < 3: neighbours.append("down")
        if c1 > 0: neighbours.append("left")
        if c1 < 3: neighbours.append("right")

        if not neighbours:  # Should not happen in a 4x4, but good practice
            continue

        choice = random.choice(neighbours)  # Pick a random valid direction

        # Perform the swap
        if choice == "up":
            grid[r1][c1], grid[r1 - 1][c1] = grid[r1 - 1][c1], grid[r1][c1]
        elif choice == "left":
            grid[r1][c1], grid[r1][c1 - 1] = grid[r1][c1 - 1], grid[r1][c1]
        elif choice == "right":
            grid[r1][c1], grid[r1][c1 + 1] = grid[r1][c1 + 1], grid[r1][c1]
        else:  # choice == "down"
            grid[r1][c1], grid[r1 + 1][c1] = grid[r1 + 1][c1], grid[r1][c1]

# Displaying Picture/Numbers based on chosen difficulty level

# Step 1: Show the solved picture first
draw_tiles()
screen.update()

# Step 2: Pause so the player can see the complete picture
time.sleep(5)  # show solved state for 5 seconds

# Step 3: Shuffle and redraw puzzle
shuffle(100000)
draw_tiles()

# Start timer and moves counter
start_timer()
update_moves()


# Actual function that defines click mechanism

def on_click(x, y):
    """Handles mouse clicks on the puzzle board."""
    global timer_running
    global moves
    global leaderboard  # Access the global leaderboard list

    # Clear any temporary messages (invalid, win) at the beginning of a new click
    # The leaderboard background is handled by display_leaderboard() itself.
    message_turtle.clear()
    bg_turtle.clear()  # Clear leaderboard background if it was visible

    # Find the blank tile's current position (r1, c1)
    r1, c1 = -1, -1
    for r in range(4):
        for c in range(4):
            if grid[r][c] is None:
                r1, c1 = r, c
                break
        if r1 != -1:
            break

    # Determine the grid cell (row, col) that was clicked by the user
    col = int((x + half) // CELL)
    row = int((half - y) // CELL)

    # Check if the clicked cell is adjacent to the blank cell (a valid move)
    if abs(row - r1) + abs(col - c1) == 1:
        # Valid move: swap the tiles
        grid[r1][c1], grid[row][col] = grid[row][col], grid[r1][c1]
        moves += 1  # Increment moves count
        update_moves()  # Update moves display
        # Determine direction of move
        if row == r1 - 1 and col == c1:  # moved up into blank
            moves_history.append("Up")
        elif row == r1 + 1 and col == c1:  # moved down into blank
            moves_history.append("Down")
        elif col == c1 - 1 and row == r1:  # moved left into blank
            moves_history.append("Left")
        elif col == c1 + 1 and row == r1:  # moved right into blank
            moves_history.append("Right")

        # Redraw numbers after a valid move
        draw_tiles()

        # Check if the puzzle is now solved
        if grid == solved_grid:
            message_turtle.goto(0, 320)  # Position for win message
            message_turtle.color("green")
            message_turtle.write("CONGRATULATIONS! YOU WON! 🎉", align="center", font=("Arial", 20, "bold"))
            fireworks()

            # ✅ show moves in popup
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Move History", f"Your move sequence:\n{moves_history}")
            root.destroy()

            timer_running = False  # Stop the timer
            screen.onclick(None)  # Disable further clicks on the board

            # Calculate final score (moves + elapsed time)
            elapsed_time = int(time.time() - start_time)
            final_score = moves + elapsed_time

            # Prompt player for their name and update leaderboard
            player_name = turtle.textinput("You Win!",
                                           f"You finished in {moves} moves and {elapsed_time} seconds!\n"
                                           f"Your total score is {final_score} pts (lower is better)!\n"
                                           "Enter your name:")
            if player_name:
                leaderboard.append((player_name, final_score))

            display_leaderboard()  # Show the updated leaderboard

    else:
        # Invalid move: display a temporary message
        message_turtle.goto(0, 320)  # Position for invalid message
        message_turtle.color("red")
        message_turtle.write("INVALID MOVE! PLEASE TRY AGAIN!", align="center", font=("Arial", 16, "normal"))
        screen.ontimer(clear_message, 650)  # Clear message after 0.65 seconds

# Final command that sets things into motion

screen.onclick(on_click)  # Register the click handler function

# Listening code for Checkpoint
screen.listen()
screen.onkey(checkpoint, "s")  # press "s" to save
screen.onkey(resume, "r")      # press "r" to resume
screen.listen()  # make sure the puzzle window is listening for key presses

turtle.done()  # Keep the turtle graphics window open until manually closed
