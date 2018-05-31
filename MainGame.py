import pygame
import math
import random
import pygame

class Text:

    #initialization function
    def init(self, screen, x, y, text, font, color):
        self.screen = screen
        self.ojx = float(x)
        self.ojy = float(y)
        self.font = font
        self.text = text
        self.color = color
        self.x = self.ojx
        self.y = self.ojy

    #updates the text and draws it
    def update(self):
        self.screen.blit(self.font.render(str(self.text),True, self.color), (self.x,self.y))

    #centers the text around the x and y point
    def center(self):
        self.x = self.ojx - self.font.size(str(self.text))[0]/2
        self.y = self.ojy - self.font.size(str(self.text))[1]/2

class Button:

    #initialization function
    def __init__(self, screen, rect, color, onColor, label):
        self.screen = screen
        self.rect = pygame.Rect(rect)
        self.color = [color, onColor, color]
        self.label = label

    #checks if the mouse is in the button area
    def inButton(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    #changes cover is inButton is true
    def hoverChange(self):
        if self.inButton():
            self.color[2] = self.color[1]
        else:
            self.color[2] = self.color[0]

    #check if user has mouse button on pressed when entering the button
    def clickButton(self):
        if pygame.mouse.get_pressed()[0] and self.inButton():
            return True
        else:
            return False

    #draws button with text
    def draw(self):
            pygame.draw.rect(self.screen, self.color[2], self.rect)
            self.label.ojx = self.rect[0] + self.rect[2]/2
            self.label.ojy = self.rect[1] + self.rect[3]/2
            self.label.center()
            self.label.update()

class Player:
    def __init__(self, pos, speedMod, turnSpd, startDeg,surface,screen):
        
        #center position
        self.pos = [pos[0],pos[1]]
        
        #position of top right corner
        self.newPos = (pos[0] - surface.get_width()/2, pos[1] - surface.get_height()/2)
        
        #accel speed modifier
        self.speedMod = speedMod
        
        #turn speed modifier
        self.turnSpd = turnSpd
        
        #degree modifier
        self.deg = startDeg
        
        #x and y speeds
        self.xSpeed = 0
        self.ySpeed = 0
        
        #surfaces
        self.surface = surface
        self.ojSurface = surface
        self.surface = pygame.transform.rotate(self.surface, self.deg)
        
        #screen and mask
        self.screen = screen
        self.mask = pygame.mask.from_surface(self.surface)
     
    #rotates the player
    def turn(self, event):
        self.surface = self.ojSurface
        
        #clockwise
        if event == 0:
            self.deg -= self.turnSpd
        
        #counter clockwise
        elif event == 1:
            self.deg += self.turnSpd
           
        self.surface = pygame.transform.rotate(self.surface, self.deg)
        
        #updates position of rect
        self.newPos = (self.pos[0] - self.surface.get_width() / 2, self.pos[1] - self.surface.get_height() / 2)
        
        #updates mask
        self.mask = pygame.mask.from_surface(self.surface)
    
    #accelerates the player
    def accel(self):
        
        #checks for 90 degrees
        if self.deg %  90 == 0:
            if self.deg/90 % 2:
                self.xSpeed += math.sin(math.radians(self.deg)) * self.speedMod
            else:
                self.ySpeed += math.cos(math.radians(self.deg)) * self.speedMod
        else:
            self.ySpeed += math.cos(math.radians(self.deg)) * self.speedMod
            self.xSpeed += math.sin(math.radians(self.deg)) * self.speedMod
    
    #move function
    def move(self):
        
        #changes position
        self.pos[0] += self.xSpeed
        self.pos[1] += self.ySpeed
        
        #resets the 
        self.newPos = (self.pos[0] - self.surface.get_width() / 2, self.pos[1] - self.surface.get_height() / 2)
        self.mask = pygame.mask.from_surface(self.surface)
       
    #blits the surface
    def draw(self):
        self.screen.blit(self.surface, self.newPos)
        
    #returns rect
    def get_rect(self):
        return pygame.Rect((self.newPos[0],self.newPos[1],self.surface.get_width(),self.surface.get_height()))
#class for match body
class Match_Body(Player):
    def __init__(self, pos, speedMod, turnSpd, startDeg,screen):
        self.pos = [pos[0],pos[1]]
        self.speedMod = speedMod
        self.turnSpd = turnSpd
        self.deg = startDeg
        self.xSpeed = 0
        self.ySpeed = 0
        
        #the only thing that changed from player class
        self.surface = pygame.image.load("body.png")
        
        self.ojSurface = self.surface
        self.surface = pygame.transform.rotate(self.surface, self.deg)
        self.screen = screen
        self.newPos = (pos[0] - self.surface.get_width() / 2, pos[1] - self.surface.get_height() / 2)
        self.mask = pygame.mask.from_surface(self.surface)
#class for match head
class Match_Head(Player):
    def __init__(self, pos, speedMod, turnSpd, startDeg,screen):
        self.pos = [pos[0],pos[1]]
        self.speedMod = speedMod
        self.turnSpd = turnSpd
        self.deg = startDeg
        self.xSpeed = 0
        self.ySpeed = 0
        
        #the only thing that changed from player class
        self.surface = pygame.image.load("head.png")
        
        self.ojSurface = self.surface
        self.surface = pygame.transform.rotate(self.surface, self.deg)
        self.screen = screen
        self.newPos = (pos[0] - self.surface.get_width() / 2, pos[1] - self.surface.get_height() / 2)
        self.mask = pygame.mask.from_surface(self.surface)
class Match:
    def __init__(self, pos, speedMod, turnSpd, startDeg,screen):
        self.screen = screen
        self.head = Match_Head(pos,speedMod,turnSpd, startDeg, screen)
        self.body = Match_Body(pos, speedMod, turnSpd, startDeg, screen)
    
    #turns the match
    def turn(self, event):
        self.head.turn(event)
        self.body.turn(event)
    
    #accelerates both the body and the head
    def accel(self):
        self.head.accel()
        self.body.accel()
    
    #draws the match
    def draw(self):
        self.body.draw()
        self.head.draw()
        #hitbox detection 
#        new_out = []
#        new_outY = []
#        for out in self.body.mask.outline():
#            new_out.append((self.body. [0] + out[0], self.body.newPos[1] + out[1]))
#        for out in self.head.mask.outline():
#            new_outY.append((self.head.newPos[0] + out[0], self.head.newPos[1] + out[1]))
#        pygame.draw.lines(self.screen, (255, 255, 255), True, new_out)
#        pygame.draw.lines(self.head.surface,(255,255,255),True, new_outY)
#        pygame.draw.rect(self.screen, (255, 255, 255),
#                        (self.body.newPos[0], self.body.newPos[1], self.body.surface.get_width(), self.body.surface.get_height()), 1)
    #collision with players
    def player_collision(self,pos,othermask):
        
        #offset between 2 players
        offset = (int(self.body.newPos[0] - pos[0]), int(self.body.newPos[1] - pos[1]))
        
        #check if other mask overlaps w/ body
        if self.body.mask.overlap(othermask,offset):
            return 1
        
        #check if other mask collides w/ head
        elif self.head.mask.overlap(othermask,offset):
            return 2   
        else:
            return 0
        
    #moves the match body and head
    def move(self):
        self.head.move()
        self.body.move()
    
    #gets rect of entire player
    def get_rect(self):
        return self.body.get_rect()
    
pygame.init()
closed = False
clock = pygame.time.Clock()
screenRes = (640,480)
screen = pygame.display.set_mode(screenRes)

#sides of the screen
sides = [(-1 * screenRes[0], 0, screenRes[0], screenRes[1]), (0, -1 * screenRes[1], screenRes[0], screenRes[1]), (screenRes[0], 0, screenRes[0], screenRes[1]), (0, screenRes[1], screenRes[0], screenRes[1])]

players = []

#resets all players
def reset():
    global players
    players = [Match((screenRes[0] / 4, screenRes[1] / 2), 0.01, 1.5, 0, screen),
               Match((screenRes[0] * 3 / 4, screenRes[1] / 2), 0.01, 1.5, 0, screen)]
reset()

#control scheme
controls = [[pygame.K_a,pygame.K_s,pygame.K_SPACE],[pygame.K_k,pygame.K_l,pygame.K_RSHIFT]]

#main
while not closed:
    clock.tick(60)
    screen.fill((0,0,0))
    
    #get keys
    keys = pygame.key.get_pressed()
    
    #testing for controls
    for i in range(len(players)):
        if keys[controls[i][0]]:
            players[i].turn(0)
        if keys[controls[i][1]]:
            players[i].turn(1)
        if keys[controls[i][2]]:
            players[i].accel()
            
    #testing for collision between players heads and bodies(1 is body 2 is head)  
    if players[0].player_collision(players[1].head.newPos,players[1].head.mask) == 1:
        reset()
        print("Player 1 wins")
    elif players[0].player_collision(players[1].head.newPos,players[1].head.mask) == 2:
        reset()
        print("TIE")
    elif players[0].player_collision(players[1].body.newPos,players[1].body.mask) == 1:
        reset()
        print("TIEB")
    elif players[0].player_collision(players[1].body.newPos,players[1].body.mask) == 2:
        reset()
        print("Player 2 wins")
        
    #loop for all players
    for j in players:
        
        #tests if players collide with sides
        for i in sides:
            if j.get_rect().colliderect(i):
                reset()
                break
        #moving all players and drawing players
        j.move()
        j.draw()
    pygame.display.update()
    for event in pygame.event.get():
        # standard quit
        if event.type == pygame.QUIT:
            pygame.display.quit()
            closed = True
pygame.quit()
