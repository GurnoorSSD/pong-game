import pygame
import sys

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 12
BALL_SPEED = 5
AI_SPEED = 4
PLAYER_SPEED = 6

# Colors for gradient
GRADIENT_COLORS = [
    (255, 70, 70),
    (255, 255, 70),
    (70, 255, 140),
    (70, 140, 255),
    (255, 70, 200),
]

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game - Mouse/Arrow Keys (Robot Mode)')

clock = pygame.time.Clock()

# Game objects
left_paddle = pygame.Rect(20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_vel = [BALL_SPEED, BALL_SPEED * (0.5 if pygame.time.get_ticks() % 2 == 0 else -0.5)]

robot_mode = False  # False = mouse control, True = arrow key control

# Scoring
player_score = 0
ai_score = 0

def draw_gradient_bg():
    # Draw vertical gradient stripes
    stripe_width = WIDTH // len(GRADIENT_COLORS)
    for i, color in enumerate(GRADIENT_COLORS):
        rect = (i * stripe_width, 0, stripe_width, HEIGHT)
        pygame.draw.rect(screen, color, rect)

def reset_ball(scored_left=None):
    ball.x = WIDTH//2 - BALL_SIZE//2
    ball.y = HEIGHT//2 - BALL_SIZE//2
    # If scored_left is True, ball moves toward player; if False, toward AI, else random
    if scored_left is None:
        ball_vel[0] = BALL_SPEED if pygame.time.get_ticks() % 2 == 0 else -BALL_SPEED
    else:
        ball_vel[0] = BALL_SPEED if scored_left else -BALL_SPEED
    ball_vel[1] = BALL_SPEED * (0.5 if pygame.time.get_ticks() % 2 == 0 else -0.5)

def handle_player_input():
    global left_paddle
    keys = pygame.key.get_pressed()
    if robot_mode:
        if keys[pygame.K_UP]:
            left_paddle.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            left_paddle.y += PLAYER_SPEED
        left_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle.y))
    else:
        mouse_y = pygame.mouse.get_pos()[1]
        left_paddle.y = mouse_y - PADDLE_HEIGHT // 2
        left_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle.y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Toggle robot mode with 'R'
            if event.key == pygame.K_r:
                robot_mode = not robot_mode

    handle_player_input()

    # AI for right paddle
    if right_paddle.centery < ball.centery:
        right_paddle.y += AI_SPEED
    elif right_paddle.centery > ball.centery:
        right_paddle.y -= AI_SPEED
    right_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle.y))

    # Ball movement
    ball.x += int(ball_vel[0])
    ball.y += int(ball_vel[1])

    # Ball collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] *= -1

    # Ball collision with paddles
    if ball.colliderect(left_paddle):
        ball.left = left_paddle.right
        ball_vel[0] *= -1
        ball_vel[1] += (ball.centery - left_paddle.centery) * 0.08
    if ball.colliderect(right_paddle):
        ball.right = right_paddle.left
        ball_vel[0] *= -1
        ball_vel[1] += (ball.centery - right_paddle.centery) * 0.08

    # Ball out of bounds (score)
    if ball.left < 0:
        ai_score += 1
        reset_ball(scored_left=False)
    if ball.right > WIDTH:
        player_score += 1
        reset_ball(scored_left=True)

    # Draw everything
    draw_gradient_bg()
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Display mode info
    font = pygame.font.SysFont(None, 32)
    mode_text = "Robot Mode (Arrow Keys)" if robot_mode else "Mouse Mode"
    info = font.render(f"Mode: {mode_text} | Toggle: R", True, BLACK)
    screen.blit(info, (WIDTH//2 - info.get_width()//2, 10))

    # Draw scores
    score_font = pygame.font.SysFont(None, 48)
    player_score_text = score_font.render(str(player_score), True, WHITE)
    ai_score_text = score_font.render(str(ai_score), True, WHITE)
    screen.blit(player_score_text, (WIDTH//2 - 60 - player_score_text.get_width(), 30))
    screen.blit(ai_score_text, (WIDTH//2 + 60, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
