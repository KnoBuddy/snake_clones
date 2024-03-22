import pygame
import random

class PowerUp:
    def __init__(self, game):
        self.game = game
        self.x = random.randint(0, self.game.width - 20)
        self.y = random.randint(0, self.game.height - 20)
        self.type = random.choice(['speed', 'shield', 'multiplier'])
        self.color = (255, 0, 255)
        self.duration = 5  # seconds

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, (self.x, self.y, 20, 20))

    def apply(self, snake):
        if self.type == 'speed':
            snake.speed *= 1.5
        elif self.type == 'shield':
            snake.shield = True
        elif self.type == 'multiplier':
            self.game.score_manager.multiplier = 2

    def deactivate(self, snake):
        if self.type == 'speed':
            snake.speed /= 1.5
        elif self.type == 'shield':
            snake.shield = False
        elif self.type == 'multiplier':
            self.game.score_manager.multiplier = 1

class Obstacle:
    def __init__(self, game):
        self.game = game
        self.x = random.randint(0, self.game.width - 20)
        self.y = random.randint(0, self.game.height - 20)
        self.color = (255, 255, 255)

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, (self.x, self.y, 20, 20))

    def check_collision(self, snake):
        if snake.x == self.x and snake.y == self.y:
            return True
        return False

class ClassicMode:
    def __init__(self, game):
        self.game = game

    def update(self):
        self.game.handle_input()
        game_over = self.game.update()
        self.game.draw()
        return game_over

class TimeAttackMode:
    def __init__(self, game):
        self.game = game
        self.time_limit = 60  # seconds
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.game.handle_input()
        game_over = self.game.update()
        self.game.draw()
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        if elapsed_time >= self.time_limit:
            game_over = True
        return game_over

class SurvivalMode:
    def __init__(self, game):
        self.game = game
        self.lives = 3

    def update(self):
        self.game.handle_input()
        game_over = self.game.update()
        if game_over:
            self.lives -= 1
            if self.lives == 0:
                game_over = True
            else:
                self.game.reset()
        self.game.draw()
        return game_over

class AnimationManager:
    def __init__(self, game):
        self.game = game

    def animate_eat(self, x, y):
        # Particle effects when the snake eats the food
        pass

    def animate_game_over(self):
        # Animated transition for game over
        pass

    def animate_level_complete(self):
        # Animated transition for level complete
        pass

    def update_background(self):
        # Dynamic background based on score or level
        pass

class Player:
    def __init__(self, game, x, y, color):
        self.game = game
        self.snake = Snake(x, y, 1)
        self.color = color

    def handle_input(self, keys):
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.snake.direction != 'DOWN':
            self.snake.direction = 'UP'
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.snake.direction != 'UP':
            self.snake.direction = 'DOWN'
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.snake.direction != 'RIGHT':
            self.snake.direction = 'LEFT'
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.snake.direction != 'LEFT':
            self.snake.direction = 'RIGHT'

    def update(self):
        self.snake.move()
        if self.snake.check_collision(self.game.width, self.game.height):
            print("Collided with the wall. Game Over!")
            return True
        if self.snake.check_self_collision():
            print("Collided with itself. Game Over!")
            return True
        return False

    def draw(self):
        for segment in self.snake.body:
            pygame.draw.rect(self.game.screen, self.color, (segment[0], segment[1], 20, 20))

class Snake:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.body = [(x, y)]
        self.direction = 'RIGHT'
        self.speed = 20
        self.shield = False

    def move(self):
        if self.direction == 'UP':
            self.y -= self.speed
        elif self.direction == 'DOWN':
            self.y += self.speed
        elif self.direction == 'LEFT':
            self.x -= self.speed
        elif self.direction == 'RIGHT':
            self.x += self.speed

        self.body.insert(0, (self.x, self.y))
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def check_collision(self, width, height):
        if self.shield:
            return False
        if self.x < 0 or self.x >= width or self.y < 0 or self.y >= height:
            return True
        return False

    def check_self_collision(self):
        if self.shield:
            return False
        for segment in self.body[1:]:
            if self.x == segment[0] and self.y == segment[1]:
                return True
        return False

class Food:
    def __init__(self, game):
        self.game = game
        self.spawn()

    def spawn(self):
        self.x = round(random.randrange(0, self.game.width - 20) / 20) * 20
        self.y = round(random.randrange(0, self.game.height - 20) / 20) * 20
        self.type = random.choice(['normal', 'bonus'])
        self.color = (0, 255, 0) if self.type == 'normal' else (255, 255, 0)
        self.points = 1 if self.type == 'normal' else 3

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, (self.x, self.y, 20, 20))

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.players = []
        self.food = Food(self)
        self.score_manager = ScoreManager(self)
        self.obstacles = []
        self.power_ups = []
        self.animation_manager = AnimationManager(self)
        self.game_mode = None
        self.start_screen = StartScreen(self)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.handle_input(keys)

    def update(self):
        for player in self.players:
            if player.update():
                return True
            if player.snake.x == self.food.x and player.snake.y == self.food.y:
                player.snake.grow()
                self.score_manager.increase_score(self.food.points)
                self.food.spawn()
                self.animation_manager.animate_eat(self.food.x, self.food.y)
                print(f"Food eaten. New food position: ({self.food.x}, {self.food.y})")

        for obstacle in self.obstacles:
            for player in self.players:
                if obstacle.check_collision(player.snake):
                    print("Collided with an obstacle. Game Over!")
                    return True

        for power_up in self.power_ups:
            for player in self.players:
                if player.snake.x == power_up.x and player.snake.y == power_up.y:
                    power_up.apply(player.snake)
                    self.power_ups.remove(power_up)
                    break

        return False

    def draw(self):
        self.screen.fill((0, 0, 0))
        for player in self.players:
            player.draw()
        self.food.draw()
        for obstacle in self.obstacles:
            obstacle.draw()
        for power_up in self.power_ups:
            power_up.draw()
        self.score_manager.display()
        self.animation_manager.update_background()
        pygame.display.update()

    def increase_difficulty(self):
        if self.score_manager.level % 5 == 0:
            self.obstacles.append(Obstacle(self))
        if self.score_manager.level % 10 == 0:
            self.power_ups.append(PowerUp(self))

    def reset(self):
        self.players = [Player(self, self.width // 4, self.height // 2, (0, 255, 0)),
                        Player(self, self.width // 4 * 3, self.height // 2, (255, 0, 0))]
        self.food.spawn()
        self.score_manager.reset()
        self.obstacles = []
        self.power_ups = []

    def run(self):
        self.start_screen.display()
        self.game_mode = self.start_screen.select_mode()

        while True:
            if isinstance(self.game_mode, ClassicMode):
                game_over = self.game_mode.update()
            elif isinstance(self.game_mode, TimeAttackMode):
                game_over = self.game_mode.update()
            elif isinstance(self.game_mode, SurvivalMode):
                game_over = self.game_mode.update()

            if game_over:
                self.animation_manager.animate_game_over()
                break

            self.increase_difficulty()
            self.clock.tick(10)

        pygame.quit()
        quit()

class StartScreen:
    def __init__(self, game):
        self.game = game

    def display(self):
        self.game.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Select Game Mode:", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.game.width // 2, self.game.height // 4))
        self.game.screen.blit(text, text_rect)

        classic_text = font.render("1. Classic Mode", True, (255, 255, 255))
        classic_rect = classic_text.get_rect(center=(self.game.width // 2, self.game.height // 4 * 2))
        self.game.screen.blit(classic_text, classic_rect)

        time_attack_text = font.render("2. Time Attack Mode", True, (255, 255, 255))
        time_attack_rect = time_attack_text.get_rect(center=(self.game.width // 2, self.game.height // 4 * 2.5))
        self.game.screen.blit(time_attack_text, time_attack_rect)

        survival_text = font.render("3. Survival Mode", True, (255, 255, 255))
        survival_rect = survival_text.get_rect(center=(self.game.width // 2, self.game.height // 4 * 3))
        self.game.screen.blit(survival_text, survival_rect)

        pygame.display.update()

    def select_mode(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return ClassicMode(self.game)
                    elif event.key == pygame.K_2:
                        return TimeAttackMode(self.game)
                    elif event.key == pygame.K_3:
                        return SurvivalMode(self.game)

class ScoreManager:
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.level = 1
        self.multiplier = 1

    def increase_score(self, points):
        self.score += points * self.multiplier
        if self.score >= self.level * 10:
            self.level += 1
            self.game.increase_difficulty()
            self.game.animation_manager.animate_level_complete()

    def reset(self):
        self.score = 0
        self.level = 1
        self.multiplier = 1

    def display(self):
        font = pygame.font.Font(None, 24)
        text = font.render(f"Score: {self.score}  Level: {self.level}  Multiplier: {self.multiplier}x", True, (255, 255, 255))
        self.game.screen.blit(text, (10, 10))

if __name__ == '__main__':
    game = Game(1280, 720)
    game.run()
