import pygame
import sys
import random
import os
from fractions import Fraction
from info_manager import update_mistake_book123
class MathBattleGame3:
    def __init__(self, screen, hero, username):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Maintain username
        self.username = username

        # 英雄属性
        self.hero = hero
        self.player_hp = hero.hp
        self.player_max_hp = hero.hp
        self.player_attack = hero.attack
        self.player_intelligence = hero.intelligence
        self.player_charisma = hero.charisma
        self.player_ability = hero.ability

        # 敌人龙属性
        self.dragon_max_hp = 1000
        self.dragon_hp = self.dragon_max_hp
        self.dragon_attack = 50
        self.dragon_image_path = "../pictures/dragon3.png"

        self.question = ""
        self.answer = None
        self.user_input = ""

        self.time_limit = 10 * 1000  # 10秒限制
        self.start_time = pygame.time.get_ticks()

        self.font_large = pygame.font.SysFont("arial", 48)
        self.font_medium = pygame.font.SysFont("arial", 40)
        self.font_small = pygame.font.SysFont("arial", 28)

        self.feedback = ""
        self.generate_question()

        self.game_over = False

        # 闪烁暴击/闪避
        self.crit_flash_time = 0
        self.dodge_flash_time = 0
        self.flash_duration = 1500  # 毫秒

        # 伤害数字动画队列（支持多个同时出现）
        self.damage_texts = []  # 格式: [{"text": "-30", "pos": (x,y), "start_time": t, "color": (r,g,b)}]

    def generate_question(self):
        question_type = random.choice(["square_root", "fraction_add", "multiple", "digit_sum"])

        if question_type == "square_root":
            num = random.choice([i * i for i in range(5, 21)])
            self.question = f"What is the square root of {num}?"
            self.answer = str(int(num ** 0.5))

        elif question_type == "fraction_add":
            a, b = random.randint(1, 5), random.randint(2, 6)
            c, d = random.randint(1, 5), random.randint(2, 6)
            self.question = f"What is {a}/{b} + {c}/{d}? (Give answer as a fraction like 5/6)"
            result = Fraction(a, b) + Fraction(c, d)
            self.answer = str(result)

        elif question_type == "multiple":
            a = random.randint(20, 100)
            b = random.choice([2, 3, 4, 5, 6, 7])
            self.question = f"Is {a} a multiple of {b}? (yes or no)"
            self.answer = "yes" if a % b == 0 else "no"

        elif question_type == "digit_sum":
            num = random.randint(100, 999)
            self.question = f"What is the sum of digits in {num}?"
            self.answer = str(sum(int(d) for d in str(num)))

        self.user_input = ""
        self.feedback = ""
        self.start_time = pygame.time.get_ticks()

    def calculate_crit(self):
        crit_rate = min((self.player_charisma // 5) * 0.01, 0.7)
        return random.random() < crit_rate

    def calculate_dodge(self):
        dodge_rate = min((self.player_intelligence // 5) * 0.01, 0.7)
        return random.random() < dodge_rate

    def draw_hero_info(self):
        card_w, card_h = 420, 260
        padding = 10
        rect = pygame.Rect(padding, padding, card_w, card_h)
        pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=12)
        pygame.draw.rect(self.screen, (220, 220, 220), rect, 2, border_radius=12)

        try:
            if os.path.exists(self.hero.image_path):
                image = pygame.image.load(self.hero.image_path).convert_alpha()
                image = pygame.transform.smoothscale(image, (130, 130))
                self.screen.blit(image, (padding + 10, padding + 40))
        except Exception as e:
            print("英雄图片加载失败:", e)

        name_surf = self.font_medium.render(self.hero.name, True, (255, 255, 255))
        self.screen.blit(name_surf, (padding + 160, padding + 20))

        small_font = pygame.font.SysFont("arial", 24)
        self.screen.blit(small_font.render(f"HP: {self.player_hp}/{self.player_max_hp}", True, (255, 100, 100)), (padding + 160, padding + 60))
        self.screen.blit(small_font.render(f"Attack: {self.player_attack}", True, (255, 255, 255)), (padding + 160, padding + 90))
        self.screen.blit(small_font.render(f"Intelligence: {self.player_intelligence}", True, (100, 255, 255)), (padding + 160, padding + 120))
        self.screen.blit(small_font.render(f"Charisma: {self.player_charisma}", True, (255, 255, 100)), (padding + 160, padding + 150))

        ability_font = pygame.font.SysFont("arial", 28, bold=True)
        ability_text = "Ability: " + (self.player_ability.split(':')[0] if self.player_ability else "None")
        self.screen.blit(ability_font.render(ability_text, True, (180, 180, 255)), (padding + 10, padding + 180))

    def draw_dragon_info(self):
        card_w, card_h = 420, 260
        padding = 10
        screen_w = self.screen.get_width()
        rect = pygame.Rect(screen_w - card_w - padding, padding, card_w, card_h)
        pygame.draw.rect(self.screen, (50, 30, 30), rect, border_radius=12)
        pygame.draw.rect(self.screen, (220, 180, 180), rect, 2, border_radius=12)

        try:
            if os.path.exists(self.dragon_image_path):
                image = pygame.image.load(self.dragon_image_path).convert_alpha()
                image = pygame.transform.smoothscale(image, (130, 130))
                self.screen.blit(image, (rect.x + 10, rect.y + 40))
        except Exception as e:
            print("龙图片加载失败:", e)

        name_surf = self.font_medium.render("Dragon", True, (255, 180, 180))
        self.screen.blit(name_surf, (rect.x + 160, rect.y + 20))

        small_font = pygame.font.SysFont("arial", 24)
        self.screen.blit(small_font.render(f"HP: {self.dragon_hp}/{self.dragon_max_hp}", True, (255, 100, 100)), (rect.x + 160, rect.y + 70))
        self.screen.blit(small_font.render(f"Attack: {self.dragon_attack}", True, (255, 255, 255)), (rect.x + 160, rect.y + 110))

    def draw_flash_text(self, text, color):
        now = pygame.time.get_ticks()
        if (now // 300) % 2 == 0:
            flash_surf = self.font_large.render(text, True, color)
            flash_rect = flash_surf.get_rect(center=(self.screen.get_width() // 2, 480))
            self.screen.blit(flash_surf, flash_rect)

    def draw_damage_texts(self):
        now = pygame.time.get_ticks()
        to_remove = []
        for dmg in self.damage_texts:
            elapsed = now - dmg["start_time"]
            if elapsed > 1000:
                to_remove.append(dmg)
                continue

            alpha = max(255 - int(255 * (elapsed / 1000)), 0)
            y_offset = int(-50 * (elapsed / 1000))

            dmg_surf = self.font_large.render(dmg["text"], True, dmg["color"])
            dmg_surf.set_alpha(alpha)

            x, y = dmg["pos"]
            self.screen.blit(dmg_surf, (x, y + y_offset))

        for dmg in to_remove:
            self.damage_texts.remove(dmg)

    def draw(self):
        self.screen.fill((30, 30, 40))

        self.draw_hero_info()
        self.draw_dragon_info()

        # 题目位置下移100像素
        question_surf = self.font_large.render(self.question, True, (255, 255, 255))
        question_rect = question_surf.get_rect(center=(self.screen.get_width() // 2, 300))
        self.screen.blit(question_surf, question_rect)

        # 输入位置下移100像素
        input_surf = self.font_large.render(self.user_input, True, (255, 255, 100))
        input_rect = input_surf.get_rect(center=(self.screen.get_width() // 2, 400))
        self.screen.blit(input_surf, input_rect)

        elapsed = pygame.time.get_ticks() - self.start_time
        remaining = max(self.time_limit - elapsed, 0)
        bar_width = 400
        bar_height = 30
        bar_x = (self.screen.get_width() - bar_width) // 2
        # 进度条位置下移100像素
        bar_y = 450

        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        if remaining > 0:
            fill_width = int(bar_width * remaining / self.time_limit)
            pygame.draw.rect(self.screen, (50, 150, 250), (bar_x, bar_y, fill_width, bar_height))

        # 反馈信息下移100像素
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

        now = pygame.time.get_ticks()
        if self.crit_flash_time and now - self.crit_flash_time < self.flash_duration:
            self.draw_flash_text("CRIT!", (255, 60, 60))
        if self.dodge_flash_time and now - self.dodge_flash_time < self.flash_duration:
            self.draw_flash_text("DODGE!", (60, 255, 60))

        self.draw_damage_texts()

        pygame.display.flip()

    def add_damage_text(self, text, pos, color):
        self.damage_texts.append({"text": text, "pos": pos, "start_time": pygame.time.get_ticks(), "color": color})

    def run(self):
        def is_valid_answer(s):
            s = s.strip().lower()
            if s == "":
                return False
            if self.answer in ["yes", "no"]:
                return s in ["yes", "no"]
            try:
                if "/" in s:
                    parts = s.split("/")
                    if len(parts) == 2 and all(part.strip().isdigit() for part in parts):
                        return True
                    else:
                        return False
                else:
                    float(s)
                    return True
            except:
                return False

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
                        return self.player_hp > 0 and self.dragon_hp <= 0
                    if self.game_over:
                        continue
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        user_ans = self.user_input.strip().lower()
                        if is_valid_answer(user_ans):
                            correct = False
                            if self.answer in ["yes", "no"]:
                                correct = (user_ans == self.answer)
                            elif "/" in self.answer:
                                correct = (user_ans == self.answer)
                            else:
                                try:
                                    correct = abs(float(user_ans) - float(self.answer)) < 0.01
                                except:
                                    correct = False

                            if correct:
                                is_crit = self.calculate_crit()
                                damage = self.player_attack * (2 if is_crit else 1)
                                self.dragon_hp -= damage
                                self.dragon_hp = max(self.dragon_hp, 0)
                                self.crit_flash_time = pygame.time.get_ticks() if is_crit else 0

                                self.feedback = f"Correct! {'CRIT! ' if is_crit else ''}Dragon -{damage} HP"
                                screen_w = self.screen.get_width()
                                dmg_x = screen_w - 360 - 10 + 160
                                dmg_y = 80
                                self.add_damage_text(f"-{damage}", (dmg_x, dmg_y), (255, 60, 60) if is_crit else (255, 200, 50))

                            else: # Wrong answer
                                update_mistake_book123(self.username, "chapter3", self.question, self.user_input, self.answer)
                                if self.calculate_dodge():
                                    self.dodge_flash_time = pygame.time.get_ticks()
                                    self.feedback = "Wrong! You dodged the attack!"
                                else:
                                    self.player_hp -= self.dragon_attack
                                    self.player_hp = max(self.player_hp, 0)
                                    self.feedback = f"Wrong! You took {self.dragon_attack} damage."
                                    dmg_x = 10 + 160
                                    dmg_y = 60
                                    self.add_damage_text(str(self.dragon_attack), (dmg_x, dmg_y), (60, 255, 60))

                            if self.player_hp <= 0 or self.dragon_hp <= 0:
                                self.game_over = True
                            else:
                                self.generate_question()
                        self.user_input = ""
                    else:
                        if event.unicode.isdigit() or event.unicode in ['/', '.', '-', 'y', 'e', 's', 'n', 'o']:
                            self.user_input += event.unicode

            # 时间到未作答惩罚
            if not self.game_over and elapsed > self.time_limit:
                update_mistake_book123(self.username, "chapter3", self.question, "", self.answer)

                if self.calculate_dodge():
                    self.dodge_flash_time = pygame.time.get_ticks()
                    self.feedback = "Time's up! Dodged!"
                else:
                    self.player_hp -= self.dragon_attack
                    self.player_hp = max(self.player_hp, 0)
                    self.feedback = f"Time's up! You took {self.dragon_attack} damage."
                    dmg_x = 10 + 160
                    dmg_y = 60
                    self.add_damage_text(f"-{self.dragon_attack}", (dmg_x, dmg_y), (60, 255, 60))

                if self.player_hp <= 0:
                    self.game_over = True
                else:
                    self.generate_question()

            self.draw()