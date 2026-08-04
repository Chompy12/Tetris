import pygame
import random
from pieces import Piece

def init_board():
    board = []
    for i in range(23):
        row = []
        for j in range(10):
            row.append(0)
        board.append(row)
    return board

def main():
    pygame.init()

    W = 1200
    H = 900
    window = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()

    board = init_board()

    base_piece_offs = [
        [(0,0),(1,0),(0,-1),(1,-1)],
        [(-1,0),(0,0),(0,-1),(1,-1)],
        [(0,0),(1,0),(-1,-1),(0,-1)],
        [(-1,0),(0,0),(1,0),(0,-1)],
        [(-1,0),(0,0),(1,0),(2,0)],
        [(-1,0),(0,0),(1,0),(-1,-1)],
        [(-1,0),(0,0),(1,0),(1,-1)]
    ]
    mode = "game"
    hasActivePiece = False
    level = 0
    frames_to_fall_table = [30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12]
    line_cleared = False
    changes_made = False
    fps = 60
    delay = 3

    running = True
    while running: # Main game loop
        window.fill((128,128,128))
        
        if mode == "game":
            fps = 30
            dir_to_move = (0,0)
            hasRotated = False
            if not hasActivePiece:
                anchor = (5, 21)
                offsets_idx = random.randint(0,6)
                active_piece = Piece(base_piece_offs[offsets_idx])
                frames_to_fall = frames_to_fall_table[level]
                hasActivePiece = True
            offsets = active_piece.offsets

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and not hasRotated:
                        active_piece.rotate_left()
                        hasRotated = True
                    elif event.key == pygame.K_e and not hasRotated:
                        active_piece.rotate_right()
                        hasRotated = True
                    elif (event.key == pygame.K_a or event.key == pygame.K_d) and not hasRotated:
                        delay = 0
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_a] and dir_to_move == (0,0) and not hasRotated: # Only move one direction or rotate one direction
                dir_to_move = (-1, 0)
            elif keys[pygame.K_d] and dir_to_move == (0,0) and not hasRotated:
                dir_to_move = (1, 0)
            elif keys[pygame.K_s]:
                frames_to_fall = 0 # Soft drop

            # Rotation
            if active_piece.offsets != offsets:
                isValidRotation = True
                for offset in active_piece.offsets:
                    pos = (anchor[0]+offset[0], anchor[1]+offset[1])
                    isValidRotation = pos[0] >= 0 and pos[0] < 10 and pos[1] >= 0 and board[pos[1]][pos[0]] == 0 and isValidRotation
                if not isValidRotation:
                    active_piece.set_offsets(offsets)

            # Horizantal movement
            if dir_to_move != (0, 0) and delay == 0:
                isValidMove = True
                for offset in offsets:
                    pos = (anchor[0]+offset[0]+dir_to_move[0], anchor[1]+offset[1])
                    isValidMove = pos[0] >= 0 and pos[0] < 10 and board[pos[1]][pos[0]] == 0 and isValidMove
                if isValidMove:
                    anchor = (anchor[0]+dir_to_move[0], anchor[1])
                delay = 3
            elif delay != 0:
                delay -= 1

            # Vertical movement
            if frames_to_fall == 0:
                isValidMove = True
                for offset in offsets:
                    pos = (anchor[0]+offset[0], anchor[1]+offset[1]-1)
                    isValidMove = pos[1] >= 0 and board[pos[1]][pos[0]] == 0 and isValidMove
                if isValidMove:
                    anchor = (anchor[0], anchor[1]-1)
                    frames_to_fall = frames_to_fall_table[level]
                else:
                    for offset in offsets:
                        pos = (anchor[0]+offset[0], anchor[1]+offset[1])
                        board[pos[1]][pos[0]] = 1
                    hasActivePiece = False
                    for row_num in range(len(board)):
                        row = board[row_num]
                        row_is_full = True
                        for tile in row:
                            row_is_full = tile != 0 and row_is_full
                        if row_is_full:
                            mode = "line clear"
                    if anchor[1] > 20:
                        mode = "game over"
                        height = 22
            else:
                frames_to_fall -= 1

        elif mode == "line clear":
            fps = 10
            if line_cleared or changes_made:
                changes_made = False
                for row_num in range(20):
                    row = board[row_num]
                    next_row = board[row_num+1]
                    for tile_num in range(len(row)):
                        if row[tile_num] == 0 and next_row[tile_num] != 0:
                            board[row_num][tile_num] = next_row[tile_num]
                            board[row_num+1][tile_num] = 0
                            changes_made = True

            if not changes_made:
                line_cleared = False
                for row_num in range(len(board)):
                    row = board[row_num]
                    row_is_full = True
                    for tile in row:
                        row_is_full = tile != 0 and row_is_full
                    if row_is_full:
                        for tilenum in range(len(row)):
                            board[row_num][tilenum] = 0
                        line_cleared = True
                if not line_cleared:
                    mode = "game"

        elif mode == "game over":
            if height >= 0:
                for tilenum in range(len(board[height])):
                    board[height][tilenum] = 1
            height -= 1
            if height < -10:
                mode = "line clear"
        
        # draw to the screen
        for row_num in range(len(board)):
            for col_num in range(len(board[row_num])):
                pygame.draw.rect(window, (0, 0, 255*board[row_num][col_num]), (440+col_num*32, 738-row_num*32, 32, 32))
        if mode == "game" and hasActivePiece:
            for offset in offsets:
                pos = (anchor[0]+offset[0], anchor[1]+offset[1])
                pygame.draw.rect(window, (0, 0, 255), (440+pos[0]*32, 738-pos[1]*32, 32, 32))
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()