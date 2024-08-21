from pygame import *
from pygame.sprite import Sprite, Group, spritecollide, groupcollide
from random import *
from time import time as timer

Window_size = (700, 500)

window = display.set_mode(Window_size)
display.set_caption("rocket shooting alien's UFO simulator(unrealistic)")



class Gamesprite(Sprite):
    def __init__(self, image_path, image_size, x, y):
        super().__init__()
        self.image = transform.scale(image.load(image_path), image_size)
        self.rect = self.image.get_rect(topleft=(x,y))
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    

class Player(Gamesprite):
    def update(self):
        
        key_pressed=key.get_pressed()
#        print(key_pressed[K_a])
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x-=10
        if key_pressed[K_d] and self.rect.x < Window_size[0]-size[0]:
            self.rect.x+=10
        
#        if key_pressed[K_SPACE] :
#            delay_burst = timer()
#            if timer() - delay_burst > 0.1:
#                self.fire()
#                pew_pew.play()
#                delay_burst = timer()
        
    def fire(self):
        bullets.add(Bullet("bullet.png", bullet_size, player.rect.x + 21, player.rect.y + 20))

class Enemy(Gamesprite):
    def __init__(self, image_path, image_size, x, y, speed):
        super().__init__(image_path, image_size, x, y)
        self.speed = speed
    def update(self):
        self.rect.y += self.speed
        global missed_score
 
        
            
    
        if self.rect.y > Window_size[1]:
            self.rect.y = 0
            self.rect.x = randint(0, 635)
            missed_score +=1

class Bullet(Gamesprite):
    def update(self):
        self.rect.y -= 100
        if self.rect.y < 0:
            self.rect.x = 1000
            self.kill()
            print("hilang gw")
#        if self.rect.colliderect(enemies.rect):
#            self.kill()


def callback_enemy():
    return True



size = (85, 100)
bullet_size = (20, 20)

player = Player("F15jet.png", size, 500, 400)
back = Gamesprite("light blue back.png", Window_size, 0, 0)
enemy = Enemy("F15jet - Copy.png", size, randint(300, 500), 0, randint(2, 6))

mixer.init()
mixer.music.load("0807.wav")
mixer.music.play()

pew_pew = mixer.Sound("fire.ogg")

FPS =60

bullets = Group()
bullet = Bullet("bullet.png", bullet_size, player.rect.x, player.rect.y)


font.init()
font1 = font.Font(None, 40)
font2 = font.Font(None, 46)
font_BIG = font.Font(None, 70)

win = font_BIG.render("YOU WIN", True, (0, 255, 0))
lose = font_BIG.render("YOU LOSE", True, (255, 0, 0))

enemies = Group()

enemies.add(Enemy("F15jet - Copy.png", size, randint(300, 500), 0, randint(5,10)))

game_STATUS = True

clock =time.Clock()

now = timer()

missed_score=0
shooted_down=0

inactive = False
while game_STATUS:
    for e in event.get():
        if e.type == QUIT:
            game_STATUS =False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                pew_pew.play()
                print("pew")
                player.fire()
                
    if not inactive:
        back.reset()

    #    bullet.reset()
    #    bullet.update()
        bullets.draw(window)
        bullets.update()

    
        player.reset()
    #    enemy1.reset()
        player.update()
    #    enemy1.update()

        enemies.draw(window)
        enemies.update()

        if spritecollide(player, enemies, False) or missed_score == 3:
            inactive = True
            window.blit(lose, (350, 250))
        
        if timer() - now > 2:
            enemies.add(Enemy("F15jet - Copy.png", size, randint(0, 500), 0, randint(5,10)))
            now = timer()
        if groupcollide(bullets, enemies, True, True):
            shooted_down += 1
            print(timer() - now)
            if timer() - now > 1:
                enemies.add(Enemy("F15jet - Copy.png", size, randint(0, 500), 0, randint(5,10)))
            if shooted_down == 10:
                inactive =True
                window.blit(win, (350, 250))

        TARGET_DESTROYED = font2.render("Hit:", True, (255, 0, 0))
        window.blit(TARGET_DESTROYED, (0, 23))
        TARGET_DESTROYED2 = font2.render("Hit:", True, (255, 0, 0))
        window.blit(TARGET_DESTROYED2, (0, 24))
        Hit = font1.render(f"Hit: {shooted_down}", True, (255, 255, 255))
        window.blit(Hit, (2.5, 25))
        Missed = font1.render(f"Missed: {missed_score}", True, (255, 0, 0))
        window.blit(Missed, (0, 65))

       


            




    display.update()
    clock.tick(FPS)




