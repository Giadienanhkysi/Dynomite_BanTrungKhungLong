import pygame
class Score:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.total = 0
        self.font = pygame.font.SysFont('Helvetica', 15)
        self.render = self.font.render(
            'Score: ' + str(self.total), True,
            self.ai_game.setting.BLACK, self.ai_game.setting.WHITE)
        self.rect = self.render.get_rect()
        self.rect.left = 5
        self.rect.bottom = self.ai_game.setting.screen_height - 5

    def update(self, deleteList):
        self.total += ((len(deleteList)) * 10) #tính điểm
        self.render = self.font.render(
            'Score: ' + str(self.total), True,
            self.ai_game.setting.BLACK, self.ai_game.setting.WHITE)

    def draw(self):
        self.screen.blit(self.render, self.rect)
