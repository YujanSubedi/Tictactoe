import ctypes
import random
import time
import pygame
from sys import exit

# Game Board and bot form ctype sorce file
cpp_game_lib = ctypes.CDLL('./bot.so')

# initilize pygame and get clock for framerate control
pygame.init()
clock = pygame.time.Clock()

# screen size, title, surface
screen = pygame.display.set_mode((1000, 780))
pygame.display.set_caption("connect 3")
bg_surface = pygame.Surface((1000, 780))
bg_surface.fill('white')

# board texture
board_surface = pygame.image.load(
    'pics/board.png').convert_alpha()
# circle tixture
alu_surface = pygame.transform.smoothscale(
    pygame.image.load('pics/alu.png').convert_alpha(), (193, 193))
# cross tixture
cross_surface = pygame.transform.smoothscale(
    pygame.image.load('pics/cross.png').convert_alpha(), (193, 193))

# fonts
text_font1 = pygame.font.Font('./font/Jetbrainsmono.ttf', 23)
text_font2 = pygame.font.Font('./font/Jetbrainsmono.ttf', 25)

# texture for new game state
new_game_surface = text_font1.render('New Game', False, (64, 64, 64))
new_game_rect = new_game_surface.get_rect(center=(850, 100))


# diplay board
def show_the_board(board, player):
    screen.blit(bg_surface, (0, 0))
    screen.blit(board_surface, (50, 50))
    screen.blit(text_font2.render('You are '+('0' if player == 1 else 'X'),
                                  False, (64, 64, 64)), (50, 10))
    for i in range(3):
        for j in range(3):
            if board[3*i+j]:
                screen.blit(alu_surface if board[3*i+j] > 0 else cross_surface,
                            (56+197*j, 56+197*i))


# find state of game
def check_game_state(board):
    winner = cpp_game_lib.get_state()
    if winner == 1 or winner == -1:
        return winner
    if winner == 2:
        return "Tie"
    return 0


# interrut the click on the board
def get_move_by_player(board, mouse_pressed):
    for i in range(3):
        for j in range(3):
            if not board[3*i+j]:
                if pygame.Rect(56+197*j, 56+197*i, 193, 193).collidepoint(
                    pygame.mouse.get_pos()):

                    pygame.draw.rect(screen, 'lightgreen',
                                     (56+197*j, 56+197*i, 193, 193))

                    if mouse_pressed:
                        return i*3+j


play_phase = False
game_over = False
new_game = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    mouse_pressed = pygame.mouse.get_pressed()[0]

    if new_game:
        players = [-1, 1]
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        cpp_game_lib.reset_board()
        cpp_board = (ctypes.c_int * 9)(*board)
        player = random.choice(players)
        current_player = 1
        new_game = False
        play_phase = True
        move = None

    if play_phase or game_over:
        show_the_board(board, player)

        if game_over:
            if game_over == 'Tie':
                screen.blit(text_font2.render(
                    game_over, False, 'black'), (200, 720))
            else:
                screen.blit(text_font2.render(
                    'Winner is ' + ('0' if game_over == 1 else 'X'),
                    False, 'black'), (70, 720))
            check_game_state(board)
            play_phase = False
            game_over = False

    if not new_game:
        if new_game_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.ellipse(screen, 'skyblue', (
                new_game_rect.left-10, new_game_rect.top-10,
                new_game_rect.width+20, new_game_rect.height+20))

            if mouse_pressed:
                time.sleep(0.2)
                new_game = True
        else:
            pygame.draw.ellipse(screen, '#f6975e', (
                new_game_rect.left-10, new_game_rect.top-10,
                new_game_rect.width+20, new_game_rect.height+20))

        screen.blit(new_game_surface, new_game_rect)

    if play_phase:
        if current_player == player:
            move = get_move_by_player(board, mouse_pressed)
        else:
            screen.blit(text_font2.render('Waiting for a move',
                                          False, (64, 64, 64)), (400, 10))
            pygame.display.update()
            move = cpp_game_lib.get_move_by_bot()
        if move is not None:
            cpp_game_lib.play_move(move)
            current_player = cpp_game_lib.get_turn_and_board(cpp_board)
            board = list(cpp_board)
            move = None
        game_over = check_game_state(board)

    pygame.display.update()
    clock.tick(60)
