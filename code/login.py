# login_screen.py
import pygame
import sys
from info_manager import *

_BACKGROUND_PATH = "../pictures/background.png"

class LoginScreen:
    def __init__(self, background_path=_BACKGROUND_PATH):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        pygame.display.set_caption("Game Login")

        self.bg_image = pygame.image.load(background_path).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))

        self.font = pygame.font.SysFont("arial", 36)
        self.small_font = pygame.font.SysFont("arial", 28)

        self.mode = 'login'  # 'login' or 'register'
        self.username = ''
        self.password = ''
        self.active_input = 'username'
        self.message = ''  # message prompt

        self.uname_rect = pygame.Rect(self.WIDTH // 2 - 50, 200, 300, 36)
        self.pwd_rect = pygame.Rect(self.WIDTH // 2 - 50, 260, 300, 36)

        self.login_btn_rect = pygame.Rect(50, 50, 120, 40)
        self.register_btn_rect = pygame.Rect(190, 50, 120, 40)

    def draw_cracked_rect(self, rect, focused):
        base_color = (120, 10, 10)
        crack_color = (200, 50, 50)

        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((*base_color, 60))
        self.screen.blit(s, (rect.x, rect.y))

        border_width = 4 if focused else 2
        pygame.draw.rect(self.screen, base_color, rect, border_width)

        gap = 6
        for x in range(rect.x, rect.x + rect.width, gap):
            if x % (gap * 2) == 0:
                pygame.draw.line(self.screen, crack_color, (x, rect.y), (x + gap // 2, rect.y + 2), 2)
                pygame.draw.line(self.screen, crack_color, (x, rect.y + rect.height), (x + gap // 2, rect.y + rect.height - 2), 2)
        for y in range(rect.y, rect.y + rect.height, gap):
            if y % (gap * 2) == 0:
                pygame.draw.line(self.screen, crack_color, (rect.x, y), (rect.x + 2, y + gap // 2), 2)
                pygame.draw.line(self.screen, crack_color, (rect.x + rect.width, y), (rect.x + rect.width - 2, y + gap // 2), 2)

    def draw_button(self, rect, text, selected):
        base_color = (120, 10, 10)
        hover_color = (180, 40, 40)
        text_color = (255, 180, 180) if selected else (180, 180, 180)

        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos) and not selected:
            color = hover_color
        else:
            color = base_color

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 50, 50), rect, 3, border_radius=8)

        txt_surf = self.small_font.render(text, True, text_color)
        self.screen.blit(txt_surf, (rect.x + rect.width // 2 - txt_surf.get_width() // 2,
                                    rect.y + rect.height // 2 - txt_surf.get_height() // 2))

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        title_text = "Rescue the Dragon Queen - Login" if self.mode == 'login' else "Rescue the Dragon Queen - Register"
        title = self.font.render(title_text, True, (200, 50, 50))
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 120))

        self.draw_button(self.login_btn_rect, "Login", self.mode == 'login')
        self.draw_button(self.register_btn_rect, "Register", self.mode == 'register')

        uname_label = self.small_font.render("Username:", True, (180, 180, 180))
        self.screen.blit(uname_label, (self.WIDTH // 2 - 200, 200))
        self.draw_cracked_rect(self.uname_rect, self.active_input == 'username')
        uname_text = self.small_font.render(self.username + ('|' if self.active_input == 'username' else ''), True, (220, 220, 220))
        self.screen.blit(uname_text, (self.uname_rect.x + 10, self.uname_rect.y + 6))

        pwd_label = self.small_font.render("Password:", True, (180, 180, 180))
        self.screen.blit(pwd_label, (self.WIDTH // 2 - 200, 260))
        self.draw_cracked_rect(self.pwd_rect, self.active_input == 'password')
        hidden_pwd = '*' * len(self.password)
        pwd_text = self.small_font.render(hidden_pwd + ('|' if self.active_input == 'password' else ''), True, (220, 220, 220))
        self.screen.blit(pwd_text, (self.pwd_rect.x + 10, self.pwd_rect.y + 6))

        submit_text = "Press ENTER to Login" if self.mode == 'login' else "Press ENTER to Register"
        submit_render = self.small_font.render(submit_text, True, (100, 100, 100))
        self.screen.blit(submit_render, (self.WIDTH // 2 - submit_render.get_width() // 2, self.HEIGHT - 100))

        if self.message:
            msg_color = (255, 100, 100) if "❌" in self.message else (100, 255, 100)
            msg_text = self.small_font.render(self.message, True, msg_color)
            self.screen.blit(msg_text, (self.WIDTH // 2 - msg_text.get_width() // 2, self.HEIGHT - 150))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.login_btn_rect.collidepoint(event.pos):
                        self.mode = 'login'
                        self.active_input = 'username'
                    elif self.register_btn_rect.collidepoint(event.pos):
                        self.mode = 'register'
                        self.active_input = 'username'
                    else:
                        self.check_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_TAB:
                        self.switch_focus_next()
                    elif event.key == pygame.K_BACKSPACE:
                        self.backspace()
                    elif event.key == pygame.K_RETURN:
                        result = self.process_submit()
                        if result == 1:
                            return 1,self.username
                        elif result == 2:
                            return 2,self.username
                    else:
                        self.add_char(event.unicode)
            clock.tick(60)

    def switch_focus_next(self):
        order = ['username', 'password']
        idx = order.index(self.active_input)
        idx = (idx + 1) % len(order)
        self.active_input = order[idx]

    def backspace(self):
        if self.active_input == 'username':
            self.username = self.username[:-1]
        elif self.active_input == 'password':
            self.password = self.password[:-1]

    def add_char(self, char):
        if not char.isprintable():
            return
        if self.active_input == 'username':
            self.username += char
        elif self.active_input == 'password':
            self.password += char

    def check_click(self, pos):
        if self.uname_rect.collidepoint(pos):
            self.active_input = 'username'
        elif self.pwd_rect.collidepoint(pos):
            self.active_input = 'password'

    # 1 Login successful
    # 2 Registration successful
    def process_submit(self):
        if self.mode == 'login':
            success = login_user(self.username, self.password)
            if success:
                self.message = "Login successful"
                return 1
            else:
                self.message = "Username not found or wrong password"
                return False
        else:
            if self.username == '':
                self.message = "Username is empty"
                return False
            if self.password == '':
                self.message = "Password is empty"
                return False
            if any(c.isspace() for c in self.username):
                self.message = "Username is invalid"
                return False
            if any(c.isspace() for c in self.password):
                self.message = "Password is invalid"
                return False

            success = register_user(self.username, self.password)
            if success:
                self.message = "Registration successful"
                return 2
            else:
                self.message = "Username already exists"
                return False
