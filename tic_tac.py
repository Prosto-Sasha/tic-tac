import pygame, sys, random


def check_win(mas, sign):
    zeroes = 0
    for row in mas:
        zeroes += 1
        if row.count(sign) == 3:
            return sign
    for col in range(3):
        if mas[0][col] == sign and mas[1][col] == sign and mas[2][col] == sign:
            return sign
    if mas[0][0] == sign and mas[1][1] == sign and mas[2][2] == sign:
        return sign
    if mas[0][2] == sign and mas[1][1] == sign and mas[2][0] == sign:
        return sign
    if zeroes == 0:
        return 'Piece'
    return False


def intel(mas):
    for col in range(3):
        if (mas[1][col] == 'x' and mas[2][col] == 'x') or (mas[1][col] == 'o' and mas[2][col] == 'o'):
            if mas[0][col] == 0:
                return 0, col
        if (mas[0][col] == 'x' and mas[2][col] == 'x') or (mas[0][col] == 'o' and mas[2][col] == 'o'):
            if mas[1][col] == 0:
                return 1, col
        if (mas[0][col] == 'x' and mas[1][col] == 'x') or (mas[0][col] == 'o' and mas[1][col] == 'o'):
            if mas[2][col] == 0:
                return 2, col

    for row in range(3):
        if (mas[row][1] == 'x' and mas[row][2] == 'x') or (mas[row][1] == 'o' and mas[row][2] == 'o'):
            if mas[row][0] == 0:
                return row, 0
        if (mas[row][0] == 'x' and mas[row][2] == 'x') or (mas[row][0] == 'o' and mas[row][2] == 'o'):
            if mas[row][1] == 0:
                return row, 1
        if (mas[row][0] == 'x' and mas[row][1] == 'x') or (mas[row][0] == 'o' and mas[row][1] == 'o'):
            if mas[row][2] == 0:
                return row, 2

    if (mas[1][1] == 'x' and mas[2][2] == 'x') or (mas[1][1] == 'o' and mas[2][2] == 'o'):
        if mas[0][0] == 0:
            return 0, 0
    if (mas[0][0] == 'x' and mas[2][2] == 'x') or (mas[0][0] == 'o' and mas[2][2] == 'o'):
        if mas[1][1] == 0:
            return 1, 1
    if (mas[0][0] == 'x' and mas[1][1] == 'x') or (mas[0][0] == 'o' and mas[1][1] == 'o'):
        if mas[2][2] == 0:
            return 2, 2

    if (mas[2][0] == 'x' and mas[1][1] == 'x') or (mas[2][0] == 'o' and mas[1][1] == 'o'):
        if mas[0][2] == 0:
            return 0, 2
    if (mas[0][2] == 'x' and mas[2][0] == 'x') or (mas[0][2] == 'o' and mas[2][0] == 'o'):
        if mas[1][1] == 0:
            return 1, 1
    if (mas[0][2] == 'x' and mas[1][1] == 'x') or (mas[0][2] == 'o' and mas[1][1] == 'o'):
        if mas[2][0] == 0:
            return 2, 0

    x, y = random.randint(0, 2), random.randint(0, 2)
    while mas[x][y] != 0:
        x, y = random.randint(0, 2), random.randint(0, 2)
    return x, y


pygame.init()

size_block = 100
margin = 5
width = heigth = size_block * 3 + margin * 4

size_window = (width, heigth)
screen = pygame.display.set_mode(size_window)
pygame.display.set_caption("Крестики-нолики")

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
mas = [[0] * 3 for i in range(3)]
query = 0
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            flag = True
            while flag:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                col = x_mouse // (size_block + margin)
                row = y_mouse // (size_block + margin)
                if mas[row][col] == 0:
                    if query % 2 == 0:
                        mas[row][col] = 'o'
                        query += 2
                        flag = False
                x, y = intel(mas)
                mas[x][y] = 'x'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_over = False
            mas = [[0] * 3 for i in range(3)]
            query = random.randint(0, 1)
            screen.fill(black)
    if not game_over:
        for row in range(3):
            for col in range(3):
                if mas[row][col] == 'x':
                    color = red
                elif mas[row][col] == 'o':
                    color = green
                else:
                    color = white
                x = col * size_block + (col + 1) * margin
                y = row * size_block + (row + 1) * margin
                pygame.draw.rect(screen, color, (x, y, size_block, size_block))
                if color == red:
                    pygame.draw.line(screen, black, (x + 5, y + 5), (x + size_block - 5, y + size_block - 5), 3)
                    pygame.draw.line(screen, black, (x + size_block - 5, y + 5), (x + 5, y + size_block - 5), 3)
                elif color == green:
                    pygame.draw.circle(screen, white, (x + size_block // 2, y + size_block // 2),
                                       size_block // 2 - 3, 3)

    if (query - 1) % 2 == 0:
        game_over = check_win(mas, 'x')
    else:
        game_over = check_win(mas, 'o')

    if game_over:
        screen.fill(black)
        font = pygame.font.SysFont("Segoe Script", 80)
        text1 = font.render(game_over, True, white)
        text_rect = text1.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text1, [text_x, text_y])

    pygame.display.update()
