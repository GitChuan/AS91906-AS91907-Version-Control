import pygame
from info_manager import *

class Login:
    def __init__(self, screen):
        pygame.init()
        # Create full screen
        self.screen = screen
        # Set length and title
        pygame.display.set_caption("Login")

        # Load background images
        self.background_image = pygame.transform.scale(pygame.image.load("../pictures/background.png").convert(),
                                                       self.screen.get_size())

        # Set font
        self.font = pygame.font.SysFont("arial", 48)
        self.smaller_font = pygame.font.SysFont("arial", 32)

        self.mode = 0 # 0: login, 1: register
        self.username = ""
        self.password = ""
        self.active_input = "username"
        self.message = ""

        self.center_x = (self.screen.get_size()[0] - 400) >> 1

        # Draw inputs area
        self.username_rect = pygame.Rect(self.center_x, 220, 400, 48)
        self.password_rect = pygame.Rect(self.center_x, 300, 400, 48)

        width = 180
        height = 50
        gap = 40

        # Draw buttons area
        self.login_button_rect = pygame.Rect((self.screen.get_size()[0] - ((width << 1) + gap)) >> 1,
                                             self.password_rect.bottom + 60, width, height)
        self.register_button_rect = pygame.Rect(
            (self.screen.get_size()[0] - ((width << 1) + gap) >> 1) + width + gap,
            self.password_rect.bottom + 60, width, height)

    def __draw_cracked_rect(self, rect, focused):
        # Make input area transparent
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((*(120, 10, 10), 60))
        self.screen.blit(s, (rect.x, rect.y))
        pygame.draw.rect(self.screen, (120, 10, 10), rect, 4 if focused else 2)

        # Draw the boarder
        gap = 6
        for x in range(rect.x, rect.x + rect.width, gap):
            if x % (gap << 1) == 0:
                pygame.draw.line(self.screen, (200, 50, 50), (x, rect.y), (x + (gap >> 1), rect.y + 2), 2)
                pygame.draw.line(self.screen, (200, 50, 50), (x, rect.y + rect.height),
                                 (x + (gap >> 1), rect.y + rect.height - 2), 2)
        for y in range(rect.y, rect.y + rect.height, gap):
            if y % (gap << 1) == 0:
                pygame.draw.line(self.screen, (200, 50, 50), (rect.x, y), (rect.x + 2, y + (gap >> 1)), 2)
                pygame.draw.line(self.screen, (200, 50, 50), (rect.x + rect.width, y),
                                 (rect.x + rect.width - 2, y + (gap >> 1)), 2)

    def __draw_button(self, rect, text, selected):
        # Get current mouse position and paint the button if it is on it.
        position = pygame.mouse.get_pos()
        color = (180, 40, 40) if rect.collidepoint(position) and not selected else (120, 10, 10)

        # Draw the button with boarder radius
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (200, 50, 50), rect, 3, border_radius=8)

        # Draw the fonts
        text_surface = self.smaller_font.render(text, True, (255, 180, 180) if selected else (180, 180, 180))
        self.screen.blit(text_surface, (rect.centerx - (text_surface.get_width() >> 1),
                                        rect.centery - (text_surface.get_height() >> 1)))

    def __draw(self):
        # Put background images into the screen
        self.screen.blit(self.background_image, (0, 0))

        # Draw the title
        title_text = "Rescue the Dragon Queen - Login" if self.mode == 0 else "Rescue the Dragon Queen - Register"
        title = self.font.render(title_text, True, (200, 50, 50))
        self.screen.blit(title, ((self.screen.get_size()[0] - title.get_width()) >> 1, 100))

        # Draw username style
        self.screen.blit(self.smaller_font.render("Username:", True, (180, 180, 180)),
                         (self.center_x - 150, self.username_rect.y + 10))
        self.__draw_cracked_rect(self.username_rect, self.active_input == "username")
        self.screen.blit(
            self.smaller_font.render(self.username + ('|' if self.active_input == "username" else ""), True,
                                     (220, 220, 220)), (self.username_rect.x + 10, self.username_rect.y + 8))

        # Draw password style
        self.screen.blit(self.smaller_font.render("Password:", True, (180, 180, 180)), (self.center_x - 150, self.password_rect.y + 10))
        self.__draw_cracked_rect(self.password_rect, self.active_input == "password")
        password_text = self.smaller_font.render(('*' * len(self.password)) + ('|' if self.active_input == "password" else ""), True,
                                            (220, 220, 220))
        self.screen.blit(password_text, (self.password_rect.x + 10, self.password_rect.y + 8))

        # Draw the buttons
        self.__draw_button(self.login_button_rect, "Login", self.mode == 0)
        self.__draw_button(self.register_button_rect, "Register", self.mode == 1)

        # Draw the remainder font
        submit_render = self.smaller_font.render("Press ENTER to Login" if self.mode == 0 else "Press ENTER to Register", True, (100, 100, 100))
        self.screen.blit(submit_render, (
            (self.screen.get_size()[0] - submit_render.get_width()) >> 1, self.screen.get_size()[1] - 100))

        # Draw respond to user
        if self.message:
            message_text = self.smaller_font.render(self.message, True, (255, 100, 100))
            self.screen.blit(message_text,
                             ((self.screen.get_size()[0] - message_text.get_width()) >> 1, self.screen.get_size()[1] - 150))
        # Refresh
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.__draw()
            for event in pygame.event.get():
                # Exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check user's click
                    if self.login_button_rect.collidepoint(event.pos):
                        self.mode = 0
                        self.active_input = "username"
                    elif self.register_button_rect.collidepoint(event.pos):
                        self.mode = 1
                        self.active_input = "username"
                    else:
                        if self.username_rect.collidepoint(event.pos):
                            self.active_input = "username"
                        elif self.password_rect.collidepoint(event.pos):
                            self.active_input = "password"
                # Check user's keyboard
                elif event.type == pygame.KEYDOWN:
                    # Esc
                    if event.key == pygame.K_ESCAPE:
                        return None
                    # Tab
                    elif event.key == pygame.K_TAB:
                        self.active_input = "password" if self.active_input == "username" else "username"
                    elif event.key == pygame.K_BACKSPACE:
                        if self.active_input == "username":
                            self.username = self.username[:-1]
                        else:
                            self.password = self.password[:-1]
                    elif event.key == pygame.K_RETURN:
                        ret = self.__check()
                        if ret == 1:  # Login successful
                            return 1, self.username
                        elif ret == 2:  # Registration successful
                            return 2, self.username
                        else: self.message = ret
                    else:  # Add char
                        char = event.unicode
                        if not char.isprintable():
                            self.message = "Input is invalid"
                            return
                        if self.active_input == "username":
                            self.username += char
                        else:
                            self.password += char
            clock.tick(60)

    # Check username and password
    def __check(self):
        # If current mode is login
        if self.mode == 0:
            if login_user(self.username, self.password):
                return 1
            else:
                return "Username not found or wrong password."
        else: # Register
            # If username is empty or contains all blank spaces
            if len(self.username) == 0:
                return "Username is empty"
            # If password is empty or contains all blank spaces
            if len(self.password) == 0:
                return "Password is empty."

            # If username contains blank spaces
            for ch in self.username:
                if ch == ' ':
                    return "Username contains spaces."
            # If password contains blank spaces
            for ch in self.password:
                if ch == ' ':
                    return "Password contains spaces."

            # If the length of username is greater than 20
            if len(self.username) > 20:
                return "Username is too long, max 20 characters."
            # If the length of password is greater than 20
            if len(self.password) > 20:
                return "Password is too long, max 20 characters"
            # Register mode
            if register_user(self.username, self.password):
                return 2
            # If same username has been found
            else:
                return "Username already exists"