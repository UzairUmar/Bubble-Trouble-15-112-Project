#Name: Uzair Umar
#Andrew ID: mumar
#Milestone 1 code
import pygame, sys
from random import randint
pygame.init()
win = pygame.display.set_mode((688,366))
pygame.display.set_caption("Bubble Trouble")

black=[0,0,0]
white=[255,255,255]
skin = [254,168,119]
grey = (200, 200, 200)

pygame.display.set_caption("Bubble Trouble")
bg = pygame.image.load('level1.jpg')
player = pygame.image.load('player.png')
playerLeft= pygame.image.load('left.png')
walkRight = [pygame.transform.flip(playerLeft,30,0)] #flipping image to make in useful for right movement
walkLeft = [playerLeft]
PlayTime= 25    #time limit for level 1
totalLives = 3      #total Lives for players
lifeImage = pygame.transform.scale(player, (20,20)) #transforming player image to display as a life
ball=pygame.image.load('rball4.png')

clock = pygame.time.Clock()

class Player:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=3
        self.left=False
        self.right=False
        self.walkCount=0

    def shoot(self):
        self.is_active = True
        weapon.update()

    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[0], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[0], (self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(player, (self.x,self.y))
        

class Weapon:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vel=10
    def draw(self,win):
        pygame.draw.line(win,black,(self.x+10,self.y),(self.x+10,self.y+300),4)     #drawing line as a weapon

class Timer:                #class to get and display time
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def draw_timer(self,win):
        CurrentTime=pygame.time.get_ticks()
        CurrentTime = CurrentTime / 1000    #coverting milliseconds to seconds
        time_left = PlayTime - CurrentTime
        time_left= int(time_left)
        font=pygame.font.Font(None,36)
        text=font.render("Time Left:" + str(time_left) ,1,black)
        win.blit(text,(self.x,self.y))

class lives:
    def __init__(self,x,y,totallives):
        self.x= x
        self.y = y
        self.totallives = totallives
    def drawlives(self,win):
        for i in range(self.totallives):
            life_rect= lifeImage.get_rect()
            life_rect.x = self.x+ 30 * i
            life_rect.y = self.y
            win.blit(lifeImage,life_rect)

class Bubble:
    def __init__(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.spd_x = 3
        self.spd_y = 3
    def drawBubble(self,win):
            win.blit(ball,(self.pos_x,self.pos_y)) #displaying bubble image on screen

            self.pos_x+= self.spd_x
            self.pos_y+= self.spd_y

            if(self.pos_y > 310 or self.pos_y < 0):             #checking if bubble hits borders of screen
                self.spd_y= self.spd_y * -1
            if self.pos_x > 630 or self.pos_x < 10:
                self.spd_x = self.spd_x * -1

class Button():
    def __init__(self, txt, location, bg=skin, fg=black, size=(130, 40), font_name="8-Bit-Madness", font_size=18):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)


    def draw(self):
        self.mouseover()

        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surface, self.rect)

    def mouseover(self):            #func to check if mouse is over button
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = grey  # mouseover color


def mousebuttondown():          #func to execute when button is clicked
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            redrawGameWindow()                  #calling Main Game Screen once button is clicked
def redrawGameWindow():
    win.blit(bg, (0,0))
    for i in arrow:
        i.draw(win)
    man.draw(win)
    time.draw_timer(win)
    life.drawlives(win)
    bubble.drawBubble(win)
    pygame.display.update()



#mainloop
man=Player(329,329,23,37)  #creating object 'man' of player class
time_left=0
time=Timer(3, 5)    #object of Timer class
life = lives(600,5,totalLives)
bounce=False
bubble= Bubble(randint(20,400),200)     #object of Bubble class
arrow=[]
run = True

screen = pygame.display.set_mode((688, 366))  #initiazlizing objects for buttons
menu = pygame.image.load('titlescreen.jpg')
screen.blit(menu,(0,0))

button_01 = Button("1 Player", (190, 200))      #creating buttons as object of button class
button_02 = Button("2 Player", (190, 240), bg=skin)
buttons = [button_01, button_02]
menu_active= True


while menu_active:      #checking if menu screen is active
    for button in buttons:
        button.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            menu_active= False
            mousebuttondown()

    

    pygame.display.flip()
while run:          #loop that executes when main game screen is Open
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in arrow:
        if i.y < 366 and i.y>0:
            i.y -= i.vel
        else:
            arrow.pop(arrow.index(i))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:            #checking keyboard action from here
        if len(arrow) < 1:
          arrow.append(Weapon(man.x,man.y))  
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < 688 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
    else:
        man.right = False
        man.left = False
        man.walkCount = 0
        
            
    redrawGameWindow() #Calling func to update and draw all events on screen

pygame.quit()












