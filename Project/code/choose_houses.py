import pygame
from choose_heros import run_character_selector
from challanges import run_challenge_selector

class HouseSelector:
    def __init__(self, screen, house_images, house_names):
        self.screen = screen
        self.images = house_images
        self.house_names = house_names
        self.active = None
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 36)
        self.title_font = pygame.font.SysFont("arial", 60, bold=True)

        self._zones = []
        self._confirm = None
        self._back = None

        self._setup()

    def _setup(self):
        w, h = self.screen.get_size()
        total = 3 * 450 + 120
        x0 = (w - total) // 2
        y0 = (h - 450) // 2

        self._zones.clear()
        for i in range(3):
            r = pygame.Rect(x0 + i * 510, y0, 450, 450)
            self._zones.append(r)

        self._confirm = pygame.Rect((w - 200) // 2, y0 + 550, 200, 60)
        self._back = pygame.Rect(w - 220, h - 80, 180, 50)

    def _render(self):
        self.screen.fill((15, 15, 15))

        pygame.draw.rect(self.screen, (50, 100, 50), self._confirm)
        msg = self.font.render("Select", True, (253, 255, 254))
        self.screen.blit(msg, msg.get_rect(center=self._confirm.center))

        # Draw back button
        pygame.draw.rect(self.screen, (100, 50, 50), self._back)
        back_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=self._back.center))

        for i, r in enumerate(self._zones):
            self.screen.blit(pygame.transform.smoothscale(self.images[i], r.size), r)
            if self.active == i:
                pygame.draw.rect(self.screen, (255, 215, 0), r, 5)
            label = self.font.render(self.house_names[i], True, (255, 255, 255))
            self.screen.blit(label, label.get_rect(center=(r.centerx, r.bottom + 30)))

        title = self.title_font.render("Choose Your House", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(self.screen.get_width() // 2, 80)))

    def run(self):
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                    return
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    p = evt.pos
                    for i, r in enumerate(self._zones):
                        if r.collidepoint(p):
                            self.active = i
                    if self._confirm.collidepoint(p) and self.active is not None:
                        return self.house_names[self.active]
                    if self._back.collidepoint(p):
                        return

            self._render()
            pygame.display.flip()
            self.clock.tick(60)


def run_house_selector(screen, username, selector, CHARACTERS):
    while True:
        picked = selector.run()
        if picked is None:
            return
        chosen = run_character_selector(screen, picked, username, CHARACTERS)
        if chosen is None:
            continue
        run_challenge_selector(screen, chosen, username)
