import pygame

class Player:
    def __init__(self, pos,surface,screen):
        self.pos = [pos[0],pos[1]]
        self.newPos = (pos[0] - surface.get_width()/2, pos[1] - surface.get_height()/2)
        self.deg = 0
        self.surface = surface
        self.ojSurface = surface
        self.screen = screen
        self.mask = pygame.mask.from_surface(self.surface)
    def turn(self, event):
        self.surface = self.ojSurface
        if event == 0:
            self.deg -= 0.1
        elif event == 1:
            self.deg += 0.1
        self.surface = pygame.transform.rotate(self.surface, self.deg)
        self.newPos = (self.pos[0] - self.surface.get_width() / 2, self.pos[1] - self.surface.get_height() / 2)
        self.mask = pygame.mask.from_surface(self.surface)
    def move(self):
        self.pos[0] = pygame.mouse.get_pos()[0]
        self.pos[1] = pygame.mouse.get_pos()[1]
        self.newPos = (self.pos[0] - self.surface.get_width() / 2, self.pos[1] - self.surface.get_height() / 2)
        self.mask = pygame.mask.from_surface(self.surface)
    def draw(self):
        self.screen.blit(self.surface, self.newPos)

screenRes = (640,480)
screen = pygame.display.set_mode(screenRes)
closed = False
players = [Player((320,240),pygame.image.load("body.png"), screen),Player((480,240),pygame.image.load("body.png"), screen)]

controls = [[pygame.K_a,pygame.K_s],[pygame.K_k,pygame.K_l]]
while not closed:
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    offset = (int(players[0].newPos[0] - players[1].newPos[0]), int(players[0].newPos[1] - players[1].newPos[1]))
    if players[0].mask.overlap(players[1].mask, offset):
        print("collided")
    for i in range(len(players)):
        if keys[controls[i][0]]:
            players[i].turn(0)
        if keys[controls[i][1]]:
            players[i].turn(1)
        players[i].draw()
    players[0].move()
    pygame.display.update()
    for event in pygame.event.get():
        # standard quit
        if event.type == pygame.QUIT:
            pygame.display.quit()
            closed = True
            pygame.quit()
