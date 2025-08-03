import pygame
from info_manager import load_rank_data

from choose_houses import HouseSelector, run_house_selector
from mistake_book import MistakeBook
from houses.character import Character
from houses.house_Lannister.Cersei_Lannister import Cersei
from houses.house_Lannister.Tyrion_Lannister import Tyrion
from houses.house_Lannister.Tywin_Lannister import Tywin
from houses.house_Stark.Arya_Stark import Arya
from houses.house_Stark.Bran_Stark import Bran
from houses.house_Stark.Eddard_Stark import Eddard
from houses.others.Jon_Snow import JonSnow

_house_names = ["House Stark", "House Lannister", "others"]
_house_paths = [
    "../pictures/stark_sigil.png",
    "../pictures/lannister_sigil.png",
    "../pictures/others.png",
]

# Dict type for each
_jon_snow = JonSnow().get_display_data()
_arya_stark = Arya().get_display_data()
_bran_stark = Bran().get_display_data()
_eddard_stark = Eddard().get_display_data()
_cersei_lannister = Cersei().get_display_data()
_tyrion_lannister = Tyrion().get_display_data()
_tywin_lannister = Tywin().get_display_data()

# List type
_CHARACTERS = {
    "House Stark": [
        Character(**_arya_stark),
        Character(**_bran_stark),
        Character(**_eddard_stark)
    ],
    "House Lannister": [
        Character(**_tyrion_lannister),
        Character(**_cersei_lannister),
        Character(**_tywin_lannister)
    ],
    "others": [
        Character(**_jon_snow)
    ]
}


# Main menu class
class Menu:
    def __init__(self, screen, username):
        self.username = username

        # Load the house images first, try to make the time reaction for each clicking to the challanges shorter.
        self.selector = HouseSelector(screen, [pygame.image.load(p).convert_alpha() for p in _house_paths], _house_names)

        pygame.init()

        # Initial the screen size
        if screen is None:
            info = pygame.display.Info()
            self.size = (info.current_w, info.current_h)
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            self.screen = screen
            self.size = self.screen.get_size()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 40)
        self.title_font = pygame.font.SysFont("arial", 70, bold=True)

        # Load the background images
        self.background = pygame.transform.scale(pygame.image.load("../pictures/menu_background.png"), self.size)

        # List
        self.buttons = []
        for i, label in enumerate(["Challenge", "Tutorial", "Ranking", "Mistake Book", "Exit"]):
            rect = pygame.Rect((self.size[0] - 300) >> 1, 220 + i * 80, 300, 60)
            self.buttons.append({"label": label, "rect": rect})

    def __render(self):
        self.screen.blit(self.background, (0, 0))
        text = self.title_font.render("Game of Thrones: The Rescue", True, (255, 0, 0))
        self.screen.blit(text, ((self.size[0] - text.get_width()) >> 1, 40))
        for button in self.buttons:
            pygame.draw.rect(self.screen, (50, 0, 0), button["rect"])
            pygame.draw.rect(self.screen, (200, 50, 50), button["rect"], 3)
            text = self.font.render(button["label"], True, (255, 255, 255))
            self.screen.blit(text, (
                button["rect"].x + ((button["rect"].width - text.get_width()) >> 1),
                button["rect"].y + ((button["rect"].height - text.get_height()) >> 1)))

        pygame.display.flip()

    # Show the interface of the ranking
    def __show_ranking(self):
        font = pygame.font.SysFont("arial", 36)
        smaller_font = pygame.font.SysFont("arial", 28)

        # Back button's area
        back_rect = pygame.Rect(50, 50, 120, 50)

        while True:
            # Black interface
            self.screen.fill((20, 20, 20))
            # Title
            title = font.render("Leaderboard", True, (255, 215, 0))
            self.screen.blit(title, ((self.screen.get_width() - title.get_width()) >> 1, 60))
            # Dram the back button
            pygame.draw.rect(self.screen, (100, 50, 50), back_rect)
            self.screen.blit(smaller_font.render("Back", True, (255, 255, 255)), (back_rect.x + 20, back_rect.y + 10))
            # Only ten users will be shown
            for i, player in enumerate(load_rank_data()[:10]):
                text = smaller_font.render(
                    f"{i + 1}. {player['username']} | {player['hero']} | Score: {player['score']} | Time: {player['time']}s",
                    True, (200, 200, 200)
                )
                self.screen.blit(text, (100, 150 + i * 40))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                    return

            self.clock.tick(60)

    # Show the tutorial
    def __show_tutorial(self):
        tutorial_texts = [
            ("Chapter 1 - Easy Arithmetic",
             "Basic addition, subtraction and multiplication questions.\nDon't let the princess down!"),
            ("Chapter 2 - Multiplication & Division",
             "Solve multiplication and division problems. Princess likes things to be simple,\nif the answer is not an integer, please round it in 1 dp."),
            ("Chapter 3 - Square Roots & Multiples",
             "Test your skills with square roots and multiples problems. Princess likes things to be simple,\nif the answer is float, please round it in 1 dp."),
            ("Chapter 4 - Calculus",
             "Solve calculus problems. The princess likes things to be simple. If you need to type x^0, just ignore the x,\nif you need to type x^1, just type x."),
            ("Chapter 5 - Dungeon Survival",
             "Survive through a dungeon to rescue the princess. Your HP should always be positive!\nAnd also, the princess admires the bravest knight!\nSo don't set your initial HP too high, unless it is necessary.")
        ]
        font = pygame.font.SysFont("arial", 40, bold=True)
        small_font = pygame.font.SysFont("arial", 28)
        back_rect = pygame.Rect(50, 50, 120, 50)

        while True:
            # Overlay Background
            self.screen.blit(self.background, (0, 0))
            overlay = pygame.Surface(self.size)  # Create a new screen
            overlay.set_alpha(180)  # Set the overlay screen's transparency
            overlay.fill((30, 30, 30))  # Color up the overlay
            self.screen.blit(overlay, (0, 0))  # Put the overlay screen
            # Draw tutorial's button
            title = font.render("Tutorial", True, (255, 215, 0))
            self.screen.blit(title, ((self.size[0]-title.get_width())>>1, 40))
            # Draw the back button
            pygame.draw.rect(self.screen, (100, 50, 50), back_rect)
            self.screen.blit(small_font.render("Back", True, (255, 255, 255)), (back_rect.x + 20, back_rect.y + 10))

            # Traverse each chapters
            for i, (chapter, desc) in enumerate(tutorial_texts):
                y = 120 + i * 155
                card_rect = pygame.Rect((self.size[0] - 1100) >> 1, y, 1100, 150 if i == 4 else 125)
                pygame.draw.rect(self.screen, (50, 50, 70), card_rect, border_radius=8)
                pygame.draw.rect(self.screen, (100, 100, 150), card_rect, 2, border_radius=8)

                # Draw each title
                self.screen.blit(small_font.render(chapter, True, (255, 255, 255)), (((self.size[0] - 1100) >> 1) + 20, y + 10))

                for j, line in enumerate(desc.split("\n")):
                    text_surface = small_font.render(line, True, (200, 200, 200))
                    self.screen.blit(text_surface, (((self.size[0] - 1100) >> 1) + 20, y + 50 + j * 28))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                    return

            self.clock.tick(60)

    # Main loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # button: dict
                    for button in self.buttons:
                        # If current button's area is where the mouse clicked
                        if button["rect"].collidepoint(event.pos):
                            label = button["label"]
                            if label == "Exit":
                                pygame.quit()
                                return
                            elif label == "Challenge":
                                run_house_selector(self.screen, self.username, self.selector, _CHARACTERS)
                            elif label == "Ranking":
                                self.__show_ranking()
                            elif label == "Mistake Book":
                                MistakeBook(self.screen, self.username).run()
                            elif label == "Tutorial":
                                self.__show_tutorial()

            self.__render()
            self.clock.tick(60)