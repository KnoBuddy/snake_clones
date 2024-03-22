import tkinter as tk
import random

def game_loop():
    update_snake_position()
    check_collisions()
    spawn_food()
    draw_everything()
    update_window_title()
    window.after(100, game_loop)

def spawn_food():
    global food_x, food_y, food_exists
    if not food_exists:
        food_x = random.randint(0, (canvas_width - snake_speed) // snake_speed) * snake_speed
        food_y = random.randint(0, (canvas_height - snake_speed) // snake_speed) * snake_speed
        food_exists = True

def update_snake_position():
    global snake, snake_direction
    head_x, head_y = snake[0]
    new_head = (head_x + direction_delta[snake_direction][0], head_y + direction_delta[snake_direction][1])
    snake.insert(0, new_head)
    if len(snake) > 1:
        snake.pop()

def grow_snake():
    global snake, snake_direction
    tail_end_x, tail_end_y = snake[-1]
    dx, dy = direction_delta[snake_direction]
    # Add a new segment in the opposite direction of movement
    new_segment = (tail_end_x - dx, tail_end_y - dy)
    snake.append(new_segment)

def check_collisions():
    global food_x, food_y, food_exists, score
    head_x, head_y = snake[0]

    if head_x < 0 or head_x >= canvas_width or head_y < 0 or head_y >= canvas_height:
        print("Game over!")
        window.quit()

    if (head_x, head_y) == (food_x, food_y):
        grow_snake()
        score += 10
        food_x, food_y = None, None
        food_exists = False
        update_window_title()

    if len(snake) > 1 and len(snake) != len(set(snake)):
        print("Game over!")
        window.quit()

def draw_snake_segment(segment):
    x, y = segment
    game_canvas.create_rectangle(x, y, x + snake_speed, y + snake_speed, fill='green')

def draw_everything():
    game_canvas.delete("all")
    for segment in snake:
        draw_snake_segment(segment)
    if food_x is not None and food_y is not None:
        game_canvas.create_rectangle(food_x, food_y, food_x + snake_speed, food_y + snake_speed, fill='red')

def change_direction(event):
    global snake_direction
    direction_map = {'w': 'Up', 'a': 'Left', 's': 'Down', 'd': 'Right'}
    if event.char in direction_map and not are_opposite_directions(snake_direction, direction_map[event.char]):
        snake_direction = direction_map[event.char]

def are_opposite_directions(dir1, dir2):
    opposite_pairs = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
    return opposite_pairs[dir1] == dir2

def update_window_title():
    window.title(f"Snake Game - Score: {score}")

if __name__ == "__main__":
    window = tk.Tk()
    canvas_width, canvas_height = 600, 400
    game_canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='black')
    game_canvas.pack()

    snake = [(100, 100)]  # Start with only the head
    snake_direction = 'Right'
    snake_speed = 10
    direction_delta = {'Up': (0, -snake_speed), 'Down': (0, snake_speed), 'Left': (-snake_speed, 0), 'Right': (snake_speed, 0)}
    food_x, food_y = None, None
    food_exists = False
    score = 0

    window.bind("<KeyPress>", change_direction)

    spawn_food()
    game_loop()
    window.mainloop()
