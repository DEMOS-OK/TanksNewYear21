import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Снаряд танка и все его фичи, ага'''
    def __init__(self, settings, screen, position, tank_type, angle):
        '''Конструктор класса'''

        #Выводим аргументы на уровень класса
        self.settings = settings
        self.screen   = screen

        #Определяем какого игрока этот танк
        self.tank_type = tank_type

        self.angle = angle #Под каким углом летит пуля
        self.vx = 0 #x-составляющая скорости
        self.vg = 0 #y-составляющая скорости
        
        #Подготовливаем спрайт к работе
        self.image  = pygame.image.load('Data/Images/Bullets/' + self.tank_type + 'Bullet.png') #Загружаем изображение
        self.image  = pygame.transform.scale(self.image, (45, 45)) #Уменьшаем размер
        self.mask   = pygame.mask.from_surface(self.image) #Делаем маску по прозрачному фону
        self.rect   = self.image.get_rect() #Получаем "прямоугольник" объекта
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.width  = self.image.get_width()
        self.height = self.image.get_height()

        #Поворачиваем изображение.
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        #Здесь image - это эталон изображения
        #А rotated_image - его повёрнутая версия. Каждый при повороте мы поворачиваем эталон.
        #Необходимо, чтобы минимизировать число артефактов
    

    def update(self):
        '''Обновляет пулю'''
        if self.vx != 0 and self.vg != 0:
            self.move() #Двигаем пулю
            self.update_rotation() #Наклон пули под действием Fт
    

    def move(self):
        '''Перемещает пулю в пространстве'''
        self.rect.x += self.vx
        self.rect.y += self.vg
    

    def update_rotation(self):
        '''Отвечает за наклон пули под действием силы тяжести'''
        if self.tank_type == 'Left':
            angle_diff = 2 #Изменение угла наклона
        else:
            angle_diff = -2

        self.rotated_image = pygame.transform.rotate(self.image, self.angle) #Поворачиваем эталонное изображение
        self.angle -= angle_diff
