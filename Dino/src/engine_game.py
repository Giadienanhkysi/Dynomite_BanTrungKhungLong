from array import array
import math, pygame, sys, copy, os, time, random, pickle, types
from pygame import color
from copy import deepcopy
from pygame.locals import *
from setting import Settings
from Egg import Egg
from Arrow import Arrow
from Score import Score
from menu import Menu
pygame.init()

NAVYBLUE = (60,  60, 100)
WHITE = (255, 255, 255)
PURPLE = (255,   0, 255)
CYAN = (0, 255, 255)
BLACK = (0,   0,   0)
COMBLUE = (233, 232, 255)



# ....
ASSETS = {    
    'leftwall': pygame.image.load('assets/img/leftwall.gif'),
    'rightwall': pygame.image.load('assets/img/rightwall.gif'),
    'background': pygame.image.load('assets/img/jungleback.jpg'),
    'efooter': pygame.image.load('assets/img/eggpilesheet.png'),
    'yolk': pygame.image.load('assets/img/yolk.png'),
    'rope' : pygame.image.load('assets/img/rope.png')

}

class Dino:
    '''Lớp game'''
    def __init__(self, ai_game):        
        
        self.ai_game = ai_game
        self.setting = ai_game.setting     
        self.screen = ai_game.screen
        self.clock = ai_game.clock        
        self.main_font = ai_game.main_font        
        
        self.display_rect = self.screen.get_rect()

        self.musicList = ai_game.musicList
        self.menu = ai_game.menu
        self.picture = pygame.transform.scale(ASSETS['background'], (self.setting.screen_width, self.setting.screen_height))
        self.efooter = pygame.transform.scale(ASSETS['efooter'], (self.setting.screen_width, 100))
        self.leftwall = pygame.transform.scale(ASSETS['leftwall'], (90, self.setting.screen_height))
        self.rightwall = pygame.transform.scale(ASSETS['rightwall'], (80, self.setting.screen_height))
        self.rope = ASSETS['rope']
        pygame.mixer.music.load(self.musicList[0])
        pygame.mixer.music.play()
        self.track = 0


        self.arrow = Arrow(self)
        self.score = Score(self)
        self.nextEgg = Egg(self, self.setting.COLORLIST[0])
        self.gameColorList = copy.deepcopy(self.setting.COLORLIST)                
        self.yolkList = []        
        self.newEgg = None
        self.eggArray = self.makeBlankBoard()
        self.y_pos = -5
        self.running = True
        self.mouse_x = 300
        self.mouse_y = 300
        self.launchEgg = False
        self.high_score = None

        self.setEggs(self.eggArray)
        self.nextEgg = Egg(self, self.gameColorList[0])
        self.nextEgg.rect.centerx = self.setting.start_x
        self.nextEgg.rect.centery = self.setting.start_y - 5
        self.lose = None

    def loop(self):       
        '''Hàm chạy game và kiểm tra điều kiện thua, in điểm''' 
        self.runGame()
        if self.lose :
            pygame.mixer.music.load('assets/sounds/game_over_sound.ogg')
            pygame.mixer.music.play()
            self.high_score = self.setting.high_score
            if(self.score.total > self.high_score):
                self.setting.write_file('assets/point.txt', self.score.total)
                self.high_score = self.score.total
            self.menu.open('gameover', self.score.total, self.high_score)

    def runGame(self):   
        '''Hàm chạy game'''                                                                    
        speed_down = self.clock.get_time()/1000 # tốc độ đi xuống của bảng trứng = fps game
        self.y_pos += speed_down * 3 #Chỉnh tốc độ bảng trứng 

        # kiểm tra nếu bảng trứng chạm vạch dưới thì game over
        for row in range(len(self.eggArray)):
            for column in range(len(self.eggArray[0])):
                if self.eggArray[row][column] != self.setting.blank:
                    if self.eggArray[row][column].rect.bottom > (self.setting.screen_height - 100):
                        self.lose = True

        #vẽ ảnh nền và vạch kẻ
        self.screen.blit(self.picture, (0, 0, self.setting.screen_height, self.setting.screen_width))
        self.screen.blit(self.rope, (30, self.setting.screen_height - 100))

        # nếu trứng đang được bắn
        if self.launchEgg == True:
            if self.newEgg == None:
                # nếu trứng mới chưa được khởi tạo thì khỏi tạo
                self.newEgg = Egg(self, self.nextEgg.color)
                # gán góc bay của trứng bằng góc bắn của đường mũi tên
                self.newEgg.angle = self.arrow.get_ang(
                    (int)(self.setting.start_x), self.setting.start_y, self.mouse_x, self.mouse_y)

            self.screen.blit(self.rope, (30, self.setting.screen_height - 100))

            # vẽ quả trứng được bắn đi
            self.newEgg.update()
            self.newEgg.draw()

            # nếu chạm tường thì gán lại góc bằng góc nảy
            if self.newEgg.rect.right >= self.setting.screen_width - 60:
                self.newEgg.angle = 180 - self.newEgg.angle
            elif self.newEgg.rect.left < 60:
                self.newEgg.angle = 180 - self.newEgg.angle

            # kiểm tra xem quả trứng đã chạm đích hay chưa nếu rồi thì dừng
            self.stopEgg(self.eggArray)

            # Cập nhật lại liên tục list màu sử dụng cho đạn trứng
            random.shuffle(self.gameColorList)


            # Khi quả trứng được bắn xong thì tạo quả trứng mới tại vị trí giữa phía cuối màn hình
            if self.launchEgg == False:                
                self.nextEgg = Egg(self, self.gameColorList[0])
                self.nextEgg.rect.centerx = self.setting.start_x                
                self.nextEgg.rect.centery = self.setting.start_y - 5
        
        
                
        self.addRowToEggTable()        
        self.setArrayPos(self.eggArray)
        self.drawEggArray(self.eggArray)
        self.drawFallEgg()


        
        self.arrow.draw(self.mouse_x, self.mouse_y)
        self.nextEgg.draw()
        
        self.screen.blit(self.leftwall, (0, 0))
        self.screen.blit(self.rightwall, (self.setting.screen_width-60, 0))        
        self.screen.blit(self.efooter, (0, self.setting.screen_width - 100,
                            self.setting.screen_height, self.setting.screen_width))

        
        self.score.draw()

        if pygame.mixer.music.get_busy() == False:
            '''Xử lý track nhạc, phát hết tự động chuyển track khác'''
            if self.track == len(self.musicList) - 1:
                self.track = 0
            else:
                self.track += 1

            pygame.mixer.music.load(self.musicList[self.track])
            pygame.mixer.music.play()
            
    def handle_key(self, event):        
        '''Hàm lấy vị trí chuột và bắt sự kiện nhấp chuột'''
        (self.mouse_x, self.mouse_y) = pygame.mouse.get_pos()                                             
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.launchEgg = True
        
    def addRowToEggTable(self):
        '''Hàm này thêm 2 hàng mới vào bảng trứng khi bảng chạy đến giá trị y nhất định, tạo hiệu ứng rơi liên tục'''
        '''Cần thêm 2 hàng vì bảng trứng sắp xếp sole nên phải thêm chẵn hàng để trứng khỏi bị lệch so với ban đầu'''
        if self.y_pos >= 0:
            array1 = [None]*14
            array2 = [None] * 14
            '''Tạo 2 hàng mới'''
            for column in range(14):
                x = Egg(self, random.choice(self.gameColorList), 0, column)
                y = Egg(self, random.choice(self.gameColorList), 1, column)
                # break
                array1[column] = x
                array2[column] = y
            '''Cập nhật lại chỉ số hàng và cột cho bảng trứng mới'''
            for i in range(len(self.eggArray)):
                for column in range(len(self.eggArray[i])):
                    if(self.eggArray[i][column] != self.setting.blank):
                        self.eggArray[i][column].row += 2
            self.eggArray.insert(0, array1)
            self.eggArray.insert(1, array2)
            '''Khởi tạo lại vị trí y để trứng không bị trôi quá y'''
            self.y_pos -= 70  # set lại vị trí của bảng trứng
            self.eggArray.pop()
            self.eggArray.pop()

    def drawFallEgg(self):
        '''Vẽ trứng rơi'''
        for egg in self.yolkList:
            egg.draw_yolk()
            egg.rect.y += 15
   
    def makeBlankBoard(self):
        '''Hàm này tạo ra bảng trứng rỗng'''
        array = []
        for row in range(self.setting.array_height):
            column = []
            for i in range(self.setting.array_width):
                column.append(self.setting.blank)
            array.append(column)

        return array

    def setEggs(self, array):
        '''Hàm này thêm những quả trứng ngẫu nhiên vào bảng trứng rỗng'''
        for row in range(self.setting.bubble_adjust):
            for column in range(len(array[row])):
                random.shuffle(self.gameColorList)
                egg = Egg(self, self.gameColorList[0], row, column)
                array[row][column] = egg

        self.setArrayPos(array)

    def setArrayPos(self, array):
        '''Hàm này khởi tạo vị trí bảng trứng và các quả trứng'''
        
        for row in range(self.setting.array_height):
            for column in range(len(array[row])):
                if array[row][column] != self.setting.blank:
                    array[row][column].rect.x = (self.setting.bubble_width * column) + 60
                    array[row][column].rect.y = (
                        self.setting.bubble_width * row) + self.y_pos

        for row in range(1, self.setting.array_height, 2):
            for column in range(len(array[row])):
                if array[row][column] != self.setting.blank:
                    array[row][column].rect.x += self.setting.bubble_radius

        for row in range(1, self.setting.array_height):
            for column in range(len(array[row])):
                if array[row][column] != self.setting.blank:
                    array[row][column].rect.y -= (self.setting.bubble_adjust * row)
    
    def checkForFloaters(self,eggArray):
        '''Hàm kiểm tra những mảng trứng bị cô lập riêng (trứng nổi)'''
        '''Tạo ra 2 mảng ánh xạ và 1 bảng copy của bảng gốc, xử lý trên mảng ánh xạ sau đó chiếu vào bảng gốc để tìm ra những quả trứng bị bỏ đi'''

        floaterList = [] # list lưu lại những quả trứng nổi
        '''tìm ra cột khác rỗng hàng đầu tiên'''
        eggList = [column for column in range(len(eggArray[0]))
                            if eggArray[0][column] != self.setting.blank]        
        newEggList = []

        for i in range(len(eggList)):
            if i == 0:
                newEggList.append(eggList[i])
            elif eggList[i] > eggList[i - 1] + 1:
                newEggList.append(eggList[i])
        
        #Tạo eggArray copy của bảng gốc chỉ xử lý trên bản copy, xử lý xong mới gán lại bản gốc tránh làm sai lệch dữ liệu
        eggArrayCopy = self.makeBlankBoard()

        for row in range(len(eggArray)):
            for column in range(len(eggArray[0])):
                if eggArray[row][column] != self.setting.blank:                                                                                                                        
                    eggArrayCopy[row][column] = Egg(self,eggArray[row][column].color,
                    eggArray[row][column].rect.centerx, eggArray[row][column].rect.centery,
                    eggArray[row][column].row, eggArray[row][column].column)
                else:                                        
                    eggArrayCopy[row][column] = self.setting.blank
        ###
        #Tạo 2 mảng ánh xạ để xử lý xóa trứng
        eggArrayMapping = self.makeBlankBoard()        
        for row in range(len(eggArray)):
            for column in range(len(eggArray[0])):
                if eggArray[row][column] != self.setting.blank:
                    eggArrayMapping[row][column] = '*'                    
                else:
                    eggArrayMapping[row][column] = self.setting.blank                    
                    
        eggArrayMapping2 = deepcopy(eggArrayMapping)        

        for row in range(len(eggArrayMapping)):
            for column in range(len(eggArrayMapping[0])):                            
                eggArrayMapping[row][column] = self.setting.blank 
      

        for column in newEggList:                    
            self.popFloaters(eggArrayMapping, eggArrayMapping2, column) #xóa trứng nổi ra khỏi bảng trứng
        

        for row in range(len(eggArrayMapping)):
            for column in range(len(eggArrayMapping[0])):                            
                if eggArrayMapping[row][column] == self.setting.blank and eggArrayMapping2[row][column] != self.setting.blank:
                    eggArrayCopy[row][column] = self.setting.blank 
                    floaterList.append(Egg(self,eggArray[row][column].color,
                    eggArray[row][column].rect.centerx, eggArray[row][column].rect.centery,
                    eggArray[row][column].row, eggArray[row][column].column, pickle.TRUE))

                    eggArray[row][column] = self.setting.blank
                
        return floaterList
   
    def popFloaters(self, eggArray, copyOfBoard, column, row=0):
        '''Hàm xóa trứng nổi'''
        if (row < 0 or row > (len(eggArray)-1)
                or column < 0 or column > (len(eggArray[0])-1)):
            return

        elif copyOfBoard[row][column] == self.setting.blank:
            return

        elif eggArray[row][column] == copyOfBoard[row][column]:
            return

        eggArray[row][column] = copyOfBoard[row][column]

        if row == 0:
            self.popFloaters(eggArray, copyOfBoard, column + 1, row)
            self.popFloaters(eggArray, copyOfBoard, column - 1, row)
            self.popFloaters(eggArray, copyOfBoard, column,     row + 1)
            self.popFloaters(eggArray, copyOfBoard, column - 1, row + 1)

        elif row % 2 == 0:
            self.popFloaters(eggArray, copyOfBoard, column + 1, row)
            self.popFloaters(eggArray, copyOfBoard, column - 1, row)
            self.popFloaters(eggArray, copyOfBoard, column,     row + 1)
            self.popFloaters(eggArray, copyOfBoard, column - 1, row + 1)
            self.popFloaters(eggArray, copyOfBoard, column,     row - 1)
            self.popFloaters(eggArray, copyOfBoard, column - 1, row - 1)

        else:
            self.popFloaters(eggArray, copyOfBoard, column + 1, row)
            self.popFloaters(eggArray, copyOfBoard, column - 1, row)
            self.popFloaters(eggArray, copyOfBoard, column,     row + 1)
            self.popFloaters(eggArray, copyOfBoard, column + 1, row + 1)
            self.popFloaters(eggArray, copyOfBoard, column,     row - 1)
            self.popFloaters(eggArray, copyOfBoard, column + 1, row - 1)

    def stopEgg(self, eggArray):
        deleteList = []
        self.yolkList = []
        popSound = pygame.mixer.Sound('assets/sounds/BreakEgg.ogg')

        for row in range(len(eggArray)):
            for column in range(len(eggArray[row])):

                if (eggArray[row][column] != self.setting.blank and self.newEgg != None): #nếu trứng khác rỗng
                    #nếu đạn va chạm bảng trứng
                    if (pygame.sprite.collide_rect(self.newEgg, eggArray[row][column])) or self.newEgg.rect.top <= 0:
                        #nếu đạn chạm vào cạnh trên cùng thì thêm trứng vào hàng rỗng đó
                        if self.newEgg.rect.top <= 0:
                            newRow, newColumn = self.addEggToTop(
                                eggArray, self.newEgg)
                        # nếu trứng chạm vào các quả trứng khác nếu bên cạnh còn trống thì
                        #  gán vị trí đó bằng trứng mới
                        elif self.newEgg.rect.centery >= eggArray[row][column].rect.centery:

                            if self.newEgg.rect.centerx >= eggArray[row][column].rect.centerx:
                                if row == 0 or (row) % 2 == 0:
                                    newRow = row + 1
                                    newColumn = column
                                    if eggArray[newRow][newColumn] != self.setting.blank:
                                        newRow = newRow - 1
                                    eggArray[newRow][newColumn] = copy.copy(
                                        self.newEgg)
                                    eggArray[newRow][newColumn].row = newRow
                                    eggArray[newRow][newColumn].column = newColumn

                                else:

                                    newRow = row + 1
                                    newColumn = column + 1
                                    if eggArray[newRow][newColumn] != self.setting.blank:
                                        newRow = newRow - 1
                                    eggArray[newRow][newColumn] = copy.copy(
                                        self.newEgg)
                                    eggArray[newRow][newColumn].row = newRow
                                    eggArray[newRow][newColumn].column = newColumn

                            elif self.newEgg.rect.centerx < eggArray[row][column].rect.centerx:
                                if row == 0 or row % 2 == 0:
                                    newRow = row + 1
                                    newColumn = column - 1
                                    if newColumn < 0:
                                        newColumn = 0
                                    if eggArray[newRow][newColumn] != self.setting.blank:
                                        newRow = newRow - 1
                                    eggArray[newRow][newColumn] = copy.copy(
                                        self.newEgg)
                                    eggArray[newRow][newColumn].row = newRow
                                    eggArray[newRow][newColumn].column = newColumn
                                else:
                                    newRow = row + 1
                                    newColumn = column
                                    if eggArray[newRow][newColumn] != self.setting.blank:
                                        newRow = newRow - 1
                                    eggArray[newRow][newColumn] = copy.copy(
                                        self.newEgg)
                                    eggArray[newRow][newColumn].row = newRow
                                    eggArray[newRow][newColumn].column = newColumn

                        elif self.newEgg.rect.centery < eggArray[row][column].rect.centery:
                            if self.newEgg.rect.centerx >= eggArray[row][column].rect.centerx:
                                if row == 0 or row % 2 == 0:
                                    newRow = row - 1
                                    newColumn = column
                                    if eggArray[newRow][newColumn] != self.setting.blank:
                                        newRow = newRow + 1
                                    eggArray[newRow][newColumn] = copy.copy(
                                        self.newEgg)
                                    eggArray[newRow][newColumn].row = newRow
                                    eggArray[newRow][newColumn].column = newColumn
                                else:
                                    newRow = row - 1
                                    newColumn = column + 1
                                    if eggArray[newRow][newColumn] != self.setting.blank:
                                        newRow = newRow + 1
                                    eggArray[newRow][newColumn] = copy.copy(
                                        self.newEgg)
                                    eggArray[newRow][newColumn].row = newRow
                                    eggArray[newRow][newColumn].column = newColumn

                            elif self.newEgg.rect.centerx <= eggArray[row][column].rect.centerx:
                                if row == 0 or row % 2 == 0:
                                    newRow = row - 1
                                    newColumn = column - 1
                                    if eggArray[newRow][newColumn] != self.setting.blank:
                                        newRow = newRow + 1
                                    eggArray[newRow][newColumn] = copy.copy(
                                        self.newEgg)
                                    eggArray[newRow][newColumn].row = newRow
                                    eggArray[newRow][newColumn].column = newColumn

                                else:
                                    newRow = row - 1
                                    newColumn = column
                                    if eggArray[newRow][newColumn] != self.setting.blank:
                                        newRow = newRow + 1
                                    eggArray[newRow][newColumn] = copy.copy(
                                        self.newEgg)
                                    eggArray[newRow][newColumn].row = newRow
                                    eggArray[newRow][newColumn].column = newColumn

                        self.popEggs(eggArray, newRow, newColumn,
                                     self.newEgg.color, deleteList)
                        floaterList = []
                        # nếu 3 quả trứng cùng màu thì xóa
                        if len(deleteList) >= 3:
                            for pos in deleteList:
                                popSound.play()
                                row = pos[0]
                                column = pos[1]
                                eggArray[row][column].isYolk = True
                                self.yolkList.append(eggArray[row][column])
                                eggArray[row][column] = self.setting.blank             
                            

                            floaterList = self.checkForFloaters(eggArray) 
                            # thêm cả những quả trứng nổi vào list bị xóa
                            for egg in floaterList:
                                self.yolkList.append(egg)

                            self.score.update(deleteList)

                        self.launchEgg = False
                        self.newEgg = None
        
    def addEggToTop(self, eggArray, egg):
        '''Thêm trứng lên trên cùng nếu hàng trên cùng bị hổng, có thể không cần hàm này nếu hàng 0 luôn lấp đầy trứng'''
        posx = egg.rect.centerx
        leftSidex = posx - self.setting.bubble_radius

        columnDivision = math.modf(float(leftSidex) / float(self.setting.bubble_width))
        column = int(columnDivision[1])
        if columnDivision[0] < 0.5:
            eggArray[0][column-1] = copy.copy(egg)
        else:
            # column += 1
            eggArray[0][column] = copy.copy(egg)
            # print(eggArray[0][column])

        row = 0

        return row, column

    def popEggs(self, eggArray, row, column, color, deleteList):
        '''Hàm lưu vị trí trứng bị xóa vào list'''
        if row < 0 or column < 0 or row > (len(eggArray)-1) or column > (len(eggArray[0])-1):
            return

        elif eggArray[row][column] == self.setting.blank:
            return

        elif eggArray[row][column].color != color:
            return

        for egg in deleteList:
            if eggArray[egg[0]][egg[1]] == eggArray[row][column]:
                return

        deleteList.append((row, column))

        if row == 0:
            self.popEggs(eggArray, row,     column - 1, color, deleteList)
            self.popEggs(eggArray, row,     column + 1, color, deleteList)
            self.popEggs(eggArray, row + 1, column,     color, deleteList)
            self.popEggs(eggArray, row + 1, column - 1, color, deleteList)

        elif row % 2 == 0:

            self.popEggs(eggArray, row + 1, column,         color, deleteList)
            self.popEggs(eggArray, row + 1, column - 1,     color, deleteList)
            self.popEggs(eggArray, row - 1, column,         color, deleteList)
            self.popEggs(eggArray, row - 1, column - 1,     color, deleteList)
            self.popEggs(eggArray, row,     column + 1,     color, deleteList)
            self.popEggs(eggArray, row,     column - 1,     color, deleteList)

        else:
            self.popEggs(eggArray, row - 1, column,     color, deleteList)
            self.popEggs(eggArray, row - 1, column + 1, color, deleteList)
            self.popEggs(eggArray, row + 1, column,     color, deleteList)
            self.popEggs(eggArray, row + 1, column + 1, color, deleteList)
            self.popEggs(eggArray, row,     column + 1, color, deleteList)
            self.popEggs(eggArray, row,     column - 1, color, deleteList)

    def drawEggArray(self, array):
        for row in range(self.setting.array_height):
            for column in range(len(array[row])):
                if array[row][column] != self.setting.blank:
                    array[row][column].draw()

    # def terminate(self):
    #     pygame.quit()
    #     sys.exit()
    

class Engine:
    '''Lớp điều khiển chương trình'''
    def __init__(self):    
        self.setting = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.setting.screen_width,
                        self.setting.screen_height))
        pygame.display.set_icon(pygame.image.load('assets/img/purple.png'))
        self.menu = Menu(self.screen, self)
        self.main_font = pygame.font.SysFont('Helvetica', 
                        self.setting.text_height)                
        pygame.display.set_caption('Ban trung khung long')        
        self.musicList = ['assets/sounds/game_music.ogg',
                        'assets/sounds/giorno_theme.ogg',
                         'assets/sounds/Goofy_Theme.ogg']
        self.running = True
        self.game = None
        
    #cac hàm dùng trong menu
    def new_game(self):    
        self.menu.is_open = False
        self.game = None
        self.game = Dino(self)               

    def terminate(self):
        '''Hàm kết thúc chương trình'''
        self.running = False
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def resume_game(self):
        if self.game != None:
            self.menu.is_open = False

    def restart_game(self):        
        self.menu.is_open = False        
        self.game = Dino(self)                    
    # hàm chạy chương trình
    def run_game(self):
        while self.running:
            self.clock.tick(120)                            
            self.handle_key()
            if self.menu.is_open:                
                self.screen.fill((0, 0, 0))
                self.menu.draw()
            else:                
                self.game.loop()            
            pygame.display.flip()

    def handle_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if self.menu.is_open:
                    self.menu.handle_key(event.key)
                elif event.key == self.setting.PAUSE_KEY:
                    self.menu.open('pause')

            if(self.menu.is_open == False):
                self.game.handle_key(event)       

if __name__ == '__main__':    
    ai = Engine()
    ai.run_game()
