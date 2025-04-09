import pygame
import random
import time

# Inicialización de pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Carrera y Obstáculos")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Definición de la clase para el carro
class Carro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 6.5
        self.invulnerable = False  # Estado de inmunidad
        self.invulnerable_time = 0  # Tiempo de activación de la inmunidad

    def update(self, keys):
        # Mover el carro con las teclas de dirección
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

        # Verificar si el poder de inmunidad ha expirado
        if self.invulnerable and time.time() - self.invulnerable_time > 3:  # 3 segundos de inmunidad
            self.invulnerable = False

# Definición de la clase para los obstáculos
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = -50
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -50
            self.rect.x = random.randint(0, SCREEN_WIDTH - 50)

# Definición de la clase para los power-ups
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = -30
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -30
            self.rect.x = random.randint(0, SCREEN_WIDTH - 30)

# Función para mostrar texto en pantalla
def mostrar_texto(texto, tamaño, color, x, y):
    font = pygame.font.SysFont("arial", tamaño)
    texto_surface = font.render(texto, True, color)
    screen.blit(texto_surface, (x, y))

# Función principal del juego
def juego():
    # Crear los grupos de sprites
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()

    # Crear el carro
    carro = Carro()
    all_sprites.add(carro)

    # Variables de puntuación
    puntuacion = 0
    tiempo_power_up = 0  # Control del tiempo desde que se recogió el power-up
    power_up_activo = False

    # Bucle principal del juego
    game_running = True
    while game_running:
        screen.fill(WHITE)
        
        # Comprobar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Actualizar el carro
        carro.update(keys)

        # Crear obstáculos y power-ups con menor frecuencia
        if random.random() < 0.01:  # Reducir la frecuencia de obstáculos
            obstaculo = Obstaculo()
            all_sprites.add(obstaculo)
            obstacles.add(obstaculo)

        if random.random() < 0.005:  # Reducir la frecuencia de power-ups
            power_up = PowerUp()
            all_sprites.add(power_up)
            power_ups.add(power_up)

        # Actualizar obstáculos y power-ups
        obstacles.update()
        power_ups.update()

        # Comprobar colisiones con obstáculos
        if pygame.sprite.spritecollide(carro, obstacles, False):
            # Si el jugador no es invulnerable, se acaba el juego
            if not carro.invulnerable:
                mostrar_texto("¡GAME OVER!", 50, RED, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
                pygame.display.update()
                time.sleep(2)
                game_running = False

        # Comprobar si se recoge un power-up
        power_up_colision = pygame.sprite.spritecollide(carro, power_ups, True)
        if power_up_colision:
            puntuacion += 10  # Sumar puntos al recoger el power-up
            carro.invulnerable = True  # Activar inmunidad
            carro.invulnerable_time = time.time()  # Registrar el tiempo de activación
            power_up_activo = True

        # Aumentar la puntuación por el tiempo que pasa si el power-up está activo
        if carro.invulnerable:
            puntuacion += 1  # Aumentar puntos por segundo mientras la inmunidad está activa

        # Mostrar la puntuación
        mostrar_texto(f"Puntuación: {puntuacion}", 30, BLACK, 10, 10)

        # Dibujar todos los sprites
        all_sprites.draw(screen)

        # Actualizar pantalla
        pygame.display.update()

        # Control de FPS
        clock.tick(FPS)

# Ejecutar el juego
if __name__ == "__main__":
    juego()
    pygame.quit()
