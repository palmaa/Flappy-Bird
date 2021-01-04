import pygame
import sys
import random

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


def crear_tuberia(altura_tuberias):
    """
    Crea una nueva tubería en cada iteración del juego
    esta tubería será añadida a la lista de tuberías
    350 es para que la tubería se genere fuera de la pantalla y el
    spawn no sea brusco
    150 == espacio entre tubería superior e inferior
    :return: (rect, rect)
    """
    posicion_tuberia = random.choice(altura_tuberias)
    tuberia_inferior = superficie_tuberia.get_rect(midtop = (300, posicion_tuberia))
    tuberia_superior = superficie_tuberia.get_rect(midbottom = (300, posicion_tuberia-180))
    return tuberia_inferior,tuberia_superior


def mover_tuberias(lista_tuberias):
    """
    Va a ir moviendo las tuberías que hemos creado y almacenado en la lista a lo
    largo de la pantalla. Para moverlas, lo que va a hacer es ir desplazando
    las tuberías a la izquierda (2.5 unidades)
    :param lista_tuberias: [rect]
    :return: lista_tuberias: [rect]
    """
    for tuberia in lista_tuberias:
        tuberia.centerx -= 2.5
    return lista_tuberias

def dibujar_tuberias(lista_tuberias):
    for tuberia in lista_tuberias:
        #Solo la tubería inferior puede cumplir esta condicion
        if tuberia.bottom >= 512:
            screen.blit(superficie_tuberia, tuberia)
        else:
            girar_tuberia = pygame.transform.flip(superficie_tuberia, False, True)
            screen.blit(girar_tuberia, tuberia)


pygame.init()

#Variables del juego
GRAVEDAD = 0.125
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

superficie_tuberia = pygame.image.load('assets/pipe-green.png').convert()
"""
Ahora ya no queremos solo poner un tubería en pantalla, sino que queremos poner
tuberías constantemente en pantalla, por lo que el proceso de convertirlo en un
rectángulo y usarlo va a ser distinto
"""

lista_tuberias = []

"""
Para que las tuberías se creen cada cierto tiempo, vamos a usar un timer con la variable
SPAWNPIPE.
El primer parámetro es qué queremos que cree, el segundo cada cuanto (ms)
"""

spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)


"""
Estas serán las posibles alturas en que se puedan generar tuberías. Cada vez que generemos una,
escogeremos un valor aleatorio de esta lista
"""
altura_tuberias = [220, 300, 400]


while True:


    #Comprovamos los eventos que vayan sucediendo en el juego

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
                movimiento_pajaro -= 6

        if event.type == spawnpipe:
            lista_tuberias.extend(crear_tuberia(altura_tuberias))


    #Dibujamos el background

    screen.blit(backgorund, (0,0))

    #Dibujamos el pájaro

    movimiento_pajaro += GRAVEDAD
    pajaro_rect.centery += movimiento_pajaro
    screen.blit(pajaro, pajaro_rect)

    #Dibujamos la tubería

    lista_tuberias = mover_tuberias(lista_tuberias)
    dibujar_tuberias(lista_tuberias)

    #Dibujamos el suelo

    x_suelo -= 1
    dibujar_suelo()

    """
    Compruebo que el suelo de la derecha no vaya a tocar el limite derecho de la pantalla
    en la siguiente iteración del bucle. Si lo hace, vuelvo a poner el suelo en su posición inicial
    """
    if(x_suelo <= -288):
        x_suelo = 0

    # Hacemos un update de los elementos de la pantalla con las nuevas posiciones

    pygame.display.update()
    #120 == max FPS
    clock.tick(120)