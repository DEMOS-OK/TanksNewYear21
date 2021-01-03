import pygame

class Settings():
    '''Класс со всеми игровыми настройками'''
    def __init__(self):
        '''Конструктор класса'''
        self.screen = self.__init_screen_settings()
    

    def __init_screen_settings(self):
        '''Возвращает настройки экрана'''
        screen_settings = {
            'size': (1200, 600),
            'bg_color': (240, 240, 240),
            'bg': pygame.image.load("Data/Images/Background.png"),
            'font_color': (255, 255, 255),
            'font_size': 18,
            'graphics': 1,
        }

        return screen_settings
