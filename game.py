import pygame

from physics import Physics
from objects.tank import Tank
from objects.earth import Earth

class Game():
    '''Основной класс игры, связывающий всё воедино'''
    def __init__(self, settings, screen):
        '''Конструктор класса'''
        
        self.settings = settings
        self.screen   = screen
    
        self.status = True

        self.init_game_objects()
        self.physics = Physics(self.settings, self.screen, self.earth)


    def init_game_objects(self):
        '''Инициализирует игровые объекты'''
        self.tank1 = Tank(self.settings, self.screen, 1)
        self.tank2 = Tank(self.settings, self.screen, 2)

        self.earth = Earth(self.settings, self.screen)


    def update(self):
        '''Обновляет все игровые события'''
        while self.status:
            self.check_events() #Проверяем события
            self.draw_game() #Рисуем игровые объекты
            self.object_physics() #Обновляем события в мире физики для объектов, ага
            self.update_objects() #Обновляем объекты

            pygame.display.flip()
    
    
    def check_events(self):
        '''Проверяет игровые события'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            self.check_key_events(event)
    

    def check_key_events(self, event):
        '''Проверяет события на нажатие клавиш'''
        moving_dict = {
            pygame.K_a: '1_left',
            pygame.K_d: '1_right',
            pygame.K_LEFT: '2_left',
            pygame.K_RIGHT: '2_right',

        }
        angle_dict = {
            pygame.K_w: '1_up',
            pygame.K_s: '1_down',
            pygame.K_UP: '2_up',
            pygame.K_DOWN: '2_down',
        }

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

            #Выбираем нужное направление движения нужному танку
            if event.key in moving_dict.keys():
                command = 'self.tank(n).moving_(dir) = (keydown)'
                direction = moving_dict[event.key].split('_')
                command = command.replace('(n)', direction[0])
                command = command.replace('(dir)', direction[1])
                command = command.replace('(keydown)', str(event.type == pygame.KEYDOWN))
                exec(command)
            
            #Направляем дуло танка в нужном направлении
            if event.key in angle_dict.keys() and event.type == pygame.KEYUP:
                command = 'self.tank(n).edit_angle([direction])'
                direction = angle_dict[event.key].split('_')
                command = command.replace('(n)', direction[0])
                command = command.replace(
                    '[direction]', "\'" + direction[1] + "\'")
                exec(command)
    

    def draw_game(self):
        ''''Рисует все игровые объекты'''
        self.screen.blit(self.settings.screen['bg'], (0, 0)) # Рисуем фон

        #Рисуем землю
        self.screen.blit(self.earth.image, (self.earth.rect.x, self.earth.rect.y))

        #Рисуем танки
        self.screen.blit(self.tank1.image, (self.tank1.rect.x, self.tank1.rect.y))
        self.screen.blit(self.tank2.image, (self.tank2.rect.x, self.tank2.rect.y))
    

    def object_physics(self):
        '''Обновляет все физические события для объектов'''

        #Подвергаем танки воздействию гравитации
        self.physics.gravitation(self.tank1)
        self.physics.gravitation(self.tank2)

        #Ограничиваем движения по холмам
        self.physics.barrier(self.tank1)
        self.physics.barrier(self.tank2)
    

    def update_objects(self):
        '''Обновляет объекты'''
        self.tank1.update()
        self.tank2.update()

