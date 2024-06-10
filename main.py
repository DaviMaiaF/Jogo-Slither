import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definições de cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definições de tela
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
LINE_GAP = 100
FPS = 10

# Definições da cobra
SEGMENT_SIZE = 20
INITIAL_SNAKE_LENGTH = 5
snake_segments = []
snake_direction = None

# Definições do semáforo
SEMAPHORE_POS = (WIDTH // 2, HEIGHT // 2)
SEMAPHORE_RADIUS = 30
SEMAPHORE_COLORS = [RED, GREEN]  # Lista de cores: vermelho e verde
SEMAPHORE_INTERVAL = 3  # Intervalo de mudança de cor do semáforo em segundos

# Lista de bolinhas
balls = []
BALL_RADIUS = 10
BALL_COLOR = BLUE

# Função para desenhar a linha


def draw_line(screen):
    pygame.draw.rect(
        screen, WHITE, ((0, HEIGHT // 2 - LINE_GAP // 2), (WIDTH, LINE_WIDTH)))

# Função para desenhar o semáforo


def draw_semaphore(screen, color):
    pygame.draw.circle(screen, color, SEMAPHORE_POS, SEMAPHORE_RADIUS)

# Função para desenhar o texto no topo da tela


def draw_text(screen, text, size, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(WIDTH // 2, 10))
    screen.blit(text_surface, text_rect)

# Função para gerar uma nova bolinha


def spawn_ball():
    x = random.randint(0, WIDTH - BALL_RADIUS * 2)
    y = random.randint(0, HEIGHT - BALL_RADIUS * 2)
    balls.append((x, y))

# Função principal do jogo


def main():
    global snake_segments, snake_direction

    # Inicialização da tela
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Semaforo Game")

    # Relógio para controle de FPS
    clock = pygame.time.Clock()

    # Posição inicial da cobra
    initial_x = WIDTH // 2
    initial_y = HEIGHT - 50
    snake_segments = [[initial_x, initial_y - i * SEGMENT_SIZE]
                      for i in range(INITIAL_SNAKE_LENGTH)]

    # Contador para mudança de cor do semáforo
    semaphore_timer = 0
    semaphore_index = 0  # Começa com vermelho

    # Variável para controlar o estado do jogo
    game_over = False

    # Variável para pontuação
    score = 0

    # Gerar as primeiras bolinhas
    for _ in range(5):
        spawn_ball()

    # Loop principal do jogo
    while True:
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if snake_direction != 'DOWN':
                        snake_direction = 'UP'
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if snake_direction != 'UP':
                        snake_direction = 'DOWN'
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if snake_direction != 'RIGHT':
                        snake_direction = 'LEFT'
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if snake_direction != 'LEFT':
                        snake_direction = 'RIGHT'
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN, pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT]:
                    snake_direction = None

        if not game_over:
            # Verificar se o semáforo está verde
            semaphore_color = SEMAPHORE_COLORS[semaphore_index]

            if snake_direction is not None:
                # Atualizar posição da cobra
                head_x, head_y = snake_segments[0]
                if snake_direction == 'UP':
                    head_y -= SEGMENT_SIZE
                elif snake_direction == 'DOWN':
                    head_y += SEGMENT_SIZE
                elif snake_direction == 'LEFT':
                    head_x -= SEGMENT_SIZE
                elif snake_direction == 'RIGHT':
                    head_x += SEGMENT_SIZE

                # Verificar colisão com as bordas da tela
                if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
                    game_over = True
                else:
                    snake_segments.insert(0, [head_x, head_y])
                    snake_segments.pop()

                # Verificar se a cobra passou da linha quando o semáforo está vermelho
                if head_y < HEIGHT // 2 - LINE_GAP // 2 and semaphore_color == RED:
                    game_over = True

                # Verificar colisão com as bolinhas
                for ball in balls[:]:
                    ball_x, ball_y = ball
                    if abs(head_x - ball_x) < BALL_RADIUS and abs(head_y - ball_y) < BALL_RADIUS:
                        balls.remove(ball)
                        spawn_ball()
                        score += 1
                        # Aumentar o tamanho da cobra
                        snake_segments.append(snake_segments[-1])

        # Limpar a tela
        screen.fill(BLACK)

        # Desenhar os elementos do jogo
        draw_line(screen)
        draw_semaphore(screen, semaphore_color)
        for segment in snake_segments:
            pygame.draw.rect(
                screen, WHITE, (*segment, SEGMENT_SIZE, SEGMENT_SIZE))
        for ball in balls:
            pygame.draw.circle(screen, BALL_COLOR, ball, BALL_RADIUS)

        if game_over:
            draw_text(screen, "Você perdeu!", 50, RED)
        else:
            draw_text(screen, f"Pontuação: {score}", 30, WHITE)

        # Atualizar a tela
        pygame.display.flip()

        if not game_over:
            # Atualizar o contador do semáforo
            semaphore_timer += 1 / FPS
            if semaphore_timer >= SEMAPHORE_INTERVAL:
                semaphore_timer = 0
                # Alternar entre vermelho e verde
                semaphore_index = (semaphore_index +
                                   1) % len(SEMAPHORE_COLORS)

        # Limitar o FPS
        clock.tick(FPS)


if __name__ == "__main__":
    main()