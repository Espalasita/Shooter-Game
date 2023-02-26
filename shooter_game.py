#Create your own shooter
from pygame import *
from random import randint
from time import time as timer

#background
window = display.set_mode((700,500))
display.set_caption("Catch")
background = transform.scale(
        image.load('galaxy.jpg'),
        (700,500)
    )
win_width = 700

#sound
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
missed = 0
score = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x = 65, size_y = 65):
        super().__init__()
        self.image=transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 10, 20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >=500:
            self.rect.y = 0
            self.rect.x = randint(0,640)
            self .speed = randint(1,3)
            missed += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,640)
            self .speed = randint(1,3)

font.init()
font1 = font.Sysfont('Arial', 70)
font2 = font.Sysfont('Arial',36)
font3 = font.Sysfont('Arial',70)
lose = font1.render('YOU LOSE!', True, (255,215, 0))
win = font3.render('YOU WIN!', True, (255,215,0))






game=True
FPS = 60
clock=time.Clock()

rocket = Player("rocket.png",50,435,5)
monsters = sprite.Group()
for i in range(5):
    ufo = Enemy("ufo.png", randint(0,640), 0,randint(1,3))
    monsters.add(ufo)
bullets = sprite.Group()
asteroid = sprite.Group()
for i in range(2):
    rock = Asteroid("asteroid.png", randint(0,640),0,randint(1,3))
    asteroid.add(rock)
    
num_fire = 0
rel_time = False
Finish = False
while game:
    for e in event.get():
        if e.type==QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    cur_time = timer()
    if Finish == False:
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        for i in sprites_list:
            score += 1
            text_lose1 = font2.render("Score: " + str(score), 1, (255,255,255))
            ufo = Enemy("ufo.png", randint(0,640), 0,randint(1,3))
            monsters.add(ufo)
            window.blit(text_lose1,(10,25))
        window.blit(background,(0,0))

        text_lose = font2.render(
            "Missed: " + str(missed), 1, (255,255,255)
            )
        window.blit(text_lose,(10,50))
        text_lose1 = font2.render(
            "Score: " + str(score), 1, (255,255,255)
            )
        if sprite.spritecollide(rocket, monsters, False):
            window.blit(lose,(200,200))
            Finish = True
        if sprite.spritecollide(rocket, asteroid, False):
            window.blit(lose,(200,200))
            Finish = True
        if score == 10:
            window.blit(win,(200,200))
            Finish = True
        if missed == 10:
            window.blit(lose,(200,200))
            Finish = True
        if rel_time == True:
            cur_time2 = timer()
            if cur_time2 - cur_time < 3:
                reload = font1.render('Wait, Reload.',1,(255,255,255))
                window.blit(reload,(200,200))
            else: 
                num_fire = 0
                rel_time = False


        window.blit(text_lose1,(10,25))
        rocket.update()
        rocket.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroid.update()
        asteroid.draw(window)
        display.update()
        clock.tick(FPS)



