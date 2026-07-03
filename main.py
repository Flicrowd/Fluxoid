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

# Загружаем логотип 512x512 и плавно сжимаем его до 200x200 для меню
menu_logo = pygame.image.load(get_path("Fluxoid_Logo.png"))
menu_logo = pygame.transform.scale(menu_logo, (200, 200))

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
menu_title_font = pygame.font.SysFont("Arial", 80, bold=True)

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
def reset_bricks():
    global bricks
    bricks = []
    for row in range(5):        
        for col in range(11):   
            bx = 110 + col * 75 
            by = 60 + row * 30  
            brick = pygame.Rect(bx, by, 70, 25)
            bricks.append(brick)

reset_bricks()

score = 0
game_over = False
win = False
running = True 

game_state = "MENU"
menu_options = ["START GAME", "SELECT MUSIC", "EXIT"]
current_menu_index = 0

while running:
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        
        elif event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_UP:
                    current_menu_index = (current_menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    current_menu_index = (current_menu_index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if current_menu_index == 0:
                        game_state = "PLAY"
                        paddle.x = 470
                        ball.x = 530
                        ball.y = 300
                        ball_dx = 5
                        ball_dy = -5
                        score = 0
                        game_over = False
                        win = False
                        reset_bricks()
                        play_selected_track()
                    elif current_menu_index == 1:
                        game_state = "MUSIC_SELECT"
                    elif current_menu_index == 2:
                        running = False

            elif game_state == "MUSIC_SELECT":
                if event.key == pygame.K_1:
                    current_track_index = 0
                    play_selected_track()
                elif event.key == pygame.K_2:
                    current_track_index = 1
                    play_selected_track()
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    game_state = "MENU"

            elif game_state == "PLAY":
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True
                elif event.key == pygame.K_ESCAPE:
                    game_state = "MENU"
                elif event.key == pygame.K_RETURN and (game_over == True or win == True):
                    game_state = "MENU"
                elif (game_over == True or win == True):
                    if event.key == pygame.K_1:
                        current_track_index = 0
                        play_selected_track()
                    elif event.key == pygame.K_2:
                        current_track_index = 1
                        play_selected_track()

        elif event.type == pygame.KEYUP:
            if game_state == "PLAY":
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False

    if game_state == "MENU":
        logo_x = (WIDTH - 200) // 2
        screen.blit(menu_logo, (logo_x, 30))
        
        title_text = menu_title_font.render("FLUXOID", True, NEON_CYAN)
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 240))
        
        for i, option in enumerate(menu_options):
            if i == current_menu_index:
                opt_text = font.render("> " + option + " <", True, NEON_ORANGE)
            else:
                opt_text = font.render(option, True, WHITE)
            screen.blit(opt_text, ((WIDTH - opt_text.get_width()) // 2, 360 + i * 55))
            
        info_text = music_font.render("Use UP / DOWN arrows and ENTER to select", True, GRAY)
        screen.blit(info_text, ((WIDTH - info_text.get_width()) // 2, 540))

    elif game_state == "MUSIC_SELECT":
        title_text = font.render("SELECT BACKGROUND MUSIC", True, NEON_CYAN)
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 100))
        
        for i, track in enumerate(tracks):
            if i == current_track_index:
                t_text = font.render(f"[{i+1}] " + track["name"] + " (Active)", True, NEON_ORANGE)
            else:
                t_text = font.render(f"[{i+1}] " + track["name"], True, WHITE)
            screen.blit(t_text, ((WIDTH - t_text.get_width()) // 2, 220 + i * 60))
            
        back_text = music_font.render("Press 1 or 2 to listen. Press ESC / ENTER to return to Menu", True, YELLOW)
        screen.blit(back_text, ((WIDTH - back_text.get_width()) // 2, 450))

    elif game_state == "PLAY":
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
            screen.blit(loss_text, ((WIDTH - loss_text.get_width()) // 2, 160))
            retryo_text = retry_font.render("Press ENTER to return to Menu", True, WHITE)
            screen.blit(retryo_text, ((WIDTH - retryo_text.get_width()) // 2, 380))
            
            current_music_text = music_font.render("Current Music: " + tracks[current_track_index]["name"], True, GRAY)
            screen.blit(current_music_text, ((WIDTH - current_music_text.get_width()) // 2, 450))
            hint_text = music_font.render("Press 1 or 2 to change music track", True, YELLOW)
            screen.blit(hint_text, ((WIDTH - hint_text.get_width()) // 2, 490))

        if win == True:
            win_text = final_font.render("YOU WIN", True, GREEN)
            screen.blit(win_text, ((WIDTH - win_text.get_width()) // 2, 160))
            retryw_text = retry_font.render("Press ENTER to return to Menu", True, WHITE)
            screen.blit(retryw_text, ((WIDTH - retryw_text.get_width()) // 2, 380))
            
            current_music_text = music_font.render("Current Music: " + tracks[current_track_index]["name"], True, GRAY)
            screen.blit(current_music_text, ((WIDTH - current_music_text.get_width()) // 2, 450))
            hint_text = music_font.render("Press 1 or 2 to change music track", True, YELLOW)
            screen.blit(hint_text, ((WIDTH - hint_text.get_width()) // 2, 490))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
