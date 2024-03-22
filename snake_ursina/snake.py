from ursina import *
import random
import configparser


GRID_SIZE = 0.5
MOVEMENT_SPEED = 0.1
WALL_THICKNESS = 0.5
BOARD_WIDTH = 20
BOARD_HEIGHT = 10
HIGH_SCORE = 0

def save_config():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'GRID_SIZE': str(GRID_SIZE),
        'MOVEMENT_SPEED': str(MOVEMENT_SPEED),
        'WALL_THICKNESS': str(WALL_THICKNESS),
        'BOARD_WIDTH': str(BOARD_WIDTH),
        'BOARD_HEIGHT': str(BOARD_HEIGHT),
        'HIGH_SCORE': str(HIGH_SCORE)
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_config():
    global GRID_SIZE, MOVEMENT_SPEED, WALL_THICKNESS, BOARD_WIDTH, BOARD_HEIGHT, HIGH_SCORE

    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'SETTINGS' in config:
        settings = config['SETTINGS']
        GRID_SIZE = float(settings.get('GRID_SIZE', GRID_SIZE))
        MOVEMENT_SPEED = float(settings.get('MOVEMENT_SPEED', MOVEMENT_SPEED))
        WALL_THICKNESS = float(settings.get('WALL_THICKNESS', WALL_THICKNESS))
        BOARD_WIDTH = int(settings.get('BOARD_WIDTH', BOARD_WIDTH))
        BOARD_HEIGHT = int(settings.get('BOARD_HEIGHT', BOARD_HEIGHT))
        HIGH_SCORE = int(settings.get('HIGH_SCORE', HIGH_SCORE))

class Snake:
    def __init__(self):
        self.head = None
        self.tongue = None
        self.left_eye = None
        self.right_eye = None
        self.tail = []
        self.current_direction = Vec2(0, 0)
        self.previous_head_position = Vec2(0, 0)
        self.next_direction = Vec2(0, 0)
        self.movement_speed = MOVEMENT_SPEED
        self.movement_timer = 0

    def create(self):
        self.head = Entity(model='circle', color=color.green, position=(0, 0), scale=(GRID_SIZE*1.4, GRID_SIZE*1.2), collider='box')
        self.tongue = Entity(model='circle', color=color.red, position=self.head.position, scale=(GRID_SIZE*0.2, GRID_SIZE*0.4), z=-0.1)
        
        eye_scale = 0.15 * GRID_SIZE
        self.left_eye = Entity(model='circle', color=color.black, position=self.head.position + Vec2(0, GRID_SIZE*0.1), scale=eye_scale, z=0.1)
        self.right_eye = Entity(model='circle', color=color.black, position=self.head.position + Vec2(0, GRID_SIZE*0.1), scale=eye_scale, z=0.1)
        
        # Set initial eye rotations
        self.left_eye.rotation_z = 0
        self.right_eye.rotation_z = 0
        
        self.tail = []

    def move(self):
        if self.head is None:
            return
        
        self.current_direction = self.next_direction  # Ensure direction update
        self.previous_head_position = self.head.position
        self.head.position += self.current_direction

        # Update head scale based on current direction
        self.head.scale = (GRID_SIZE*1.4, GRID_SIZE*1.2) if self.current_direction.x != 0 else (GRID_SIZE*1.2, GRID_SIZE*1.4)
        
        # Update tongue and eyes position and rotation
        if self.current_direction == Vec2(0, GRID_SIZE):  # Moving up
            tongue_offset = Vec2(0, GRID_SIZE*0.6)
            tongue_rotation = 0
        elif self.current_direction == Vec2(0, -GRID_SIZE):  # Moving down
            tongue_offset = Vec2(0, -GRID_SIZE*0.6)
            tongue_rotation = 180
        elif self.current_direction == Vec2(GRID_SIZE, 0):  # Moving right
            tongue_offset = Vec2(GRID_SIZE*0.6, 0)
            tongue_rotation = 270
        elif self.current_direction == Vec2(-GRID_SIZE, 0):  # Moving left
            tongue_offset = Vec2(-GRID_SIZE*0.6, 0)
            tongue_rotation = 90
        else:
            tongue_offset = Vec2(0, -GRID_SIZE*0.6)
            tongue_rotation = 180

        self.tongue.position = self.head.position + tongue_offset
        self.tongue.rotation_z = tongue_rotation
        self.tongue.z = -0.1  # Adjust tongue z-position

        if self.current_direction == Vec2(0, GRID_SIZE):  # Moving up
            left_eye_offset = Vec2(-GRID_SIZE*0.2, 0)
            right_eye_offset = Vec2(GRID_SIZE*0.2, 0)
        elif self.current_direction == Vec2(0, -GRID_SIZE):  # Moving down
            left_eye_offset = Vec2(-GRID_SIZE*0.2, 0)
            right_eye_offset = Vec2(GRID_SIZE*0.2, 0)
        elif self.current_direction == Vec2(GRID_SIZE, 0):  # Moving right
            left_eye_offset = Vec2(0, GRID_SIZE*0.2)
            right_eye_offset = Vec2(0, -GRID_SIZE*0.2)
        elif self.current_direction == Vec2(-GRID_SIZE, 0):  # Moving left
            left_eye_offset = Vec2(0, -GRID_SIZE*0.2)
            right_eye_offset = Vec2(0, GRID_SIZE*0.2)
        else:
            left_eye_offset = Vec2(-GRID_SIZE*0.2, 0)
            right_eye_offset = Vec2(GRID_SIZE*0.2, 0)

        self.left_eye.position = self.head.position + left_eye_offset
        self.right_eye.position = self.head.position + right_eye_offset
        self.left_eye.z = -0.1  # Adjust left eye z-position
        self.right_eye.z = -0.1  # Adjust right eye z-position
        
        # Rotate eyes based on the current direction
        if self.current_direction.x != 0:
            self.left_eye.rotation_z = 90
            self.right_eye.rotation_z = 90
        else:
            self.left_eye.rotation_z = 0
            self.right_eye.rotation_z = 0

        if len(self.tail) > 0:
            for i in range(len(self.tail) - 1, 0, -1):
                self.tail[i].position = self.tail[i-1].position

            self.tail[0].position = self.previous_head_position

            # Update tail segment scales based on their relative positions
            for i in range(len(self.tail) - 1):
                direction = self.tail[i].position - self.tail[i+1].position
                # Update scale based on where the segment is relative to the next one as well as the current direction
                if len(self.tail) > 2:
                    self.tail[-3].scale = (GRID_SIZE*1.1, GRID_SIZE*1) if self.tail[-3].position.x != 0 else (GRID_SIZE*1, GRID_SIZE*1.1)
                if len(self.tail) > 1:
                    self.tail[-2].scale = (GRID_SIZE*1.1, GRID_SIZE*0.85) if self.tail[-2].position.x != 0 else (GRID_SIZE*0.85, GRID_SIZE*1.1)
                if len(self.tail) > 0:
                    self.tail[-1].scale = (GRID_SIZE*1.1, GRID_SIZE*0.7) if self.tail[-1].position.x != 0 else (GRID_SIZE*0.7, GRID_SIZE*1.1)
                else:
                    self.tail[i].scale = (GRID_SIZE*1.3, GRID_SIZE*1.2) if direction.x != 0 else (GRID_SIZE*1.2, GRID_SIZE*1.3)
            
            # If onyl one segment, update scale based on the current direction of the head
            if len(self.tail) == 1:
                self.tail[0].scale = (GRID_SIZE*1.1, GRID_SIZE*1) if self.current_direction.x != 0 else (GRID_SIZE*1, GRID_SIZE*1.1)
            
    def grow(self):
        if len(self.tail) > 0:
            new_segment_position = self.tail[-1].position
            # Make the previous last segment normal before adding a new one
            self.tail[-1].model = 'circle'  # Revert model if you change it
            self.tail[-1].scale = (GRID_SIZE * 1.3, GRID_SIZE * 1.2)  # Normal scale
        else:
            new_segment_position = self.head.position - self.current_direction
    
        new_segment_scale = (GRID_SIZE*1.3, GRID_SIZE*1.2) if self.current_direction.x != 0 else (GRID_SIZE*1.2, GRID_SIZE*1.3)
        new_segment = Entity(model='circle', color=color.green, position=new_segment_position, scale=new_segment_scale, collider='box')
    
        self.tail.append(new_segment)

class Food:
    def __init__(self):
        self.entity = None
        self.stem = None

    def create(self):
        self.entity = Entity(model='circle', color=color.red, scale=(GRID_SIZE, GRID_SIZE), collider='box')
        self.stem = Entity(model='quad', color=color.brown, scale=(GRID_SIZE*0.2, GRID_SIZE*0.4), z=-0.1)
        self.respawn()

    def respawn(self):
        margin_x = 2
        margin_y = 2
        x_range = range(int(-BOARD_WIDTH/2 + margin_x), int(BOARD_WIDTH/2 - margin_x))
        y_range = range(int(-BOARD_HEIGHT/2 + margin_y), int(BOARD_HEIGHT/2 - margin_y))

        valid_position_found = False
        while not valid_position_found:
            new_x = random.choice(x_range) * GRID_SIZE
            new_y = random.choice(y_range) * GRID_SIZE
            new_position = Vec2(new_x, new_y)  # Convert to Vec2

            if (
                new_position != (snake.head.x, snake.head.y) and
                new_position not in [(segment.x, segment.y) for segment in snake.tail] and
                all(not self.entity.intersects(wall.entity).hit for wall in game.walls)
            ):
                valid_position_found = True

        self.entity.position = new_position
        self.stem.position = new_position + Vec2(0, GRID_SIZE*0.5)
        self.stem.z = -0.1  # Adjust stem z-position

class Wall:
    def __init__(self, position, scale):
        self.entity = Entity(model='quad', color=color.gray, position=position, scale=scale, collider='box')

class Game(Entity):
    def __init__(self):
        super().__init__()
        self.snake = Snake()
        self.food = Food()
        self.walls = []
        self.score = 0
        self.level = 1

    def create_walls(self):
        # Calculate grid extent including the walls
        grid_width = BOARD_WIDTH * GRID_SIZE
        grid_height = BOARD_HEIGHT * GRID_SIZE

        # Define wall position offsets to place walls just outside the grid
        offset_x = grid_width / 2 + WALL_THICKNESS / 2
        offset_y = grid_height / 2 + WALL_THICKNESS / 2

        # Place walls just outside the visible grid area
        self.walls = [
            Wall(Vec2(0, offset_y), Vec2(grid_width + WALL_THICKNESS, WALL_THICKNESS)),  # Top wall
            Wall(Vec2(0, -offset_y), Vec2(grid_width + WALL_THICKNESS, WALL_THICKNESS)),  # Bottom wall
            Wall(Vec2(-offset_x, 0), Vec2(WALL_THICKNESS, grid_height + WALL_THICKNESS)),  # Left wall
            Wall(Vec2(offset_x, 0), Vec2(WALL_THICKNESS, grid_height + WALL_THICKNESS))  # Right wall
        ]

    def update(self):
        self.snake.movement_timer += time.dt
        if self.snake.movement_timer >= self.snake.movement_speed:
            self.snake.current_direction = self.snake.next_direction  # Update direction
            self.snake.movement_timer = 0
            self.snake.move()
            self.check_collisions()
            self.check_level_up()
            self.super_food.respawn()  # Check if super food should respawn

    def check_level_up(self):
        required_score = 0
        for i in range(1, self.level + 1):
            required_score += 5 * i  # Calculate cumulative score required to reach the next level

        # Check if current score is enough to level up
        if self.score >= required_score:
            self.level += 1
            self.snake.movement_speed *= 0.9  # Increase the snake's speed
            level_text.text = f"Level: {self.level}"  # Update the level text

        score_text.text = f"Score: {self.score}"

    def input(self, key):
        if key in ['d', 'right'] and self.snake.current_direction != Vec2(-GRID_SIZE, 0):
            self.snake.next_direction = Vec2(GRID_SIZE, 0)
        elif key in ['a', 'left'] and self.snake.current_direction != Vec2(GRID_SIZE, 0):
            self.snake.next_direction = Vec2(-GRID_SIZE, 0)
        elif key in ['w', 'up'] and self.snake.current_direction != Vec2(0, -GRID_SIZE):
            self.snake.next_direction = Vec2(0, GRID_SIZE)
        elif key in ['s', 'down'] and self.snake.current_direction != Vec2(0, GRID_SIZE):
            self.snake.next_direction = Vec2(0, -GRID_SIZE)

    def check_collisions(self):
        if self.snake.head is None or self.food.entity is None:
            return

        if (self.snake.head.x, self.snake.head.y) == (self.food.entity.x, self.food.entity.y):
            self.snake.grow()
            self.food.respawn()
            self.score += 1

        # First check if the super food has spawned
        if self.super_food.entity is not None:
            if (self.snake.head.x, self.snake.head.y) == (self.super_food.entity.x, self.super_food.entity.y):
                self.snake.grow()
                self.super_food.respawn(force=True)

        for segment in self.snake.tail[1:]:
            if (self.snake.head.x, self.snake.head.y) == (segment.x, segment.y):
                print("Collision with tail detected!")  # Debug print
                self.game_over()
                return

        # Check if the snake's head is outside the game board
        if (
            self.snake.head.x < -BOARD_WIDTH * GRID_SIZE / 2 or
            self.snake.head.x >= BOARD_WIDTH * GRID_SIZE / 2 or
            self.snake.head.y < -BOARD_HEIGHT * GRID_SIZE / 2 or
            self.snake.head.y >= BOARD_HEIGHT * GRID_SIZE / 2
        ):
            self.game_over()

    def game_over(self):
        global HIGH_SCORE
        print(f"Game Over! Score: {self.score}")
        if self.score > HIGH_SCORE:
            print(f"New High Score: {self.score}")
            HIGH_SCORE = self.score
            save_config()
            high_score_text.text = f"High Score: {HIGH_SCORE}"
        print(f"Level: {self.level}")
        self.reset_game()

    def create_pause_menu(self):
        self.pause_handler = Entity(ignore_paused=True)
        self.pause_text = Text('PAUSED', origin=(0, -8), scale=2, enabled=False)

        # Create a background entity for the pause menu
        self.pause_background = Entity(
            parent=self.pause_handler,
            model='quad',
            scale=(44, 24),
            color=color.rgb(50, 50, 50, 100),
            enabled=False,
            z=-0.5
        )

        self.resume_button = Button(text='Resume', scale=(0.25, 0.05), y=0.3, color=color.azure, on_click=self.resume_game)
        self.quit_button = Button(text='Quit', scale=(0.25, 0.05), y=0.2, color=color.azure, on_click=application.quit)
        
        self.grid_size_label = Text('Grid Size:', position=(-0.3, 0.1), scale=1.5)
        self.grid_size_input = InputField(position=(.2, 0.1), scale=(0.25, 0.05), text=str(GRID_SIZE), color=color.gray)
        self.grid_size_input.highlight_color = color.light_gray

        self.movement_speed_label = Text('Movement Speed:', position=(-0.3, 0), scale=1.5)
        self.movement_speed_input = InputField(position=(.2, 0), scale=(0.25, 0.05), text=str(MOVEMENT_SPEED), color=color.gray)
        self.movement_speed_input.highlight_color = color.light_gray

        self.wall_thickness_label = Text('Wall Thickness:', position=(-0.3, -0.1), scale=1.5)
        self.wall_thickness_input = InputField(position=(.2, -0.1), scale=(0.25, 0.05), text=str(WALL_THICKNESS), color=color.gray)
        self.wall_thickness_input.highlight_color = color.light_gray

        self.board_width_label = Text('Board Width:', position=(-0.3, -0.2), scale=1.5)
        self.board_width_input = InputField(position=(.2, -0.2), scale=(0.25, 0.05), text=str(BOARD_WIDTH), color=color.gray)
        self.board_width_input.highlight_color = color.light_gray

        self.board_height_label = Text('Board Height:', position=(-0.3, -0.3), scale=1.5)
        self.board_height_input = InputField(position=(.2, -0.3), scale=(0.25, 0.05), text=str(BOARD_HEIGHT), color=color.gray)
        self.board_height_input.highlight_color = color.light_gray

        for entity in (self.pause_text, self.grid_size_label, self.grid_size_input,
                        self.movement_speed_label, self.movement_speed_input,
                        self.wall_thickness_label, self.wall_thickness_input,
                        self.board_width_label, self.board_width_input,
                        self.board_height_label, self.board_height_input,
                        self.resume_button, self.quit_button):
            entity.enabled = False

        def pause_handler_input(key):
            if key == 'escape':
                if not self.pause_text.enabled:
                    self.pause_game()
                else:
                    self.resume_game()

        self.pause_handler.input = pause_handler_input

    def pause_game(self):
        application.paused = True
        self.pause_text.enabled = True
        self.pause_background.enabled = True
        self.grid_size_label.enabled = True
        self.grid_size_input.enabled = True
        self.movement_speed_label.enabled = True
        self.movement_speed_input.enabled = True
        self.wall_thickness_label.enabled = True
        self.wall_thickness_input.enabled = True
        self.board_width_label.enabled = True
        self.board_width_input.enabled = True
        self.board_height_label.enabled = True
        self.board_height_input.enabled = True
        self.resume_button.enabled = True
        self.quit_button.enabled = True

    def resume_game(self):
        global GRID_SIZE, MOVEMENT_SPEED, WALL_THICKNESS, BOARD_WIDTH, BOARD_HEIGHT
        GRID_SIZE = float(self.grid_size_input.text)
        MOVEMENT_SPEED = float(self.movement_speed_input.text)
        WALL_THICKNESS = float(self.wall_thickness_input.text)
        BOARD_WIDTH = int(self.board_width_input.text)
        BOARD_HEIGHT = int(self.board_height_input.text)

        save_config()

        application.paused = False
        self.pause_text.enabled = False
        self.pause_background.enabled = False
        self.grid_size_label.enabled = False
        self.grid_size_input.enabled = False
        self.movement_speed_label.enabled = False
        self.movement_speed_input.enabled = False
        self.wall_thickness_label.enabled = False
        self.wall_thickness_input.enabled = False
        self.board_width_label.enabled = False
        self.board_width_input.enabled = False
        self.board_height_label.enabled = False
        self.board_height_input.enabled = False
        self.resume_button.enabled = False
        self.quit_button.enabled = False

        self.reset_game()
    
    def reset_game(self):
        destroy(self.snake.head)
        destroy(self.snake.tongue)
        destroy(self.snake.left_eye)
        destroy(self.snake.right_eye)
        for segment in self.snake.tail:
            destroy(segment)
        destroy(self.food.entity)
        destroy(self.food.stem)

        for wall in self.walls:
            destroy(wall.entity)

        self.walls = []
        self.create_walls()

        self.snake.create()
        self.snake.current_direction = Vec2(0, 0)  # Reset current direction
        self.snake.next_direction = Vec2(0, 0)  # Reset next direction
        self.food.create()
        self.snake.tail = []
        self.score = 0
        self.level = 1
        score_text.text = f"Score: {self.score}"
        level_text.text = f"Level: {self.level}"

if __name__ == '__main__':
    load_config()

    app = Ursina()

    score_text = Text(text="Score: 0", position=(-0.5, 0.5), scale=2, color=color.white)
    level_text = Text(text="Level: 1", position=(0.2, 0.5), scale=2, color=color.white)
    high_score_text = Text(text=f"High Score: {HIGH_SCORE}", position=(-0.25, -0.45), scale=2, color=color.white)

    window.title = "Snake Game"
    window.position = Vec2(192, 108)
    window.borderless = False
    window.fullscreen = False
    window.exit_button.visible = False
    window.fps_counter.enabled = False
    window.entity_counter.enabled = False
    window.collider_counter.enabled = False

    camera.orthographic = True
    # Dynamically adjust camera's field of view to fit the entire game board
    # including the walls, based on the board's dimensions and the window's aspect ratio
    # Set the camera's fov to frame the board including the walls
    window_aspect_ratio = window.size[0] / window.size[1]
    camera.fov = max(BOARD_WIDTH * GRID_SIZE + WALL_THICKNESS * 2, BOARD_HEIGHT * GRID_SIZE + WALL_THICKNESS * 2) / window_aspect_ratio

    game = Game()
    snake = game.snake
    food = game.food

    game.create_walls()
    game.create_pause_menu()
    snake.create()
    food.create()

    app.run()
