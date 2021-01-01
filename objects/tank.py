import pygame
from pygame.sprite import Sprite

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
        self.angle = 15  # Число от 0 до 60

        self.image  = pygame.image.load('Data/Images/Tanks/' + self.tank_type + 'Tank' + str(self.angle) + '.png') #Загружаем изображение
        self.mask   = pygame.mask.from_surface(self.image) #Делаем маску по прозрачному фону
        self.rect   = self.image.get_rect() #Получаем "прямоугольник" объекта
        self.width  = self.image.get_width()
        self.height = self.image.get_height()

        #Располагаем в зависимости от номера игрока
        if player == 1:
            self.rect.x  = 100
            self.rect.y  = self.settings.screen['size'][1] - 300 - self.height
        elif player == 2:
            self.rect.x  = self.settings.screen['size'][0] - 100 - self.width
            self.rect.y  = self.settings.screen['size'][1] - 300 - self.height
        
        #По умолчанию нет движения
        self.moving_right = False
        self.moving_left  = False
        self.velocity_x = 4
    

    def update(self):
        '''Обновляет события танка'''
        self.move()
        self.update_images()
    

    def move(self):
        '''Движение танка'''
        if self.moving_right:
            self.rect.x += self.velocity_x
        if self.moving_left:
            self.rect.x -= self.velocity_x
    

    def update_images(self):
        '''Отслеживает изменения путей картинок и обновляет картинки'''
        self.image = pygame.image.load(
            'Data/Images/Tanks/' + self.tank_type + 'Tank' + str(self.angle) + '.png')  # Загружаем изображение


    def edit_angle(self, direction):
        '''Меняет угол наклона дула'''
        if direction == 'up':
            if self.angle in range(0, 56):
                self.angle += 5
        elif direction == 'down':
            if self.angle in range(5, 61):
                self.angle -= 5

    
