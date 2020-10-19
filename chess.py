import pygame as pg
import os
from copy import deepcopy

# All icons made by Freepik from www.flaticon.com

# To do: fix bug where pawns jump pieces at origin
# To do: restrict movement into check.

class Graphics:
    HEIGHT = 800
    WIDTH = 800
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    BROWN = (165, 42, 42)
    BLUE = (0,  0,  255)
    WHITE = (255,255,255)
    BLACK = (0,   0,   0)
    GREEN = (0,255,0)
    DARK_GREEN = (0,100,0)
    TAN = (210,180,140)
    YELLOW = (255,255,0)
    RED = (255,0,0)
    def __init__(self):
        self.init = pg.init()
        self.set_caption = pg.display.set_caption("Chess")
    def update(self):
        pg.display.update()
    @staticmethod
    def pixelate(tuple):
        x, y = tuple
        return (Board.SQUARE_SIZE * x, Board.SQUARE_SIZE * y)
    def draw(self):
        self.draw_board()
        self.draw_pieces()
        self.draw_check()
        if Game.is_piece_selected():
            self.draw_possible_moves()
            self.draw_selection()
            
        self.update()
    def draw_pieces(self):
        for square in game.squares:
            if square.piece:
                self.screen.blit(square.piece.image, self.pixelate(square.coords))
    def draw_board(self):
        self.screen.fill(Board.SQUARE_COLOR_2)
        for y_coord in range(0,Board.HEIGHT,2):
            for x_coord in range(0, Board.WIDTH, 2):
                x_pixel, y_pixel = self.pixelate((x_coord, y_coord))
                pg.draw.rect(self.screen,Board.SQUARE_COLOR_1,(x_pixel, y_pixel, Board.SQUARE_SIZE,Board.SQUARE_SIZE))
        for y_coord in range(1,Board.HEIGHT,2):
            for x_coord in range(1, Board.WIDTH, 2):
                x_pixel, y_pixel = self.pixelate((x_coord, y_coord))
                pg.draw.rect(self.screen,Board.SQUARE_COLOR_1,(x_pixel, y_pixel, Board.SQUARE_SIZE,Board.SQUARE_SIZE))
    def draw_selection(self):
        for square in game.squares:
            if square.piece and square.piece.selected:
                x_pixel, y_pixel = self.pixelate(square.coords)
                # pg.draw.rect(self.screen,self.GREEN,(x_pixel + 5, y_pixel + 5, Board.SQUARE_SIZE - 10,Board.SQUARE_SIZE - 10),5)
                pg.draw.circle(self.screen,self.GREEN, (x_pixel + int(Board.SQUARE_SIZE / 2), y_pixel + int(Board.SQUARE_SIZE / 2)), 5)
    def draw_possible_moves(self):
        for square in game.squares:
            if square.piece and square.piece.selected:
                for coords in square.piece.possible_moves:
                    x_pixel, y_pixel = self.pixelate(coords)
                    pg.draw.rect(self.screen,self.YELLOW,(x_pixel + 1, y_pixel + 1, Board.SQUARE_SIZE - 2,Board.SQUARE_SIZE - 2),5)
                    # pg.draw.rect(self.screen,self.YELLOW,(x_pixel, y_pixel, Board.SQUARE_SIZE,Board.SQUARE_SIZE),5)
    def draw_check(self):
        for square in game.squares:
            if square.piece:
                if square.piece.name == 'king':
                    if square.piece.checked:
                        x_pixel, y_pixel = self.pixelate(square.coords)
                        pg.draw.circle(self.screen,self.RED, (x_pixel + int(Board.SQUARE_SIZE / 2), y_pixel + int(Board.SQUARE_SIZE / 2)), 5)

class Game:
    def __init__(self):
        self.squares = set()
        self.all_friendly_possible_moves = set()
        self.all_enemy_possible_moves = set()
        self.safe_moves = set()
        self.turn = 'black'
        self.running = True
    def run(self):
        graphics = Graphics()
        board = Board()
        self.set_squares()
        self.set_pieces()
        while self.running:
            graphics.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:                       
                        self.select_piece()
                        moved = self.move_piece()
                        self.check_king()
                        if moved:
                            self.change_turns()
                        
    def set_squares(self):
        for y_coord in range(Board.HEIGHT):
            for x_coord in range(Board.WIDTH):
                self.squares.add(Square((x_coord, y_coord)))     
    def set_pawns(self):
        # y_coord = Board.HEIGHT - 2
        # for x_coord in range(Board.WIDTH):
        #     for square in self.squares:
        #         if square.coords == (x_coord, y_coord):
        #             square.piece = Pawn('pawn', 'white', square.coords)
        # y_coord = 1
        # for x_coord in range(Board.WIDTH):
        #     for square in self.squares:
        #         if square.coords == (x_coord, y_coord):
        #             square.piece = Pawn('pawn', 'black', square.coords)
        for square in self.squares:
            if square.coords == (3,5):
                square.piece = Pawn('pawn', 'black', square.coords)
    def set_rooks(self):
        for square in self.squares:
            if square.coords == (1,0):
                square.piece = Rook('rook', 'black', square.coords)
            if square.coords == (7,0):
                square.piece = Rook('rook', 'black', square.coords)
            if square.coords == (7,7):
                square.piece = Rook('rook', 'white', square.coords)
            if square.coords == (0,7):
                square.piece = Rook('rook', 'white', square.coords)                 
    def set_knights(self):
        for square in self.squares:
            if square.coords == (1,7):
                square.piece = Knight('knight', 'white', square.coords)
            if square.coords == (6,7):
                square.piece = Knight('knight', 'white', square.coords)
            if square.coords == (1,0):
                square.piece = Knight('knight', 'black', square.coords)
            if square.coords == (6,0):
                square.piece = Knight('knight', 'black', square.coords)
    def set_bishops(self):
        for square in self.squares:
            # if square.coords == (2, 7):
            #     square.piece = Bishop('bishop', 'white', square.coords)
            if square.coords == (5, 7):
                square.piece = Bishop('bishop', 'white', square.coords)
            # if square.coords == (5, 0):
            #     square.piece = Bishop('bishop', 'black', square.coords)
            # if square.coords == (2, 0):
            #     square.piece = Bishop('bishop', 'black', square.coords)
    def set_queens(self):
        for square in self.squares:
            if square.coords == (3, 7):
                square.piece = Queen('queen', 'white', square.coords)
            if square.coords == (3, 0):
                square.piece = Queen('queen', 'black', square.coords)
    def set_kings(self):
        for square in self.squares:
            if square.coords == (4, 7):
                square.piece = King('king', 'white', square.coords)
            # if square.coords == (4, 0):
            #     square.piece = King('king', 'black', square.coords)
            if square.coords == (2, 4):
                square.piece = King('king', 'black', square.coords)
    ### Set Pieces ###
    def set_pieces(self):
        self.set_pawns()
        # self.set_rooks()
        # self.set_knights()
        self.set_bishops()
        # self.set_queens()
        self.set_kings()
    def select_piece(self):
        for square in self.squares:
            if square.piece and self.turn == square.piece.color and square.is_clicked():
                selected_before_reset = square.piece.selected
                self.unselect_pieces()
                square.piece.selected = not selected_before_reset
                square.piece.update_possible_moves()
                square.piece.update_possible_moves_considering_safe()
                return True
    def unselect_pieces(self):
        for square in self.squares:
            if square.piece and square.piece.selected == True:
                square.piece.selected = False
    @staticmethod
    def is_piece_selected():
        for square in game.squares:
            if square.piece and square.piece.selected:
                return True
        return False
    def print_possible_moves(self):
        for square in self.squares:
            if square.piece and square.piece.selected:
                print(square.piece.possible_moves)
    ### Move ###
    def move_piece(self):
        possible_moves = set()
        for square in self.squares:
            if square.piece and square.piece.selected:
                possible_moves = square.piece.possible_moves
                attacking_piece = square.piece
                attacking_square = square
                piece_coords = square.coords
        for square in self.squares:
            if square.is_clicked() and square.coords in possible_moves:
                attacking_square.piece = None               
                square.piece = attacking_piece
                square.piece.location = square.coords
                self.unselect_pieces()
                moved = True
                # Move rook if King is castled
                if attacking_piece.name == 'king':
                    x_king_before, y_king_before = piece_coords
                    x_king_after, y_king_after = square.coords
                    def move_rook(x_rook_pos, y_rook_pos, king_factor, rook_factor):
                        for square_rook in self.squares:
                            if square_rook.piece:
                                x_rook, y_rook = square_rook.coords
                                if square_rook.piece.name == 'rook' \
                                and square_rook.piece.color == attacking_piece.color \
                                and y_rook == y_rook_pos \
                                and x_rook == x_rook_pos:
                                    rook_exists = True
                                    square_rook_before = square_rook
                                    break
                                else:
                                    rook_exists = False
                        if rook_exists:
                            if y_king_before == y_king_after:
                                if x_king_before == x_king_after - king_factor:
                                    x_rook_destination = x_rook_pos + rook_factor
                                    y_rook_destination = y_king_before
                                    for square in self.squares:
                                        if square.piece == None:
                                            if square.coords == (x_rook_destination, y_rook_destination):
                                                moving_rook = square_rook_before.piece
                                                square_rook.piece = None
                                                square.piece = moving_rook
                                                square.piece.location = square.coords      
                    
                    move_rook(0, 7, -2, 3) # Lower left
                    move_rook(7, 7, 2, -2) # Lower right
                    move_rook(0, 0, -2, 3) # Upper left
                    move_rook(7, 0, 2, -2) # Upper right
                return moved
    def change_turns(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
    def return_opposite_turn(self):
        if self.turn == 'white':
            return 'black'
        else:
            return 'white'
    def update_all_friendly_possible_moves(self):
        self.all_friendly_possible_moves = set()
        for square in self.squares:
            if square.piece:
                if square.piece.color == self.turn:
                    square.piece.update_possible_moves()
                    self.all_friendly_possible_moves.update(square.piece.possible_moves)
    def update_all_enemy_possible_moves(self):
        self.change_turns()
        self.all_enemy_possible_moves = set()
        for square in self.squares:
            if square.piece:
                if square.piece.color == self.turn:
                    square.piece.update_possible_moves()
                    self.all_enemy_possible_moves.update(square.piece.possible_moves)
        self.change_turns()
    def check_king(self):
        self.update_all_friendly_possible_moves()
        self.update_all_enemy_possible_moves()
        for square in self.squares:
            if square.piece:
                if square.piece.name == 'king':
                    if square.piece.color != self.turn:
                        if square.coords in self.all_friendly_possible_moves: 
                            square.piece.checked = True
                        else:
                            square.piece.checked = False
                    else:
                        if square.coords in self.all_enemy_possible_moves: 
                            square.piece.checked = True
                        else:
                            square.piece.checked = False
                            
    def is_friendly_king_checked(self):
        self.update_all_friendly_possible_moves()
        self.update_all_enemy_possible_moves()
        for square in self.squares:
            if square.piece:
                if square.piece.name == 'king':
                    if square.piece.color == self.turn:
                        if square.coords in self.all_enemy_possible_moves: 
                            return True
                        else:
                            return False

    def update_safe_moves(self):
        self.safe_moves = set()
        for square in game.squares:
            if square.piece:
                if square.piece.color == self.turn:
                    moving_piece = square.piece
                    moving_square = square
                    possible_moves = square.piece.possible_moves.copy()
                    for move in possible_moves:
                        for square in game.squares:
                            if square.coords == move:
                                moving_square.piece == None
                                captured_piece = square.piece
                                square.piece = moving_piece
                                square.piece.location = square.coords
                                if not self.is_friendly_king_checked():
                                    game.safe_moves.add(move)
                                moving_square.piece = moving_piece
                                square.piece = captured_piece
                                moving_square.piece.location = moving_square.coords


class Board:
    WIDTH = 8
    HEIGHT = WIDTH
    SQUARE_SIZE = 100
    BOARD_SIZE = SQUARE_SIZE * WIDTH
    SQUARE_COLOR_1 = Graphics.TAN
    SQUARE_COLOR_2 = Graphics.DARK_GREEN

class Square:
    def __init__(self, coords):
        self.coords = coords
        self.highlighted = False
        self.piece = None
    def is_clicked(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        square_x, square_y = Graphics.pixelate(self.coords)
        if square_x <= mouse_x <= square_x + Board.SQUARE_SIZE and square_y <= mouse_y <= square_y + Board.SQUARE_SIZE:
            return True
        return False
        
class Piece:
    def __init__(self, name, color, location):
        self.name = name
        self.color = color
        self.image = pg.transform.scale(pg.image.load(os.path.join('pngs', self.name + '_' + self.color + '.png')), (Board.SQUARE_SIZE, Board.SQUARE_SIZE))
        self.location = location
        self.origin = location
        self.possible_moves = set()
        self.possible_captures = set()
        self.selected = False
        self.checked = False
        self.update_possible_moves()

    def update_possible_moves_considering_safe(self):
        game.update_safe_moves()
        possible_moves_static = self.possible_moves.copy()
        for move in possible_moves_static:
            if move not in game.safe_moves:
                self.possible_moves.remove(move)

class Pawn(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
            self.possible_moves = set()
            self.possible_captures = set()
            x_piece, y_piece = self.location
            for square in game.squares:
                x_possible_square, y_possible_square = square.coords
                if not square.piece:
                # Adds regular movement
                    if x_piece == x_possible_square and y_piece + self.direction_vertical() == y_possible_square:
                        self.possible_moves.add(square.coords)
                # Adds movement from original position    
                    if x_piece == x_possible_square and y_piece + self.direction_vertical() * 2 == y_possible_square and self.origin == self.location:
                        self.possible_moves.add(square.coords) 
                # Adds capture possibilities (left)
                direction_x, direction_y = self.diagonal_direction_left()
                if square.piece and square.piece.color != game.turn:
                    if x_piece + direction_x == x_possible_square and y_piece + direction_y == y_possible_square:
                        self.possible_moves.add(square.coords)
                        self.possible_captures.add(square.coords)
                # Adds capture possibilities (Right)
                    direction_x, direction_y = self.diagonal_direction_right()
                    if x_piece + direction_x == x_possible_square and y_piece + direction_y == y_possible_square:
                        self.possible_moves.add(square.coords)
                        self.possible_captures.add(square.coords)
    def is_forward_empty(self):
        for square in game.squares:
            x_selected, y_selected = square.coords
            x_forward, y_forward = x_selected, y_selected + self.direction_vertical()
            for square in game.squares:
                if square.coords == (x_forward, y_forward):
                    if square.piece:
                        return False
                    return True 
    def is_behind_empty(self):
        for square in game.squares:
            x_selected, y_selected = square.coords
            x_forward, y_forward = x_selected, y_selected - self.direction_vertical()
            for square in game.squares:
                if square.coords == (x_forward, y_forward):
                    if square.piece:
                        return False
                    return True 
    def direction_vertical(self):
        if self.color == 'white':
            return -1
        else:
            return 1
    def diagonal_direction_left(self):
        if self.color == 'white':
            return (-1, -1)
        else:
            return (-1, 1)
    def diagonal_direction_right(self):
        if self.color == 'white':
            return (1, -1)
        else:
            return (1, 1)              

class Rook(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
        self.possible_moves = set()
        x_piece, y_piece = self.location
        def update_possible_move(x_coord, y_coord):
            for square in game.squares:
                if square.coords == (x_coord, y_coord):
                    if square.piece and square.piece.color == game.turn:
                        return True
                    self.possible_moves.add((x_coord, y_coord))
                    if square.piece and square.piece.color != game.turn:
                        return True
        #Adds possible moves to the right
        for x in range(x_piece + 1, Board.WIDTH):
            if update_possible_move(x, y_piece):
                break
        # Adds possible moves to the left           
        for x in range(x_piece - 1,-1, -1):
            if update_possible_move(x, y_piece):
                break
        # Adds possible moves up
        for y in range(y_piece - 1, -1, -1):
            if update_possible_move(x_piece, y):
                break
        # Adds possible moves down
        for y in range(y_piece + 1,Board.WIDTH):
            if update_possible_move(x_piece, y):
                break

class Knight(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
        self.possible_moves = set()
        x_piece, y_piece = self.location
        # Direction listed first is one square away from location
        # e.g. #UR = Upper Right or up one, right two
        factors_set = set()
        factors_set.add((2, -1))  #UR
        factors_set.add((1, -2))  #RU
        factors_set.add((-2, -1)) #UL
        factors_set.add((-1, -2)) #LU
        factors_set.add((2, 1))   #DR
        factors_set.add((1, 2))   #RD
        factors_set.add((-2 ,1))  #DL
        factors_set.add((-1, 2))  #LD
        def update_possible_move(factors):
            x_factor, y_factor = factors
            for square in game.squares:
                x_possible_square, y_possible_square = square.coords
                # if square.piece:
                if square.piece and square.piece.color == game.turn:
                    pass
                elif x_piece == x_possible_square - x_factor:
                    if y_piece == y_possible_square - y_factor:
                        self.possible_moves.add((square.coords))
        for factors in factors_set:
            update_possible_move(factors)

class Bishop(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
        self.possible_moves = set()
        x_piece, y_piece = self.location
        def update_possible_move(x_coord, y_coord):
            for square in game.squares:
                if square.coords == (x_coord, y_coord):
                    if square.piece and square.piece.color == game.turn:
                        return True
                    self.possible_moves.add((x_coord, y_coord))
                    if square.piece and square.piece.color != game.turn:
                        return True
        # Adds possible moves in the upper right direction
        for x, y in zip(range(x_piece + 1, Board.WIDTH), range(y_piece - 1, -1, -1)):
            if update_possible_move(x, y):
                break
        # Adds possible moves in the upper left direction
        for x, y in zip(range(x_piece - 1,-1, -1), range(y_piece - 1, -1, -1)):
            if update_possible_move(x, y):
                break
        # Adds possible moves in the lower right direction
        for x, y in zip(range(x_piece + 1, Board.WIDTH), range(y_piece + 1,Board.WIDTH)):
            if update_possible_move(x, y):
                break
        # Adds possible moves in the lower left direction
        for x, y in zip(range(x_piece - 1,-1, -1), range(y_piece + 1,Board.WIDTH)):
            if update_possible_move(x, y):
                break                

class Queen(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
        self.possible_moves = set()
        x_piece, y_piece = self.location
        def update_possible_move(x_coord, y_coord):
            for square in game.squares:
                if square.coords == (x_coord, y_coord):
                    if square.piece and square.piece.color == game.turn:
                        return True
                    self.possible_moves.add((x_coord, y_coord))
                    if square.piece and square.piece.color != game.turn:
                        return True
                # Adds possible moves in the upper right direction
        for x, y in zip(range(x_piece + 1, Board.WIDTH), range(y_piece - 1, -1, -1)):
            if update_possible_move(x, y):
                break
        # Adds possible moves in the upper left direction
        for x, y in zip(range(x_piece - 1,-1, -1), range(y_piece - 1, -1, -1)):
            if update_possible_move(x, y):
                break
        # Adds possible moves in the lower right direction
        for x, y in zip(range(x_piece + 1, Board.WIDTH), range(y_piece + 1,Board.WIDTH)):
            if update_possible_move(x, y):
                break
        # Adds possible moves in the lower left direction
        for x, y in zip(range(x_piece - 1,-1, -1), range(y_piece + 1,Board.WIDTH)):
            if update_possible_move(x, y):
                break
        #Adds possible moves to the right
        for x in range(x_piece + 1, Board.WIDTH):
            if update_possible_move(x, y_piece):
                break
        # Adds possible moves to the left           
        for x in range(x_piece - 1,-1, -1):
            if update_possible_move(x, y_piece):
                break
        # Adds possible moves up
        for y in range(y_piece - 1, -1, -1):
            if update_possible_move(x_piece, y):
                break
        # Adds possible moves down
        for y in range(y_piece + 1,Board.WIDTH):
            if update_possible_move(x_piece, y):
                break

class King(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
        
    def update_possible_moves(self):
        self.possible_moves = set()
        x_piece, y_piece = self.location
        factors_set = set()
        # Comments indicate direction e.g. U = Up, DL = Down left, etc.
        factors_set.add((1, -1))  #UR
        factors_set.add((0, -1))  #U
        factors_set.add((-1, -1)) #UL
        factors_set.add((-1, 0))  #L
        factors_set.add((-1, 1))  #DL
        factors_set.add((0, 1))   #D
        factors_set.add((1 ,1))   #DR
        factors_set.add((1, 0))   #R        
        def update_possible_move(factors):
            x_factor, y_factor = factors
            for square in game.squares:
                x_possible_square, y_possible_square = square.coords
                if square.piece and square.piece.color == game.turn:
                    pass
                elif x_piece == x_possible_square - x_factor:
                    if y_piece == y_possible_square - y_factor:
                        self.possible_moves.add((square.coords))
        for factors in factors_set:
            update_possible_move(factors)
        # Adds possible castle moves
        def add_possible_castle(turn, x_rook_pos, y_rook_pos, factor):
            if not self.checked:
                for square in game.squares:
                    if not square.piece:
                        x_square, y_square = square.coords
                        x_piece, y_piece = self.location
                        if game.turn == turn:
                            if x_square == x_piece + factor:
                                if y_square == y_piece:
                                    for square_rook in game.squares:
                                        if square_rook.piece:
                                            if square_rook.piece.name == 'rook':
                                                if square_rook.piece.color == game.turn:
                                                    x_rook, y_rook = square_rook.coords
                                                    if y_rook == y_rook_pos:
                                                        if x_rook == x_rook_pos:
                                                            self.possible_moves.add(square.coords)
        if self.origin == self.location:
            # checks if there is a piece between king and rook
            def any_piece(turn, side):
                if side == 'left':
                    x_squares = [1,2,3]
                else:
                    x_squares = [5,6]
                if turn == 'white':
                    y_square_pos = 7
                else:
                    y_square_pos = 0            
                for square in game.squares:
                    x_square, y_square = square.coords
                    if y_square == y_square_pos:
                        if x_square in x_squares:
                            if square.piece:
                                return True
            if not any_piece('white', 'left'):
                # Lower left side castle
                add_possible_castle('white', 0, 7, -2)
            if not any_piece('white', 'right'):
                # Lower right side castle
                add_possible_castle('white', 7, 7,  2)
            if not any_piece('black', 'left'):
                # Upper left side castle
                add_possible_castle('black', 0, 0, -2)
            if not any_piece('black', 'right'):
                # Upper right side castle
                add_possible_castle('black', 7, 0,  2)
    def make_checked(self):
        if not self.checked:
            self.checked = True

def main():
    global game
    game = Game()
    game.run()

if __name__ == "__main__":
    main()