import pygame
import sys
import random
import time

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


def comprovar_colision(lista_tuberias, pajaro_rect):
    """
    Comprueva si el pájaro colisiona con la tubería, ya sea la superior
    o la inferior
    Además, comprovamos que el jugador no sobrevuele la pantalla ni colisione
    contra el suelo
    :param lista_tuberias: [rect]
    :return: bool
    """

    #Colision con la tuberia
    for tuberia in lista_tuberias:
        if pajaro_rect.colliderect(tuberia):
            sonido_muerte.play()
            return True

    #Está en la pantalla
    if pajaro_rect.top <= -100 or pajaro_rect.bottom >= y_suelo:
        return True


    return False


def rotar_pajaro(pajaro, movimiento_pajaro):
    """
    Rota al pajaro hacia arriba o hacia abajo según esté cayendo o volando
    para dar mayor sensacion de movimiento
    :param pajaro: rect
    :param movimiento_pajaro: int
    :return: rect
    """
    nuevo_pajaro = pygame.transform.rotozoom(pajaro, -movimiento_pajaro*2, 1)
    return nuevo_pajaro


def animacion_pajaro(lista_pajaros, indice, rect):
    """
    Devuelve al pajaro con un aleteo distinto cada vez
    :param lista_pajaros: [img]
    :param indice: int
    :param rect: pajaro_rect
    :return: superficie, rect
    """
    pajaro = lista_pajaros[indice]
    pajaro_rect = pajaro.get_rect(center = (50, rect.centery))
    return pajaro, pajaro_rect

def mostrar_puntuacion(puntuacion, estado_juego, max_punt):

    """
    Muestra la puntuación por pantalla, haciendole algunos retoques explicados en el
    punto 9 del archivo coding.txt
    :param puntuacion: int
    :param estado_juego: str
    :return: None
    """

    if estado_juego == 'Juego_principal':
        if puntuacion > 0:
            puntuacion = int((puntuacion)/17)
        superficie_puntuacion = fuente.render(str(puntuacion), True, (255,255,255))
        puntuacion_rect = superficie_puntuacion.get_rect(center = (144, 50))
        screen.blit(superficie_puntuacion, puntuacion_rect)

    if estado_juego == 'Game_over':
        if puntuacion > 0:
            puntuacion = int((puntuacion)/17)
        superficie_puntuacion = fuente.render(f'Score: {puntuacion}', True, (255,255,255))
        puntuacion_rect = superficie_puntuacion.get_rect(center = (144, 50))
        screen.blit(superficie_puntuacion, puntuacion_rect)
        max_puntuacion = actualizar_puntuacion(puntuacion, max_punt)
        superficie_max_puntuacion = fuente.render(f'High Score: {max_puntuacion}', True, (255,255,255))
        puntuacion_max_rect = superficie_max_puntuacion.get_rect(center = (144, 425))
        screen.blit(superficie_max_puntuacion, puntuacion_max_rect)





def comprovar_aumento(lista_tuberias, pajaro_rect, puntuacion):

    """
    Comprueva que el pajaro pase por la tubería para aumentar la puntuación
    :param lista_tuberias: [rect]
    :param pajaro_rect: rect
    :param puntuacion: int
    :return: int
    """
    #sonar = True
    for tuberia in lista_tuberias:

        if pajaro_rect.centerx > tuberia.midleft[0] and pajaro_rect.centerx < tuberia.midright[0]:
            puntuacion += 1
            #if sonar:
                #sonido_punto.play()
                #sonar = False
            return puntuacion

    return puntuacion


def actualizar_puntuacion(puntuacion, max_puntuacion):
    if int(puntuacion/17) > max_puntuacion:
        max_puntuacion = (puntuacion/17)

    return max_puntuacion



pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=256)
pygame.init()

fuente = pygame.font.Font('04B_19.TTF', 20)
inicio = time.time()

#Variables del juego
GRAVEDAD = 0.125
movimiento_pajaro = 0
colision = False
puntuacion = 0
max_puntuacion = 0
puntuacion_comprovada = False

screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
backgorund = pygame.image.load('assets/background-day.png').convert()


suelo = pygame.image.load('assets/base.png').convert()
x_suelo = 0
y_suelo = 450

#El código está comentado ya que este código es sin animaciones
#pajaro = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()

"""
Los parámetros de rect son: donde queremos el pajaro respecto al rectángulo
y dónde ponemos el rectángulo (50, 256); en medio de la pantalla en altura y desplazado
a la izquierda en anchura.
"""
#El código está comentado ya que este código es sin animaciones
#pajaro_rect = pajaro.get_rect(center = (50, 256))

pajaro_abajo = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
pajaro_medio = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
pajaro_arriba = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
lista_pajaros = [pajaro_abajo, pajaro_medio, pajaro_arriba]
indice_lista_pajaros = 0
pajaro = lista_pajaros[indice_lista_pajaros]
pajaro_rect = pajaro.get_rect(center = (50,256))

aleteo_pajaro = pygame.USEREVENT+1
pygame.time.set_timer(aleteo_pajaro, 200)

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


"""
Imagen que se verá cuando muramos
"""

game_over = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over.get_rect(center = (144,256))


"""
Importamos los sonidos del juego
"""

sonido_aleteo = pygame.mixer.Sound('sound/sfx_wing.wav')
sonido_muerte = pygame.mixer.Sound('sound/sfx_hit.wav')
sonido_punto = pygame.mixer.Sound('sound/sfx_point.wav')

while True:


    #Comprovamos los eventos que vayan sucediendo en el juego

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #Si el jugador da a la cruz, cerraremos el juego
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not colision:
                #Si el jugador la da a una tecla y es el espacio, el pájaro va a saltar
                """
                Con la primera linea, conseguimos que al saltar no haya gravedad
                por lo que el salto se puede producir, en caso contrario
                solo mantendríamos al pajaro contrarrestando la gravedad
                pero jamás iria hacia arriba
                Además, sonará el ruidito del aleteo
                """
                sonido_aleteo.play()
                movimiento_pajaro = 0
                movimiento_pajaro -= 6

            #Si el jugador choca y le da al espacio, resetea el juego
            if event.key == pygame.K_SPACE and colision:
                #Haremos que el jugador vuelva a poder jugar
                colision = False
                #Eliminaremos las tuberias de la partida anterior
                lista_tuberias.clear()
                #Resetearemos la posición del pájaro
                pajaro_rect.center = (50, 256)
                movimiento_pajaro = 0
                #Reseteamos puntuacion
                puntuacion = 0

        if event.type == spawnpipe:
            lista_tuberias.extend(crear_tuberia(altura_tuberias))

        if event.type == aleteo_pajaro:
            if (indice_lista_pajaros < 2):
                indice_lista_pajaros += 1
            else:
                indice_lista_pajaros = 0

            pajaro, pajaro_rect = animacion_pajaro(lista_pajaros, indice_lista_pajaros, pajaro_rect)

    #Dibujamos el background

    screen.blit(backgorund, (0,0))

    if not colision:

        #Dibujamos el pájaro

        movimiento_pajaro += GRAVEDAD
        pajaro_rotado = rotar_pajaro(pajaro, movimiento_pajaro)
        pajaro_rect.centery += movimiento_pajaro
        screen.blit(pajaro_rotado, pajaro_rect)

        #Comprovamos si hay colision

        colision = comprovar_colision(lista_tuberias, pajaro_rect)

        #Dibujamos la tubería

        lista_tuberias = mover_tuberias(lista_tuberias)
        dibujar_tuberias(lista_tuberias)

        #Mostramos la puntuación
        max_puntuacion = int(actualizar_puntuacion(puntuacion, max_puntuacion))
        mostrar_puntuacion(puntuacion, 'Juego_principal', max_puntuacion)

        #Comprovaremos si debemos aumentar la puntuación
        puntuacion = comprovar_aumento(lista_tuberias, pajaro_rect, puntuacion)


    #En caso de que haya colision, mostraremos por pantalla la puntuacion y el record
    else:
        screen.blit(game_over, game_over_rect)
        mostrar_puntuacion(puntuacion, 'Game_over', max_puntuacion)


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
