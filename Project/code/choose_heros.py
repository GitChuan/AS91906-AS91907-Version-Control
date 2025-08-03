import pygame
import sys

class CharacterSelector:
    def __init__(self, screen, characters, username):
        self.username = username

        self.screen = screen
        self.characters = characters
        self.active = None
        self.font = pygame.font.SysFont("arial", 28)
        self.name_font = pygame.font.SysFont("arial", 32, bold=True)
        self.clock = pygame.time.Clock()
        self._zones = []
        self._confirm = None
        self._back = None
        self._setup()

    # Draw the layout for the heros
    def _setup(self):
        # Calculate the whole heros width
        width = len(self.characters) * 300 + (len(self.characters) - 1) * 60
        x0 = (self.screen.get_size()[0] - width) >> 1
        y0 = (self.screen.get_size()[1] - 450) >> 1

        # Clear the previous list
        self._zones.clear()
        # Append each character's area into list
        for i in range(len(self.characters)):
            rect = pygame.Rect(x0 + i * 360, y0, 300, 450)
            self._zones.append(rect)

        # Create the select button's area
        self._confirm = pygame.Rect(
            (self.screen.get_size()[0] - 200) >> 1,
            y0 + 450 + 80,
            200, 60
        )

        # Create the back button's area
        self._back = pygame.Rect(
            self.screen.get_size()[0] - 220,
            self.screen.get_size()[1] - 80,
            180, 50
        )

    # Draw all the components
    def _render(self):
        self.screen.fill((10, 10, 10))
        # Title
        text = pygame.font.SysFont("arial", 48, bold=True).render("Choose Your Hero", True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen.get_width() >> 1, 60))
        self.screen.blit(text, rect)

        for i, rect in enumerate(self._zones):
            character = self.characters[i]
            self.screen.blit(pygame.transform.smoothscale(pygame.image.load(character.image_path).convert_alpha(), (rect.width, rect.height - 130)), rect.topleft)

            if self.active == i:
                click = pygame.Rect(rect.x, rect.y, rect.width, rect.height + 70)
                pygame.draw.rect(self.screen, (255, 215, 0), click, 5)

            name = self.name_font.render(character.name, True, (255, 255, 255))
            self.screen.blit(name, (rect.x + 10, rect.bottom - 120))

            list = [
                f"HP: {character.hp}",
                f"Attack: {character.attack}",
                f"Intelligence: {character.intelligence}",
                f"Charisma: {character.charisma}"
            ]

            for j, line in enumerate(list):
                self.screen.blit(self.font.render(line, True, (230, 230, 230)), (rect.x + 10, rect.bottom - 85 + j * 25))

        pygame.draw.rect(self.screen, (0, 128, 0), self._confirm)
        text = self.font.render("Select", True, (255, 255, 255))
        rect = text.get_rect(center=self._confirm.center)
        self.screen.blit(text, rect)

        pygame.draw.rect(self.screen, (128, 0, 0), self._back)
        text = self.font.render("Back", True, (255, 255, 255))
        rect = text.get_rect(center=self._back.center)
        self.screen.blit(text, rect)

        pygame.display.flip()

    # Main loop
    def run(self):
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                    return None # Esc
                elif evt.type == pygame.MOUSEBUTTONDOWN:
                    pos = evt.pos # Get current pos
                    for i, rect in enumerate(self._zones):
                        # If user's mouse has clicked the current rect(area of ith hero)
                        if rect.collidepoint(pos):
                            self.active = i
                    # If user's mouse has clicked the "select" button on the specific hero
                    if self._confirm.collidepoint(pos) and self.active is not None:
                        result = self.show_info(self.characters[self.active])
                        # If user confirm choosing
                        if result:
                            return result
                        self.active = None
                    if self._back.collidepoint(pos):
                        return None

            self._render()
            self.clock.tick(60)

    # Enter a more specific interface to explain hero's information
    def show_info(self, character):
        # Set font
        name = pygame.font.SysFont("arial", 36, bold=True)

        # Set images
        image = pygame.transform.smoothscale(pygame.image.load(character.image_path).convert_alpha(), (300, 400))

        # Set buttons
        confirm = pygame.Rect(400, 500, 200, 60)
        back = pygame.Rect(50, 500, 150, 60)

        # Wait for user to respond
        while True:
            self.screen.fill((5, 5, 5))
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                    return None
                elif evt.type == pygame.MOUSEBUTTONDOWN:
                    if confirm.collidepoint(evt.pos):
                        return character
                    if back.collidepoint(evt.pos):
                        return None
            # Put images
            self.screen.blit(image, (50, 80))
            self.screen.blit(name.render(character.name, True, (255, 255, 255)), (400, 50))

            list = [
                f"HP: {character.hp}",
                f"Attack: {character.attack}",
                f"Intelligence: {character.intelligence}",
                f"Charisma: {character.charisma}"
            ]

            # Draw each information
            for i, line in enumerate(list):
                text = self.font.render(line, True, (200, 200, 200))
                self.screen.blit(text, (400, 100 + i * 35))

            # Draw confirm button
            pygame.draw.rect(self.screen, (0, 128, 0), confirm)
            text = self.font.render("Confirm", True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=confirm.center))

            # Draw back button
            pygame.draw.rect(self.screen, (128, 0, 0), back)
            text = self.font.render("Back", True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=back.center))

            pygame.display.flip()
            self.clock.tick(60)

# External function
def run_character_selector(screen, housename, username, CHARACTERS):
    return CharacterSelector(screen, CHARACTERS.get(housename),username).run()