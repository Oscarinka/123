import pygame
import random as rnd
import os

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Жесткая змейка')
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

block_size = 20
snake_speed = 7

font_style = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont(None, 40)

white = (255, 255, 255)
light_blue = (173, 216, 230)
black = (0, 0, 0)
orange = (255, 165, 0)
green = (0, 255, 0)
red = (255, 0, 0)

apple_icon = pygame.image.load("icon.png")
pygame.display.set_icon(apple_icon)

high_score_file = "high_score.txt"

def get_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read())
    return 0

def set_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

high_score = get_high_score()

def show_message(msg, color, y_displace=0, size=30):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(msg, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (display_width / 2, display_height / 2 + y_displace)
    display.blit(text_surface, text_rect)

def game_loop():
    global high_score

    def draw_snake(snake_body):
        for block in snake_body:
            pygame.draw.rect(display, green, [block[0], block[1], block_size, block_size])

    def draw_score(score):
        value = score_font.render("Очки: " + str(score), True, black)
        display.blit(value, [0, 0])

    def draw_high_score(high_score):
        value = score_font.render("Рекорд: " + str(high_score), True, black)
        display.blit(value, [0, 40])

    def spawn_food():
        food_x = rnd.randint(0, (display_width - block_size) // block_size) * block_size
        food_y = rnd.randint(0, (display_height - block_size) // block_size) * block_size
        return food_x, food_y

    game_over = False
    game_close = False

    snake_head_x = display_width / 2
    snake_head_y = display_height / 2

    snake_head_x_change = 0
    snake_head_y_change = 0

    snake_body = []
    length_of_snake = 1

    food_x1, food_y1 = spawn_food()
    food_x2, food_y2 = spawn_food()

    score = 0

    while not game_over:
        while game_close:
            display.fill(light_blue)
            show_message("Для перезапуска игры нажмите любую клавишу на клавиатуре", black, -50)
            draw_score(score)
            draw_high_score(high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if score > high_score:
                        high_score = score
                        set_high_score(high_score)
                    game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_head_x_change = -block_size
                    snake_head_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_head_x_change = block_size
                    snake_head_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_head_y_change = -block_size
                    snake_head_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_head_y_change = block_size
                    snake_head_x_change = 0

        if snake_head_x >= display_width or snake_head_x < 0 or snake_head_y >= display_height or snake_head_y < 0:
            game_close = True

        snake_head_x += snake_head_x_change
        snake_head_y += snake_head_y_change
        display.fill(light_blue)

        pygame.draw.rect(display, red, [food_x2, food_y2, block_size, block_size])

        snake_head = []
        snake_head.append(snake_head_x)
        snake_head.append(snake_head_y)
        snake_body.append(snake_head)
        if len(snake_body) > length_of_snake:
            del snake_body[0]

        for block in snake_body[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_body)
        draw_score(length_of_snake - 1)
        draw_high_score(high_score)

        pygame.display.update()

        if snake_head_x == food_x1 and snake_head_y == food_y1:
            food_x1, food_y1 = spawn_food()
            length_of_snake += 1
            score += 1
        elif snake_head_x == food_x2 and snake_head_y == food_y2:
            food_x2, food_y2 = spawn_food()
            length_of_snake += 1
            score += 1

        if score > high_score:
            high_score = score

        clock.tick(snake_speed)

def choose_difficulty():
    intro = True
    selected_difficulty = None

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill(light_blue)
        show_message("Выберите уровень сложности", black, -50)
        show_message("Нажмите 1 для легкого уровня", black, 50)
        show_message("Нажмите 2 для среднего уровня", black, 100)
        show_message("Нажмите 3 для сложного уровня", black, 150)
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            selected_difficulty = "easy"
            intro = False
        elif keys[pygame.K_2]:
            selected_difficulty = "medium"
            intro = False
        elif keys[pygame.K_3]:
            selected_difficulty = "hard"
            intro = False

    return selected_difficulty

def set_difficulty(difficulty):
    global snake_speed
    if difficulty == "easy":
        snake_speed = 7
    elif difficulty == "medium":
        snake_speed = 10
    elif difficulty == "hard":
        snake_speed = 15

def game_intro():
    pygame.display.set_caption('Жесткая змейка')
    pygame.display.set_icon(icon)

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        difficulty = choose_difficulty()
        set_difficulty(difficulty)

        display.fill(light_blue)
        show_message("Приветствую", black, -50)
        show_message("Для начала игры нажмите любую клавишу на клавиатуре", black, 50)
        show_message("Игру разработали Балыкин Александр и Давидчик Юрий", black, 285)
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            intro = False

game_intro()
game_loop()