import pygame
from Modules.Text import *
# from Game_CF.Modules.Menu import *
from Modules.Color import *
from pygame.sprite import Sprite
from Modules.Button import *

pygame.init()

display1 = pygame.display.set_mode((0, 0))

spritesFolder = 'Resources/Sprites/'

class Personaje1(Sprite):
    def __init__(self):
        self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(50, 240)
        self.muerto = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        # //////////////////// BOTON PARA ATQUE ESPECIAL PJ1 ////////////////////////
        if teclas[pygame.K_SPACE]:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita7.png").convert_alpha()
        elif ataque.rect.x > 860:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita1.png").convert_alpha()
        # //////////////////// BOTONES PARA GOLPES BÁSICOS PJ1 //////////////////////
        if teclas[pygame.K_r]:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita2.png").convert_alpha()
        elif teclas[pygame.K_t]:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita3.png").convert_alpha()
        elif ataque.rect.x > 860:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita1.png").convert_alpha()
        # //////////////////// BOTONES PARA MOVERSE PJ1 /////////////////////////////
        if teclas[pygame.K_a]:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita1inv.png").convert_alpha()
            if self.rect.x > 0:
                self.rect.x -= 2
        elif teclas[pygame.K_d]:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita1.png").convert_alpha()
            if self.rect.x < 1140:
                self.rect.x += 2
            
        if teclas[pygame.K_w]:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita5.png").convert_alpha()
            if self.rect.y > 0:
                self.rect.y -= 2
        elif teclas[pygame.K_s]:
            self.image = personaje1 = pygame.image.load(spritesFolder + "Melcocha/melcochita6.png").convert_alpha()
            if self.rect.y < 240:
                self.rect.y += 2


# ATAQUE PERSONAJE 1
class AtaqueP1(Sprite):
    def __init__(self):
        self.image = ataque = pygame.image.load(spritesFolder + "Melcocha/lanzamientomelcochita.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(1000, 1500)

    def update(self):
        teclas = pygame.key.get_pressed()
        if self.rect.x > 1400:
            if teclas[pygame.K_SPACE]:
                self.rect.x = (personaje1.rect.x + 60)
                self.rect.y = (personaje1.rect.y + 14)
        if self.rect.x < 1700:
            self.rect.x += 2


# VIDA PERSONAJE 1
class BarraVidaPJ1(Sprite):
    def __init__(self):
        self.image = barravidapj1 = pygame.image.load(spritesFolder + "Imagenes/barravidapj1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(50, 20)

    def update(self):
        if barravidapj1.rect.x <= -152:
            personaje1.muerto = 1
        if disparo.rect.y >= (personaje1.rect.y - 56):
            if disparo.rect.y <= (personaje1.rect.y + 62):
                if disparo.rect.x >= personaje1.rect.x:
                    if disparo.rect.x <= (personaje1.rect.x + 43):
                        barravidapj1.rect.x -= 26
                        disparo.rect.x = -400
        if minicell.rect.y >= (personaje1.rect.y - 56):
            if minicell.rect.y <= (personaje1.rect.y + 62):
                if minicell.rect.x >= personaje1.rect.x:
                    if minicell.rect.x <= (personaje1.rect.x + 43):
                        barravidapj1.rect.x -= 26
                        disparo.rect.x = -400


# /////////////////////////////////////////////--- PERSONAJE 2 ---///////////////////////////////////////

class Personaje2(Sprite):
    def __init__(self):
        self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/parado_izq_magaly.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(1000, 240)
        self.muerto = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_i]:
            self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/atacando_izq_magaly.png").convert_alpha()
        elif ataque.rect.x > 860:
            self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/parado_izq_magaly.png").convert_alpha()

        if teclas[pygame.K_p]:
            self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/mag_puñete_izq.png").convert_alpha()
        elif teclas[pygame.K_o]:
            self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/mag_patada_izq.png").convert_alpha()
        elif ataque.rect.x > 860:
            self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/parado_izq_magaly.png").convert_alpha()

        if teclas[pygame.K_LEFT]:
            self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/derecha_magaly_p2.png").convert_alpha()
            if self.rect.x > 0:
                self.rect.x -= 2
        elif teclas[pygame.K_RIGHT]:
            self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/derecha_magaly_p1.png").convert_alpha()
            if self.rect.x < 1140:
                self.rect.x += 2

        if teclas[pygame.K_UP]:
            self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/magaly_arriba_izq.png").convert_alpha()
            if self.rect.y > 0:
                self.rect.y -= 2
        elif teclas[pygame.K_DOWN]:
            if self.rect.y < 240:
                self.image = personaje2 = pygame.image.load(spritesFolder + "Magaly/magaly_abajo_izq.png").convert_alpha()
                self.rect.y += 2


# ATAQUE PERSONAJE 2
class Disparo(Sprite):
    def __init__(self):
        self.image = barravidapj1 = pygame.image.load("Images/Imagenes/disparominicell.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(-400, -400)

    def update(self):
        if self.rect.x == -400:
            if personaje2.rect.y == personaje1.rect.y:
                self.rect.x = (minicell.rect.x - 60)
                self.rect.y = (minicell.rect.y - 14)
        if self.rect.x > -400:
            self.rect.x -= 5


# if __name__ == '__main__':
#   # Variables.
#   salir = False
#
#   # Establezco la pantalla.
#   screen = pygame.display.set_mode((1200,363))
#
#   # Establezco el título.
#   pygame.display.set_caption("Entregable 4")
#
#   # Creo dos objetos surface.
#   fondo = pygame.image.load("Images/Imagenes/fondo1.png").convert()
#   vidapj1 = pygame.image.load("Images/Imagenes/cuadrovidapj1.png").convert_alpha()
#
#   # Objetos
#   temporizador = pygame.time.Clock()
#   personaje1 = Personaje1()
#   personaje2 = Personaje2()
#   ataque = AtaqueP1()
#   barravidapj1 = BarraVidaPJ1()
#
#   # Movimiento del personaje.
#   while not salir:
#       personaje1.update()
#       personaje2.update()
#       ataque.update()
#
#       # actualizacion grafica
#       screen.blit(fondo, (0, 0))
#       screen.blit(personaje1.image, personaje1.rect)
#       screen.blit(personaje2.image, personaje2.rect)
#       screen.blit(ataque.image, ataque.rect)
#       screen.blit(barravidapj1.image, barravidapj1.rect)
#
#       pygame.display.flip()
#
#       # gestion de eventos
#       for evento in pygame.event.get():
#           if evento.type == pygame.QUIT:
#               salir = True

class Personaje(Sprite):
    def __init__(self, nombre='', vida=100):
        self.nombre = nombre
        self.ataque = ''
        self.vida = vida
        self.image = personaje = pygame.image.load(spritesFolder + "peluchin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(50, 51)
        self.muerto = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            self.image = personaje = pygame.image.load(spritesFolder + "atacando.png").convert_alpha()
        elif ataque.rect.x > 860:
            self.image = personaje = pygame.image.load(spritesFolder + "peluchin.png").convert_alpha()

        if teclas[pygame.K_a]:
            self.image = personaje = pygame.image.load(spritesFolder + "puñete.png").convert_alpha()
        elif teclas[pygame.K_s]:
            self.image = personaje = pygame.image.load(spritesFolder + "patada.png").convert_alpha()
        elif ataque.rect.x > 860:
            self.image = personaje = pygame.image.load(spritesFolder + "peluchin.png").convert_alpha()

        # if teclas[pygame.K_s]:
        #    self.image = personaje = pygame.image.load(spritesFolder + "patada.png").convert_alpha()

        if teclas[pygame.K_LEFT]:
            self.image = personaje = pygame.image.load(spritesFolder + "izquierda.png").convert_alpha()
            if self.rect.x > 0:
                self.rect.x -= 2
        elif teclas[pygame.K_RIGHT]:
            self.image = personaje = pygame.image.load(spritesFolder + "derecha.png").convert_alpha()
            if self.rect.x < 1000:
                self.rect.x += 2

        if teclas[pygame.K_UP]:
            self.image = personaje = pygame.image.load(spritesFolder + "arriba.png").convert_alpha()
            if self.rect.y > 0:
                self.rect.y -= 2
        elif teclas[pygame.K_DOWN]:
            if self.rect.y < 480:
                self.image = personaje = pygame.image.load(spritesFolder + "abajo.png").convert_alpha()
                self.rect.y += 2

    def health_bar(self, display):
        pos = (20, 25, 400, 40)
        bar_width = self.vida * 4
        bar = (20, 25, bar_width, 40)

        pygame.draw.rect(display1, pygame.Color('white'), pos, 0)
        pygame.draw.rect(display1, pygame.Color('green'), bar, 0)
        pygame.draw.rect(display1, pygame.Color('black'), pos, 5)


class Ataque(Sprite):
    def __init__(self):
        self.image = ataque = pygame.image.load(spritesFolder + "ataque.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(1000, 1500)

    def update(self):
        teclas = pygame.key.get_pressed()
        if self.rect.x > 1400:
            if teclas[pygame.K_SPACE]:
                self.rect.x = (personaje.rect.x + 60)
                self.rect.y = (personaje.rect.y + 14)
        if self.rect.x < 1700:
            self.rect.x += 2


personaje = Personaje()
ataque = Ataque()
fondo = pygame.image.load(spritesFolder + "AMOR.jpg").convert()
personaje1 = Personaje1()
personaje2 = Personaje2()
ataque = AtaqueP1()
barravidapj1 = BarraVidaPJ1()


class MainGame:
    def __init__(self, display):
        pygame.init()
        self.display = display
        self.clock = pygame.time.Clock()

    def game(self):
        self.display = pygame.display.set_mode((1200, 363))

        fondo = pygame.image.load(spritesFolder + "Imagenes/fondo1.png").convert()
        vidapj1 = pygame.image.load(spritesFolder + "Imagenes/cuadrovidapj1.png").convert_alpha()

        # Objetos
        # temporizador = pygame.time.Clock()
        # personaje1 = Personaje1()
        # personaje2 = Personaje2()
        # ataque = AtaqueP1()
        # barravidapj1 = BarraVidaPJ1()
        # menu = Menu()

        while 1:
            personaje1.update()
            personaje2.update()
            ataque.update()

            self.display.blit(fondo, (0, 0))
            self.display.blit(personaje1.image, personaje1.rect)
            self.display.blit(personaje2.image, personaje2.rect)
            self.display.blit(ataque.image, ataque.rect)
            self.display.blit(barravidapj1.image, barravidapj1.rect)

            pygame.display.flip()

            # gestion de eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # button = Button('Salir', 1010, 25, 125, 50, black, bright_red, 35, self.game_quit)
            # # button = Button('Salir', 1010, 25, 125, 50, black, bright_red, 35, menu.game_menu)
            # button.draw_button(self.display)

            pygame.display.update()
            self.clock.tick()

    @staticmethod
    def game_quit():
        pygame.quit()
        quit()
