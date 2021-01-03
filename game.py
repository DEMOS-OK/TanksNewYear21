import pygame

from physics import Physics
from objects.tank import Tank
from objects.earth import Earth
from objects.label import Label
from objects.bg_effect import Effect

class Game():
    '''Основной класс игры, связывающий всё воедино'''
    def __init__(self, settings, screen):
        '''Конструктор класса'''
        
        #Вывод главных объектов на уровень класса
        self.settings = settings
        self.screen   = screen
    
        #Идёт игра или нет (для меню)
        self.status = True

        #Инициализация объектов
        self.init_game_objects()
        self.physics = Physics(self.settings, self.screen, self.earth)


    def init_game_objects(self):
        '''Инициализирует игровые объекты'''

        #Танки
        self.tank1 = Tank(self.settings, self.screen, 1)
        self.tank2 = Tank(self.settings, self.screen, 2)

        #Земля
        self.earth = Earth(self.settings, self.screen)

        #Фоновый эффект
        self.effect = Effect(self.settings, self.screen)

        #Метки
        self.hp1 = Label(self.settings, self.screen, self.tank1.health, 100, 50) #Здоровье
        self.hp2 = Label(self.settings, self.screen, self.tank2.health, self.settings.screen['size'][0] - 100, 50)

        self.power1 = Label(self.settings, self.screen, self.tank1.power, 100, 75) #Сила атаки
        self.power2 = Label(self.settings, self.screen, self.tank2.power, self.settings.screen['size'][0] - 100, 75)

        self.move_instr1 = Label(self.settings, self.screen, '', 100, 100) #Управление
        self.attack_instr1 = Label(self.settings, self.screen, '', 100, 125)
        self.move_instr2 = Label(self.settings, self.screen, '', self.settings.screen['size'][0] - 100, 100)
        self.attack_instr2 = Label(self.settings, self.screen, '', self.settings.screen['size'][0] - 100, 125)

        #Метка победителя
        self.winner = Label(self.settings, self.screen, '', self.settings.screen['size'][0]//2, self.settings.screen['size'][1]//2)


    def update(self):
        '''Обновляет все игровые события'''
        while True:
            self.check_events() #Проверяем события
            self.draw_game() #Рисуем игровые объекты
            self.object_physics() #Обновляем события в мире физики для объектов, ага
            self.update_objects() #Обновляем объекты
            self.update_labels() #Обновляем тексты меток

            pygame.display.flip() #Перерисовываем кадр
    
    
    def check_events(self):
        '''Проверяет игровые события'''
        for event in pygame.event.get():
            #Выход из игры при нажатии на крестик
            if event.type == pygame.QUIT:
                exit()
            
            #Обработка нажатий с клавиатуры
            if self.status:
                self.check_key_events(event)
    

    def check_key_events(self, event):
        '''Проверяет события на нажатие клавиш'''
        
        #Словари типа {кнопка: действие}
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
        fire_dict = {
            pygame.K_g: '1_fire',
            pygame.K_k: '2_fire',
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
                command = command.replace('[direction]', "\'" + direction[1] + "\'")
                exec(command)
            
            #Стреляем из нужного танка
            if event.key in fire_dict.keys() and event.type == pygame.KEYUP:
                command = 'self.tank' + fire_dict[event.key].split('_')[0] + '.fire()'
                exec(command)
    

    def draw_game(self):
        ''''Рисует все игровые объекты'''
        self.screen.blit(self.settings.screen['bg'], (0, 0)) # Рисуем фон
        
        if self.settings.screen['graphics']:
            self.screen.blit(self.effect.image, (self.effect.rect.x, self.effect.rect.y)) #Рисуем фоновый эффект

        #Если игра активна, то рисуем все игровые объекты, иначе конечный экран
        if self.status:

            #Рисуем землю
            self.screen.blit(self.earth.image, (self.earth.rect.x, self.earth.rect.y))


            #Рисуем танки и их снаряды
            self.screen.blit(self.tank1.image, (self.tank1.rect.x, self.tank1.rect.y))
            if hasattr(self.tank1, 'bullet'):
                self.screen.blit(self.tank1.bullet.rotated_image, (self.tank1.bullet.rect.x, self.tank1.bullet.rect.y))

            self.screen.blit(self.tank2.image, (self.tank2.rect.x, self.tank2.rect.y))
            if hasattr(self.tank2, 'bullet'):
                self.screen.blit(self.tank2.bullet.rotated_image, (self.tank2.bullet.rect.x, self.tank2.bullet.rect.y))
            

            #Отрисовываем метки
            self.hp1.show_text()
            self.hp2.show_text()
            self.power1.show_text()
            self.power2.show_text()
            self.move_instr1.show_text()
            self.move_instr2.show_text()
            self.attack_instr1.show_text()
            self.attack_instr2.show_text()
        else:
            self.winner.show_text()


    def object_physics(self):
        '''Обновляет все физические события для объектов'''

        #Подвергаем танки воздействию гравитации
        self.physics.gravitation(self.tank1)
        self.physics.gravitation(self.tank2)

        #Если есть снаряд, то подвергаем его гравитации и коллизиям
        if hasattr(self.tank1, 'bullet'):
            self.physics.gravitation(self.tank1.bullet)
            self.physics.collisions(self.tank2, self.tank1)
        if hasattr(self.tank2, 'bullet'):
            self.physics.gravitation(self.tank2.bullet)
            self.physics.collisions(self.tank1, self.tank2)

        #Ограничиваем движения по холмам и уход за границы
        self.physics.barrier(self.tank1)
        self.physics.barrier(self.tank2)

    

    def update_objects(self):
        '''Обновляет объекты'''
        self.tank1.update()
        self.tank2.update()
        self.effect.update()

        if self.tank1.health <= 0 or self.tank2.health <= 0:
            self.status = False
    

    def update_labels(self):
        '''Обновляет тексты меток'''
        #Метки хп
        self.hp1.text = 'Health: ' + str(self.tank1.health)
        self.hp1.prepare_text()
        self.hp2.text = 'Health: ' + str(self.tank2.health)
        self.hp2.prepare_text()

        #Метки мощности
        self.power1.text = 'Power: ' + str(self.tank1.power)
        self.power1.prepare_text()
        self.power2.text = 'Power: ' + str(self.tank2.power)
        self.power2.prepare_text()

        #Метки с инструкциями
        self.move_instr1.text = 'Движение: w, a, s, d'
        self.move_instr1.prepare_text()
        self.attack_instr1.text = 'Атака: G'
        self.attack_instr1.prepare_text()
        self.move_instr2.text = 'Движение: up, left, down, right'
        self.move_instr2.prepare_text()
        self.attack_instr2.text = 'Атака: K'
        self.attack_instr2.prepare_text()

        #Метка победителя
        if not self.status:
            self.winner.text = 'Выиграл игрок #' + str(1 if self.tank2.health <= 0 else 2)
            self.winner.prepare_text()

