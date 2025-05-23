import pygame
import random
import time

# Inicialización de pygame
pygame.init()
pygame.mixer.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255 ,0)
# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Carrera y Obstáculos")

# Antes del bucle principal
fondo = pygame.image.load("Carreras1.png").convert()
fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
fondo_y = -SCREEN_HEIGHT
velocidad_fondo = 5  # Nueva variable para el fondo

# FPS
clock = pygame.time.Clock()
FPS = 60



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

    def get_hitbox(self):
        return self.rect.inflate(-50, -30)

    def draw(self, surface):
        if not self.invulnerable or int(time.time() * 10) % 2 == 0:
            surface.blit(self.image, self.rect)

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

    def get_hitbox(self):
        return self.rect.inflate(-20, -20)

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

    def get_hitbox(self):
        return self.rect.inflate(-20, -20)  # Más pequeño


class RaraVez(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("brrbrrafanador.jpg")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 70)
        self.rect.y = -70
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def get_hitbox(self):
        return self.rect.inflate(-10, -10)  # Más pequeño
    

def mostrar_texto(texto, tamaño, color, x, y):
    font = pygame.font.SysFont("arial", tamaño)
    texto_surface = font.render(texto, True, color)
    screen.blit(texto_surface, (x, y))


def pantalla_inicio():
    esperando = True
    while esperando:
        screen.fill(BLACK)
        mostrar_texto("AFANADOR RACING", 60, BLUE, SCREEN_WIDTH//4.8, SCREEN_HEIGHT//4)
        mostrar_texto("Presiona una tecla para empezar", 36, WHITE, SCREEN_WIDTH//4.3, SCREEN_HEIGHT//2.2)
        mostrar_texto("(Usa las flechas para moverte)", 28, WHITE, SCREEN_WIDTH//3.2, SCREEN_HEIGHT//1.6)
        mostrar_texto("Consejos: Evita a los afanadores mas no al brr brr afanador y las estrellas, estas te ayudaran.", 28, WHITE, SCREEN_WIDTH//20, SCREEN_HEIGHT//1.4)
        mostrar_texto(" estas te ayudaran.", 28, WHITE, SCREEN_WIDTH//2.6, SCREEN_HEIGHT//1.3)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                esperando = False
def juego():
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    raros = pygame.sprite.Group()

    # Cargar fondo y variables asociadas
    fondo = pygame.image.load("Carreras1.png").convert()
    fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
    fondo_y = -SCREEN_HEIGHT
    velocidad_fondo = 5

    carro = Carro()
    motor_sonido = pygame.mixer.Sound("engine-61234.mp3")
    motor_sonido.set_volume(0.3)
    motor_sonido.play(loops=-1)
    all_sprites.add(carro)

    puntuacion = 0
    game_running = True

    efecto_lentitud_activo = False
    tiempo_lentitud = 0
    velocidad_original = {}

    while game_running:
        # Mover el fondo
        fondo_y += velocidad_fondo
        if fondo_y >= 0:
            fondo_y = -SCREEN_HEIGHT

        # Dibujar el fondo
        screen.blit(fondo, (0, fondo_y))

       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        keys = pygame.key.get_pressed()
        carro.update(keys)

        if len(obstacles) < 6:
            if random.random() < 0.01:
                obstaculo = Obstaculo()
                all_sprites.add(obstaculo)
                obstacles.add(obstaculo)

        if random.random() < 0.003:
            power_up = PowerUp()
            all_sprites.add(power_up)
            power_ups.add(power_up)

        if random.random() < 0.001:  # Muy rara vez
            raro = RaraVez()
            all_sprites.add(raro)
            raros.add(raro)

        obstacles.update()
        power_ups.update()
        raros.update()

        if any(obst.get_hitbox().colliderect(carro.get_hitbox()) for obst in obstacles):
            if not carro.invulnerable:
                pygame.mixer.music.load("WhatsApp Ptt 2025-04-25 at 9.36.53 AM.mp3")
                pygame.mixer.music.play()
                mostrar_texto("¡GAME OVER, BROTHER!", 50, RED, SCREEN_WIDTH // 5 , SCREEN_HEIGHT // 2.25)
                pygame.display.update()
                time.sleep(2)
                game_running = False

        power_up_colision = any(p.get_hitbox().colliderect(carro.get_hitbox()) for p in power_ups)
        if power_up_colision:
            for p in power_ups:
                if p.get_hitbox().colliderect(carro.get_hitbox()):
                 power_ups.remove(p)
                 all_sprites.remove(p)
            puntuacion += 10
            carro.invulnerable = True
            carro.invulnerable_time = time.time()
            pygame.mixer.Sound("coin-upaif-14631.mp3").play()

        colision_rara = any(r.get_hitbox().colliderect(carro.get_hitbox()) for r in raros)
        if colision_rara and not efecto_lentitud_activo:
             for r in raros:
                if r.get_hitbox().colliderect(carro.get_hitbox()):
                    raros.remove(r)
                    all_sprites.remove(r)
             efecto_lentitud_activo = True
             tiempo_lentitud = time.time()
             velocidad_original.clear()

             for obstaculo in obstacles:
                velocidad_original[obstaculo] = obstaculo.speed
                obstaculo.speed = max(1, obstaculo.speed - 3)
             pygame.mixer.Sound("WhatsApp Ptt 2025-05-06 at 2-VEED.mp3").play()

        # Restaurar velocidad original después de 5 segundos
        if efecto_lentitud_activo and time.time() - tiempo_lentitud > 5:
            for obstaculo in obstacles:
                if obstaculo in velocidad_original:
                    obstaculo.speed = velocidad_original[obstaculo]
            efecto_lentitud_activo = False

        puntuacion += 1
        mostrar_texto(f"Puntuación: {int(puntuacion)}", 30, WHITE, 10, 10)

        for sprite in all_sprites:
            if isinstance(sprite, Carro):
                sprite.draw(screen)
            else:
                screen.blit(sprite.image, sprite.rect)

        pygame.display.update()
        clock.tick(FPS)

    motor_sonido.stop()

if __name__ == "__main__":
    pantalla_inicio()
    juego()
    pygame.quit()