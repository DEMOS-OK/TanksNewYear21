import pygame.font

class Label():
    '''Класс "Метка" для работы с текстом'''
    def __init__(self, settings, screen, text, x, y):
        '''Конструктор класса'''

        #Вывод свойств на уровень класса
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect() #получение прямоугольника экрана

        #Цвет текста
        self.text_color = settings.screen['font_color']
        self.font = pygame.font.SysFont(None, settings.screen['font_size'])

        self.text = str(text)
        self.x = x
        self.y = y

        self.prepare_text()


    def prepare_text(self):
        '''Подготовка текста'''
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.centery = self.y
        self.text_image_rect.centerx = self.x


    def show_text(self):
        '''Нанесение текста'''
        self.screen.blit(self.text_image, self.text_image_rect)
