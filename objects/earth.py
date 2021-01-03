import pygame
from pygame.sprite import Sprite


class Earth(Sprite):
    '''Класс Земля и все его возможности, ага'''

    def __init__(self, settings, screen):
        '''Конструктор класса'''
        super(Earth, self).__init__()  #Наследуем свойства класса-родителя Sprite

        #Выводим аргументы на уровень класса
        self.settings = settings
        self.screen = screen

        self.image = pygame.image.load('Data/Images/Earth.png')  #Загружаем изображение

        #Делаем маску по прозрачному фону
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()  #Получаем "прямоугольник" объекта
