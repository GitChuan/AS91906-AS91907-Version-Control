import pygame
import sys

from Project.code.houses.character import Character
from Project.code.houses.house_Lannister.Cersei_Lannister import Cersei
from Project.code.houses.house_Lannister.Tyrion_Lannister import Tyrion
from Project.code.houses.house_Lannister.Tywin_Lannister import Tywin
from Project.code.houses.house_Stark.Arya_Stark import Arya
from Project.code.houses.house_Stark.Bran_Stark import Bran
from Project.code.houses.house_Stark.Eddard_Stark import Eddard
from Project.code.houses.others.Jon_Snow import JonSnow

jon_snow = JonSnow().get_display_data()
arya_stark = Arya().get_display_data()
bran_stark = Bran().get_display_data()
eddard_stark = Eddard().get_display_data()
cersei_lannister = Cersei().get_display_data()
tyrion_lannister = Tyrion().get_display_data()
tywin_lannister = Tywin().get_display_data()


# class Character:
#     def __init__(self, name, image_path, hp, attack, intelligence, charisma, ability):
#         self.name = name
#         self.image_path = image_path
#         self.hp = hp
#         self.attack = attack
#         self.intelligence = intelligence
#         self.charisma = charisma
#         self.ability = ability


CHARACTERS = {
    "House Stark": [
        Character(**arya_stark),
        Character(**bran_stark),
        Character(**eddard_stark)
    ],
    "House Lannister": [
        Character(**tyrion_lannister),
        Character(**cersei_lannister),
        Character(**tywin_lannister)
    ],
    "others": [
        Character(**jon_snow)
    ]
}


class CharacterSelector:
    def __init__(self, screen, characters, username):
        self.username = username # useless here, but could add lock hero function

        self.screen = screen
        self.characters = characters
        self.selected_index = None
        self.font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 32, bold=True)
        self.clock = pygame.time.Clock()
        self.card_rects = []
        self.select_button_rect = None
        self.back_button_rect = None
        self.create_layout()

    def create_layout(self):
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = 300, 450
        gap = 60

        total_width = len(self.characters) * image_width + (len(self.characters) - 1) * gap
        start_x = (screen_width - total_width) // 2
        y = (screen_height - image_height) // 2

        self.card_rects.clear()
        for i in range(len(self.characters)):
            rect = pygame.Rect(start_x + i * (image_width + gap), y, image_width, image_height)
            self.card_rects.append(rect)

        self.select_button_rect = pygame.Rect(
            (screen_width - 200) // 2,
            y + image_height + 80,
            200, 60
        )

        self.back_button_rect = pygame.Rect(
            screen_width - 220,
            screen_height - 80,
            180, 50
        )

    def draw(self):
        self.screen.fill((10, 10, 10))

        title_font = pygame.font.SysFont("arial", 48, bold=True)
        title_text = title_font.render("Choose Your Hero", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 60))
        self.screen.blit(title_text, title_rect)

        for i, rect in enumerate(self.card_rects):
            character = self.characters[i]
            image = pygame.image.load(character.image_path).convert_alpha()
            image = pygame.transform.smoothscale(image, (rect.width, rect.height - 130))
            self.screen.blit(image, rect.topleft)

            if self.selected_index == i:
                highlight_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height + 70)
                pygame.draw.rect(self.screen, (255, 215, 0), highlight_rect, 5)

            name = self.name_font.render(character.name, True, (255, 255, 255))
            self.screen.blit(name, (rect.x + 10, rect.bottom - 120))

            stats = [
                f"HP: {character.hp}",
                f"Attack: {character.attack}",
                f"Intelligence: {character.intelligence}",
                f"Charisma: {character.charisma}"
            ]
            for j, line in enumerate(stats):
                text = self.font.render(line, True, (230, 230, 230))
                self.screen.blit(text, (rect.x + 10, rect.bottom - 85 + j * 25))

        pygame.draw.rect(self.screen, (0, 128, 0), self.select_button_rect)
        button_text = self.font.render("Select", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=self.select_button_rect.center)
        self.screen.blit(button_text, button_rect)

        pygame.draw.rect(self.screen, (128, 0, 0), self.back_button_rect)
        back_text = self.font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for i, rect in enumerate(self.card_rects):
                        if rect.collidepoint(pos):
                            self.selected_index = i
                    if self.select_button_rect.collidepoint(pos) and self.selected_index is not None:
                        result = self.show_character_detail(self.characters[self.selected_index])
                        if result:
                            return result
                        self.selected_index = None
                    if self.back_button_rect.collidepoint(pos):
                        return "back"

            self.draw()
            self.clock.tick(60)

    def show_character_detail(self, character):
        font = pygame.font.SysFont("arial", 28)
        name_font = pygame.font.SysFont("arial", 36, bold=True)
        clock = pygame.time.Clock()

        image = pygame.image.load(character.image_path).convert_alpha()
        image = pygame.transform.smoothscale(image, (300, 400))

        confirm_button_rect = pygame.Rect(400, 500, 200, 60)
        back_button_rect = pygame.Rect(50, 500, 150, 60)

        while True:
            self.screen.fill((5, 5, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_button_rect.collidepoint(event.pos):
                        return character
                    if back_button_rect.collidepoint(event.pos):
                        return None

            self.screen.blit(image, (50, 80))

            name_text = name_font.render(character.name, True, (255, 255, 255))
            self.screen.blit(name_text, (400, 50))

            stats = [
                f"HP: {character.hp}",
                f"Attack: {character.attack}",
                f"Intelligence: {character.intelligence}",
                f"Charisma: {character.charisma}"
            ]
            for i, line in enumerate(stats):
                stat_text = font.render(line, True, (200, 200, 200))
                self.screen.blit(stat_text, (400, 100 + i * 35))

            ability_lines = character.ability.split('\n')
            ability_title = font.render("Ability:", True, (180, 180, 255))
            self.screen.blit(ability_title, (400, 280))
            for i, line in enumerate(ability_lines):
                ability_text = font.render(line, True, (150, 150, 255))
                self.screen.blit(ability_text, (400, 320 + i * 30))

            pygame.draw.rect(self.screen, (0, 128, 0), confirm_button_rect)
            confirm_text = font.render("Confirm", True, (255, 255, 255))
            confirm_rect = confirm_text.get_rect(center=confirm_button_rect.center)
            self.screen.blit(confirm_text, confirm_rect)

            pygame.draw.rect(self.screen, (128, 0, 0), back_button_rect)
            back_text = font.render("Back", True, (255, 255, 255))
            back_rect = back_text.get_rect(center=back_button_rect.center)
            self.screen.blit(back_text, back_rect)

            pygame.display.flip()
            clock.tick(60)


def run_character_selector(house_name, username):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Hero Selection")

    characters = CHARACTERS.get(house_name, [])
    return CharacterSelector(screen, characters,username).run()


# if __name__ == "__main__":
#     selected = run_character_selector("House Stark")
#     if isinstance(selected, Character):
#         print("You selected:", selected.name)
#     elif selected == "back":
#         print("User clicked back.")
#     else:
#         print("No selection made.")
