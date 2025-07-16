import pygame
import sys
from info_manager import load_users, save_user

class MistakeBook:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.user_data = load_users().get(username, {})
        self.mistake_book = self.user_data.get("mistake_book", {})

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 24)

        self.state = "chapter_select"  # chapter_select / question_list / question_detail / confirm_delete
        self.selected_chapter = None
        self.selected_question = None

        self.page = 0
        self.per_page = 15

    def run(self):
        running = True
        while running:
            self.screen.fill((30, 30, 40))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "chapter_select":
                            running = False
                        elif self.state == "question_list":
                            self.state = "chapter_select"
                            self.selected_chapter = None
                            self.page = 0
                        elif self.state == "question_detail":
                            self.state = "question_list"
                        elif self.state == "confirm_delete":
                            self.state = "question_detail"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键
                        pos = event.pos
                        if self.state == "chapter_select":
                            self.handle_chapter_click(pos)
                        elif self.state == "question_list":
                            self.handle_question_click(pos)
                            self.handle_pagination_click(pos)
                        elif self.state == "question_detail":
                            self.handle_detail_buttons(pos)
                        elif self.state == "confirm_delete":
                            self.handle_confirm_buttons(pos)

            if self.state == "chapter_select":
                self.draw_chapter_buttons()
            elif self.state == "question_list":
                self.draw_question_list()
            elif self.state == "question_detail":
                self.draw_question_detail()
            elif self.state == "confirm_delete":
                self.draw_confirm_delete()

            pygame.display.flip()
            self.clock.tick(60)

    def draw_chapter_buttons(self):
        screen_w, screen_h = self.screen.get_size()
        btn_w, btn_h = 300, 60
        gap = 20
        start_y = (screen_h - (btn_h + gap) * 5) // 2

        for i in range(1, 6):
            x = (screen_w - btn_w) // 2
            y = start_y + (i - 1) * (btn_h + gap)
            text = f"Chapter {i}"
            surf = self.font.render(text, True, (255, 255, 255))
            rect = pygame.Rect(x, y, btn_w, btn_h)
            pygame.draw.rect(self.screen, (70, 70, 120), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            self.screen.blit(surf, (rect.x + 20, rect.y + 15))
            setattr(self, f"chapter{i}_rect", rect)

    def handle_chapter_click(self, pos):
        for i in range(1, 6):
            rect = getattr(self, f"chapter{i}_rect")
            if rect.collidepoint(pos):
                self.selected_chapter = f"chapter{i}"
                self.state = "question_list"
                self.selected_question = None
                self.page = 0
                break

    def draw_question_list(self):
        questions = list(self.mistake_book.get(self.selected_chapter, {}).keys())
        total = len(questions)

        start = self.page * self.per_page
        end = start + self.per_page
        visible = questions[start:end]

        if not questions:
            text = self.font.render("No mistakes in this chapter.", True, (200, 200, 200))
            self.screen.blit(text, (50, 50))
            return

        for i, q in enumerate(visible):
            surf = self.small_font.render(q, True, (180, 180, 180))
            rect = pygame.Rect(50, 50 + i * 50, self.screen.get_width() - 100, 40)  # 宽度适配屏幕宽度，左右各留50边距
            pygame.draw.rect(self.screen, (50, 50, 80), rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
            self.screen.blit(surf, rect.topleft)
            setattr(self, f"question_{i}_rect", rect)

        # 分页信息
        max_page = max(1, (total - 1) // self.per_page + 1)
        page_info = self.small_font.render(f"Total: {total} | Page: {self.page + 1}/{max_page}", True, (200, 200, 200))
        self.screen.blit(page_info, (50, self.screen.get_height() - 80))

        # 左右按钮（只有题目超过一页时显示）
        if total > self.per_page:
            btn_y = self.screen.get_height() - 70
            btn_w, btn_h = 60, 40
            # 左按钮靠近屏幕中间偏左
            self.prev_btn = pygame.Rect(self.screen.get_width() // 2 - 100, btn_y, btn_w, btn_h)
            # 右按钮靠近屏幕中间偏右
            self.next_btn = pygame.Rect(self.screen.get_width() // 2 + 40, btn_y, btn_w, btn_h)
            pygame.draw.rect(self.screen, (70, 70, 120), self.prev_btn)
            pygame.draw.rect(self.screen, (70, 70, 120), self.next_btn)
            self.screen.blit(self.small_font.render("<", True, (255, 255, 255)), (self.prev_btn.x + 20, self.prev_btn.y + 5))
            self.screen.blit(self.small_font.render(">", True, (255, 255, 255)), (self.next_btn.x + 20, self.next_btn.y + 5))

    def handle_pagination_click(self, pos):
        questions = list(self.mistake_book.get(self.selected_chapter, {}).keys())
        max_page = max(0, (len(questions) - 1) // self.per_page)
        if hasattr(self, 'prev_btn') and self.prev_btn.collidepoint(pos) and self.page > 0:
            self.page -= 1
        if hasattr(self, 'next_btn') and self.next_btn.collidepoint(pos) and self.page < max_page:
            self.page += 1

    def handle_question_click(self, pos):
        questions = list(self.mistake_book.get(self.selected_chapter, {}).keys())
        visible = questions[self.page * self.per_page:(self.page + 1) * self.per_page]
        for i, q in enumerate(visible):
            rect = getattr(self, f"question_{i}_rect")
            if rect.collidepoint(pos):
                self.selected_question = q
                self.state = "question_detail"
                break

    def draw_question_detail(self):
        mistake = self.mistake_book[self.selected_chapter][self.selected_question]
        y = 100
        question_surf = self.font.render(f"Question: {self.selected_question}", True, (255, 255, 255))
        user_ans_surf = self.font.render(f"Your answer: {mistake['user_answer']}", True, (255, 100, 100))
        correct_ans_surf = self.font.render(f"Correct answer: {mistake['correct_answer']}", True, (100, 255, 100))
        self.screen.blit(question_surf, (50, y))
        self.screen.blit(user_ans_surf, (50, y + 80))
        self.screen.blit(correct_ans_surf, (50, y + 160))

        # 删除按钮
        self.delete_btn = pygame.Rect(50, y + 250, 150, 50)
        pygame.draw.rect(self.screen, (180, 50, 50), self.delete_btn)
        pygame.draw.rect(self.screen, (255, 255, 255), self.delete_btn, 2)
        del_txt = self.small_font.render("Delete", True, (255, 255, 255))
        self.screen.blit(del_txt, (self.delete_btn.x + 30, self.delete_btn.y + 10))

    def handle_detail_buttons(self, pos):
        if self.delete_btn.collidepoint(pos):
            self.state = "confirm_delete"

    def draw_confirm_delete(self):
        pygame.draw.rect(self.screen, (50, 50, 50), (300, 250, 600, 200))
        txt = self.font.render("Confirm delete this mistake?", True, (255, 255, 255))
        self.screen.blit(txt, (350, 280))
        self.yes_btn = pygame.Rect(350, 350, 100, 50)
        self.no_btn = pygame.Rect(550, 350, 100, 50)
        pygame.draw.rect(self.screen, (50, 150, 50), self.yes_btn)
        pygame.draw.rect(self.screen, (150, 50, 50), self.no_btn)
        self.screen.blit(self.small_font.render("Yes", True, (255, 255, 255)), (self.yes_btn.x + 30, self.yes_btn.y + 10))
        self.screen.blit(self.small_font.render("No", True, (255, 255, 255)), (self.no_btn.x + 30, self.no_btn.y + 10))

    def handle_confirm_buttons(self, pos):
        if self.yes_btn.collidepoint(pos):
            del self.mistake_book[self.selected_chapter][self.selected_question]
            save_user(self.username, self.user_data)
            self.user_data = load_users().get(self.username, {})
            self.mistake_book = self.user_data.get("mistake_book", {})
            self.state = "question_list"
            self.selected_question = None
        elif self.no_btn.collidepoint(pos):
            self.state = "question_detail"
