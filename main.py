import pygame
import sys

def dibujar_suelo():
    """
    Dibujamos dos suelos: uno al lado del otro
    de forma que cuando el de la derecha toque el limite derecho de la pantalla
    el de la izquierda vuelva a aparecer en pantalla
    dando así sensación de movimiento
    :return: None
    """
    screen.blit(suelo, (x_suelo,y_suelo))
    screen.blit(suelo, (x_suelo+288,y_suelo))



pygame.init()

#Variables del juego
GRAVEDAD = 0.25
movimiento_pajaro = 0

screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
backgorund = pygame.image.load('assets/background-day.png').convert()

suelo = pygame.image.load('assets/base.png').convert()
x_suelo = 0
y_suelo = 450

pajaro = pygame.image.load('assets/bluebird-midflap.png').convert()

"""
Los parámetros de rect son: donde queremos el pajaro respecto al rectángulo
y dónde ponemos el rectángulo (50, 256); en medio de la pantalla en altura y desplazado
a la izquierda en anchura.
"""
pajaro_rect = pajaro.get_rect(center = (50, 256))



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #Si el jugador da a la cruz, cerraremos el juego
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #Si el jugador la da a una tecla y es el espacio, el pájaro va a saltar
                """
                Con la primera linea, conseguimos que al saltar no haya gravedad
                por lo que el salto se puede producir, en caso contrario
                solo mantendríamos al pajaro contrarrestando la gravedad
                pero jamás iria hacia arriba
                """
                movimiento_pajaro = 0
                movimiento_pajaro -= 12

    screen.blit(backgorund, (0,0))

    movimiento_pajaro += GRAVEDAD
    pajaro_rect.centery += movimiento_pajaro

    screen.blit(pajaro, pajaro_rect)
    x_suelo -= 1
    dibujar_suelo()

    """
    Compruebo que el suelo de la derecha no vaya a tocar el limite derecho de la pantalla
    en la siguiente iteración del bucle. Si lo hace, vuelvo a poner el suelo en su posición inicial
    """
    if(x_suelo <= -288):
        x_suelo = 0


    pygame.display.update()
    #120 == max FPS
    clock.tick(120)