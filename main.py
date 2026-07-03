import pygame, sys
def get_path(name): return getattr(sys, '_MEIPASS', '.') + '/' + name

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1060, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fluxoid")

tracks = [
    {"file": "background.mp3", "name": "One Sly Move"},
    {"file": "track2.mp3", "name": "Cloud Dancer"},
    {"file": "track3.mp3", "name": "Galactic Rap"},
    {"file": "track4.mp3", "name": "Mesmerizing Galaxy Loop"}
]
current_track_index = 0

def play_selected_track():
    pygame.mixer.music.load(get_path(tracks[current_track_index]["file"]))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)

play_selected_track()

bg_img = pygame.image.load(get_path("background.png"))
pygame.display.set_icon(pygame.image.load(get_path("Fluxoid_Logo.png")))
menu_logo = pygame.transform.scale(pygame.image.load(get_path("Fluxoid_Logo.png")), (200, 200))
game_over_sound = pygame.mixer.Sound(get_path("game_over.wav"))
win_sound = pygame.mixer.Sound(get_path("win.wav"))

WHITE, NEON_CYAN, NEON_ORANGE, YELLOW, RED, GREEN, GRAY = (255,255,255), (0,200,255), (255,120,0), (255,215,0), (230,50,50), (50,230,50), (150,150,150)
clock, FPS = pygame.time.Clock(), 60
font = pygame.font.SysFont("Arial", 36)
retry_font = pygame.font.SysFont("Arial", 28)
final_font = pygame.font.SysFont("Arial", 72)
music_font = pygame.font.SysFont("Arial", 24)
menu_title_font = pygame.font.SysFont("Arial", 80, bold=True)

paddle = pygame.Rect(470, 550, 120, 15)
move_left, move_right = False, False
ball = pygame.Rect(530, 300, 16, 16)
ball_dx, ball_dy = 5, -5
bricks = []

def reset_bricks():
    global bricks
    bricks = [pygame.Rect(110 + col * 75, 60 + row * 30, 70, 25) for row in range(5) for col in range(11)]

reset_bricks()
score, game_over, win, running = 0, False, False, True
game_state, menu_options, current_menu_index = "MENU", ["START GAME", "SELECT MUSIC", "EXIT"], 0

while running:
    screen.blit(bg_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_UP: current_menu_index = (current_menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN: current_menu_index = (current_menu_index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if current_menu_index == 0:
                        game_state, score, game_over, win, move_left, move_right = "PLAY", 0, False, False, False, False
                        paddle.x, ball.x, ball.y, ball_dx, ball_dy = 470, 530, 300, 5, -5
                        reset_bricks()
                        play_selected_track()
                    elif current_menu_index == 1: game_state = "MUSIC_SELECT"
                    elif current_menu_index == 2: running = False
            elif game_state == "MUSIC_SELECT":
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    current_track_index = event.key - pygame.K_1
                    play_selected_track()
                elif event.key in [pygame.K_ESCAPE, pygame.K_RETURN]: game_state = "MENU"
            elif game_state == "PLAY":
                if event.key == pygame.K_LEFT: move_left = True
                elif event.key == pygame.K_RIGHT: move_right = True
                elif event.key == pygame.K_ESCAPE: game_state = "MENU"
                elif event.key == pygame.K_RETURN and (game_over or win): game_state = "MENU"
                elif (game_over or win) and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    current_track_index = event.key - pygame.K_1
                    play_selected_track()
        elif event.type == pygame.KEYUP and game_state == "PLAY":
            if event.key == pygame.K_LEFT: move_left = False
            elif event.key == pygame.K_RIGHT: move_right = False

    if game_state == "MENU":
        screen.blit(menu_logo, ((WIDTH - 200) // 2, 30))
        t_text = menu_title_font.render("FLUXOID", True, NEON_CYAN)
        screen.blit(t_text, ((WIDTH - t_text.get_width()) // 2, 240))
        for i, opt in enumerate(menu_options):
            txt = font.render(f"> {opt} <" if i == current_menu_index else opt, True, NEON_ORANGE if i == current_menu_index else WHITE)
            screen.blit(txt, ((WIDTH - txt.get_width()) // 2, 360 + i * 55))
        inf = music_font.render("Use UP / DOWN arrows and ENTER to select", True, GRAY)
        screen.blit(inf, ((WIDTH - inf.get_width()) // 2, 540))
    elif game_state == "MUSIC_SELECT":
        t_text = font.render("SELECT BACKGROUND MUSIC", True, NEON_CYAN)
        screen.blit(t_text, ((WIDTH - t_text.get_width()) // 2, 60))
        for i, trk in enumerate(tracks):
            txt = font.render(f"[{i+1}] {trk['name']} (Active)" if i == current_track_index else f"[{i+1}] {trk['name']}", True, NEON_ORANGE if i == current_track_index else WHITE)
            screen.blit(txt, ((WIDTH - txt.get_width()) // 2, 160 + i * 55))
        back = music_font.render("Press 1, 2, 3, 4 to listen. Press ESC / ENTER to return to Menu", True, YELLOW)
        screen.blit(back, ((WIDTH - back.get_width()) // 2, 450))
    elif game_state == "PLAY":
        if not game_over and not win:
            if move_left and paddle.x > 0: paddle.x -= 8
            if move_right and paddle.x < WIDTH - 120: paddle.x += 8
            ball.x += ball_dx
            ball.y += ball_dy
            if ball.x <= 0 or ball.x >= WIDTH - 16: ball_dx = -ball_dx
            if ball.y <= 0: ball_dy = -ball_dy
            if ball.y >= HEIGHT:
                game_over = True
                pygame.mixer.music.stop()
                game_over_sound.play()
            if ball.colliderect(paddle): ball_dy = -ball_dy
            for brk in bricks:
                if ball.colliderect(brk):
                    bricks.remove(brk)
                    ball_dy = -ball_dy
                    score += 10
                    break
            if not bricks:
                win = True
                pygame.mixer.music.stop()
                win_sound.play()
            pygame.draw.rect(screen, NEON_CYAN, paddle)
            pygame.draw.circle(screen, WHITE, ball.center, 8)
            for brk in bricks: pygame.draw.rect(screen, NEON_ORANGE, brk)
            screen.blit(font.render(f"Score: {score}", True, YELLOW), (20, 15))
        if game_over or win:
            f_txt = final_font.render("GAME OVER" if game_over else "YOU WIN", True, RED if game_over else GREEN)
            screen.blit(f_txt, ((WIDTH - f_txt.get_width()) // 2, 160))
            r_txt = retry_font.render("Press ENTER to return to Menu", True, WHITE)
            screen.blit(r_txt, ((WIDTH - r_txt.get_width()) // 2, 380))
            m_txt = music_font.render(f"Current Music: {tracks[current_track_index]['name']}", True, GRAY)
            screen.blit(m_txt, ((WIDTH - m_txt.get_width()) // 2, 450))
            h_txt = music_font.render("Press 1, 2, 3, 4 to change music track", True, YELLOW)
            screen.blit(h_txt, ((WIDTH - h_txt.get_width()) // 2, 490))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
