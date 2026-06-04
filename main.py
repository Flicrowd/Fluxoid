import pygame
import sys

def get_path(name):
    return getattr(sys, '_MEIPASS', '.') + '/' + name

pygame.init()
pygame.mixer.init() 

WIDTH = 1060
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fluxoid")

tracks = [
    {"file": "background.mp3", "name": "One Sly Move"},
    {"file": "track2.mp3", "name": "Cloud Dancer"}
]
current_track_index = 0

def play_selected_track():
    pygame.mixer.music.load(get_path(tracks[current_track_index]["file"]))
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(0.4)

play_selected_track()

bg_img = pygame.image.load(get_path("background.png"))
icon = pygame.image.load(get_path("Fluxoid_Logo.png"))
pygame.display.set_icon(icon)

game_over_sound = pygame.mixer.Sound(get_path("game_over.wav"))
win_sound = pygame.mixer.Sound(get_path("win.wav"))

WHITE = (255, 255, 255)
NEON_CYAN = (0, 200, 255)
NEON_ORANGE = (255, 120, 0)
YELLOW = (255, 215, 0)
RED = (230, 50, 50)
GREEN = (50, 230, 50)
GRAY = (150, 150, 150)

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont("Arial", 36)
retry_font = pygame.font.SysFont("Arial", 28)
final_font = pygame.font.SysFont("Arial", 72)
music_font = pygame.font.SysFont("Arial", 24)

paddle_width = 120
paddle_height = 15
paddle_x = 470  
paddle_y = 550
paddle_speed = 8
paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

move_left = False
move_right = False

ball_size = 16
ball_x = 530     
ball_y = 300
ball = pygame.Rect(ball_x, ball_y, ball_size, ball_size)

ball_dx = 5
ball_dy = -5

bricks = []
for row in range(5):        
    for col in range(11):   
        bx = 110 + col * 75 
        by = 60 + row * 30  
        brick = pygame.Rect(bx, by, 70, 25)
        bricks.append(brick)

score = 0
game_over = False
win = False
running = True 

while running:
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_1:
                current_track_index = 0
                play_selected_track()
            elif event.key == pygame.K_2:
                current_track_index = 1
                play_selected_track()
            elif event.key == pygame.K_RETURN and (game_over == True or win == True):
                paddle.x = 470
                ball.x = 530
                ball.y = 300
                ball_dx = 5
                ball_dy = -5
                score = 0
                game_over = False
                win = False
                move_left = False
                move_right = False
                bricks = []
                for row in range(5):        
                    for col in range(11):   
                        bx = 110 + col * 75 
                        by = 60 + row * 30  
                        brick = pygame.Rect(bx, by, 70, 25)
                        bricks.append(brick)
                play_selected_track()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    if game_over == False and win == False:
        if move_left == True and paddle.x > 0:
            paddle.x -= paddle_speed
        if move_right == True and paddle.x < WIDTH - paddle_width:
            paddle.x += paddle_speed

        ball.x += ball_dx
        ball.y += ball_dy

        if ball.x <= 0 or ball.x >= WIDTH - ball_size:
            ball_dx = -ball_dx
        
        if ball.y <= 0:
            ball_dy = -ball_dy

        if ball.y >= HEIGHT:
            game_over = True
            pygame.mixer.music.stop() 
            game_over_sound.play()

        if ball.colliderect(paddle):
            ball_dy = -ball_dy

        for brick in bricks:
            if ball.colliderect(brick):
                bricks.remove(brick)  
                ball_dy = -ball_dy    
                score += 10           
                break  

        if len(bricks) == 0:
            win = True
            pygame.mixer.music.stop() 
            win_sound.play()

        pygame.draw.rect(screen, NEON_CYAN, paddle)
        pygame.draw.circle(screen, WHITE, ball.center, 8)

        for brick in bricks:
            pygame.draw.rect(screen, NEON_ORANGE, brick)

        score_text = font.render("Score: " + str(score), True, YELLOW)
        screen.blit(score_text, (20, 15))

    if game_over == True:
        loss_text = final_font.render("GAME OVER", True, RED)
        screen.blit(loss_text, (350, 200))
        retryo_text = retry_font.render("To play again press ENTER", True, WHITE)
        screen.blit(retryo_text, (380, 420))
        
        current_music_text = music_font.render("Current Music: " + tracks[current_track_index]["name"], True, GRAY)
        music_x = (WIDTH - current_music_text.get_width()) // 2
        screen.blit(current_music_text, (music_x, 470))
        
        hint_text = music_font.render("Press 1 or 2 to change music track", True, YELLOW)
        hint_x = (WIDTH - hint_text.get_width()) // 2
        screen.blit(hint_text, (hint_x, 510))

    if win == True:
        win_text = final_font.render("YOU WIN", True, GREEN)
        screen.blit(win_text, (390, 200))
        retryw_text = retry_font.render("To play again press ENTER", True, WHITE)
        screen.blit(retryw_text, (380, 420))
        
        current_music_text = music_font.render("Current Music: " + tracks[current_track_index]["name"], True, GRAY)
        music_x = (WIDTH - current_music_text.get_width()) // 2
        screen.blit(current_music_text, (music_x, 470))
        
        hint_text = music_font.render("Press 1 or 2 to change music track", True, YELLOW)
        hint_x = (WIDTH - hint_text.get_width()) // 2
        screen.blit(hint_text, (hint_x, 510))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
