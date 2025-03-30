import tkinter as tk
import random
import tkinter.messagebox as msg

import pygame
import time

# 通用窗口居中函数
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

class VersionPage:
    def __init__(self, title):
        self.page = tk.Toplevel()
        self.page.title(title)
        center_window(self.page, 400, 400)

        tk.Label(self.page, text=f"Welcome to {title} Mode!", font=("Arial", 14)).pack(pady=20)
        tk.Label(self.page, text="If you are ready\nclick \"Begin\" to begin the competition!",
                 fg="blue", bg="lightyellow", font=("Arial", 14)).pack(pady=20)

        # 根据 title 选择不同的模式开始类
        def start_version():
            self.page.destroy()  # 先关闭当前窗口
            if title == "Easy":
                BeginEasy(title)
            elif title == "Medium":
                BeginMedium(title)
            elif title == "Hard":
                BeginHard(title)

        tk.Button(self.page, text="Begin", bg="green", command=start_version,
                  width=20, height=2).pack(pady=10)

        tk.Label(self.page, text="Otherwise, click \"Back\" to return to the front page",
                 fg="blue", bg="lightyellow", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.page, text="Back", bg="yellow", command=self.page.destroy,
                  width=20, height=2).pack(pady=10)


class BeginEasy:
    def __init__(self, title):
        self.page = tk.Toplevel()
        self.page.title(title)
        self.page.withdraw()  # 隐藏tk页面，直接进入pygame

        pygame.init()
        screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Easy Version")
        clock = pygame.time.Clock()

        font = pygame.font.SysFont(None, 36)
        running = True
        score = 0
        time_limit = 3600  # 秒
        start_time = time.time()
        input_text = ''
        expression = ''
        answer = 0

        # 生成随机表达式
        def generate_expression():
            operators = ['+', '-', '*', '/']

            def generate_simple_expr(range_val):
                num1 = random.randint(1, range_val)
                num2 = random.randint(1, range_val)
                operator = random.choice(operators)
                return f"{num1} {operator} {num2}"

            def generate_complex_expr(depth=1, range_val=10):
                if depth == 0:
                    return generate_simple_expr(range_val)
                operator = random.choice(operators)
                left = generate_complex_expr(depth - 1, range_val)
                right = generate_complex_expr(depth - 1, range_val)
                if operator in ['+', '-']:
                    return f"{left} {operator} {right}"
                else:
                    return f"({left} {operator} {right})"

            expr = generate_complex_expr(depth=1, range_val=10)
            return expr

        # 生成新题目
        def new_question():
            nonlocal expression, answer
            expression = generate_expression()
            try:
                answer = round(eval(expression), 2)
            except ZeroDivisionError:
                new_question()

        new_question()
        feedback = ''
        while running:
            screen.fill((255, 255, 255))
            elapsed_time = time.time() - start_time

            if elapsed_time >= time_limit:
                running = False
                continue

            # 显示题目
            question_text = font.render("Solve: " + expression+ "(Answer to 1 decimal place)", True, (0, 0, 0))
            screen.blit(question_text, (50, 100))

            input_surface = font.render("Your Answer: " + input_text, True, (0, 0, 255))
            screen.blit(input_surface, (50, 150))

            score_text = font.render(f"Score: {score}", True, (0, 128, 0))
            screen.blit(score_text, (50, 20))

            time_left = font.render(f"Time Left: {int(time_limit - elapsed_time)}s", True, (255, 0, 0))
            screen.blit(time_left, (400, 20))

            feedback_surface = font.render(feedback, True, (128, 0, 128))
            screen.blit(feedback_surface, (50, 200))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            user_answer = float(input_text)
                            if round(user_answer, 1) == answer:
                                score += 1.5
                                new_question()
                                feedback = "Correct!"
                            else:
                                feedback = "Wrong, try again!"
                        except ValueError:
                            feedback = "Invalid input!"
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            clock.tick(30)

        pygame.quit()

        msg.showinfo("Time's Up!", f"Your final score is: {score}")
        self.page.destroy()



class BeginMedium:
    def __init__(self, title):
        self.page = tk.Toplevel()
        self.page.title(title)
        self.page.withdraw()  # 隐藏tk页面，直接进入pygame

        pygame.init()
        screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("Medium Version")
        clock = pygame.time.Clock()

        font = pygame.font.SysFont(None, 36)
        running = True
        score = 0
        time_limit = 3600  # 秒
        start_time = time.time()
        input_text = ''
        expression = ''
        answer = rand = 0


        def generate_exponent():
            nonlocal expression, answer
            choice = random.choice([1, 2])
            base = random.randint(1, 10)
            exponent = random.randint(1, 2)

            if choice == 1:
                exponent = 1 / exponent

            answer = base ** exponent
            return f"{base} to the power of {exponent}"

        def generate_number():
            nonlocal answer
            number = random.randint(3, 200)
            i = 2
            answer = 1
            while i * i <= number:
                if number % i == 0:
                    answer = 2
                    break
                i=i+1
            return f"Is {number} a prime number?"

        def new_question():
            nonlocal rand, expression
            rand = random.randint(1, 2)
            if rand == 1:
                expression =  generate_exponent()+"( Answer to 1 decimal place)"
            else: expression =  generate_number() + "Only \"yes\" or \"no\" are accepted."

        new_question()
        feedback = ''

        while running:
            screen.fill((255, 255, 255))
            elapsed_time = time.time() - start_time

            if elapsed_time >= time_limit:
                running = False
                continue

            # 显示题目
            question_text = font.render("Solve: " + expression, True, (0, 0, 0))
            screen.blit(question_text, (50, 100))

            input_surface = font.render("Your Answer: " + input_text, True, (0, 0, 255))
            screen.blit(input_surface, (50, 150))

            score_text = font.render(f"Score: {score}", True, (0, 128, 0))
            screen.blit(score_text, (50, 20))

            time_left = font.render(f"Time Left: {int(time_limit - elapsed_time)}s", True, (255, 0, 0))
            screen.blit(time_left, (400, 20))

            feedback_surface = font.render(feedback, True, (128, 0, 128))
            screen.blit(feedback_surface, (50, 200))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if rand == 1:
                            try:
                                user_answer = float(input_text)
                                answer = round(answer, 1)
                                if  answer == user_answer:
                                    score += 1.5
                                    new_question()
                                    feedback = "Correct!"
                                else:
                                    feedback = "Wrong, try again!"
                            except ValueError:
                                feedback = "Invalid input!"
                        else:
                            lower_input = input_text.lower()
                            user_answer = -1
                            if "yes" == lower_input:
                                user_answer = 1
                            elif "no" == lower_input:
                                user_answer = 2
                            if user_answer == -1:
                                feedback = "Invalid input!"
                            elif user_answer == answer:
                                feedback = "Correct!"
                                score += 1.5
                                new_question()
                            else:
                                feedback = "Wrong, try again!"
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        clock.tick(30)

        pygame.quit()

        # 显示分数
        msg.showinfo("Time's Up!", f"Your final score is: {score}")
        self.page.destroy()


class BeginHard:
    def __init__(self, title):
        self.page = tk.Toplevel()
        self.page.title(title)
        self.page.withdraw()  # 隐藏tk页面，直接进入pygame

        screen_height = 800
        screen_width = 1300
        pygame.init()
        screen = pygame.display.set_mode((1300, 800))
        pygame.display.set_caption("Hard Version")
        clock = pygame.time.Clock()

        font = pygame.font.SysFont(None, 36)
        running = True
        score = 0
        time_limit = 100  # 秒
        start_time = time.time()
        input_text = ''
        expression = ''
        answer = 0
        question_type = 0  # 1=gcd/lcm, 2=grid path
        rows = cols = 0
        grid = None
        cell_size = 30
        max_cell_number = 20

        def get_gcd(num1, num2):
            return num1 if num2 == 0 else get_gcd(num2, num1 % num2)

        def get_lcm(num1, num2):
            return num1 * num2 // get_gcd(num1, num2)

        def generate_gcd_or_lcm():
            nonlocal answer
            rand = random.randint(1, 2)
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)

            if rand == 1:  # GCD
                gcd = get_gcd(num1, num2)
                if gcd <= 1:
                    return generate_gcd_or_lcm()
                else:
                    answer = gcd
                    return f"Find the Greatest Common Divisor of {num1} and {num2}"
            else:  # LCM
                lcm = get_lcm(num1, num2)
                answer = lcm
                return f"Find the Least Common Multiple of {num1} and {num2}"

        def bfs(grid):
            from collections import deque
            directions = [(0,1), (1,0), (-1,0), (0,-1)]
            visited = [[False]*cols for _ in range(rows)]
            queue = deque([(0, 0, 0)])  # row, col, steps
            visited[0][0] = True

            while queue:
                r, c, steps = queue.popleft()
                if r == rows - 1 and c == cols - 1:
                    return steps
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 1:
                        visited[nr][nc] = True
                        queue.append((nr, nc, steps + 1))
            return -1

        def drew_graph():
            # 清除屏幕
            screen.fill((255, 255, 255))

            # 计算网格宽度和高度
            grid_width = cols * cell_size
            grid_height = rows * cell_size

            # 计算偏移量（使网格居中）
            x_offset = (screen_width+400 - grid_width) // 2
            y_offset = (screen_height - grid_height) // 2


            # 绘制每个格子
            for row in range(rows):
                for col in range(cols):
                    # 每个格子的颜色
                    color = (255, 0, 0) if grid[row][col] == 0 else (0, 255, 0)
                    pygame.draw.rect(screen, color,
                                     pygame.Rect(col * cell_size + x_offset, row * cell_size + y_offset, cell_size,
                                                 cell_size))

            # 绘制网格的边框
            for row in range(rows + 1):
                pygame.draw.line(screen, (0, 0, 0), (x_offset, row * cell_size + y_offset),
                                 (x_offset + cols * cell_size, row * cell_size + y_offset))  # 动态调整宽度

            for col in range(cols + 1):
                pygame.draw.line(screen, (0, 0, 0), (col * cell_size + x_offset, y_offset),
                                 (col * cell_size + x_offset, y_offset + rows * cell_size))  # 动态调整高度

            grid_image = pygame.image.load("pictures/head_picture.png")
            #./pictures/head_picture.png
            grid_image = pygame.transform.scale(grid_image, (cell_size, cell_size))
            screen.blit(grid_image, (x_offset, y_offset))

            grid_image = pygame.image.load("pictures/watermelon.png")
            grid_image = pygame.transform.scale(grid_image, (cell_size, cell_size))
            screen.blit(grid_image, (x_offset+(cols-1)*cell_size, y_offset+(rows-1)*cell_size))


        def generate_graph():
            nonlocal answer, rows, cols, grid
            rows, cols = random.randint(5, max_cell_number), random.randint(5, max_cell_number)
            grid = [[random.choice([0, 1,1,1]) for _ in range(cols)] for _ in range(rows)]
            grid[0][0] = grid[rows - 1][cols - 1] = 1
            steps = bfs(grid)

            if steps == -1:
                return generate_graph()  # 递归生成新的图形直到找到有效路径
            else:
                answer = steps  # 更新答案
                drew_graph()  # 绘制新的图形
                return "Find the minimum steps for Ryan to get his watermelon"

        def new_question():
            nonlocal expression, question_type
            question_type = random.randint(1, 2)
            if question_type == 1:
                expression = generate_gcd_or_lcm()  # 假设这是生成GCD/LCM题目的函数
            else:
                expression = generate_graph()  # 生成网格问题

        # 主事件循环
        feedback = ''
        new_question()

        while running:
            screen.fill((255, 255, 255))  # 每一帧清空屏幕

            if question_type == 2:
                drew_graph()
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_limit:
                running = False
                continue

            question_text = font.render("Solve: " + expression, True, (0, 0, 0))
            screen.blit(question_text, (20, 80))

            input_surface = font.render("Your Answer: " + input_text, True, (0, 0, 255))
            screen.blit(input_surface, (20, 250))

            score_text = font.render(f"Score: {score}", True, (0, 128, 0))
            screen.blit(score_text, (20, 20))

            time_left = font.render(f"Time Left: {int(time_limit - elapsed_time)}s", True, (255, 0, 0))
            screen.blit(time_left, (1050, 20))

            feedback_surface = font.render(feedback, True, (128, 0, 128))
            screen.blit(feedback_surface, (20, 300))

            pygame.display.flip()  # 刷新屏幕

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            user_answer = int(input_text)
                            if user_answer == answer:
                                score += 2
                                feedback = "Correct!"
                                new_question()  # 更新问题
                            else:
                                feedback = "Wrong, try again!"
                        except ValueError:
                            feedback = "Invalid input!"
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            clock.tick(30)  # 控制帧率
        pygame.quit()
        msg.showinfo("Time's Up!", f"Your final score is: {score}")
        self.page.destroy()


class FrontPage:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Lynfield College IMO")
        center_window(self.window, 800, 500)

        # 欢迎语
        welcome_text = "Welcome to Lynfield College IMO!\n\nPlease select a difficulty level to continue."
        tk.Label(self.window, text=welcome_text, fg="blue", bg="lightyellow", font=("Arial", 16)).pack(pady=20)

        # 难度选择按钮
        tk.Button(self.window, text="EASY", bg="green", width=20, height=2, command=self.show_easy).pack(pady=15)
        tk.Button(self.window, text="MEDIUM", bg="yellow", width=20, height=2, command=self.show_medium).pack(pady=15)
        tk.Button(self.window, text="HARD", bg="red", width=20, height=2, command=self.show_hard).pack(pady=15)

        # 简介按钮
        tk.Label(self.window, text="Down below is how the problem might include", fg="black",
                 bg="lightgrey", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.window, text="Introduction", command=self.show_description).pack(pady=10)

        self.window.mainloop()

    def show_easy(self):
        VersionPage("Easy")

    def show_medium(self):
        VersionPage("Medium")

    def show_hard(self):
        VersionPage("Hard")

    def show_description(self):
        desc_win = tk.Toplevel()
        desc_win.title("Level Descriptions")
        center_window(desc_win, 450, 300)

        # 创建一个 Canvas 组件和 Scrollbar 组件
        canvas = tk.Canvas(desc_win)
        scrollbar = tk.Scrollbar(desc_win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # 创建一个 Frame 来放置描述文本
        description_frame = tk.Frame(canvas)

        # 添加描述文本到 Frame 中
        desc_text = (
                    "EASY:\n  Simple addition, subtraction,\n multiplication and division.\n\n"
                    "MEDIUM:\n  Simple exponents, simplifying expressions,\n solving equation and so on.\n\n"
                    "HARD:\n  Greatest Common Divisor, Least Common Multiple, \n  Graph Theory and so on."
                )

        label = tk.Label(description_frame, text=desc_text, justify="left", fg="black", bg="lightyellow",
                         font=("Arial", 12), padx=10, pady=10)
        label.pack(fill="both", expand=True)

        # 将 Frame 放置到 Canvas 中
        canvas.create_window((0, 0), window=description_frame, anchor="nw")

        # 配置滚动条
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # 更新 Canvas 滚动区域大小
        description_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        tk.Button(desc_win, text="Close", command=desc_win.destroy).pack(pady=10)


# 启动主页面
if __name__ == "__main__":
    FrontPage()
