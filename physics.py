import pygame

class Physics():
    '''Класс, отвечающий за физику в игре'''
    def __init__(self, settings, screen, earth):
        self.settings = settings
        self.screen = screen

        self.earth = earth #Главный объект физики, ага

        self.g = 0.5 #Ускорение свободного падения
        self.vg = 0 #Скорость падения объектов


    def gravitation(self, obj):
        '''Подвергает какой-то объект действию силы тяжести'''

        #Притягиваем объект к Земле, если он не контактирует с Землёй
        if not pygame.sprite.collide_mask(self.earth, obj):
            if hasattr(obj, 'vg'):
                obj.rect.y += obj.vg #двигаем объект вниз
                obj.vg += self.g #увеличиваем скорость объекта на ускорение свободного падения
            else:
                obj.vg = self.vg
        else:
            obj.vg = self.vg #сбрасываем скорость
    

    def barrier(self, obj):
        '''Запрещает движение в опредёленных направлениях'''

        #Запрещаем въезжать на холм
        if obj.rect.x in range(230, 780):
            if obj.rect.x < 300:
                obj.moving_right = False
            else:
                obj.moving_left = False
        
        #Ограничения по экрану
        if obj.rect.x <= 0:
            obj.moving_left = False
        
        if (obj.rect.x + obj.width) >= self.settings.screen['size'][0]:
            obj.moving_right = False
        
