import pygame
import sys

from Project.code.chapter1 import MathBattleGame1
from Project.code.chapter2 import MathBattleGame2
from Project.code.chapter3 import MathBattleGame3
from Project.code.chapter4 import MathBattleGame4
from Project.code.chapter5 import MathBattleGame5
from Project.code.info_manager import update_progress, load_users

image_paths = [
    "../pictures/chapter1.png",
    "../pictures/chapter2.png",
    "../pictures/chapter3.png",
    "../pictures/chapter4.png",
    "../pictures/chapter5.png",
]

class ChallengeSelect:
    def __init__(self, screen, username, chapter_images, selected_character=None):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 32)
        self.clock = pygame.time.Clock()
        self.chapter_images = chapter_images
        self.selected_character = selected_character

        self.chapters = [
            {"name": "Chapter 1", "unlocked": True},
            {"name": "Chapter 2", "unlocked": False},
            {"name": "Chapter 3", "unlocked": False},
            {"name": "Chapter 4", "unlocked": False},
            {"name": "Chapter 5", "unlocked": False},
        ]

        user = load_users()[username]
        curr_level = user["current_level"]

        for i in range(min(curr_level + 1, 5)):
            self.chapters[i]["unlocked"] = True

        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        self.buttons.clear()
        height = 160
        width = 600
        gap = 40
        screen_w, screen_h = self.screen.get_size()
        total_height = len(self.chapters) * height + (len(self.chapters) - 1) * gap
        start_y = (screen_h - total_height) // 2
        x = (screen_w - width) // 2

        for i in range(len(self.chapters)):
            rect = pygame.Rect(x, start_y + i * (height + gap), width, height)
            self.buttons.append(rect)

    def draw(self):
        self.screen.fill((15, 15, 15))

        if self.selected_character:
            self.draw_hero_card()

        for i, ch in enumerate(self.chapters):
            rect = self.buttons[i]
            image = pygame.transform.smoothscale(self.chapter_images[i], rect.size)

            if not ch["unlocked"]:
                arr = pygame.surfarray.pixels3d(image)
                avg = arr[:, :, :3].mean(axis=2)
                arr[:, :, 0] = avg
                arr[:, :, 1] = avg
                arr[:, :, 2] = avg
                del arr

            self.screen.blit(image, rect)

            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            self.screen.blit(overlay, rect.topleft)

            text = self.font.render(ch["name"], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

            if not ch["unlocked"]:
                lock_font = pygame.font.SysFont("arial", 40)
                lock_text = lock_font.render("🔒", True, (255, 255, 255))
                lock_rect = lock_text.get_rect(center=(rect.right - 40, rect.top + 40))
                self.screen.blit(lock_text, lock_rect)

        pygame.display.flip()

    def draw_hero_card(self):
        card_rect = pygame.Rect(30, 30, 320, 180)
        pygame.draw.rect(self.screen, (40, 40, 40), card_rect, border_radius=12)
        pygame.draw.rect(self.screen, (200, 200, 200), card_rect, width=2, border_radius=12)

        # 头像
        image = pygame.image.load(self.selected_character.image_path).convert_alpha()
        image = pygame.transform.smoothscale(image, (100, 100))
        self.screen.blit(image, (card_rect.x + 15, card_rect.y + 15))

        # 字体
        name_font = pygame.font.SysFont("arial", 28, bold=True)
        stat_font = pygame.font.SysFont("arial", 22)
        ability_font = pygame.font.SysFont("arial", 20, italic=True)

        # 名字
        name_text = name_font.render(self.selected_character.name, True, (255, 255, 255))
        self.screen.blit(name_text, (card_rect.x + 130, card_rect.y + 10))

        # 属性
        stats = [
            f"HP: {self.selected_character.hp}",
            f"Attack: {self.selected_character.attack}",
            f"Intelligence: {self.selected_character.intelligence}",
            f"Charisma: {self.selected_character.charisma}",
        ]
        for i, line in enumerate(stats):
            stat_text = stat_font.render(line, True, (200, 200, 200))
            self.screen.blit(stat_text, (card_rect.x + 130, card_rect.y + 45 + i * 25))

        # 技能名称放左下角，距离卡片左边15像素，底部向上偏15像素
        ability_name = self.selected_character.ability.split(':')[0]
        ability_text = ability_font.render(f"Ability: {ability_name}", True, (150, 150, 255))
        ability_pos_x = card_rect.x + 15
        ability_pos_y = card_rect.bottom - 15 - ability_text.get_height()
        self.screen.blit(ability_text, (ability_pos_x, ability_pos_y))

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
                    for i, rect in enumerate(self.buttons):
                        if rect.collidepoint(pos) and self.chapters[i]["unlocked"]:
                            # print(f"进入{self.chapters[i]['name']}")
                            return i
            self.draw()
            self.clock.tick(60)

    def unlock_next(self, chapter_index):
        if chapter_index + 1 < len(self.chapters):
            self.chapters[chapter_index + 1]["unlocked"] = True


def run_challenge_select(screen, selected_character=None,username=None):
    chapter_images = [pygame.image.load(path).convert_alpha() for path in image_paths]
    selector = ChallengeSelect(screen, username, chapter_images, selected_character)

    while True:
        selected = selector.run()
        if selected is None:
            break
        if selected == 0:
            is_win = MathBattleGame1(screen, selected_character, username).run()
            if is_win:
                selector.unlock_next(selected)
                update_progress(username,1,selected_character,0,0)

        elif selected == 1:
            is_win = MathBattleGame2(screen, selected_character, username).run()
            if is_win:
                selector.unlock_next(selected)
                update_progress(username,2,selected_character,0,0)

        elif selected == 2:
            is_win = MathBattleGame3(screen, selected_character, username).run()
            if is_win:
                selector.unlock_next(selected)
                update_progress(username,3,selected_character,0,0)
        elif selected == 3:
            is_win = MathBattleGame4(screen, selected_character).run()
            if is_win:
                selector.unlock_next(selected)
                update_progress(username,4,selected_character,0,0)
        else:
            result = MathBattleGame5(screen, selected_character).run()
            if result[0] is True:
                selector.unlock_next(selected)
                update_progress(username,5,selected_character.name,result[1],1)
