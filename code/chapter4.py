import pygame
import sys
import random
import os

class MathBattleGame4:
    def __init__(self, screen, hero):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.hero = hero
        self.player_hp = hero.hp
        self.player_max_hp = hero.hp
        self.player_attack = hero.attack
        self.player_intelligence = hero.intelligence
        self.player_charisma = hero.charisma
        self.player_ability = hero.ability

        self.grid_size = 8
        self.cell_size = 60

        self.grid = []
        for _ in range(self.grid_size):
            row = []
            for _ in range(self.grid_size):
                r = random.random()
                if r < 0.1:
                    # 少量回血格子，回复5-15
                    val = random.randint(5, 15)
                elif r < 0.6:
                    # 敌人格子，造成较大伤害20-50
                    val = -random.randint(20, 100)
                else:
                    # 空地0
                    val = 0
                row.append(val)
            self.grid.append(row)

        self.start = (0, 0)
        self.end = (self.grid_size - 1, self.grid_size - 1)
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.end[0]][self.end[1]] = 0

        self.player_pos = self.start
        self.visited = [[False]*self.grid_size for _ in range(self.grid_size)]
        self.visited[self.start[0]][self.start[1]] = True

        self.font_large = pygame.font.SysFont("arial", 48)
        self.font_medium = pygame.font.SysFont("arial", 36)
        self.font_small = pygame.font.SysFont("arial", 28)

        self.font_card_title = pygame.font.SysFont("arial", 40, bold=True)
        self.font_card_text = pygame.font.SysFont("arial", 26)

        self.feedback = ""
        self.game_over = False
        self.win = False

    def draw_hero_info(self):
        card_w, card_h = 300, 400
        padding = 20
        rect = pygame.Rect(padding, padding, card_w, card_h)
        pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=12)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, 2, border_radius=12)

        try:
            if os.path.exists(self.hero.image_path):
                image = pygame.image.load(self.hero.image_path).convert_alpha()
                image = pygame.transform.smoothscale(image, (150, 150))
                self.screen.blit(image, (padding + 75, padding + 20))
        except Exception as e:
            print("英雄图片加载失败:", e)

        name_surf = self.font_card_title.render(self.hero.name, True, (255, 255, 255))
        self.screen.blit(name_surf, (padding + 20, padding + 180))

        attr_y = padding + 230
        line_gap = 35
        self.screen.blit(self.font_card_text.render(f"HP: {self.player_hp}/{self.player_max_hp}", True, (255, 100, 100)), (padding + 20, attr_y))
        self.screen.blit(self.font_card_text.render(f"Attack: {self.player_attack}", True, (255, 255, 255)), (padding + 20, attr_y + line_gap))
        self.screen.blit(self.font_card_text.render(f"Intelligence: {self.player_intelligence}", True, (100, 255, 255)), (padding + 20, attr_y + line_gap*2))
        self.screen.blit(self.font_card_text.render(f"Charisma: {self.player_charisma}", True, (255, 255, 100)), (padding + 20, attr_y + line_gap*3))

        ability_text = "Ability: " + (self.player_ability if self.player_ability else "None")
        ability_surf = self.font_card_text.render(ability_text, True, (180, 180, 255))
        self.screen.blit(ability_surf, (padding + 20, attr_y + line_gap*5))

    def draw_grid(self):
        offset_x = 350
        top_left_x = offset_x + (self.screen.get_width() - offset_x - self.grid_size * self.cell_size) // 2
        top_left_y = 100

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                rect = pygame.Rect(top_left_x + j * self.cell_size, top_left_y + i * self.cell_size,
                                   self.cell_size, self.cell_size)

                value = self.grid[i][j]
                if value > 0:
                    base_color = (0, 180, 0)    # 回血绿
                elif value < 0 and abs(value) >= 20:
                    base_color = (180, 0, 0)    # 强敌红
                elif value < 0:
                    base_color = (150, 0, 0)    # 普通伤害暗红
                else:
                    base_color = (160, 160, 160)  # 空地灰

                pygame.draw.rect(self.screen, base_color, rect)
                pygame.draw.rect(self.screen, (80, 80, 80), rect, 2)

                if (i, j) == self.player_pos:
                    pygame.draw.rect(self.screen, (50, 50, 255), rect)

                if value != 0:
                    text = self.font_small.render(f"{value:+}", True, (255, 255, 255))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

        sx, sy = self.start
        ex, ey = self.end
        start_rect = pygame.Rect(top_left_x + sy * self.cell_size, top_left_y + sx * self.cell_size,
                                 self.cell_size, self.cell_size)
        end_rect = pygame.Rect(top_left_x + ey * self.cell_size, top_left_y + ex * self.cell_size,
                               self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (50, 255, 50), start_rect, 3)
        pygame.draw.rect(self.screen, (255, 255, 0), end_rect, 3)

    def draw(self):
        self.screen.fill((30, 30, 40))

        self.draw_hero_info()
        self.draw_grid()

        hp_surf = self.font_medium.render(f"HP: {self.player_hp}/{self.player_max_hp}", True, (255, 100, 100))
        self.screen.blit(hp_surf, (self.screen.get_width() - 250, 20))

        feedback_surf = self.font_medium.render(self.feedback, True, (255, 255, 0))
        self.screen.blit(feedback_surf, (self.screen.get_width() - 500, 60))

        if self.game_over:
            result_text = "You Win!" if self.win else "You Lose!"
            result_surf = self.font_large.render(result_text, True, (255, 255, 0))
            rect = result_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
            self.screen.blit(result_surf, rect)

        pygame.display.flip()

    def move_player(self, dx, dy):
        if self.game_over:
            return

        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            new_pos = (new_x, new_y)

            if self.visited[new_x][new_y]:
                damage = abs(self.grid[new_x][new_y]) if self.grid[new_x][new_y] < 0 else 10
                self.player_hp -= damage
                self.feedback = f"Went back! Took {damage} damage!"
                if self.player_hp <= 0:
                    self.player_hp = 0
                    self.game_over = True
                    self.win = False
            else:
                self.visited[new_x][new_y] = True

                val = self.grid[new_x][new_y]
                if val > 0:
                    self.player_hp += val
                    if self.player_hp > self.player_max_hp:
                        self.player_hp = self.player_max_hp
                    self.feedback = f"Got +{val} HP!"
                elif val < 0:
                    self.player_hp += val
                    if self.player_hp <= 0:
                        self.player_hp = 0
                        self.game_over = True
                        self.win = False
                    self.feedback = f"Took {abs(val)} damage!"
                else:
                    self.feedback = ""

            self.player_pos = new_pos

            if self.player_pos == self.end:
                self.game_over = True
                self.win = True

    def run(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.player_hp > 0

                    if not self.game_over:
                        if event.key == pygame.K_UP:
                            self.move_player(-1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move_player(1, 0)
                        elif event.key == pygame.K_LEFT:
                            self.move_player(0, -1)
                        elif event.key == pygame.K_RIGHT:
                            self.move_player(0, 1)

            self.draw()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Grid HP Game Demo")

    class Hero:
        def __init__(self):
            self.image_path = "../pictures/arya_stark.png"
            self.name = "Arya Stark"
            self.hp = 120
            self.attack = 30
            self.intelligence = 25
            self.charisma = 20
            self.ability = "Needle Slash"

    hero = Hero()
    game = MathBattleGame4(screen, hero)
    game.run()

    pygame.quit()
    sys.exit()
