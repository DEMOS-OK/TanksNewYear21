import pygame
from math import sin, cos, radians

from pygame.sprite import Sprite
from objects.bullet import Bullet


class Tank(Sprite):
    '''Класс Танк и все его возможности, ага'''
    def __init__(self, settings, screen, player):
        ''''Конструктор класса'''
        super(Tank, self).__init__() #Наследуем свойства класса-родителя Sprite

        #Выводим аргументы на уровень класса
        self.settings = settings
        self.screen   = screen    

        #Определяем какого игрока этот танк
        if player == 1:
            self.tank_type = 'Left'
        elif player == 2:
            self.tank_type = 'Right'

        #Под каким углом стреляет танк
        self.angle = 0  # Число от 0 до 60

        #Всё, что касается изображений
        self.image    = pygame.image.load('Data/Images/Tanks/' + self.tank_type + 'Tank' + str(self.angle) + '.png') #Загружаем изображение
        self.img_path = 'Data/Images/Tanks/' + self.tank_type + 'Tank' + str(self.angle) + '.png' #Сохраняем путь
        self.mask     = pygame.mask.from_surface(self.image) #Делаем маску по прозрачному фону
        self.rect     = self.image.get_rect() #Получаем "прямоугольник" объекта
        self.width    = self.image.get_width() #Получаем ширину объекта
        self.height   = self.image.get_height() #получаем высоту объекта

        #Располагаем в зависимости от номера игрока
        if player == 1: #Первого игрока в левой части
            self.rect.x  = 100
            self.rect.y  = self.settings.screen['size'][1] - 300 - self.height
        elif player == 2: #Второго игрока в правой части
            self.rect.x  = self.settings.screen['size'][0] - 100 - self.width
            self.rect.y  = self.settings.screen['size'][1] - 300 - self.height
        
        #По умолчанию нет движения
        self.moving_right = False #Движется ли танк в данный момент
        self.moving_left  = False
        self.velocity_x   = 4 #Скорость движения танка

        #Сдвиг координат ствола от изначальных при разных углах наклона для танков
        self.offset = {
            'right': {
                'x': {0: 0, 5: -2, 10: -1, 15: -1, 20: -1, 25: -3, 30: -5, 35: -8, 40: -14, 45: -22, 50: -27, 55: -33, 60: -39},
                'y': {0: 0, 5: 12, 10: 20, 15: 28, 20: 40, 25: 49, 30: 58, 35: 65, 40: 71, 45: 75, 50: 80, 55: 86, 60: 91}
            },
            'left': {
                'x': {0: 0, 5: 4, 10: 8, 15: 10, 20: 14, 25: 18, 30: 22, 35: 26, 40: 33, 45: 40, 50: 45, 55: 53, 60: 58},
                'y': {0: 0, 5: 12, 10: 24, 15: 32, 20: 41, 25: 50, 30: 60, 35: 67, 40: 73, 45: 79, 50: 84, 55: 88, 60: 96}
            },
        }
    

    def update(self):
        '''Обновляет события танка'''
        self.move() #Движение танка
        self.update_images() #Обновляем картинки
        self.update_trunk_coords() #Обновляем координаты ствола
        if hasattr(self, 'bullet'): #Обновляем пулю, если существует.
            self.bullet.update()
    

    def move(self):
        '''Движение танка'''
        if self.moving_right: #Движение вправо
            self.rect.x += self.velocity_x
        if self.moving_left: #Движение влево
            self.rect.x -= self.velocity_x
    

    def update_images(self):
        '''Отслеживает изменения путей картинок и обновляет картинки'''

        #Если  изменился угол наклона ствола, то надо обновить картинку
        if self.img_path != 'Data/Images/Tanks/' + self.tank_type + 'Tank' + str(self.angle) + '.png':
            #Загружаем изображение и запоминаем его путь
            self.image = pygame.image.load('Data/Images/Tanks/' + self.tank_type + 'Tank' + str(self.angle) + '.png')
            self.img_path = 'Data/Images/Tanks/' + self.tank_type + 'Tank' + str(self.angle) + '.png'
                

    def update_trunk_coords(self):
        '''Определяет координаты ствола в зависимости от его угла наклона'''

        #Расчёт координат ствола
        if self.tank_type == 'Left':
            self.trunk_x = self.rect.right - self.offset['left']['x'][self.angle]
            self.trunk_y = self.rect.y + self.height*0.45 - self.offset['left']['y'][self.angle]
        else:
            self.trunk_x = self.rect.x - self.offset['right']['x'][self.angle]
            self.trunk_y = self.rect.y + self.height*0.45 - self.offset['right']['y'][self.angle]


    def edit_angle(self, direction):
        '''Меняет угол наклона дула'''
        if direction == 'up':
            if self.angle in range(0, 56):
                self.angle += 5
        elif direction == 'down':
            if self.angle in range(5, 61):
                self.angle -= 5
    

    def fire(self):
        '''Выпускает пульку :D '''
        if self.tank_type == 'Left':
            position = (self.trunk_x, self.trunk_y)
            angle = self.angle
            vx = 20
        elif self.tank_type == 'Right':
            position = (self.trunk_x - 45, self.trunk_y) #Здесь 45 - это ширина пули, слабое место в коде
            angle = -self.angle
            vx = -20

        #Создаём пулю и задаём ей скорость
        self.bullet = Bullet(self.settings, self.screen, position, self.tank_type, angle)
        self.bullet.vx = vx * cos(radians(self.angle))
        self.bullet.vg = -20 * sin(radians(self.angle))
    
