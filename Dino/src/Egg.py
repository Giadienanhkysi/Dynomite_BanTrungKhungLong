import pygame
import math
from setting import Settings
ASSETS = {
    'color': {1: pygame.image.load('assets/img/red.png'),
              2: pygame.image.load('assets/img/green.png'),
              3: pygame.image.load('assets/img/blue.png'),
              4: pygame.image.load('assets/img/yellow.png'),
              5: pygame.image.load('assets/img/purple.png'),
              6: pygame.image.load('assets/img/magenta.png'), },
    'leftwall': pygame.image.load('assets/img/leftwall.gif'),
    'rightwall': pygame.image.load('assets/img/rightwall.gif'),
    'background': pygame.image.load('assets/img/jungleback.jpg'),
    'efooter': pygame.image.load('assets/img/eggpilesheet.png'),
    'yolk': pygame.image.load('assets/img/yolk.png'),
    'rope' : pygame.image.load('assets/img/rope.png')

}
class Egg(pygame.sprite.Sprite):
    def __init__(self, ai_game, color,
         centerx=Settings().start_x, centery=Settings().start_y,
         isFloater = False,row=0, column=0):
        pygame.sprite.Sprite.__init__(self)
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.speed = 10
        self.color = color
        self.radius = self.ai_game.setting.bubble_radius
        self.angle = 0
        self.row = row
        self.column = column
        self.isYolk = False
        self.isFloater = isFloater

    def update(self):
        '''Hàm cập nhật lại vị trí quả trứng'''
        if self.angle == 90:
            xmove = 0
            ymove = self.speed * -1
        elif self.angle < 90:
            xmove = self.xcalculate(self.angle)
            ymove = self.ycalculate(self.angle)
        elif self.angle > 90:
            xmove = self.xcalculate(180 - self.angle) * -1
            ymove = self.ycalculate(180 - self.angle)

        self.rect.centerx += xmove
        self.rect.centery += ymove

    def draw(self):
        '''Hàm vẽ trứng'''        
        self.screen.blit(ASSETS['color'][self.color], self.rect)

    def draw_yolk(self):
        '''Hàm này dể vẽ trứng vỡ và trứng rụng'''
        if self.isYolk:
            self.screen.blit(ASSETS['yolk'], (self.rect.x, self.rect.y))
        elif self.isFloater:
            '''nếu là trứng rụng thì tăng dần tọa độ y'''
            self.draw()

    def xcalculate(self, angle):
        radians = math.radians(angle)
        xmove = math.cos(radians)*(self.speed)
        return xmove

    def ycalculate(self, angle):
        radians = math.radians(angle)
        ymove = math.sin(radians)*(self.speed) * -1
        return ymove
   
