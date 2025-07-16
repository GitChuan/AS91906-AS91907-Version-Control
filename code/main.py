from Project.code.main_menu import MainMenu
from Project.code.login import *
from open_video import *

def wait(screen, duration=2):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 40)
    width, height = screen.get_size()
    bar_width = width // 2
    bar_height = 30
    bar_x = (width - bar_width) // 2
    bar_y = height // 2 + 60

    start_time = pygame.time.get_ticks()

    # 背景渐入变量
    alpha = 0
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((10, 10, 10))

    while True:
        screen.fill((10, 10, 10))

        # 淡入效果
        if alpha < 255:
            alpha = min(alpha + 5, 255)
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))

        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        progress = min(elapsed / duration, 1)

        # 进度条
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height), border_radius=8)
        pygame.draw.rect(screen, (200, 50, 50), (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=8)

        # “Loading...”文本
        text = font.render("Loading...", True, (180, 180, 180))
        screen.blit(text, (width // 2 - text.get_width() // 2, bar_y - 60))

        # 百分比
        percent = font.render(f"{int(progress * 100)}%", True, (220, 220, 220))
        screen.blit(percent, (width // 2 - percent.get_width() // 2, bar_y + bar_height + 20))

        pygame.display.flip()
        clock.tick(60)

        if progress >= 1:
            break

def exit_game():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    pygame.font.init()

    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)

    success_code = LoginScreen().run()
    if success_code is None:
        exit_game()

    wait(screen)
    if success_code[0] == 2: # new user, play the video
        IntroPlayer().play()
        wait(screen)

    username = success_code[1]
    MainMenu(screen=screen, username=username).run()

if __name__ == '__main__':
    main()