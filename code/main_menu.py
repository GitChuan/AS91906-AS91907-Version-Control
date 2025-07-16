import pygame
import sys
import os
import json
from moviepy.editor import VideoFileClip
from Project.code.choose_houses import select_houses_run
from mistake_book import MistakeBook

def lerp_color(color1, color2, t):
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

def load_rank_data():
    if not os.path.exists("users_save.json"):
        return []
    with open("users_save.json", "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            return []

    ranks = []
    for name, info in users.items():
        if info.get("current_level") == 5 and info.get("last_level_info"):
            final = info["last_level_info"]
            ranks.append({
                "username": name,
                "hero": final.get("hero", "Unknown"),
                "score": final.get("score", 0),
                "time": final.get("time_seconds", 9999)
            })
    return sorted(ranks, key=lambda x: (-x["score"], x["time"]))

def show_ranking(screen):
    ranks = load_rank_data()
    font = pygame.font.SysFont("arial", 36)
    small_font = pygame.font.SysFont("arial", 28)
    clock = pygame.time.Clock()

    back_rect = pygame.Rect(50, 50, 120, 50)

    while True:
        screen.fill((20, 20, 20))

        title = font.render("Leaderboard", True, (255, 215, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 60))

        pygame.draw.rect(screen, (100, 50, 50), back_rect)
        back_text = small_font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (back_rect.x + 20, back_rect.y + 10))

        for i, player in enumerate(ranks[:10]):
            line = f"{i+1}. {player['username']} | {player['hero']} | Score: {player['score']} | Time: {player['time']}s"
            text = small_font.render(line, True, (200, 200, 200))
            screen.blit(text, (100, 150 + i * 40))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
        clock.tick(60)

class MainMenu:
    def __init__(self, screen=None, username=None, video_path="../videos/menu_background.mp4", music_path="../sounds/menu_music.mp3"):
        self.username = username

        pygame.init()
        if screen is None:
            info = pygame.display.Info()
            self.size = (info.current_w, info.current_h)
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            self.screen = screen
            self.size = self.screen.get_size()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 40)
        self.title_font = pygame.font.SysFont("arial", 70, bold=True)

        self.clip = VideoFileClip(video_path)
        self.fps = self.clip.fps

        self.music_path = music_path
        self.music_on = True
        pygame.mixer.init()
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        if pygame.mixer.get_init():
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

        btn_width, btn_height = 300, 60
        btn_x = (self.size[0] - btn_width) // 2
        self.start_y = 220
        self.gap = 20

        self.buttons = []
        labels = ["Challenge", "Ranking", "Mistake Book", "Settings", "Exit"]
        for i, label in enumerate(labels):
            btn_y = self.start_y + i * (btn_height + self.gap)
            rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
            self.buttons.append({"label": label, "rect": rect})

        self.in_settings = False

        self.title_colors = [
            (255, 50, 50), (255, 255, 50), (50, 255, 50),
            (50, 255, 255), (50, 50, 255), (255, 50, 255)
        ]
        self.color_cycle_time = 3000

    def draw_title(self):
        t = (pygame.time.get_ticks() % self.color_cycle_time) / self.color_cycle_time
        n = len(self.title_colors)
        idx1 = int(t * n) % n
        idx2 = (idx1 + 1) % n
        local_t = (t * n) - int(t * n)
        color = lerp_color(self.title_colors[idx1], self.title_colors[idx2], local_t)

        title_text = "Game of Thrones: The Rescue"
        text = self.title_font.render(title_text, True, color)
        x = (self.size[0] - text.get_width()) // 2
        y = 40
        self.screen.blit(text, (x, y))

    def draw_buttons(self):
        buttons = self.buttons if not self.in_settings else []
        for btn in buttons:
            pygame.draw.rect(self.screen, (50, 0, 0), btn["rect"])
            pygame.draw.rect(self.screen, (200, 50, 50), btn["rect"], 3)
            text = self.font.render(btn["label"], True, (255, 255, 255))
            self.screen.blit(text, (
                btn["rect"].x + btn["rect"].width // 2 - text.get_width() // 2,
                btn["rect"].y + btn["rect"].height // 2 - text.get_height() // 2))

    def run(self):
        frame_iter = self.clip.iter_frames(fps=self.fps, dtype='uint8')
        while True:
            try:
                frame = next(frame_iter)
            except StopIteration:
                frame_iter = self.clip.iter_frames(fps=self.fps, dtype='uint8')
                frame = next(frame_iter)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.in_settings:
                        self.in_settings = False
                    else:
                        self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if not self.in_settings:
                        for btn in self.buttons:
                            if btn["rect"].collidepoint(pos):
                                label = btn["label"]
                                if label == "Exit":
                                    self.exit_game()
                                elif label == "Challenge":
                                    select_houses_run(self.screen, self.username)
                                elif label == "Ranking":
                                    show_ranking(self.screen)
                                elif label == "Mistake Book":
                                    MistakeBook(self.screen, self.username).run()
                                elif label == "Settings":
                                    self.in_settings = True

            surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            surf = pygame.transform.scale(surf, self.size)
            self.screen.blit(surf, (0, 0))

            self.draw_title()
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def exit_game(self):
        self.clip.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    MainMenu().run()
