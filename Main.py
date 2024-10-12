import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (0, 0,0)
class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE # define the window size like(1000,520) so divide 1000/40
        self.y = random.randint(1,12)*SIZE

class Snake:
    def __init__(self,parent_screen, length):
        self.parent_screen = parent_screen
        self.block =pygame.image.load("resources/block.jpg").convert() # loading an image to the program
        self.direction = 'down'
        self.length = length
        self.x = [SIZE]*length
        self.y = [SIZE]*length

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)


    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'


    def walk(self):
        # this for loop is for reversed direction
        for i in range(self.length-1, 0, -1): # -1 for length, it will not consider 0 it will go till 1 and last -1 is for step size
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        self.draw()


# defining to create/drawing a new block
    def draw(self):
        # self.parent_screen.fill(BACKGROUND_COLOR)  # if we run the code without this line then blocks will, but it will not delete the previous blocks

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i]))  # blit means drawing or placing an image at the screen while 100,100 represents the x,y coordinates position
        pygame.display.flip()  # we can use update() instead of flip(), it updates the screen


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Classical Snake and Apple Game")

        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 520))  # screen size and surface == background
        self.surface.fill((1, 1, 1))  # choosing color
        self.snake = Snake(self.surface,1)
        self.snake.draw() # initializing snake
        self.apple = Apple(self.surface)
        self.apple.draw() # initializing apple

    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding apple logic
        if self.is_collision(self.snake.x[0],self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself logic
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

        # snake colliding with wall
        if not (0<= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0]<=520):
            self.play_sound("crash")
            raise "Hit the boundary"

    def display_score(self):
        font = pygame.font.SysFont('aria',30)
        score = font.render(f'score:{self.snake.length}',True,(250,250,250))
        self.surface.blit(score,(510,10)) # placing something at the surface


    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('aria',30)
        line1 = font.render(f'score:{self.snake.length}',True,(250,250,250))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play the game again press ENTER. To exit press ESCAPE.",True,(250,250,250))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        # this while loop define the functionality of closing the Prompt window from the (X) bar at top
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:  # up and down movement is for y-axis
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:  # while left and right is for x-axis
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()


                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.1)

if __name__ == "__main__":
    game = Game()
    game.run()