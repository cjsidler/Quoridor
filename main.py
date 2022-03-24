import pygame
from pygame import gfxdraw
from Quoridor import *

pygame.font.init()

FPS = 60

WIDTH, HEIGHT = 603, 650
ROWS, COLS = 9, 9
SQUARE_SIZE = WIDTH // COLS
FENCE_LENGTH = SQUARE_SIZE * 2
FENCE_WIDTH = SQUARE_SIZE // 7
FONT_WIN = pygame.font.SysFont('arialroundedbold', 70)
FONT_PLAYER = pygame.font.SysFont('arialroundedbold', 14)
FONT_TURN = pygame.font.SysFont('arialroundedbold', 20)
PAWN_SIZE = int(SQUARE_SIZE // 3.75)


# rgb
TILE_COLOR = (247, 228, 183)
BASE_COLOR = (222, 202, 162)
FENCE_COLOR = (94, 62, 45)
P1_COLOR = (199, 90, 36)
P2_COLOR = (121, 181, 153)
DIVIDER_COLOR = (148, 126, 115)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DEST_CIRCLE = (150, 150, 150)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Quoridor')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def draw_board():
    # background color
    WIN.fill(TILE_COLOR)

    # baseline tiles
    for i in range(9):
        pygame.draw.rect(WIN, BASE_COLOR, (0 + (SQUARE_SIZE * i), 0, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(WIN, BASE_COLOR, (0 + (SQUARE_SIZE * i), (SQUARE_SIZE * 8), SQUARE_SIZE, SQUARE_SIZE))

    # divider lines
    for i in range(1, 10):
        gfxdraw.hline(WIN, 0, SQUARE_SIZE * 9, i * SQUARE_SIZE, DIVIDER_COLOR)
        gfxdraw.vline(WIN, i * SQUARE_SIZE, 0, SQUARE_SIZE * 9, DIVIDER_COLOR)


def draw_fences(game):
    for row in game.get_fences():
        for vertex in row:
            if vertex.get_h_fence_start() or vertex.get_v_fence_start():
                y, x = vertex.get_coords()

                x *= SQUARE_SIZE
                y *= SQUARE_SIZE

                if vertex.get_h_fence_start():
                    pygame.draw.rect(WIN, FENCE_COLOR, (x, y - (FENCE_WIDTH // 2), FENCE_LENGTH, FENCE_WIDTH))

                if vertex.get_v_fence_start():
                    pygame.draw.rect(WIN, FENCE_COLOR, (x - (FENCE_WIDTH // 2), y, FENCE_WIDTH, FENCE_LENGTH))


def draw_players(game):
    for i in [1, 2]:
        y, x = game.get_player_loc(i)
    
        piece_x = x * SQUARE_SIZE + (SQUARE_SIZE // 2)
        piece_y = y * SQUARE_SIZE + (SQUARE_SIZE // 2)

        if i == 1:
            color = P1_COLOR
            player = 'P1'
        else:
            color = P2_COLOR
            player = 'P2'

        gfxdraw.aacircle(WIN, piece_x, piece_y, PAWN_SIZE, color)
        gfxdraw.filled_circle(WIN, piece_x, piece_y, PAWN_SIZE, color)

        text = FONT_PLAYER.render(player, True, WHITE)
        text_rect = text.get_rect(center=(piece_x, piece_y))
        WIN.blit(text, text_rect)


def calc_fence_click_locations():
    """
    Populates a list of valid fence click locations.
    """
    fence_click_locs = []

    # for vertical fence locations:
    # make a tuple for (top, right, bot, left, orientation?)
    for x in range(1, 9):
        for y in range(0, 9):
            top = y * SQUARE_SIZE + (SQUARE_SIZE // 4)
            bot = y * SQUARE_SIZE + 3 * (SQUARE_SIZE // 4)

            left = x * SQUARE_SIZE - (FENCE_WIDTH // 2)
            right = x * SQUARE_SIZE + (FENCE_WIDTH // 2)

            orientation = 'v'

            fence_click_locs.append((top, right, bot, left, orientation))

    # for horizontal fence locations:
    for x in range(0, 9):
        for y in range(1, 9):
            top = y * SQUARE_SIZE - (FENCE_WIDTH // 2)
            bot = y * SQUARE_SIZE + (FENCE_WIDTH // 2)

            left = x * SQUARE_SIZE + (SQUARE_SIZE // 4)
            right = x * SQUARE_SIZE + 3 * (SQUARE_SIZE // 4)

            orientation = 'h'

            fence_click_locs.append((top, right, bot, left, orientation))

    return fence_click_locs


def get_fence_loc(bounds):
    """
    Takes a tuple with the bounds an orientation of a fence click location and
    returns the coordinates of the tile the player wants to place a fence.
    Bounds will be (top, right, bot, left, orientation) where top, right, bot,
    and left are integers representing a pixel location and orientation is
    'h' or 'v' (the type of fence the player wants to place).
    """


    pass


def check_center_tile_clicked(pos, dest):
    """
    Takes a mouse click position and dest Tile coords (row, col)
    and returns True if center area of dest tile was clicked.
    """
    dest_y, dest_x = dest
    x, y = pos

    left = dest_x * SQUARE_SIZE + (SQUARE_SIZE // 2) - PAWN_SIZE
    right = dest_x * SQUARE_SIZE + (SQUARE_SIZE // 2) + PAWN_SIZE
    top = dest_y * SQUARE_SIZE + (SQUARE_SIZE // 2) - PAWN_SIZE
    bottom = dest_y * SQUARE_SIZE + (SQUARE_SIZE // 2) + PAWN_SIZE

    if left <= x <= right and top <= y <= bottom:
        return True
    return False


def check_valid_dest_clicked(game, pos):
    """
    Takes the mouse position for a click and returns True if a valid destination Tile has been clicked.
    """
    dests = game.get_valid_destinations()

    for dest in dests:
        if check_center_tile_clicked(pos, dest):
            return True
    return False


def draw_valid_dest_circles(game):
    """
    Draws little gray circles on each valid destination tile.
    """
    for dest in game.get_valid_destinations():
        y, x = dest

        dest_x = x * SQUARE_SIZE + (SQUARE_SIZE // 2)
        dest_y = y * SQUARE_SIZE + (SQUARE_SIZE // 2)

        gfxdraw.aacircle(WIN, dest_x, dest_y, 8, DEST_CIRCLE)
        gfxdraw.filled_circle(WIN, dest_x, dest_y, 8, DEST_CIRCLE)


def draw_winner(player):
    """
    Draws a winner message in the center of the screen.
    """
    if player == 1:
        msg = "Player 1 Wins!"
        player_color = P1_COLOR
    else:
        msg = "Player 2 Wins!"
        player_color = P2_COLOR

    text = FONT_WIN.render(msg, True, player_color)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    WIN.blit(text, text_rect)


def draw_post_msg():
    """
    Draws a message at the bottom when game is over.
    """
    vert_placement = (HEIGHT - WIDTH) / 2 + WIDTH

    text = FONT_TURN.render("Thanks for playing!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, vert_placement))
    WIN.blit(text, text_rect)


def draw_turn(player):
    """
    Draws a message at the bottom when game is over.
    """
    vert_placement = (HEIGHT - WIDTH) / 2 + WIDTH

    if player == 1:
        msg = "Player 1's Turn"
        font_color = P1_COLOR
    else:
        msg = "Player 2's Turn"
        font_color = P2_COLOR

    text = FONT_TURN.render(msg, True, font_color)
    text_rect = text.get_rect(center=(WIDTH / 2, vert_placement))
    WIN.blit(text, text_rect)


def main():
    run = True
    clock = pygame.time.Clock()

    q_game = QuoridorGame()
    draw_board()
    valid_fence_click_locs = calc_fence_click_locations()

    while run:
        clock.tick(FPS)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                row, col = get_row_col_from_mouse(pos)
                print('row: ', row, 'col: ', col, 'pos: ', pos)

                player_loc = q_game.get_player_loc(q_game.get_turn())

                # if the game isn't over, show whose turn it is and allow move to be made
                if not (q_game.is_winner(1) or q_game.is_winner(2)):
                    player = q_game.get_turn()

                    # toggle selected status when turn player's pawn clicked
                    if check_center_tile_clicked(pos, player_loc):
                        q_game.toggle_selected()
                    # if selected is already true and valid destination clicked, move pawn to destination
                    elif q_game.get_selected() and check_valid_dest_clicked(q_game, pos):
                        q_game.move_pawn(player, (row, col))
                        q_game.toggle_selected()
                    # if selected is false and valid fence placement clicked, place fence
                    elif not q_game.get_selected():
                        for loc in valid_fence_click_locs:
                            top, right, bot, left, orientation = loc

                            if left <= x <= right and top <= y <= bot:
                                if orientation == 'v':
                                    row = y // SQUARE_SIZE
                                    col = round(x / SQUARE_SIZE)
                                else:
                                    row = round(y / SQUARE_SIZE)
                                    col = x // SQUARE_SIZE
                                print(player, orientation, (row, col), (x, y))
                                q_game.place_fence(player, orientation, (row, col))

        draw_board()
        draw_fences(q_game)
        draw_players(q_game)
        if q_game.get_selected():
            draw_valid_dest_circles(q_game)

        # draw whose turn it is or a message for the winner if game is over
        if q_game.is_winner(1):
            draw_winner(1)
            draw_post_msg()
        elif q_game.is_winner(2):
            draw_winner(2)
            draw_post_msg()
        else:
            draw_turn(q_game.get_turn())

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
