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
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_RED = (139, 0, 0)  # Cor do olho da cobra

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

# Definições do semáforo
SEMAPHORE_POS = (WIDTH - 50, 50)  # Posição no canto superior direito
SEMAPHORE_RADIUS = 30
GREEN_INTERVAL = 5  # Intervalo de tempo para o semáforo verde em segundos
RED_INTERVAL = 3  # Intervalo de tempo para o semáforo vermelho em segundos
YELLOW_DURATION = 1  # Duração do semáforo amarelo em segundos

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

# Hit box extra radius
EXTRA_HITBOX_RADIUS = 10  # Aumentar a hitbox em 10 pixels

# Função para desenhar o semáforo
def draw_semaphore(screen, color):
    pygame.draw.circle(screen, color, SEMAPHORE_POS, SEMAPHORE_RADIUS)

# Função para desenhar o texto na tela
def draw_text(screen, text, size, color, position):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

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
    global score, can_spawn_ball, FPS
    head_x, head_y = snake_segments[0]
    for ball in balls[:]:
        ball_x, ball_y = ball
        distance = ((head_x - ball_x) ** 2 + (head_y - ball_y) ** 2) ** 0.5
        if distance < SEGMENT_SIZE / 2 + BALL_RADIUS + EXTRA_HITBOX_RADIUS:
            balls.remove(ball)
            can_spawn_ball = True
            score += 1
            spawn_ball()
            FPS += SPEED_INCREASE  # Aumenta a velocidade da cobra

# Função para reiniciar o jogo
def restart_game():
    global snake_segments, snake_direction, can_spawn_ball, score, is_paused, game_over, semaphore_timer, semaphore_state, semaphore_color, semaphore_total_timer, FPS

    # Posição inicial da cobra
    initial_x = WIDTH // 2
    initial_y = HEIGHT - 50
    snake_segments = [[initial_x, initial_y - i * SEGMENT_SIZE] for i in range(INITIAL_SNAKE_LENGTH)]

    # Reiniciar direção da cobra
    snake_direction = None

    # Reiniciar semáforo
    semaphore_timer = 0
    semaphore_state = 'GREEN'
    semaphore_total_timer = GREEN_INTERVAL
    semaphore_color = GREEN

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

# Função principal do jogo
def main():
    global snake_segments, snake_direction, can_spawn_ball, score, is_paused, game_over, semaphore_timer, semaphore_state, semaphore_color, semaphore_total_timer, FPS

    # Inicialização da tela
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Semaforo Game")

    # Relógio para controle de FPS
    clock = pygame.time.Clock()

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
                    is_paused = not is_paused
                elif event.key == pygame.K_r and game_over:
                    restart_game()
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

            if snake_direction is not None and semaphore_color == RED:
                game_over = True
            else:
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

                    # Verificar colisão com as bolinhas e spawnar nova bolinha
                    check_collision_and_spawn()

        # Limpar a tela
        screen.fill(BLACK)

        # Desenhar os elementos do jogo
        draw_semaphore(screen, semaphore_color)
        for segment in snake_segments:
            pygame.draw.rect(screen, WHITE, (*segment, SEGMENT_SIZE, SEGMENT_SIZE))

        # Desenhar o pixel indicando a frente da cobra
        head_x, head_y = snake_segments[0]
        pygame.draw.circle(screen, DARK_RED, (head_x + SEGMENT_SIZE // 2, head_y + SEGMENT_SIZE // 2), 3)

        for ball in balls:
            pygame.draw.circle(screen, BALL_COLOR, ball, BALL_RADIUS)

        # Desenhar a borda do mapa
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 5)

        if game_over:
            draw_text(screen, "Você perdeu!", 50, RED, (WIDTH // 2, HEIGHT // 2))
            draw_text(screen, "Pressione 'R' para reiniciar", 30, WHITE, (WIDTH // 2, HEIGHT // 2 + 50))
        else:
            draw_text(screen, f"Pontuação: {score}", 30, WHITE, (WIDTH // 2, 30))
            draw_text(screen, f"Tempo: {semaphore_total_timer - semaphore_timer:.1f}", 30, WHITE, (WIDTH - 100, 100))

        # Atualizar a tela
        pygame.display.flip()

        if not game_over:
            # Atualizar o contador do semáforo
            semaphore_timer += 1 / FPS

            # Lógica para mudar a cor do semáforo
            if semaphore_state == 'GREEN' and semaphore_total_timer - semaphore_timer <= YELLOW_DURATION:
                semaphore_state = 'YELLOW'
                semaphore_color = YELLOW
                semaphore_timer = 0
                semaphore_total_timer = YELLOW_DURATION
            elif semaphore_state == 'YELLOW' and semaphore_timer >= YELLOW_DURATION:
                semaphore_state = 'RED'
                semaphore_color = RED
                semaphore_timer = 0
                semaphore_total_timer = RED_INTERVAL
            elif semaphore_state == 'RED' and semaphore_timer >= RED_INTERVAL:
                semaphore_state = 'GREEN'
                semaphore_color = GREEN
                semaphore_timer = 0
                semaphore_total_timer = GREEN_INTERVAL

        # Limitar o FPS
        clock.tick(FPS)

if __name__ == "__main__":
    main()
