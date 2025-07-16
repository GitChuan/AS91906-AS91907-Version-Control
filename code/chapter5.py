import pygame
import sys
import random
import os

class Hero:
    def __init__(self, name, hp, attack, image_path):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.image_path = image_path

class MathBattleGame5:
    def __init__(self, screen, hero):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.hero = hero

        self.grid_size = 13
        self.cell_size = 55
        self.grid = self.generate_grid()

        self.start = (0, 0)
        self.end = (self.grid_size - 1, self.grid_size - 1)
        self.player_pos = self.start

        self.visited = set()
        self.visited.add(self.player_pos)
        self.path_stack = [self.player_pos]

        self.font = pygame.font.SysFont("arial", 36)
        self.small_font = pygame.font.SysFont("arial", 28)

        self.input_hp = ""
        self.asking_hp = True
        self.user_hp = self.user_max_hp = 0

        self.feedback = ""
        self.game_over = False
        self.win = False
        self.min_required_hp = self.calculate_minimum_hp(self.grid)

    def generate_grid(self):
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) == (0, 0) or (i, j) == (self.grid_size - 1, self.grid_size - 1):
                    grid[i][j] = 0
                else:
                    rand = random.random()
                    if rand < 0.1:
                        grid[i][j] = random.randint(10, 20)  # heal (rare)
                    elif rand < 0.9:
                        grid[i][j] = -random.randint(20, 40)  # damage (common)
                    else:
                        grid[i][j] = 0
        return grid

    def calculate_minimum_hp(self, dungeon):
        n = len(dungeon)
        m = len(dungeon[0])
        dp = [[0] * m for _ in range(n)]

        dp[n-1][m-1] = dungeon[n-1][m-1] if dungeon[n-1][m-1] < 0 else 0

        for i in reversed(range(n)):
            for j in reversed(range(m)):
                if i == n-1 and j == m-1:
                    continue
                value = dungeon[i][j]
                if i == n-1:
                    val = value + dp[i][j+1]
                    dp[i][j] = val if val < 0 else 0
                elif j == m-1:
                    val = value + dp[i+1][j]
                    dp[i][j] = val if val < 0 else 0
                else:
                    down = value + dp[i+1][j]
                    right = value + dp[i][j+1]
                    dp[i][j] = max(down if down < 0 else 0, right if right < 0 else 0)
        return abs(dp[0][0]) + 1

    def draw_hero_info(self):
        card_w, card_h = 350, 160
        padding = 10
        rect = pygame.Rect(padding, padding, card_w, card_h)
        pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=12)
        pygame.draw.rect(self.screen, (220, 220, 220), rect, 2, border_radius=12)

        try:
            if os.path.exists(self.hero.image_path):
                image = pygame.image.load(self.hero.image_path).convert_alpha()
                image = pygame.transform.smoothscale(image, (100, 100))
                self.screen.blit(image, (padding + 10, padding + 30))
        except Exception as e:
            print("英雄图片加载失败:", e)

        name_surf = self.small_font.render(self.hero.name, True, (255, 255, 255))
        self.screen.blit(name_surf, (padding + 120, padding + 20))
        self.screen.blit(self.small_font.render(f"HP: {self.hero.hp}", True, (255, 100, 100)), (padding + 120, padding + 60))
        self.screen.blit(self.small_font.render(f"Attack: {self.hero.attack}", True, (255, 255, 255)), (padding + 120, padding + 100))

    def draw_grid(self):
        start_x = (self.screen.get_width() - self.grid_size * self.cell_size) // 2
        start_y = 180

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = start_x + j * self.cell_size
                y = start_y + i * self.cell_size
                value = self.grid[i][j]
                color = (200, 200, 200) if value == 0 else ((100, 255, 100) if value > 0 else (255, 100, 100))
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 2)

                val_text = f"+{value}" if value > 0 else (f"{value}" if value < 0 else "0")
                val_surf = self.small_font.render(val_text, True, (0, 0, 0))
                val_rect = val_surf.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                self.screen.blit(val_surf, val_rect)

                if (i, j) == self.player_pos:
                    pygame.draw.rect(self.screen, (50, 50, 255), (x+5, y+5, self.cell_size-10, self.cell_size-10))
                if (i, j) == self.end:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x+10, y+10, self.cell_size-20, self.cell_size-20))

    def draw_interface(self):
        self.screen.fill((30, 30, 40))
        self.draw_hero_info()
        self.draw_grid()

        if self.asking_hp:
            prompt = self.font.render("Enter starting HP (min required: {}):".format(self.min_required_hp), True, (255, 255, 0))
            input_surf = self.font.render(self.input_hp, True, (255, 255, 255))
            self.screen.blit(prompt, (80, 20))
            self.screen.blit(input_surf, (600, 20))
        else:
            hp_surf = self.font.render(f"HP: {self.user_hp}", True, (255, 100, 100))
            self.screen.blit(hp_surf, (500, 20))
            self.screen.blit(self.font.render(self.feedback, True, (255, 255, 0)), (50, 60))

            if self.game_over:
                result_text = "You Win!" if self.win else "You Lose!"
                result = self.font.render(result_text, True, (0, 255, 0) if self.win else (255, 0, 0))
                self.screen.blit(result, (self.screen.get_width() // 2 - 100, 700))

        pygame.display.flip()

    def move_player(self, dx, dy):
        if self.game_over or self.asking_hp:
            return False, 0

        if (dx, dy) not in [(1, 0), (0, 1)]:
            self.feedback = "You can only move right or down!"
            return False,0

        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            new_pos = (new_x, new_y)
            self.player_pos = new_pos
            self.path_stack.append(new_pos)
            self.visited.add(new_pos)
            value = self.grid[new_x][new_y]
            self.user_hp += value
            self.feedback = f"Stepped on: {value}"

            if self.user_hp <= 0:
                self.user_hp = 0
                self.game_over = True
                self.win = False

            if self.player_pos == self.end:
                self.game_over = True
                ratio = self.min_required_hp / self.user_hp if self.user_hp != 0 else 2
                if ratio >= 0.8:
                    self.feedback = f"Victory! Score: {int((self.min_required_hp / self.user_max_hp) * 1000)}"
                    self.win = True
                else:
                    self.feedback = f"Too inefficient! Needed {self.min_required_hp}, used {self.user_max_hp}"
                    self.win = False

                self.draw_interface()
                pygame.display.flip()

                # 等待用户按键或点击关闭窗口再退出
                while True:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif e.type == pygame.KEYDOWN:
                            return self.win,(int((self.min_required_hp / self.user_max_hp) * 1000))

        return False, 0

    def run(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False, 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False, 0
                    elif self.asking_hp:
                        if event.key == pygame.K_RETURN:
                            if self.input_hp.isdigit():
                                self.user_hp = int(self.input_hp)
                                self.user_max_hp = self.user_hp
                                self.asking_hp = False
                                self.feedback = ""
                            else:
                                self.feedback = "Invalid input!"
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_hp = self.input_hp[:-1]
                        else:
                            self.input_hp += event.unicode
                    else:
                        if event.key == pygame.K_DOWN:
                            result = self.move_player(1, 0)
                            if result[0] is True: return True, result[1]
                        elif event.key == pygame.K_RIGHT:
                            result = self.move_player(0, 1)
                            if result[0] is True: return True, result[1]
            self.draw_interface()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 800), pygame.FULLSCREEN)
    pygame.display.set_caption("Math Game Chapter 5 - Minimum HP Dungeon")

    hero = Hero("Arya Stark", 120, 30, "../pictures/arya_stark.png")
    game = MathBattleGame5(screen, hero)
    game.run()
    pygame.quit()
