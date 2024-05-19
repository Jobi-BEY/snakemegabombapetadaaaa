from pygame import *
from random import randint, choice
class GameSprite(sprite.Sprite):
    def __init__(self,img,x,y,w,h,speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.rect.w = w
        self.rect.h = h
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Food(GameSprite):
    def __init__(self,img,x,y,w,h,speed):
        super().__init__(img,x,y,w,h,speed)
        self.images = list()
        self.images.append(self.image)
    def add_image(self, img):
        w = self.rect.width
        h = self.rect.height
        new_image = transform.scale(image.load(img), (w,h))
        self.images.append(new_image)
    def new_position(self):
        self.rect.x = randint(5,375-5-self.rect.width)
        self.rect.y = randint(5,375-5-self.rect.height)
        self.image = choice(self.images)
class Snake(GameSprite):
    def __init__(self,img,x,y,w,h,speed):
        super().__init__(img,x,y,w,h,speed)
        self.images = list()
        self.images.append(self.image)
        for i in range(3):
            self.image = transform.rotate(self.image, 90)
            self.images.append(self.image)
    def update(self, direction):
        if direction == 'left':
            self.rect.x -= self.speed
            self.image = self.images[1]
        if direction == 'right':
            self.rect.x += self.speed
            self.image = self.images[3]
        if direction == 'down':
            self.rect.y += self.speed
            self.image = self.images[2]
        if direction == 'up':
            self.rect.y -= self.speed
            self.image = self.images[0]
window = display.set_mode((375,375))
display.set_caption('saveEcoCity')
background = transform.scale(image.load('fonsnake.png'),(375,375))
my_food = Food('gepl.png', 100,100,25,25,0)
my_food.add_image('orage.png')
clock = time.Clock()
head = Snake('hed.png',175, 175, 25, 25, 3)
tale = Snake('body.png', -100, -100,25,25,0)
snake = [head]

FPS = 60
eat = 0
finish = False
game = True
direction = 'stop'
while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_q:
            my_food.new_position()
        if e.type == KEYDOWN:
            if e.key == K_w:
                direction = 'up'
            if e.key == K_s:
                direction = 'down'
            if e.key == K_a:
                direction = 'left'
            if e.key == K_d:
                direction = 'right'
    if finish != True:
        if head.rect.x>350 or head.rect.x<0:
            finish = True
        if head.rect.y>350 or head.rect.y<0:
            finish = True
        if head.rect.colliderect(my_food.rect):
            my_food.new_position()
            eat += 1
            tale.rect.x = head.rect.x
            tale.rect.y = head.rect.y
            snake.append(tale)
        window.blit(background,(0,0))
        my_food.reset()
        head.update(direction)
        head.reset()
        for i in range(len(snake)-1, 0, -1):
            snake[i].rect.x = snake[i-1].rect.x
            snake[i].rect.y = snake[i-1].rect.y
            snake[i].reset()

        head.update(direction)
        head.reset()
    display.update()
    clock.tick(FPS)