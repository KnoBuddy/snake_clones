from ursina import *
from random import randint

app = Ursina()
window.fullscreen = False
window.borderless = False
window.title = "Snake Game"

grid_size = 8
camera.orthographic = True
camera.fov = grid_size * 2  # Adjust the FOV to fit the grid size
camera.position = (grid_size / 2, grid_size / 2)

snake = Entity(model='cube', color=color.green, scale=1)
food = Entity(model='cube', color=color.red, scale=1)
score = Text(text='Score: 0', position=(-0.5, 0.45), scale=2, color=color.white)
snake.direction = Vec2(0, 0)
snake.tail = []
snake.tail_length = 0
movement_delay = 0.1
last_moved = 0

def spawn_food():
    food.position = (randint(-grid_size + 1, grid_size - 1), randint(-grid_size + 1, grid_size - 1))

def create_walls():
    for x in range(-grid_size, grid_size + 1):
        Entity(model='cube', color=color.gray, position=(x, grid_size), scale=1)
        Entity(model='cube', color=color.gray, position=(x, -grid_size), scale=1)
    for y in range(-grid_size, grid_size + 1):
        Entity(model='cube', color=color.gray, position=(grid_size, y), scale=1)
        Entity(model='cube', color=color.gray, position=(-grid_size, y), scale=1)

def move_snake():
    snake.x += snake.direction.x
    snake.y += snake.direction.y

def check_food_collision():
    global food
    if abs(snake.x - food.x) < 1 and abs(snake.y - food.y) < 1:
        spawn_food()
        snake.tail_length += 1
        score.text = f'Score: {snake.tail_length}'

def update_snake_tail():
    if snake.tail_length > 0:
        snake.tail.append((snake.x, snake.y))
        if len(snake.tail) > snake.tail_length:
            snake.tail.pop(0)

def handle_input():
    if held_keys['d'] and snake.direction != Vec2(-1, 0):
        snake.direction = Vec2(1, 0)
    elif held_keys['a'] and snake.direction != Vec2(1, 0):
        snake.direction = Vec2(-1, 0)
    elif held_keys['w'] and snake.direction != Vec2(0, -1):
        snake.direction = Vec2(0, 1)
    elif held_keys['s'] and snake.direction != Vec2(0, 1):
        snake.direction = Vec2(0, -1)

def check_boundaries():
    if abs(snake.x) >= grid_size or abs(snake.y) >= grid_size:
        print('Game Over! Out of boundaries.')
        application.quit()

def check_self_collision():
    if (snake.x, snake.y) in snake.tail[:-1]:
        print(f'Game Over! Snake collided with itself. Position: ({snake.x}, {snake.y}), Tail: {snake.tail}')
        application.quit()

def update():
    global last_moved
    current_time = time.time()
    if current_time - last_moved < movement_delay:
        return
    last_moved = current_time

    handle_input()
    move_snake()
    check_food_collision()
    update_snake_tail()
    check_boundaries()
    check_self_collision()

spawn_food()
create_walls()
EditorCamera()
app.run()
