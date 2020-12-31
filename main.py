import pygame
from settings import Settings
from game     import Game

def start():
    #Инициализируем класс с игровыми настройками
    settings = Settings()

    #Запускаем библиотеку
    pygame.init()

    #Настраиваем дисплей
    screen = pygame.display.set_mode(settings.screen['size'])
    pygame.display.set_caption('Tanks New Year')

    #Инициализируем основной класс и запускаем игровой процесс
    game = Game(settings, screen)
    game.update()



#Разрешаем запускать только напрямую.
if __name__ == '__main__':
    start()
