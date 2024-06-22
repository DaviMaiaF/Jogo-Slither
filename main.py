import pygame
import sys
import random
import threading
from threading import Semaphore

# Inicialização do Pygame
pygame.init()

# Inicialização do mixer de áudio
pygame.mixer.init()

# Carregar a música de fundo
pygame.mixer.music.load('audio/Eric Skiff - Underclocked ♫ NO COPYRIGHT 8-bit Music + Background (128).mp3')


# Definições de cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_RED = (139, 0, 0)  # Cor do olho da cobra

original_ball_image = pygame.image.load('img/fruit.png')
ball_image = pygame.transform.scale(original_ball_image, (28, 28))

# Definições de tela
WIDTH, HEIGHT = 600, 600
FPS = 10
SPEED_INCREASE = 0.5  # Aumento da velocidade a cada fruta comida

# Definições da cobra
SEGMENT_SIZE = 20
INITIAL_SNAKE_LENGTH = 5
snake_segments = []
snake_direction = None  # Direção inicial definida como None
keys_pressed = {pygame.K_UP: False, pygame.K_DOWN: False,
                pygame.K_LEFT: False, pygame.K_RIGHT: False}

# Lista de bolinhas
balls = []
BALL_RADIUS = 10
BALL_COLOR = BLUE

# Variável para controle de spawn de bolinha
can_spawn_ball = True

# Definições da margem segura e área da HUD
MARGIN = 50
HUD_HEIGHT = 100

# Variável de controle de pausa
is_paused = False
pause_semaphore = Semaphore(1)  # Semáforo para controle de pausa

# Hit box extra radius
EXTRA_HITBOX_RADIUS = 10  # Aumentar a hitbox em 10 pixels

# Função para desenhar o texto na tela
def draw_text(screen, text, size, color, position):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)
    return text_rect

# Função para gerar uma nova bolinha
def spawn_ball():
    global can_spawn_ball
    if len(balls) < 5:
        x = random.randint(MARGIN, WIDTH - MARGIN - BALL_RADIUS * 2)
        y = random.randint(HUD_HEIGHT, HEIGHT - MARGIN - BALL_RADIUS * 2)
        balls.append((x, y))
        can_spawn_ball = False

# Função para verificar colisão com as bolinhas e spawnar nova bolinha
def check_collision_and_spawn():
    global can_spawn_ball, FPS
    head_x, head_y = snake_segments[0]
    for ball in balls[:]:
        ball_x, ball_y = ball
        distance = ((head_x - ball_x) ** 2 + (head_y - ball_y) ** 2) ** 0.5
        if distance < SEGMENT_SIZE / 2 + BALL_RADIUS + EXTRA_HITBOX_RADIUS:
            balls.remove(ball)
            can_spawn_ball = True
            spawn_ball()
            with pause_semaphore:
                global score
                score += 1
            FPS += SPEED_INCREASE  # Aumenta a velocidade da cobra

# Função para reiniciar o jogo
def restart_game():
    global snake_segments, snake_direction, can_spawn_ball, score, is_paused, game_over

    # Posição inicial da cobra
    initial_x = WIDTH // 2
    initial_y = HEIGHT - 50
    snake_segments = [[initial_x, initial_y - i * SEGMENT_SIZE] for i in range(INITIAL_SNAKE_LENGTH)]

    # Reiniciar direção da cobra
    snake_direction = None

    # Reiniciar estado do jogo
    game_over = False
    is_paused = False

    # Reiniciar pontuação
    score = 0

    # Limpar bolinhas e gerar novas
    balls.clear()
    for _ in range(10):
        spawn_ball()

    # Reiniciar FPS
    FPS = 10

# Função para desenhar o menu de pausa
def pause_menu(screen):
    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Retorna ao jogo sem exibir o menu de pausa

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verifica se o clique foi em "Retornar ao Jogo"
                if resume_button.collidepoint(mouse_x, mouse_y):
                    return  # Retorna ao jogo
                # Verifica se o clique foi em "Sair"
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        # Desenha o fundo semi-transparente
        pause_bg = pygame.Surface((WIDTH, HEIGHT))
        pause_bg.set_alpha(128)  # Configura a transparência
        pause_bg.fill(BLACK)
        screen.blit(pause_bg, (0, 0))

        # Desenha o texto do menu de pausa
        draw_text(screen, "Jogo Pausado", 50, WHITE, (WIDTH // 2, HEIGHT // 4))

        # Desenha os botões
        resume_button = draw_text(screen, "Retornar ao Jogo", 30, WHITE, (WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(screen, WHITE, resume_button.inflate(20, 10), 2)

        exit_button = draw_text(screen, "Sair", 30, WHITE, (WIDTH // 2, HEIGHT // 2 + 60))
        pygame.draw.rect(screen, WHITE, exit_button.inflate(20, 10), 2)

        # Atualiza a tela
        pygame.display.flip()

# Função para desenhar o menu principal
def main_menu(screen):
    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verifica se o clique foi em "Iniciar Jogo"
                if start_button.collidepoint(mouse_x, mouse_y):
                    return  # Inicia o jogo
                # Verifica se o clique foi em "Sair"
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        # Desenha o fundo
        screen.fill(BLACK)

        # Desenha os botões
        start_button = draw_text(screen, "Iniciar Jogo", 30, WHITE, (WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(screen, WHITE, start_button.inflate(20, 10), 2)

        exit_button = draw_text(screen, "Sair", 30, WHITE, (WIDTH // 2, HEIGHT // 2 + 60))
        pygame.draw.rect(screen, WHITE, exit_button.inflate(20, 10), 2)

        # Desenha o texto do menu principal
        draw_text(screen, "Bem vindo ao", 50, WHITE, (WIDTH // 2, HEIGHT // 4))
        draw_text(screen, "Slither game", 50, WHITE, (WIDTH // 2, HEIGHT // 4 + 60))

        # Atualiza a tela
        pygame.display.flip()

# Função principal do jogo
def game_logic():
    global snake_segments, snake_direction, can_spawn_ball, score, is_paused, game_over

    # Tocar a música de fundo em loop
    pygame.mixer.music.play(-1)

    # Inicialização da tela
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Semaforo Game")

    # Relógio para controle de FPS
    clock = pygame.time.Clock()

    # Exibir o menu principal
    main_menu(screen)

    # Reiniciar o jogo pela primeira vez
    restart_game()

    # Loop principal do jogo
    while True:
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in keys_pressed:
                    keys_pressed[event.key] = True
                elif event.key == pygame.K_SPACE:
                    with pause_semaphore:
                        is_paused = not is_paused
                elif event.key == pygame.K_r and game_over:
                    restart_game()
                elif event.key == pygame.K_ESCAPE:
                    if not game_over:
                        is_paused = True
                        pause_menu(screen)
                        is_paused = False

            elif event.type == pygame.KEYUP:
                if event.key in keys_pressed:
                    keys_pressed[event.key] = False

        if not is_paused and not game_over:
            # Atualizar a direção da cobra com base nas teclas pressionadas
            if keys_pressed[pygame.K_UP] and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif keys_pressed[pygame.K_DOWN] and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif keys_pressed[pygame.K_LEFT] and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif keys_pressed[pygame.K_RIGHT] and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

            # Atualizar posição da cobra
            if snake_direction is not None:
                head_x, head_y = snake_segments[0].copy()
                if snake_direction == 'UP':
                    head_y -= SEGMENT_SIZE
                elif snake_direction == 'DOWN':
                    head_y += SEGMENT_SIZE
                elif snake_direction == 'LEFT':
                    head_x -= SEGMENT_SIZE
                elif snake_direction == 'RIGHT':
                    head_x += SEGMENT_SIZE

                # Verificar colisão com as bordas da tela
                if head_x < 0 or head_x >= WIDTH or head_y < HUD_HEIGHT or head_y >= HEIGHT:
                    game_over = True
                else:
                    snake_segments.insert(0, [head_x, head_y])
                    snake_segments.pop()

                # Verificar colisão com as bolinhas e spawnar nova bolinha
                check_collision_and_spawn()

        # Limpar a tela
        screen.fill(BLACK)

        # Desenhar a borda do mapa
        pygame.draw.rect(screen, WHITE, (0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT), 5)

        # Desenhar cobra
        for segment in snake_segments:
            pygame.draw.rect(screen, WHITE, (*segment, SEGMENT_SIZE, SEGMENT_SIZE))

        # Desenhar o pixel indicando a frente da cobra
        head_x, head_y = snake_segments[0]
        pygame.draw.circle(screen, DARK_RED, (head_x + SEGMENT_SIZE // 2, head_y + SEGMENT_SIZE // 2), 3)

        # Desenhar bolinhas
        for ball in balls:
            screen.blit(ball_image, ball)

        # Verificar se o jogo acabou
        if game_over:
            draw_text(screen, "Você perdeu!", 50, RED, (WIDTH // 2, HEIGHT // 2))
            draw_text(screen, "Pressione 'R' para reiniciar", 30, WHITE, (WIDTH // 2, HEIGHT // 2 + 50))
        else:
            draw_text(screen, f"Pontuação: {score}", 30, WHITE, (WIDTH // 2, 30))

        # Atualizar a tela
        pygame.display.flip()

        # Limitar o FPS
        clock.tick(FPS)

# Função para iniciar o jogo em uma thread separada
def start_game_thread():
    threading.Thread(target=game_logic).start()

# Função principal
if __name__ == "__main__":
    start_game_thread()
