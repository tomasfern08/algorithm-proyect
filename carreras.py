import pygame 
import random
import time

# Inicialización de pygame
pygame.init()
pygame.mixer.init()  # Inicializa el módulo de audio

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Carrera y Obstáculos")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Variables para las líneas de carretera
linea_ancho = 10
linea_alto = 40
espacio_lineas = 30
velocidad_lineas = 5

# Crear lista de líneas
lineas = []
for i in range(0, SCREEN_HEIGHT, linea_alto + espacio_lineas):
    lineas.append(i)

class Carro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pngegg.png")
        self.image = pygame.transform.scale(self.image, (150, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 6.5
        self.invulnerable = False
        self.invulnerable_time = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

        if self.invulnerable and time.time() - self.invulnerable_time > 3:
            self.invulnerable = False

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("afanador.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = -50
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -50
            self.rect.x = random.randint(0, SCREEN_WIDTH - 50)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("powerup.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = -30
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -30
            self.rect.x = random.randint(0, SCREEN_WIDTH - 30)

def mostrar_texto(texto, tamaño, color, x, y):
    font = pygame.font.SysFont("arial", tamaño)
    texto_surface = font.render(texto, True, color)
    screen.blit(texto_surface, (x, y))

def juego():
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()

    carro = Carro()
    all_sprites.add(carro)

    puntuacion = 0
    game_running = True

    while game_running:
        screen.fill(BLACK)

        for i in range(len(lineas)):
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - linea_ancho//2, lineas[i], linea_ancho, linea_alto))
            lineas[i] += velocidad_lineas
            if lineas[i] > SCREEN_HEIGHT:
                lineas[i] = -linea_alto

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        keys = pygame.key.get_pressed()
        carro.update(keys)

        if random.random() < 0.01:
            obstaculo = Obstaculo()
            all_sprites.add(obstaculo)
            obstacles.add(obstaculo)

        if random.random() < 0.005:
            power_up = PowerUp()
            all_sprites.add(power_up)
            power_ups.add(power_up)

        obstacles.update()
        power_ups.update()

        if pygame.sprite.spritecollide(carro, obstacles, False):
            if not carro.invulnerable:
                # 👇 Reproducir sonido de Game Over
                pygame.mixer.music.load("WhatsApp Ptt 2025-04-25 at 9.36.53 AM.mp3")
                pygame.mixer.music.play()

                mostrar_texto("¡GAME OVER, BROTHER!", 50, RED, SCREEN_WIDTH // 5 , SCREEN_HEIGHT // 2.25)
                pygame.display.update()
                time.sleep(2)
                game_running = False

        power_up_colision = pygame.sprite.spritecollide(carro, power_ups, True)
        if power_up_colision:
            puntuacion += 10
            carro.invulnerable = True
            carro.invulnerable_time = time.time()

        puntuacion += 1 / 1
        mostrar_texto(f"Puntuación: {int(puntuacion)}", 30, WHITE, 10, 10)
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    juego()
    pygame.quit()