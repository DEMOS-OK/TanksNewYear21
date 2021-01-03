import pygame

from pygame.sprite import Sprite

class Effect(Sprite):
    '''Эффект на фоне'''
    def __init__(self, settings, screen):
        '''Конструктор класса'''
        super(Effect, self).__init__()  #Наследуем свойства класса-родителя Sprite

        #Выводим аргументы на уровень класса
        self.settings = settings
        self.screen = screen

        self.image = pygame.image.load('Data/Images/BackEffect.png')  #Загружаем изображение
        self.image = pygame.transform.scale(self.image, (3600, 2730))

        self.rect = self.image.get_rect()  #Получаем "прямоугольник" объекта
        self.rect.x = -settings.screen['size'][0]*2
        self.rect.y = 0
    
        self.direction = 'Right'

    def update(self):
        ''''Обновление эффекта'''
        self.move()
    

    def move(self):
        '''Движение эффекта'''
        if self.rect.x < 0 and self.direction == 'Right':
            self.rect.x += 1
            self.direction = 'Right'
        elif self.rect.x > self.settings.screen['size'][0]*2:
            self.rect.x -= 1
            self.direction = 'Left'
        else:
            self.direction = 'Right'