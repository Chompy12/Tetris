import pygame
import random
from pieces import Piece
from spritesheet import SpriteSheet

def init_board():
    board = []
    for i in range(23):
        row = []
        for j in range(10):
            row.append(0)
        board.append(row)
    return board

def get_tile(tile_num:int):
    tiles = SpriteSheet('assets/Tiles.png')
    tile_num = tile_num%3 + 1
    width = 32
    height = 32
    x = (tile_num-1) * 32
    y = 0
    return tiles.get_image(x, y, width, height)

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
    frames_to_fall_table = [30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12,11,10,9,8,7,6,5,4,3,2,1,0]
    lines_to_next_level = 20
    changes_made = False
    fps = 60
    delay = 3
    score = 0
    font = pygame.font.SysFont(None, 36)

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
                    isValidRotation = pos[0] >= 0 and pos[0] < 10 and pos[1] >= 0 and pos[1] < len(board) and board[pos[1]][pos[0]] == 0 and isValidRotation
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
                    try:
                        frames_to_fall = frames_to_fall_table[level]
                    except IndexError:
                        frames_to_fall = 0
                else:
                    for offset in offsets:
                        pos = (anchor[0]+offset[0], anchor[1]+offset[1])
                        board[pos[1]][pos[0]] = active_piece.color
                    hasActivePiece = False
                    if anchor[1] > 20:
                        mode = "game over"
                        height = 20
                    else:
                        mode = "line clear"
            else:
                frames_to_fall -= 1

        elif mode == "line clear":
            fps = 10
            if changes_made:
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
                num_lines_cleared = 0
                for row_num in range(len(board)):
                    row = board[row_num]
                    row_is_full = True
                    for tile in row:
                        row_is_full = tile != 0 and row_is_full
                    if row_is_full:
                        for tilenum in range(len(row)):
                            board[row_num][tilenum] = 0
                        num_lines_cleared += 1
                if num_lines_cleared == 0:
                    mode = "game"
                else:
                    lines_to_next_level -= num_lines_cleared
                    if lines_to_next_level <= 0:
                        level+=1
                        lines_to_next_level = 20
                    score += ((num_lines_cleared-1)*200+100)*(level+1)
                    changes_made = True

        elif mode == "game over":
            if height >= 0:
                for tilenum in range(len(board[height])):
                    board[height][tilenum] = (height%3) + 1
            height -= 1
            if height < -10:
                for row_num in range(len(board)):
                    for col_num in range(len(board[row_num])):
                        board[row_num][col_num] = 0
                score = 0
                level = 0
                mode = "game"
        
        # draw to the screen
        for row_num in range(len(board)):
            for col_num in range(len(board[row_num])):
                if row_num > 20:
                    pygame.draw.rect(window, (128,128,128), (440+col_num*32, 738-row_num*32, 32, 32))
                elif board[row_num][col_num] != 0:
                    img = get_tile(board[row_num][col_num])
                    pos = (440+col_num*32, 738-row_num*32)
                    window.blit(img, pos)
                else:
                    pygame.draw.rect(window, (0, 0, 0), (440+col_num*32, 738-row_num*32, 32, 32))
        if mode == "game" and hasActivePiece:
            for offset in offsets:
                if anchor[1]+offset[1] <= 20:
                    img = get_tile(active_piece.color)
                    pos = (440+(anchor[0]+offset[0])*32, 738-(anchor[1]+offset[1])*32)
                    window.blit(img, pos)
        score_text = font.render(f"{score}", True, (255,255,255))
        window.blit(score_text, (10, 10))
        level_text = font.render(f"{level}", True, (255,255,255))
        window.blit(level_text, (10, 40))
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()