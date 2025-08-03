import pygame
import sys
import random
from info_manager import update_mistake_book1234

CRIT_THRESHOLD = 0.5
DODGE_THRESHOLD = 0.3

class MathBattleGame4:
    def __init__(self, screen, hero, username):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Maintain username
        self.username = username

        self.hero = hero
        self.player_hp = hero.hp
        self.player_max_hp = hero.hp
        self.player_attack = hero.attack
        self.player_intelligence = hero.intelligence
        self.player_charisma = hero.charisma
        self.player_ability = hero.ability

        self.dragon_max_hp = 1000
        self.dragon_hp = self.dragon_max_hp
        self.dragon_attack = 55
        self.dragon_image_path = "../pictures/dragon4.png"

        self.question = ""
        self.answer = ""
        self.user_input = ""

        self.time_limit = 30 * 1000 # Millisecond
        self.start_time = pygame.time.get_ticks()

        self.font_large = pygame.font.SysFont("arial", 48)
        self.font_medium = pygame.font.SysFont("arial", 40)
        self.font_small = pygame.font.SysFont("arial", 28)

        self.feedback = ""
        self.generate_question()

        self.game_over = False
        self.crit_flash_time = 0
        self.dodge_flash_time = 0
        self.flash_duration = 1500 # Millisecond

        # List
        self.damage_texts = []

    # New question
    def generate_question(self):
        # Power of x
        degree = random.randint(1, 3)
        terms = []
        answer_terms = []

        # From high to low power
        for power in reversed(range(degree + 1)):
            # Avoid 0x^a
            coef = random.randint(1, 5) if power > 0 else random.randint(0, 10)
            # If the coefficient is 0
            if coef == 0:
                continue
            # If current power is 0
            if power == 0:
                terms.append(f"{coef}")
            # If current power is 1
            elif power == 1:
                terms.append(f"{coef}x")
                answer_terms.append(f"{coef}")
            # If current power >= 2
            else:
                terms.append(f"{coef}x^{power}")
                if power > 2:
                    answer_terms.append(f"{coef * power}x^{power - 1}")
                else :
                    answer_terms.append(f"{coef * power}x")

        # Join question with +
        func_str = "+".join(terms)
        # Join answer with +
        derivative_str = "+".join(answer_terms) if answer_terms else "0"

        self.question = f"Find the derivative of f(x) = {func_str}"
        self.answer = derivative_str.strip()
        self.user_input = ""
        self.feedback = ""
        self.start_time = pygame.time.get_ticks()

    # Is crit hit
    def calculate_crit(self):
        crit_rate = min((self.player_charisma // 5) * 0.01, CRIT_THRESHOLD)
        return random.random() < crit_rate

    # Is dodge the attack
    def calculate_dodge(self):
        dodge_rate = min((self.player_intelligence // 5) * 0.01, DODGE_THRESHOLD)
        return random.random() < dodge_rate

    # Draw hero card
    def draw_hero_info(self):
        card_w, card_h = 420, 260
        padding = 10
        rect = pygame.Rect(padding, padding, card_w, card_h)
        pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=12)
        pygame.draw.rect(self.screen, (220, 220, 220), rect, 2, border_radius=12)

        # Set the images for hero
        image = pygame.image.load(self.hero.image_path).convert_alpha()
        image = pygame.transform.smoothscale(image, (130, 130))
        self.screen.blit(image, (padding + 10, padding + 40))

        # Set the hero's name
        name_surf = self.font_medium.render(self.hero.name, True, (255, 255, 255))
        self.screen.blit(name_surf, (padding + 160, padding + 20))

        # Set the hero's detail
        small_font = pygame.font.SysFont("arial", 24)
        self.screen.blit(small_font.render(f"HP: {self.player_hp}/{self.player_max_hp}", True, (255, 100, 100)), (padding + 160, padding + 60))
        self.screen.blit(small_font.render(f"Attack: {self.player_attack}", True, (255, 255, 255)), (padding + 160, padding + 90))
        self.screen.blit(small_font.render(f"Intelligence: {self.player_intelligence}", True, (100, 255, 255)), (padding + 160, padding + 120))
        self.screen.blit(small_font.render(f"Charisma: {self.player_charisma}", True, (255, 255, 100)), (padding + 160, padding + 150))

        # ability_font = pygame.font.SysFont("arial", 28, bold=True)
        # ability_text = "Ability: " + (self.player_ability.split(':')[0] if self.player_ability else "None")
        # self.screen.blit(ability_font.render(ability_text, True, (180, 180, 255)), (padding + 10, padding + 180))

    # Draw enemy card
    def draw_dragon_info(self):
        card_w, card_h = 420, 260
        padding = 10
        screen_w = self.screen.get_width()
        rect = pygame.Rect(screen_w - card_w - padding, padding, card_w, card_h)
        pygame.draw.rect(self.screen, (50, 30, 30), rect, border_radius=12)
        pygame.draw.rect(self.screen, (220, 180, 180), rect, 2, border_radius=12)

        # Set enemy's images
        image = pygame.image.load(self.dragon_image_path).convert_alpha()
        image = pygame.transform.smoothscale(image, (130, 130))
        self.screen.blit(image, (rect.x + 10, rect.y + 40))

        # Set enemy's name
        name_surf = self.font_medium.render("Dragon", True, (255, 180, 180))
        self.screen.blit(name_surf, (rect.x + 160, rect.y + 20))

        # Set enemy's detail
        small_font = pygame.font.SysFont("arial", 24)
        self.screen.blit(small_font.render(f"HP: {self.dragon_hp}/{self.dragon_max_hp}", True, (255, 100, 100)), (rect.x + 160, rect.y + 70))
        self.screen.blit(small_font.render(f"Attack: {self.dragon_attack}", True, (255, 255, 255)), (rect.x + 160, rect.y + 110))

    # Draw damage text
    def draw_damage_texts(self):
        now = pygame.time.get_ticks()
        to_remove = []
        for dmg in self.damage_texts:
            elapsed = now - dmg["start_time"]

            # If exist time is more than 1s, then delete it (make it disappear completely)
            if elapsed > 1000:
                to_remove.append(dmg)
                continue
            # From 255 to 0
            alpha = max(255 - int(255 * (elapsed / 1000)), 0)
            # From 0 to -50 (go up)
            y_offset = int(-50 * (elapsed / 1000))

            dmg_surf = self.font_large.render(dmg["text"], True, dmg["color"])
            dmg_surf.set_alpha(alpha)

            x, y = dmg["pos"]
            self.screen.blit(dmg_surf, (x, y + y_offset))

        for dmg in to_remove:
            self.damage_texts.remove(dmg)

    # Draw all the components
    def draw(self):
        self.screen.fill((20, 30, 40))

        self.draw_hero_info()
        self.draw_dragon_info()

        # Draw question
        question_surf = self.font_large.render(self.question, True, (255, 255, 255))
        question_rect = question_surf.get_rect(center=(self.screen.get_width() >> 1, 300))
        self.screen.blit(question_surf, question_rect)

        # Draw input
        input_surf = self.font_large.render(self.user_input, True, (255, 255, 100))
        input_rect = input_surf.get_rect(center=(self.screen.get_width() >> 1, 400))
        self.screen.blit(input_surf, input_rect)

        # Create time bar
        elapsed = pygame.time.get_ticks() - self.start_time
        remaining = max(self.time_limit - elapsed, 0)
        bar_width, bar_height = 400, 30
        bar_x = (self.screen.get_width() - bar_width) >> 1
        bar_y = 450

        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        if remaining > 0:
            fill_width = int(bar_width * remaining / self.time_limit)
            pygame.draw.rect(self.screen, (50, 150, 250), (bar_x, bar_y, fill_width, bar_height))

        feedback_surf = self.font_medium.render(self.feedback, True, (255, 100, 100))
        feedback_rect = feedback_surf.get_rect(center=(self.screen.get_width() // 2, 520))
        self.screen.blit(feedback_surf, feedback_rect)

        if self.game_over:
            result = "You Win!" if self.dragon_hp <= 0 else "You Lose!"
            result_surf = self.font_large.render(result, True, (255, 255, 0))
            result_rect = result_surf.get_rect(center=(self.screen.get_width() // 2, 580))
            self.screen.blit(result_surf, result_rect)

            info_surf = self.font_small.render("Press ESC to exit.", True, (200, 200, 200))
            info_rect = info_surf.get_rect(center=(self.screen.get_width() // 2, 640))
            self.screen.blit(info_surf, info_rect)

        self.draw_damage_texts()
        pygame.display.flip()

    def add_damage_text(self, text, pos, color):
        self.damage_texts.append({"text": text, "pos": pos, "start_time": pygame.time.get_ticks(), "color": color})

    # Main loop
    def run(self):
        def check(s):
            # If user's input is invalid or not simplest
            if len(s) == 0 or "x^0" in s or "x^1" in s:
                return False
            # If user's input begins with "+"
            if s[0] == '+':
                return False
            # Count for minus
            cnt_minus = 0
            # Record previous char
            prev = ''
            for c in s:
                if c == '^':
                    if prev != 'x': return False
                    prev = c
                    cnt_minus = 0
                elif c >= 'a' and c <= 'z':
                    if c == 'x':
                        prev = c
                        cnt_minus = 0
                        continue
                    return False
                elif c == '-':
                    cnt_minus += 1
                    if cnt_minus > 1:
                        return False
                    prev = c
                elif c == '+':
                    if prev == '+':
                        return False
                    prev = c
                    cnt_minus = 0
                elif c >= '0' and c <= '9':
                    prev = c
                    cnt_minus = 0
            return True

        running = True
        while running:
            self.clock.tick(60)
            elapsed = pygame.time.get_ticks() - self.start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.player_hp > 0 and self.dragon_hp <= 0 # true: win, false: lose
                    if self.game_over:
                        continue # Continue is for keeping this program running, wait for the user to respond.
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1] # Delete input char
                    elif event.key == pygame.K_RETURN:
                        user_answer = self.user_input.strip().lower() # Turn user's input into lower case and delete blank space
                        isValid = check(user_answer) # Boolean type for checking valid
                        # If not valid
                        if not isValid:
                            self.feedback = "Input is invalid!"
                            self.user_input = ""
                            continue

                        correct = (user_answer == self.answer.strip().lower()) # Boolean type for checking correct
                        # If correct
                        if correct:
                            # Check whether a critical hit has been made.
                            is_crit = self.calculate_crit()
                            damage = self.player_attack * (2 if is_crit else 1) # Double the attack amount if it is a critical hit.
                            self.dragon_hp -= damage
                            self.dragon_hp = max(self.dragon_hp, 0)
                            if is_crit:
                                self.crit_flash_time = pygame.time.get_ticks()

                            self.feedback = f"Correct! {'CRIT! ' if is_crit else ''}Dragon -{damage} HP"
                            self.add_damage_text(f"-{damage}", (self.screen.get_width() - 360, 80),
                                                 (255, 60, 60) if is_crit else (255, 200, 50))
                        else: # Wrong answer
                            # Update this question into mistake book.
                            update_mistake_book1234(self.username, "chapter4", self.question, self.user_input, self.answer)
                            # Check whether a dodge has been made.
                            if self.calculate_dodge():
                                self.dodge_flash_time = pygame.time.get_ticks()
                                self.feedback = "Wrong! You dodged the attack!" # Avoid this attack
                            else: # Take this attack
                                self.player_hp -= self.dragon_attack
                                self.player_hp = max(self.player_hp, 0)
                                self.feedback = f"Wrong! You took {self.dragon_attack} damage." # Show the message to the user
                                self.add_damage_text(f"-{self.dragon_attack}", (160, 80), (60, 255, 60))

                        if self.player_hp <= 0 or self.dragon_hp <= 0:
                            self.game_over = True
                        else:
                            self.generate_question()
                        # Clear the user input area when restart
                        self.user_input = ""
                    else:
                        self.user_input += event.unicode # Append user input

            # Time limit exceed
            if not self.game_over and elapsed > self.time_limit:
                # Update this question into mistake book
                update_mistake_book1234(self.username, "chapter4", self.question, "", self.answer)
                # Check whether a dodge has been made.
                if self.calculate_dodge():
                    self.dodge_flash_time = pygame.time.get_ticks()
                    self.feedback = "Time's up! Dodged!"
                else:
                    self.player_hp -= self.dragon_attack
                    self.player_hp = max(self.player_hp, 0)
                    self.feedback = f"Time's up! You took {self.dragon_attack} damage."
                    self.add_damage_text(f"-{self.dragon_attack}", (160, 80), (60, 255, 60))

                if self.player_hp <= 0:
                    self.game_over = True
                else:
                    self.generate_question()

            self.draw()
