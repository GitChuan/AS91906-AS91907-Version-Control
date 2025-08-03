import time
import pygame
import sys
import random
from info_manager import update_mistake_book5

class MathBattleGame5:
    def __init__(self, screen, hero, username):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.hero = hero

        self.user_path = ""

        # Maintain username
        self.username = username

        self.start_time = time.time()
        self.used_time = 0

        self.grid_size = 10
        self.cell_size = 60
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
        ret = self.calculate_minimum_hp(self.grid)
        self.min_required_hp = ret[0]
        self.optimal_path = ret[1]

    # Generate grid
    def generate_grid(self):
        grid = []
        for row in range(self.grid_size):
            # Current line
            line = []
            for col in range(self.grid_size):
                if (row == 0 and col == 0) or (row == self.grid_size - 1 and col == self.grid_size - 1):
                    line.append(0)
                    continue
                r = random.random()
                if r < 0.11:
                    # Add hp
                    line.append(random.randint(12, 24))
                elif r < 0.9:
                    # Lose hp
                    line.append(-random.randint(18, 43))
                else:
                    # 0 empty
                    line.append(0)
            grid.append(line)
        return grid

    # Ideas are from https://leetcode.com/problems/dungeon-game/description/
    def calculate_minimum_hp(self, d):
        h = len(d)
        w = len(d[0])
        f = [[0] * w for _ in range(h)]
        p = [[''] * w for _ in range(h)]
        f[-1][-1] = max(1, 1 - d[-1][-1])
        for j in range(w - 2, -1, -1):
            f[-1][j] = max(1, f[-1][j + 1] - d[-1][j])
            p[-1][j] = 'R'
        for i in range(h - 2, -1, -1):
            f[i][-1] = max(1, f[i + 1][-1] - d[i][-1])
            p[i][-1] = 'D'
        for i in range(h - 2, -1, -1):
            for j in range(w - 2, -1, -1):
                if f[i + 1][j] < f[i][j + 1]:
                    p[i][j] = 'D'
                    need = f[i + 1][j]
                else:
                    p[i][j] = 'R'
                    need = f[i][j + 1]
                f[i][j] = max(1, need - d[i][j])
        i = j = 0
        res = ''
        while i != h - 1 or j != w - 1:
            if p[i][j] == 'R':
                res += 'R'
                j += 1
            else:
                res += 'D'
                i += 1
        return f[0][0], res

    # Draw hero card
    def draw_hero_info(self):
        w, h = 350, 160
        pad = 10
        r = pygame.Rect(pad, pad, w, h)
        pygame.draw.rect(self.screen, (40, 40, 40), r, border_radius=12)
        pygame.draw.rect(self.screen, (220, 220, 220), r, 2, border_radius=12)

        img = pygame.image.load(self.hero.image_path).convert_alpha()
        img = pygame.transform.smoothscale(img, (100, 100))
        self.screen.blit(img, (pad + 10, pad + 30))

        txt = self.small_font.render(self.hero.name, 1, (255, 255, 255))
        self.screen.blit(txt, (pad + 120, pad + 20))

        hp = f"HP: {self.hero.hp}"
        atk = f"Attack: {self.hero.attack}"
        self.screen.blit(self.small_font.render(hp, 1, (255, 100, 100)), (pad + 120, pad + 60))
        self.screen.blit(self.small_font.render(atk, 1, (255, 255, 255)), (pad + 120, pad + 100))

    # Draw grid
    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cx = (self.screen.get_width() - self.grid_size * self.cell_size) // 2 + j * self.cell_size
                cy = 180 + i * self.cell_size
                val = self.grid[i][j]
                col = (200, 200, 200)
                if val != 0:
                    col = (100, 255, 100) if val > 0 else (255, 100, 100)
                pygame.draw.rect(self.screen, col, (cx, cy, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (cx, cy, self.cell_size, self.cell_size), 2)

                txt = f"+{val}" if val > 0 else str(val)
                if val == 0:
                    txt = "0"
                t_surf = self.small_font.render(txt, 1, (0, 0, 0))
                t_rect = t_surf.get_rect(center=(cx + self.cell_size // 2, cy + self.cell_size // 2))
                self.screen.blit(t_surf, t_rect)

                if (i, j) == self.player_pos:
                    pygame.draw.rect(self.screen, (50, 50, 255),
                                     (cx + 5, cy + 5, self.cell_size - 10, self.cell_size - 10))
                elif (i, j) == self.end:
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     (cx + 10, cy + 10, self.cell_size - 20, self.cell_size - 20))

    # Draw interface
    def draw_interface(self):
        self.screen.fill((30, 30, 40))
        self.draw_hero_info()
        self.draw_grid()

        if self.asking_hp:
            hp_text = self.font.render(self.input_hp, True, (255, 255, 255))
            prompt = self.font.render("Enter starting HP", True, (255, 255, 0))
            self.screen.blit(prompt, (450, 20))
            self.screen.blit(hp_text, (750, 20))

            if self.feedback:
                fb = self.font.render(self.feedback, True, (255, 0, 0))
                self.screen.blit(fb, (450, 80))
        else:
            hp_display = self.font.render(f"HP: {self.user_hp}", True, (255, 100, 100))
            self.screen.blit(hp_display, (500, 20))

            fb_msg = self.font.render(self.feedback, True, (255, 255, 0))
            self.screen.blit(fb_msg, (50, 800))

            if self.game_over:
                result_text = "You Win!" if self.win else "You Lose!"
                result_color = (0, 255, 0) if self.win else (255, 0, 0)
                result_surf = self.font.render(result_text, True, result_color)
                self.screen.blit(result_surf, (self.screen.get_width() // 2 - 100, 800))

        pygame.display.flip()

    # Move player
    def move(self, dx, dy):
        if self.game_over or self.asking_hp:
            return False, 0

        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            self.player_pos = (new_x, new_y)
            self.path_stack.append(self.player_pos)
            self.visited.add(self.player_pos)

            current_value = self.grid[new_x][new_y]
            self.user_hp += current_value
            self.feedback = f"Stepped on: {current_value}"

            if self.user_hp <= 0:
                self.user_hp = 0
                self.game_over = True
                self.win = False
                self.used_time = round(time.time() - self.start_time, 2)

                update_mistake_book5(
                    self.username, "chapter5", self.grid, self.user_path,
                    self.input_hp, self.optimal_path, self.min_required_hp
                )

            if self.player_pos == self.end:
                self.game_over = True
                self.used_time = round(time.time() - self.start_time, 2)

                if self.user_max_hp != 0:
                    efficiency = self.min_required_hp / self.user_max_hp
                else:
                    efficiency = -1

                if efficiency >= 0.6:
                    self.feedback = f"Victory! Score: {int(efficiency * 1000)}"
                    self.win = True
                else:
                    self.feedback = f"Too inefficient! Needed {self.min_required_hp}, used {self.user_max_hp}"
                    self.win = False

                self.draw_interface()
                pygame.display.flip()

                if not self.win or int(self.input_hp) > self.min_required_hp:
                    update_mistake_book5(
                        self.username, "chapter5", self.grid, self.user_path,
                        self.input_hp, self.optimal_path, self.min_required_hp
                    )

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            return self.win, int(efficiency * 1000)

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
                            # Check for valid input
                            if self.input_hp.isdigit() and int(self.input_hp) > 0 and self.input_hp[0] != '0':
                                self.user_hp = int(self.input_hp)
                                self.user_max_hp = self.user_hp
                                self.asking_hp = False
                                self.feedback = ""
                            else:
                                self.feedback = "Invalid input!"
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_hp = self.input_hp[:-1] # Delete char at the end of the input
                        else:
                            self.input_hp += event.unicode # Append char at the end of the input
                    else: # Only moving down or right is allowed
                        if event.key == pygame.K_DOWN: # User moves down
                            self.user_path += 'D'
                            result = self.move(1, 0)
                            if result[0] is True: return True, result[1],self.used_time
                        elif event.key == pygame.K_RIGHT: # User moves right
                            self.user_path += 'R'
                            result = self.move(0, 1)
                            if result[0] is True: return True, result[1],self.used_time
                        else: self.feedback = "You can only move right or down!"
            self.draw_interface()