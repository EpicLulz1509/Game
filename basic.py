import pygame
import time

pygame.init()
border_x = 1920
border_y = 1080
win = pygame.display.set_mode((border_x,border_y))
pygame.display.set_caption("First game")

clock = pygame.time.Clock()

walkRight = [pygame.image.load('Sprites\\r2.png'), pygame.image.load('Sprites\\r3.png'), pygame.image.load('Sprites\\r4.png'), pygame.image.load('Sprites\\r1.png'), pygame.image.load('Sprites\\r2.png'), pygame.image.load('Sprites\\r3.png'), pygame.image.load('Sprites\\r4.png'), pygame.image.load('Sprites\\r1.png'), pygame.image.load('Sprites\\r2.png')]
walkLeft = [pygame.image.load('Sprites\\l2.png'), pygame.image.load('Sprites\\l3.png'), pygame.image.load('Sprites\\l4.png'), pygame.image.load('Sprites\\l1.png'), pygame.image.load('Sprites\\l2.png'), pygame.image.load('Sprites\\l3.png'), pygame.image.load('Sprites\\l4.png'), pygame.image.load('Sprites\\l1.png'), pygame.image.load('Sprites\\l1.png')]
bg = pygame.image.load('Sprites\\bdkg.png')
char = [pygame.image.load('Sprites\\r1.png'), pygame.image.load('Sprites\\l1.png'), pygame.image.load('Sprites\\exp.png')]
moveProj = [pygame.image.load('Sprites\\p1.png'), pygame.image.load('Sprites\\p2.png'), pygame.image.load('Sprites\\p3.png')]
enemyWalkRight = [pygame.image.load('Sprites\\er1.png'), pygame.image.load('Sprites\\er2.png'), pygame.image.load('Sprites\\er3.png'), pygame.image.load('Sprites\\er4.png'), pygame.image.load('Sprites\\er5.png'), pygame.image.load('Sprites\\er6.png')]
enemyWalkLeft = [pygame.image.load('Sprites\\el1.png'), pygame.image.load('Sprites\\el2.png'), pygame.image.load('Sprites\\el3.png'), pygame.image.load('Sprites\\el4.png'), pygame.image.load('Sprites\\el5.png'), pygame.image.load('Sprites\\el6.png')]

bulletSound = pygame.mixer.Sound('Music\\shoot.wav')
screamSound = pygame.mixer.Sound('Music\\scream.wav')
crySound = pygame.mixer.Sound('Music\\cry.wav')
musicTheme = pygame.mixer.music.load('Music\\theme.mp3')
pygame.mixer.music.play(-1)


score = 0

class Player():
    def __init__(self):
        self.x = 574
        self.y = 795
        self.width = 30
        self.height = 60
        self.vel = 10
        self.left = False
        self.right = False
        self.isJump = False
        self.health = 10
        self.jumpCount = 10
        self.walkCount = 0
        self.count = 1
        self.hitbox = (self.x+20, self.y, 80, 180)
        
    def draw(self, win):
        if self.walkCount >= 32:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount//4], (self.x,self.y))
            self.walkCount += 1
            self.left = False
            self.count = 0
        elif self.right:
            win.blit(walkRight[self.walkCount//4], (self.x,self.y))
            self.walkCount += 1
            self.right = False
            self.count = 1
        else:
            if(self.count == 1):    
                win.blit(char[0], (self.x,self.y))
            elif(self.count == 0):    
                win.blit(char[1], (self.x,self.y))
        
        self.hitbox = (self.x+10, self.y, 80, 180)
        if self.health > 6:
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 100 - (10 * (10-self.health)) + 1, 20))
        elif self.health > 3 and self.health <= 6:
            pygame.draw.rect(win, (255,255,0), (self.hitbox[0], self.hitbox[1] - 20, 100 - (10 * (10-self.health)) + 1, 20))
        else:
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 100 - (10 * (10-self.health)) + 1, 20))
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.x = 100
        self.walkCount = 0
        self.health -= 4
        font1 = pygame.font.SysFont('comicsans', 200)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (960 - (text.get_width()/2), 540 - (text.get_height()/2)))
        pygame.display.update()
        pygame.time.delay(1000)
        boxer.health += 5
        

class Projectile():
    def __init__(self, x, y, facing, vel):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 2 * facing * vel

    def draw(self, win):
        if self.facing == 1:
            win.blit(moveProj[1], (self.x,self.y))
        elif self.facing == -1:
            win.blit(moveProj[2], (self.x,self.y))
        # pygame.draw.circle(win, (0,0,0), (self.x,self.y), 20)


class Enemy():
    def __init__(self):
        self.x = 100
        self.y = 795
        self.width = 30
        self.height = 60
        self.end = 1800
        self.path = [self.x, self.end]
        self.vel = 5    
        self.walkCount = 0
        self.hitbox = (self.x+20, self.y, 100, 180)
        self.health = 10
        self.visible = True
    
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount >= 24:
                self.walkCount = 0
            if self.vel < 0:
                win.blit(enemyWalkLeft[self.walkCount//4], (self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(enemyWalkRight[self.walkCount//4], (self.x,self.y))
                self.walkCount += 1
                
            self.hitbox = (self.x+20, self.y, 100, 180)
            if self.health > 6:
                pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 100 - (10 * (10-self.health)) + 1, 20))
            elif self.health > 3 and self.health <= 6:
                pygame.draw.rect(win, (255,255,0), (self.hitbox[0], self.hitbox[1] - 20, 100 - (10 * (10-self.health)) + 1, 20))
            else:
                pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 100 - (10 * (10-self.health)) + 1, 20))
            # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
    
    def hit(self, win):
        if self.health > 0:
            # win.blit(moveProj[1], (self.x + self.width, self.y + self.height/2))
            self.health -= 1
        else:
            self.visible = False
        print("hit")
        
    def move(self):
        if self.vel > 0:
            if self.x < self.vel + self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

        



def gameWindow():
    win.blit(bg, (0,0))
    text = font.render(f'Score: {score}', 1, (0,0,0))
    win.blit(text, (1700, 10))
    man.draw(win) 
    boxer.draw(win)   
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update() 



font = pygame.font.SysFont("Segoe UI", 50, True)
man = Player()
bullets = []
shootCount = 0
boxer = Enemy()

#main loop
running = True
while running:
    # pygame.time.delay(100) 
    clock.tick(32)

    if boxer.visible == True:
        if man.hitbox[1] < boxer.hitbox[1] + boxer.hitbox[3] and man.hitbox[1] + man.hitbox[3] > boxer.hitbox[1]:
            if man.hitbox[0] < boxer.hitbox[0] + boxer.hitbox[2] and man.hitbox[0] + man.hitbox[2] > boxer.hitbox[0]:
                crySound.play()
                man.hit()
                score -= 5
                # bullets.pop(bullets.index(bullet))

    if shootCount > 0:
        shootCount += 1
    if shootCount > 3:
        shootCount = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
            if bullet.y < boxer.hitbox[1] + boxer.hitbox[3] and bullet.y > boxer.hitbox[1]:
                if bullet.x < boxer.hitbox[0] + boxer.hitbox[2] and bullet.x > boxer.hitbox[0]:
                    screamSound.play()
                    boxer.hit(win)
                    score += 1
                    bullets.pop(bullets.index(bullet))

            if bullet.x < 1920 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.left = True
        man.right = False
        man.x -= man.vel
    if keys[pygame.K_RIGHT] and man.x < border_x - man.width - man.vel:
        man.left = False
        man.right = True
        man.x += man.vel

    if not(man.isJump):
        # if keys[pygame.K_UP] and y > vel:
        #     y -= vel
        # if keys[pygame.K_DOWN] and y < border_y - height - vel:
        #     y += vel
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -=  man.jumpCount ** 2 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    if keys[pygame.K_SPACE] and shootCount == 0:
        bulletSound.play()
        shootCount = 1
        facing = 1
        if(man.count == 0):
            facing = -1
        else:
            facing = 1
        if(len(bullets) < 5):
            bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.height//2), facing, man.vel))


    gameWindow()


pygame.quit()