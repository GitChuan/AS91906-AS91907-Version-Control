import pygame
import sys

from Project.code.choose_heros import run_character_selector
from Project.code.challanges import run_challenge_select  # ✅ 加这个

# 图片路径
house_names = ["House Stark", "House Lannister", "others"]
house_paths = [
    "../pictures/stark_sigil.png",
    "../pictures/lannister_sigil.png",
    "../pictures/others.png",
]

class HouseSelector:
    def __init__(self, screen, house_images, house_names):
        self.screen = screen
        self.house_images = house_images
        self.house_names = house_names
        self.selected_index = None
        self.font = pygame.font.SysFont("arial", 36)
        self.title_font = pygame.font.SysFont("arial", 60, bold=True)
        self.clock = pygame.time.Clock()

        self.house_rects = []
        self.select_button_rect = None
        self.back_button_rect = None
        self.create_layout()

    def create_layout(self):
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = int(300 * 1.5), int(350 * 1.5)
        gap = 60

        total_width = 3 * image_width + 2 * gap
        start_x = (screen_width - total_width) // 2
        y = (screen_height - image_height) // 2

        self.house_rects.clear()
        for i in range(3):
            rect = pygame.Rect(start_x + i * (image_width + gap), y, image_width, image_height)
            self.house_rects.append(rect)

        self.select_button_rect = pygame.Rect(
            (screen_width - 200) // 2,
            y + image_height + 100,
            200, 60
        )

        self.back_button_rect = pygame.Rect(
            screen_width - 220,
            screen_height - 80,
            180, 50
        )

    def draw(self):
        self.screen.fill((15, 15, 15))

        title_text = self.title_font.render("Choose Your House", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(title_text, title_rect)

        for i, rect in enumerate(self.house_rects):
            image = pygame.transform.smoothscale(self.house_images[i], rect.size)
            self.screen.blit(image, rect)

            if self.selected_index == i:
                pygame.draw.rect(self.screen, (255, 215, 0), rect, 5)

            label = self.font.render(self.house_names[i], True, (255, 255, 255))
            label_rect = label.get_rect(center=(rect.centerx, rect.bottom + 30))
            self.screen.blit(label, label_rect)

        pygame.draw.rect(self.screen, (50, 100, 50), self.select_button_rect)
        select_text = self.font.render("Select", True, (255, 255, 255))
        select_rect = select_text.get_rect(center=self.select_button_rect.center)
        self.screen.blit(select_text, select_rect)

        pygame.draw.rect(self.screen, (100, 50, 50), self.back_button_rect)
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
                    for i, rect in enumerate(self.house_rects):
                        if rect.collidepoint(pos):
                            self.selected_index = i
                    if self.select_button_rect.collidepoint(pos) and self.selected_index is not None:
                        return self.house_names[self.selected_index]
                    if self.back_button_rect.collidepoint(pos):
                        return None

            self.draw()
            self.clock.tick(60)


def select_houses_run(screen, username):
    while True:
        house_images = [pygame.image.load(p).convert_alpha() for p in house_paths]
        selector = HouseSelector(screen, house_images, house_names)
        result = selector.run()
        if result is None:
            break

        selected_hero = run_character_selector(result, username)
        if selected_hero is None:break
        if selected_hero == "back":continue
        run_challenge_select(screen, selected_hero, username)
