#Создай собственный Шутер!

from pygame import *
from random import randint
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(700,500))
window.blit(background,(0,0))
clock = time.Clock()
fps = 60
game = True
finish = False
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 10
            
        if keys_pressed[K_RIGHT]and self.rect.x < 605:
            self.rect.x += 10
            
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15, 20, 15) 
        bullets.add(bullet) 
points = 0
lost = 0             
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(50,650)
            self.rect.y = 0
            global lost
            lost += 1
monsters = sprite.Group()
font.init()
#СДЕЛАЙ ШРИФТ СИСТЕМНЫМ - СМ. 7ОЙ СЛАЙД В ТЕОРИИ
font1 = font.SysFont('Arial', 50)
ladno = font.SysFont('Arial',50)
okay = font.SysFont('Arial',50)
score = font1.render(
    'Счёт:',True, (100,100,0)
)
miss = font1.render(
    'Пропущено:', True, (100,100,0)
)
lose = font1.render(
    'ты проиграл',True, (100,100,0)
)
pobeda = font1.render(
    'ты выиграл',True, (100,100,0)
)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > 500:
            self.kill()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png',randint(50,650),10,80,50,randint(1,6))
    monsters.add(monster)
for i in range(5):
    asteroid = Enemy('asteroid.png',randint(50,650),10,80,50,randint(1,1))
    asteroids.add(asteroid)   


igrok = Player('rocket.png',350,450,80,100,10)
sprites_list = sprite.spritecollide(
    igrok, monsters, False
)
sprites_list = sprite.groupcollide(
    monsters, bullets, True, True
)
sprites_list2 = sprite.spritecollide(
    igrok, asteroids, False
)
sprites_list2 = sprite.groupcollide(
    asteroids, bullets, True, True
)  
mixer.init()
mixer.music.load('space.ogg')
mixer.music.load('fire.ogg')
mixer.music.play()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                igrok.fire()
    sprites_list = sprite.groupcollide(monsters, bullets, True,True)
    sprites_list2 = sprite.groupcollide(asteroids, bullets, True,True)

    for s in sprites_list:
        points += 1
        monster = Enemy('ufo.png',randint(50,650),10,80,50,randint(1,6))
        monsters.add(monster)
    for l in sprites_list2:
        points += 1
        asteroid = Enemy('asteroid.png',randint(50,650),10,80,50,randint(1,6))
        asteroids.add(asteroid)
    if lost >=10:
        window.blit(lose,(100,200))
        finish = True
    if sprite.spritecollide(igrok,monsters, False):
        window.blit(lose,(100,200))
        finish = True

    if sprite.spritecollide(igrok,asteroids, False):
        window.blit(lose,(100,200))
        finish = True    

    if points >=10:
        window.blit(pobeda,(100,200))
        finish = True

    if not finish:
        window.blit(background,(0,0))
        igrok.update()
        igrok.reset()
        
            
            
        kk = ladno.render( str(points),True,(100,100,0))
        gg = okay.render( str(lost),True,(100,100,0))
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        window.blit(gg,(230,50))
        window.blit(kk,(110,20))   
        window.blit(score,(20,20))
        window.blit(miss,(20,50))

    clock.tick(fps)
    display.update()    
       
         