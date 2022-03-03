from setting import *
class Arrow:
    def __init__(self, ai_game):
        pygame.sprite.Sprite.__init__(self)
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.angle = 90
    

    def draw(self, mouse_x, mouse_y):
        x, y = self.get_point_line((int)(Settings().start_x), Settings().start_y, mouse_x, mouse_y)
        pygame.draw.line(self.screen, (0, 0, 255), [(int)(
            Settings().start_x), Settings().start_y], [int(x), int(y)], self.ai_game.setting.width_line)

    def get_angle(self, x1, y1, x2, y2):
        '''Hàm này trả về tan góc bắn'''
        return (y2-y1)/(x2-x1)

    def get_point_line(self, x1, y1, x2, y2):
        '''Hàm này trả về điểm dùng để vẽ đường thẳng dựa vào vị trí con trỏ chuột(đường thẳng độ dài cố định)'''
        if(x2-x1 != 0):
            m = (self.get_angle(x1, y1, x2, y2))
            if(m < 0):
                x = (self.ai_game.setting.size_line/math.sqrt(((m*m)+1)))+x1
                y = y1 + ((m*(x-x1)))
            else:
                x = -(self.ai_game.setting.size_line/math.sqrt(((m*m)+1)))+x1
                y = y1 + ((m*(x-x1)))
        else:
            x = x1
            y = y1-self.ai_game.setting.size_line

        return [x, y]

    def get_ang(self, x1, y1, x2, y2):
        '''Hàm này trả về góc khi bắt đầu bắn quả trứng'''
        xd = (x2-x1)
        yd = (y2-y1)
        Angle = 90
        if(xd != 0):
            if(x2 > x1):
                '''bắn sang phải'''
                Angle = - (math.degrees(math.atan(yd/xd)))
            else:
                '''bắn sang trái'''
                Angle = 180 - math.degrees(math.atan(yd/xd))
        return Angle
