import pygame
import os
import random
pygame.init()

S = pygame.display.set_mode((1100,600))
pygame.display.set_caption("CATCH ME IF U CAN")
# for music mixer is imported
from pygame import mixer
mixer.music.load('music.mp3')
mixer.music.play(-1)

back_ground = pygame.image.load(os.path.join("Track.png"))
CLOUD = pygame.image.load(os.path.join("cloud.jpg"))
RUN = [pygame.image.load(os.path.join("nobitha 2.jpg")),
           pygame.image.load(os.path.join("1.png"))]
JUMP = pygame.image.load(os.path.join("2.png"))
DUCK = [pygame.image.load(os.path.join("Nobyrollerskates-removebg-preview.png")),
           pygame.image.load(os.path.join("Nobyrollerskates-removebg-preview.png"))]

SMALL = [pygame.image.load(os.path.join("Teacher_nobitha (2).jpg")),

                pygame.image.load(os.path.join("topper_prev_ui.png")),
                pygame.image.load(os.path.join("nobithamom.jpg"))]
LARGE= [pygame.image.load(os.path.join("geyan.jpg")),
                pygame.image.load(os.path.join("playground uncle.jpg")),
                pygame.image.load(os.path.join("sunio.jpg"))]

DORA= [pygame.image.load(os.path.join("doramon 1.png")),
        pygame.image.load(os.path.join("doramon 1.png"))]

def main():
    # back ground position of x,y co ordinates
    global game_speed, x_pos_bg, y_pos_bg
    global dora_characters
    global points
    run = True

    clock = pygame.time.Clock()
    player = Nobita()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 400


    points = 0

    font = pygame.font.Font('freesansbold.ttf', 20)

    dora_characters = []
    
    collision = 0

    def score():
        global points, game_speed
        points += 1
        if points %80 == 0:
            game_speed += 1
# import os
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        S.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        
        
        image_width = back_ground.get_width()
        S.blit(back_ground, (x_pos_bg, y_pos_bg))
        S.blit(back_ground, (image_width + x_pos_bg, y_pos_bg))


        if x_pos_bg <= -image_width:
            S.blit(back_ground, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        S.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()

        player.draw(S)
        player.update(user_input)

        if len(dora_characters) == 0:
            if random.randint(0, 2) == 0:
                dora_characters.append(Small(SMALL))
            elif random.randint(0, 2) == 1:
                dora_characters.append(Large(LARGE))
            elif random.randint(0, 2) == 2:
                dora_characters.append(Dora(DORA))

        for obstacle in dora_characters:
            obstacle.draw(S)
            
            obstacle.update()
            if player.nobita_rect.colliderect(obstacle.rect):
                pygame.time.delay(150)
                collision += 1
                menu(collision)

        background()

        cloud.draw(S)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

class Nobita:
    xcod_nobita = 100
    ycod_nobita = 310
    ycod_duck_nobita = 390
    jumpspeed = 12

    def __init__(self):
        self.duckingimage = DUCK
        self.runningimage = RUN
        self.jumpingimage = JUMP

        self.nobita_duck = False
        self.nobita_run = True
        self.nobita_jump = False

        self.initial_index = 0
        self.jump_vel = self.jumpspeed
        self.image = self.runningimage[0]
        self.nobita_rect = self.image.get_rect()
        self.nobita_rect.x = self.xcod_nobita
        self.nobita_rect.y = self.ycod_nobita

    def update(self, user_input):
        
        if self.nobita_run:
            self.run()
        if self.nobita_jump:
            self.jump()
        if self.nobita_duck:
            self.duck()

        if self.initial_index >= 10:
            self.initial_index = 0

        if user_input[pygame.K_UP] and not self.nobita_jump:

        
            self.nobita_run = False
            self.nobita_jump = True
            self.nobita_duck = False

            
        elif user_input[pygame.K_DOWN] and not self.nobita_jump:
            
            self.nobita_run = False
            self.nobita_jump = False
            self.nobita_duck = True

        elif not (self.nobita_jump or user_input[pygame.K_DOWN]):
            
            self.nobita_run = True
            self.nobita_jump = False
            self.nobita_duck = False

    
    def run(self):
        self.image = self.runningimage[self.initial_index // 5]
        self.nobita_rect = self.image.get_rect()
        self.nobita_rect.x = self.xcod_nobita
        self.nobita_rect.y = self.ycod_nobita
        self.initial_index += 1

    def jump(self):
        self.image = self.jumpingimage
        if self.nobita_jump:
            self.nobita_rect.y -= self.jump_vel * 4
            self.jump_vel -= 1
        if self.jump_vel < - self.jumpspeed:
            self.nobita_jump = False
            self.jump_vel = self.jumpspeed

    def duck(self):
        self.image = self.duckingimage[self.initial_index // 5]

        self.nobita_rect = self.image.get_rect()

        self.nobita_rect.x = self.xcod_nobita

        self.nobita_rect.y = self.ycod_duck_nobita

        self.initial_index += 1


    def draw(self, S):
        S.blit(self.image, (self.nobita_rect.x, self.nobita_rect.y))


class Cloud:
    def __init__(self):
        self.x = 1100 + random.randint(1000,2000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = 1100+ random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, S):
        S.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = 1100

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            dora_characters.pop()

    def draw(self, S):
        S.blit(self.image[self.type], self.rect)


class Small(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 280


class Large(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Dora(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, S):
        if self.index >9:
            self.index = 0
        S.blit(self.image[self.index//5], self.rect)
        self.index += 1



def menu(collision):
    global points
    run = True

    while run:

        S.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 20)

        if collision == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif collision > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (550,350)
            S.blit(score, scoreRect)


        textRect = text.get_rect()
        textRect.center = (550,300)

        S.blit(text, textRect)
        S.blit(RUN[0], (510, 160))
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(collision=0)

# PLZ CHNAGE DEATHCOUNTT O SOME MEANING FU LAND DELETE THIS COMMENT


