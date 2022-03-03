import pygame
pygame.init()
import math
class Settings:
    def __init__(self):
        self.screen_width = 680
        self.screen_height = 680
        self.bg_color = (230, 230, 230)
        self.text_height = 20
        self.main_font = 'Helvetica'
        self.bubble_radius = 20
        self.bubble_width = self.bubble_radius * 2
        self.bubble_layers = 5
        self.bubble_adjust = 5        
        self.start_x = self.screen_width / 2
        self.start_y = self.screen_height - self.bubble_radius
        self.array_width = 14
        self.array_height = 20
        self.blank = '.'

        self.GRAY = (100, 100, 100)
        self.NAVYBLUE = (60,  60, 100)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255,   0)
        self.ORANGE = (255, 128,   0)
        self.PURPLE = (255,   0, 255)
        self.CYAN = (0, 255, 255)
        self.BLACK = (0,   0,   0)
        self.COMBLUE = (233, 232, 255)        
        self.BGCOLOR = self.WHITE
        self.RED = 1
        self.GREEN = 2
        self.BLUE = 3
        self.YELLOW = 4
        self.PURPLE = 5
        self.MAGENTA = 6
        self.COLORLIST = [self.RED, self.GREEN, self.BLUE, self.YELLOW, self.PURPLE, self.MAGENTA]

        self.size_line = 250
        self.width_line = 2

        self.DEFAULT_SINGLEPLAYER_CONTROLS = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'place_bomb': pygame.K_SPACE,
        }          
       
        self.GET_PRESSED = pygame.key.get_pressed()

        self.PAUSE_KEY = pygame.K_ESCAPE
        self.SELECT_KEY = pygame.K_RETURN
        self.UP_KEY = pygame.K_UP 
        self.DOWN_KEY = pygame.K_DOWN
        
        self.GAME_FONT_MENU = pygame.font.Font('assets/font/PixelMiners-KKal.otf', 32) 
        self.GAME_FONT_GAME_BAR = pygame.font.Font('assets/font/PixelMiners-KKal.otf', 20) 
        

        self.screen_size = 650, 780
        self.running = True
        self.playtime = 200
        self.high_score = self.read_file('assets/point.txt')
        
    def read_file(self, file_name):
        with open(file_name) as file_object:
            return int(file_object.read())

    def write_file(self, file_name, score):
        with open(file_name, 'w') as file_object:
            file_object.write(str(score))