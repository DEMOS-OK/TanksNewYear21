import pygame

class Game():
    '''Основной класс игры, связывающий всё воедино'''
    def __init__(self, settings, screen):
        '''Конструктор класса'''
        
        self.settings = settings
        self.screen   = screen
    
        self.status = True


    def update(self):
        '''Обновляет все игровые события'''
        while self.status:
            self.check_events() #Проверяем события

            self.screen.blit(self.settings.screen['bg'], (0, 0)) #Рисуем фон

            pygame.display.flip()
    
    
    def check_events(self):
        '''Проверяет игровые события'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

