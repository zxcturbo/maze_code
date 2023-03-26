from pygame import *

window = display.set_mode((700,500))
display.set_caption('очень крутое название')
clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (60,60))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

x1 = 46
y1 = 305      

class Player(GameSprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__(player_image, player_speed, player_x, player_y)
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 3:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 410:
            self.rect.y += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 3:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    

class Enemy(GameSprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__(player_image, player_speed, player_x, player_y)
        self.move = 'право'
    def update(self):
        # keys_pressed = key.get_pressed()
        if self.rect.x <= 490:
            self.move = 'право'
        if self.rect.x >= 630:
            self.move = 'лево'
        
        if self.move == 'лево':
            self.rect.x -= self.speed
        if self.move == 'право':
            self.rect.x += self.speed
        
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_width,wall_height, wall_x, wall_y ):
        super().__init__()
        self.color1 = color_1
        self.color2 = color_2
        self.color3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color1, self.color2, self.color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

background = transform.scale(image.load('background.jpg'), (700,500))
screamer = transform.scale(image.load('screamer.jpg'), (700,500))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')
# bu = mixer.Sound('gdfgdgf.ogg')
game = True
finish = False

hero = Player("hero.png", 5, 46, 305)
enemy = Enemy('cyborg.png', 4, 490, 280)
treasure = GameSprite('treasure.png', 0,580,40)

w1 = Wall(0,250,30,10,370,170,5)
w2 = Wall(0,250,30,370,10,170,450)
w3 = Wall(0,250,30,10,370,310,90)
w4 = Wall(0,250,30,10,370,480,5)
w5 = Wall(0,250,30,90,10,390,160)
w6 = Wall(0,250,30,90,10,390,330)
w7 = Wall(0,250,30,90,10,310,245)


hp = 3

font.init()
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN!', True, (255,215,0))
lose = font.render("YOU LOSE!", True, (255,0,0))

while game:
    heal_point = font.render("HP: " + str(hp), True, (255,0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0,0))
        hero.reset()
        hero.update()
        window.blit(heal_point,(0,0))
        if sprite.collide_rect(hero, treasure):
            finish = True
            mixer.music.stop()
            money.play()
            window.blit(win, (200,200))
        if hp != 0:
            if (sprite.collide_rect(hero, enemy) or 
            sprite.collide_rect(hero, w1) or
            sprite.collide_rect(hero, w2) or
            sprite.collide_rect(hero, w3) or
            sprite.collide_rect(hero, w4) or
            sprite.collide_rect(hero, w5) or
            sprite.collide_rect(hero, w6) or
            sprite.collide_rect(hero, w7)):
                hero.rect.x = 46
                hero.rect.y = 305
                hp -=1
                print(hp)
                kick.play()
                
        else:
            mixer.music.stop()
            finish = True
            # bu.play()
            # window.blit(screamer, (0,0))
            window.blit(lose, (200,200))    
            
        
        enemy.reset()
        enemy.update()
        treasure.reset()
        w1.reset()
        w2.reset()
        w3.reset()
        w4.reset()
        w5.reset()
        w6.reset()
        w7.reset()
        clock.tick(FPS)
        display.update()