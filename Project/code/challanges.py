import pygame
import sys

from chapter1 import MathBattleGame1
from chapter2 import MathBattleGame2
from chapter3 import MathBattleGame3
from chapter4 import MathBattleGame4
from chapter5 import MathBattleGame5
from info_manager import update_progress, load_users

# Image paths for each chapter
image_paths = [
    "../pictures/chapter1.png",
    "../pictures/chapter2.png",
    "../pictures/chapter3.png",
    "../pictures/chapter4.png",
    "../pictures/chapter5.png",
]

# Select chapters class
class ChallengeSelect:
    def __init__(self, screen, username, chapter_images, selected_character):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 32)
        self.clock = pygame.time.Clock()
        self.images = chapter_images
        self.selected_character = selected_character

        self.max_level = 5

        # Dict type to store each chapter's status
        self.chapters = [
            {"name": "Chapter 1", "unlocked": True},
            {"name": "Chapter 2", "unlocked": False},
            {"name": "Chapter 3", "unlocked": False},
            {"name": "Chapter 4", "unlocked": False},
            {"name": "Chapter 5", "unlocked": False},
        ]

        # Load user
        user = load_users()[username]
        curr_level = user["current_level"]
        for i in range(min(curr_level + 1, 5)):
            self.chapters[i]["unlocked"] = True

        self.buttons = []  # Store each chapter's button
        self._set_up()

    # Create the button layout
    def _set_up(self):
        self.buttons.clear()
        height = 160
        width = 600
        gap = 40
        total_height = len(self.chapters) * height + (len(self.chapters) - 1) * gap
        start_y = (self.screen.get_height() - total_height) >> 1
        x = (self.screen.get_width() - width) >> 1

        # Create each chapter's area
        i = 0
        while i < self.max_level:
            rect = pygame.Rect(x, start_y + i * (height + gap), width, height)
            self.buttons.append(rect)
            i+=1

    # Draw the whole interface
    def _render(self):
        self.screen.fill((15, 15, 15))  # Background color

        if self.selected_character:
            self.draw_hero_card()  # Draw the hero card

        # Draw each chapter and button
        i = 0
        while i < self.max_level:
            rect = self.buttons[i]
            image = pygame.transform.smoothscale(self.images[i], rect.size)
            if not self.chapters[i]["unlocked"]:
                arr = pygame.surfarray.pixels3d(image)
                avg = arr[:, :, :3].mean(axis=2)
                arr[:, :, 0] = avg
                arr[:, :, 1] = avg
                arr[:, :, 2] = avg
                del arr

            self.screen.blit(image, rect)

            # Create a transparent surface
            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            # Cover it into chapter images
            self.screen.blit(overlay, rect.topleft)

            # Create the chapter name
            text = self.font.render(self.chapters[i]["name"], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

            i+=1

        pygame.display.flip()

    # Draw the hero card
    def draw_hero_card(self):
        card_rect = pygame.Rect(30, 30, 320, 180)
        pygame.draw.rect(self.screen, (40, 40, 40), card_rect, border_radius=12)
        pygame.draw.rect(self.screen, (200, 200, 200), card_rect, width=2, border_radius=12)

        # Head picture
        image = pygame.image.load(self.selected_character.image_path).convert_alpha()
        image = pygame.transform.smoothscale(image, (100, 100))
        self.screen.blit(image, (card_rect.x + 15, card_rect.y + 15))

        # Create the font and its style
        font = pygame.font.SysFont("arial", 28, bold=True)
        smaller_font = pygame.font.SysFont("arial", 22)

        # Hero's name
        name_text = font.render(self.selected_character.name, True, (255, 255, 255))
        self.screen.blit(name_text, (card_rect.x + 130, card_rect.y + 10))

        # Hero's property
        stats = [
            f"HP: {self.selected_character.hp}",
            f"Attack: {self.selected_character.attack}",
            f"Intelligence: {self.selected_character.intelligence}",
            f"Charisma: {self.selected_character.charisma}",
        ]

        # Draw hero's property into the card
        i = 0
        n = len(stats)
        while i < n:
            text = smaller_font.render(stats[i], True, (200, 200, 200))
            self.screen.blit(text, (card_rect.x + 130, card_rect.y + 45 + i * 25))
            i+=1

    # Main loop
    def run(self):
        while True:
            for env in pygame.event.get():
                if env.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif env.type == pygame.KEYDOWN and env.key == pygame.K_ESCAPE:
                    return None  # Esc
                elif env.type == pygame.MOUSEBUTTONDOWN:
                    pos = env.pos
                    i = 0
                    n = len(self.buttons)
                    while i < n:
                        if self.buttons[i].collidepoint(pos) and self.chapters[i]["unlocked"]:
                            return i
                        i+=1
            self._render()
            self.clock.tick(60)

    # Unlock the next chapter
    def unlock_next(self, chapter_index):
        if chapter_index + 1 < len(self.chapters):
            self.chapters[chapter_index + 1]["unlocked"] = True

# Main function
def run_challenge_selector(screen, hero=None, username=None):
    selector = ChallengeSelect(screen, username, [pygame.image.load(path).convert_alpha() for path in image_paths], hero)

    while True:
        selected = selector.run()
        if selected is None:
            break

        # If user selects chapter 1
        if selected == 0:
            is_win = MathBattleGame1(screen, hero, username).run()
            if is_win:
                selector.unlock_next(selected)
                update_progress(username, 1, hero, 0, 0)

        # If user selects chapter 2
        elif selected == 1:
            is_win = MathBattleGame2(screen, hero, username).run()
            if is_win:
                selector.unlock_next(selected)
                update_progress(username, 2, hero, 0, 0)

        # If user selects chapter 3
        elif selected == 2:
            is_win = MathBattleGame3(screen, hero, username).run()
            if is_win:
                selector.unlock_next(selected)
                update_progress(username, 3, hero, 0, 0)
        # If user selects chapter 4
        elif selected == 3:
            is_win = MathBattleGame4(screen, hero, username).run()
            if is_win:
                selector.unlock_next(selected)
                update_progress(username, 4, hero, 0, 0)
        # If user selects chapter 5
        else:  # result = (True/False, score, used_time/None)
            result = MathBattleGame5(screen, hero, username).run()
            if result[0] is True:
                selector.unlock_next(selected)
                update_progress(username, 5, hero.name, result[1], result[2])
