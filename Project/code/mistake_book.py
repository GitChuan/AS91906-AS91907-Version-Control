import pygame
from info_manager import load_users, save_user


class MistakeBook:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        # Load the mistake data from database
        self.user_data = load_users().get(username, {})
        self.mistake_book = self.user_data.get("mistake_book", {})

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 24)

        # Four status
        # chapter_select / question_list / question_detail / confirm_delete
        # 0             /  1            /   2             /  3
        self.state = 0 # chapter_select
        self.selected_chapter = None  # Current chapter
        self.selected_question = None  # Used only in chapter5
        self.selected_question_key = None  # Used for others

        self.page = 0
        self.per_page = 15  # Maximum 15 mistakes in one page

        self.chapter_rects = {}

    def run(self):
        while True:
            self.screen.fill((30, 30, 40))  # Background color
            for evt in pygame.event.get():
                if evt.type == pygame.KEYDOWN:
                    # Base on Esc and current page
                    if evt.key == pygame.K_ESCAPE:
                        if self.state == 0: # chapter_select
                            return
                        elif self.state == 1: # question_list
                            self.state -= 1
                            self.selected_chapter = None
                            self.page = 0
                        elif self.state == 2: # question_detail
                            self.state -= 1
                        elif self.state == 3: # confirm_delete
                            self.state -= 1
                elif evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                    p = evt.pos
                    if self.state == 0: # chapter_select
                        for i in range(1, 6):
                            block = self.chapter_rects.get(f"chapter{i}")
                            if block and block.collidepoint(p):
                                self.selected_chapter = f"chapter{i}"
                                self.state = 1
                                self.selected_question = None
                                self.selected_question_key = None
                                self.page = 0
                                break
                    elif self.state == 1: # question_list
                        self.compute_question(p)
                        self.compute_page(p)
                    elif self.state == 2: # question_detail
                        if self.delete.collidepoint(p):
                            self.state = 3
                    elif self.state == 3: # confirm_delete
                        if self.yes.collidepoint(p):
                            if self.selected_chapter == "chapter5":
                                del self.mistake_book["chapter5"][self.selected_question]
                            else:
                                del self.mistake_book[self.selected_chapter][self.selected_question_key]

                            save_user(self.username, self.user_data)
                            self.user_data = load_users().get(self.username, {})  # Update interface
                            self.mistake_book = self.user_data.get("mistake_book", {})

                            self.state = 1
                            self.selected_question = None
                            self.selected_question_key = None

                        elif self.no.collidepoint(p):
                            self.state = 2
                elif evt.type == pygame.QUIT:
                    pygame.quit()
                    return

            if self.state == 0: # chapter_select
                # Make each chapter's button be in the center
                total_height = 5 * 60 + 4 * 20
                start_y = (self.screen.get_height() - total_height) >> 1

                # Draw each chapter
                for i in range(1, 6):
                    x = (self.screen.get_width() - 300) >> 1
                    y = start_y + (i - 1) * 80
                    block = pygame.Rect(x, y, 300, 60)
                    pygame.draw.rect(self.screen, (70, 70, 120), block)  # Background
                    pygame.draw.rect(self.screen, (255, 255, 255), block, 2)  # Boarder
                    self.screen.blit(self.font.render(f"Chapter {i}", True, (255, 255, 255)),
                                     (block.x + 20, block.y + 15))  # Font
                    self.chapter_rects[f"chapter{i}"] = block
            elif self.state == 1: # question_list
                self.draw_question_list()
            elif self.state == 2: # question_detail
                self.draw_question_detail()
            elif self.state == 3:  # confirm_delete
                self.draw_confirm_delete()

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

    # Draw the mistakes from a chapter
    def draw_question_list(self):
        if self.selected_chapter == "chapter5":
            questions = self.mistake_book.get(self.selected_chapter, [])
        else:
            questions = list(self.mistake_book.get(self.selected_chapter, {}).keys())
        total = len(questions)

        # Current page starting index
        start = self.page * self.per_page
        # Current page ending index
        end = start + self.per_page

        if not questions:
            text = self.font.render("No mistakes in this chapter.", True, (200, 200, 200))
            self.screen.blit(text, (50, 50))
            return

        # Draw current page
        for i, q in enumerate(questions[start:end]):
            if self.selected_chapter == "chapter5":
                text = f"Mistake #{start + i + 1}"
            else:
                text = q
            block = pygame.Rect(50, 50 + i * 50, self.screen.get_width() - 100, 40)
            pygame.draw.rect(self.screen, (50, 50, 80), block)
            pygame.draw.rect(self.screen, (100, 100, 100), block, 1)
            self.screen.blit(self.small_font.render(text, True, (180, 180, 180)), block.topleft)
            setattr(self, f"question_{i}_rect", block)  # Store the mistake area

        # Draw page information
        page_info = self.small_font.render(f"Total: {total} | Page: {self.page + 1}/{max(0, (total - 1) // self.per_page) + 1}", True, (200, 200, 200))
        self.screen.blit(page_info, (50, self.screen.get_height() - 80))

        # If more than one page, draw the switch page buttons
        if total > self.per_page:
            y = self.screen.get_height() - 70
            w, h = 60, 40
            self.prev = pygame.Rect((self.screen.get_width() >> 1) - 100, y, w, h)
            self.next = pygame.Rect((self.screen.get_width() >> 1) + 40, y, w, h)
            pygame.draw.rect(self.screen, (70, 70, 120), self.prev)
            pygame.draw.rect(self.screen, (70, 70, 120), self.next)
            self.screen.blit(self.small_font.render("<", True, (255, 255, 255)),
                             (self.prev.x + 20, self.prev.y + 5))
            self.screen.blit(self.small_font.render(">", True, (255, 255, 255)),
                             (self.next.x + 20, self.next.y + 5))

    # Switch page
    def compute_page(self, pos):
        if self.selected_chapter == "chapter5":  # If is chapter 5, then question is a list
            questions = self.mistake_book.get(self.selected_chapter, [])
        else:  # Otherwise, convert keys in dict into list
            questions = list(self.mistake_book.get(self.selected_chapter, {}).keys())
        if hasattr(self, "prev") and self.prev.collidepoint(pos) and self.page > 0:
            self.page -= 1
        if hasattr(self, "next") and self.next.collidepoint(pos) and self.page < max(0, (len(questions) - 1) // self.per_page):
            self.page += 1

    def compute_question(self, pos):
        if self.selected_chapter == "chapter5":
            questions = self.mistake_book.get(self.selected_chapter, [])
        else:
            questions = list(self.mistake_book.get(self.selected_chapter, {}).keys())
        i = self.page * self.per_page
        j = (self.page + 1) * self.per_page
        visible = questions[i:j]
        for i, q in enumerate(visible):
            if getattr(self, f"question_{i}_rect").collidepoint(pos):
                if self.selected_chapter == "chapter5":
                    self.selected_question = self.page * self.per_page + i
                    self.selected_question_key = None
                else:
                    self.selected_question_key = q
                    self.selected_question = None
                self.state = 2
                break

    def get_grid(self, grid, top_left_x, top_left_y, cell_size,
                  optimal_path=None, user_path=None):
        n = len(grid)
        m = len(grid[0])

        # Convert string into grid path
        def compute(string):
            graph = [(0, 0)]
            x, y = 0, 0
            for ch in string:
                if ch == 'R':
                    y += 1
                elif ch == 'D':
                    x += 1
                graph.append((x, y))
            return set(graph)

        for i in range(n):
            for j in range(m):
                block = pygame.Rect(top_left_x + j * cell_size, top_left_y + i * cell_size, cell_size, cell_size)
                val = grid[i][j]

                # Set color
                if val == 0:
                    base_color = (200, 200, 200)
                elif val > 0:
                    base_color = (100, 255, 100)
                else:
                    base_color = (255, 100, 100)

                pygame.draw.rect(self.screen, base_color, block)
                pygame.draw.rect(self.screen, (0, 0, 0), block, 2)  # Black Boarder

                text = self.small_font.render(f"+{val}" if val > 0 else str(val), True, (0, 0, 0))
                self.screen.blit(text, text.get_rect(center=block.center))

                # Draw optimal path
                if optimal_path is not None:
                    if (i, j) in compute(optimal_path):
                        s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                        s.fill((180, 100, 255, 120))
                        self.screen.blit(s, block.topleft)

                # Draw user's path
                if user_path is not None:
                    if (i, j) in compute(user_path):
                        s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                        s.fill((255, 255, 0, 120))
                        self.screen.blit(s, block.topleft)

    def draw_question_detail(self):
        x = 50
        y = 100

        if self.selected_chapter == "chapter5":
            mistake = self.mistake_book[self.selected_chapter][self.selected_question]
            question_grid = mistake.get("question", [])
            user_path = mistake.get("user_path", "")
            user_hp = mistake.get("user_hp", "")
            optimal_path = mistake.get("optimal_path", "")
            optimal_hp = mistake.get("optimal_hp", "")

            self.screen.blit(self.font.render(f"Question Grid (Chapter 5)", True, (255, 255, 255)), (x, y))
            self.screen.blit(self.font.render(f"Your path: {user_path}", True, (255, 100, 100)), (x, y + 40))
            self.screen.blit(self.font.render(f"Your HP: {user_hp}", True, (255, 180, 100)), (x, y + 80))
            self.screen.blit(self.font.render(f"Optimal path: {optimal_path}", True, (180, 100, 255)), (x, y + 120))
            self.screen.blit(self.font.render(f"Optimal HP: {optimal_hp}", True, (100, 255, 255)), (x, y + 160))

            y += 230
            gap = x
            width = 42 * len(question_grid[0]) if question_grid else 0

            self.screen.blit(self.font.render("Initial Grid", True, (255, 255, 255)), (x, y - 30))
            self.screen.blit(self.font.render("Optimal Path", True, (180, 100, 255)), (x + width + gap, y - 30))
            self.screen.blit(self.font.render("Your Path", True, (255, 180, 100)), (x + 2 * (width + gap), y - 30))

            # Initial, optimal, user's
            self.get_grid(question_grid, x, y, 42)
            self.get_grid(question_grid, x + width + gap, y, 42, optimal_path=optimal_path)
            self.get_grid(question_grid, x + 2 * (width + gap), y, 42, user_path=user_path)
        else:
            mistake = self.mistake_book[self.selected_chapter][self.selected_question_key]
            user_ans = mistake.get("user_answer", "")
            optimal_ans = mistake.get("correct_answer", "")

            question = self.font.render(f"Question: {self.selected_question_key}", True, (255, 255, 255))
            user_answer = self.font.render(f"Your answer: {user_ans}", True, (255, 100, 100))
            optimal_answer = self.font.render(f"Correct answer: {optimal_ans}", True, (100, 255, 100))

            self.screen.blit(question, (50, y))
            self.screen.blit(user_answer, (50, y + 80))
            self.screen.blit(optimal_answer, (50, y + 160))

        # Draw delete button
        self.delete = pygame.Rect(self.screen.get_width() - 200, self.screen.get_height() - 100, 150, 50)
        pygame.draw.rect(self.screen, (180, 50, 50), self.delete)
        pygame.draw.rect(self.screen, (255, 255, 255), self.delete, 2)
        text = self.small_font.render("Delete", True, (255, 255, 255))
        self.screen.blit(text, (self.delete.x + ((150 - text.get_width()) >> 1),
                                self.delete.y + ((50 - text.get_height()) >> 1)))

    # Draw deleting button
    def draw_confirm_delete(self):
        w, h = 600, 200
        popup_x = (self.screen.get_width() - w) >> 1
        popup_y = (self.screen.get_height() - h) >> 1

        pygame.draw.rect(self.screen, (50, 50, 50), (popup_x, popup_y, w, h))
        self.screen.blit(self.font.render("Confirm delete this mistake?", True, (255, 255, 255)), (popup_x + 50, popup_y + 30))

        self.yes = pygame.Rect(popup_x + 50, popup_y + 100, 100, 50)
        pygame.draw.rect(self.screen, (50, 150, 50), self.yes)
        self.no = pygame.Rect(popup_x + w - 150, popup_y + 100, 100, 50)

        pygame.draw.rect(self.screen, (150, 50, 50), self.no)

        self.screen.blit(self.small_font.render("Yes", True, (255, 255, 255)), (self.yes.x + 30, self.yes.y + 10))
        self.screen.blit(self.small_font.render("No", True, (255, 255, 255)), (self.no.x + 30, self.no.y + 10))