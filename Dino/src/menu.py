import pygame
from setting import Settings

ASSETS = {
    'logo_game': pygame.image.load('assets/img/logo.png'),
    'menu_pointer': pygame.image.load('assets/img/menu_pointer.png'),     
}


class MenuOption:
    def __init__(self, screen, label, select):
        self.screen = screen
        self.label = label
        self.select = select #biến này lưu 1 hàm mở menu

    def draw(self, y, point):                
        cursor = ASSETS['menu_pointer']
        label = Settings().GAME_FONT_MENU.render(self.label, True, (255, 255, 255))

        if point:#kiem tra xem select dang chi vao dau
            self.screen.blit(cursor, cursor.get_rect(left=120, centery=y))
        self.screen.blit(label, label.get_rect(left=190, centery=y))

class Menu:
    def __init__(self, screen, ai_game):
        self.ai_game = ai_game
        self.screen = screen
        self.is_open = True
        self.selected = 0
        self.mode = 'main'
        self.score = None
        self.high_score = None        
        self.options = {
          'main': [
            MenuOption(screen, 'Play', self.ai_game.new_game),            
            MenuOption(screen, 'Quit Game', self.ai_game.terminate),
          ],
          'pause': [
            MenuOption(screen, 'Continue', self.ai_game.resume_game), 
            #truyền vào tham số là một function
            # (vì self.open trả về nonetype nên phải thêm lambda)
            MenuOption(screen, 'Main menu',  lambda: self.open('main'))
          ],
          'gameover': [
            MenuOption(screen, 'New Game', self.ai_game.restart_game), 
            MenuOption(screen, 'Main menu',  lambda: self.open('main'))
          ],              
        }
    
    def open(self, mode, score=None, high_score=None, ):
        '''Hàm này để mở các menu'''
        # biến score và high_score dùng để in ra màn hình gameover trong menu gameover
        self.score = score
        self.high_score = high_score
        if self.mode != mode:
            self.selected = 0 #khi chuyen menu, con tro luon o vi tri dau tien
        self.mode = mode
        self.is_open = True        

    def draw(self):
        if self.mode == 'main' or self.mode == 'pause':
            logo_game = ASSETS['logo_game']
            self.screen.blit(logo_game, logo_game.get_rect(centerx=325, top=0))
        elif self.mode == 'gameover':
            gameover_label = Settings().GAME_FONT_MENU.render('Game Over!!', True, (255, 255, 255))
            score = 'YourScore:  {:05d}'.format(self.score)
            score = Settings().GAME_FONT_MENU.render(score, True, (255, 255, 255))
            high_score = 'HighScore:  {:05d}'.format(self.high_score)
            high_score = Settings().GAME_FONT_MENU.render(high_score, True, (255, 255, 255))

            self.screen.blit(gameover_label, gameover_label.get_rect(left=80, top=190))
            self.screen.blit(score, gameover_label.get_rect(left=80, top=250))
            self.screen.blit(high_score, gameover_label.get_rect(left=80, top=300))        

        y = 500 #vị trí dòng đầu
        for i, option in enumerate(self.options[self.mode]):
          option.draw(y, self.selected == i)
          y += 70 #khoang cach giua cac dong
        
    def handle_key(self, key):        
        if key == Settings().PAUSE_KEY and self.mode == 'pause':
            #nếu đang ở pause bấm pause key lần nữa để resume game
            self.ai_game.resume_game()
        elif key == Settings().SELECT_KEY:
            #bấm enter sẽ gọi đến biến function select của menu option
            self.options[self.mode][self.selected].select()
        elif key == Settings().UP_KEY:
            if self.selected == 0:
                self.selected = len(self.options[self.mode]) - 1 #nhay xuong cuoi
            else:
                self.selected -= 1
        elif key == Settings().DOWN_KEY:
            if self.selected == len(self.options[self.mode]) - 1:
                self.selected = 0 #nhay len dau
            else:
                self.selected += 1