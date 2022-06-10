import pygame as pg
import os

# All icons made by Freepik from www.flaticon.com

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
        if game.is_piece_selected():
            self.draw_possible_moves()
            self.draw_selection()
            
        self.update()
    def draw_pieces(self):
        for square in board.squares:
            if square.piece:
                self.screen.blit(square.piece.image, self.pixelate(square.coords))
    def draw_board(self):
        for square in board.squares:
            if square.color == Board.SQUARE_COLOR_1:
                x_pixel, y_pixel = self.pixelate(square.coords)
                pg.draw.rect(self.screen,Board.SQUARE_COLOR_1,(x_pixel, y_pixel, Board.SQUARE_SIZE,Board.SQUARE_SIZE))
            else:
                x_pixel, y_pixel = self.pixelate(square.coords)
                pg.draw.rect(self.screen,Board.SQUARE_COLOR_2,(x_pixel, y_pixel, Board.SQUARE_SIZE,Board.SQUARE_SIZE))
    def draw_selection(self):
        for square in board.squares:
            if square.piece and square.piece.selected:
                x_pixel, y_pixel = self.pixelate(square.coords)
                pg.draw.circle(self.screen,self.GREEN, (x_pixel + int(Board.SQUARE_SIZE / 2), y_pixel + int(Board.SQUARE_SIZE / 2)), 5)
    def draw_possible_moves(self):
        for square in board.squares:
            if square.piece and square.piece.selected:
                for coords in square.piece.possible_safe_moves:
                    x_pixel, y_pixel = self.pixelate(coords)
                    pg.draw.rect(self.screen,self.YELLOW,(x_pixel + 1, y_pixel + 1, Board.SQUARE_SIZE - 2,Board.SQUARE_SIZE - 2),5)
    def draw_check(self):
        for square in board.squares:
            if square.piece:
                if square.piece.name == 'king':
                    if square.piece.checked:
                        x_pixel, y_pixel = self.pixelate(square.coords)
                        pg.draw.circle(self.screen,self.RED, (x_pixel + int(Board.SQUARE_SIZE / 2), y_pixel + int(Board.SQUARE_SIZE / 2)), 5)

class Game:
    def __init__(self):
        self.all_friendly_possible_moves = set() ###
        self.all_enemy_possible_moves = set()
        self.safe_moves = set()
        self.turn = 'white'
        self.running = True
    def run(self):
        global graphics
        graphics = Graphics()
        global board
        board = Board()
        board.set_squares()
        board.set_pieces()
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
                            board.flip_board()
    def select_piece(self):
        for square in board.squares:
            if square.piece and self.turn == square.piece.color and square.is_clicked():
                selected_before_reset = square.piece.selected
                self.unselect_pieces()
                square.piece.selected = not selected_before_reset
                square.piece.update_possible_safe_moves()
                return True
    def unselect_pieces(self):
        for square in board.squares:
            if square.piece and square.piece.selected == True:
                square.piece.selected = False
    def is_piece_selected(self):
        for square in board.squares:
            if square.piece and square.piece.selected:
                return True
        return False
    ### Move ###
    def move_piece(self):
        possible_moves = set()
        for square in board.squares:
            if square.piece and square.piece.selected:
                possible_moves = square.piece.possible_safe_moves
                attacking_piece = square.piece
                attacking_square = square
                piece_coords = square.coords
        moved = False
        for square in board.squares:
            if square.is_clicked() and square.coords in possible_moves:
                attacking_square.piece = None               
                square.piece = attacking_piece
                square.piece.location = square.coords
                self.unselect_pieces()
                moved = True
                attacking_piece.origin_lost = True
                # Move rook if King is castled
                if attacking_piece.name == 'king':
                    x_king_before, y_king_before = piece_coords
                    x_king_after, y_king_after = square.coords
                    def move_rook(x_rook_pos, y_rook_pos, king_factor, rook_factor):
                        for square_rook in board.squares:
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
                                    for square in board.squares:
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
            if moved == True:
                self.change_turns()
                return moved
    def change_turns(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
    def update_all_friendly_possible_moves(self):
        self.all_friendly_possible_moves = set()
        for square in board.squares:
            if square.piece:
                if square.piece.color == self.turn:
                    square.piece.update_possible_moves()
                    self.all_friendly_possible_moves.update(square.piece.possible_moves)
    def update_all_enemy_possible_moves(self):
        self.change_turns()
        self.all_enemy_possible_moves = set()
        for square in board.squares:
            if square.piece:
                if square.piece.color == self.turn:
                    square.piece.update_possible_moves()
                    self.all_enemy_possible_moves.update(square.piece.possible_moves)

        self.change_turns()
    def check_king(self):
        self.update_all_enemy_possible_moves()
        king = None
        king_other = None
        for square in board.squares:
                if square.piece:
                    if square.piece.name == 'king':
                        if square.piece.color == self.turn:
                            king = square.piece
                        elif square.piece.color != self.turn:
                            king_other = square.piece
        if king:    
            if self.is_friendly_king_checked():
                king.checked = True
            else:
                king.checked = False
        if king_other:    
            self.change_turns()
            if self.is_friendly_king_checked():
                king_other.checked = True
            else:
                king_other.checked = False
            self.change_turns()
    def is_friendly_king_checked(self):
        self.update_all_enemy_possible_moves()
        for square in board.squares:
            if square.piece:
                if square.piece.name == 'king':
                    if square.piece.color == self.turn:
                        if square.coords in self.all_enemy_possible_moves: 
                            return True
                        else:
                            return False                       

class Board:
    WIDTH = 8
    HEIGHT = WIDTH
    SQUARE_SIZE = 100
    BOARD_SIZE = SQUARE_SIZE * WIDTH
    SQUARE_COLOR_1 = Graphics.TAN
    SQUARE_COLOR_2 = Graphics.DARK_GREEN
    def __init__(self):
        self.squares = set()
        self.flip = False
    def set_squares(self):
        for y_coord in range(0,Board.HEIGHT,2):
            for x_coord in range(0, Board.WIDTH, 2):
                self.squares.add(Square((x_coord, y_coord), Board.SQUARE_COLOR_1))
        for y_coord in range(1,Board.HEIGHT,2):
            for x_coord in range(1, Board.WIDTH, 2):
                self.squares.add(Square((x_coord, y_coord), Board.SQUARE_COLOR_1))
        for y_coord in range(0,Board.HEIGHT,2):
            for x_coord in range(1, Board.WIDTH, 2):
                self.squares.add(Square((x_coord, y_coord), Board.SQUARE_COLOR_2))
        for y_coord in range(1,Board.HEIGHT,2):
            for x_coord in range(0, Board.WIDTH, 2):
                self.squares.add(Square((x_coord, y_coord), Board.SQUARE_COLOR_2))
    def set_pawns(self):
        y_coord = Board.HEIGHT - 2
        for x_coord in range(Board.WIDTH):
            for square in self.squares:
                if square.coords == (x_coord, y_coord):
                    square.piece = Pawn('pawn', 'white', square.coords)
        y_coord = 1
        for x_coord in range(Board.WIDTH):
            for square in self.squares:
                if square.coords == (x_coord, y_coord):
                    square.piece = Pawn('pawn', 'black', square.coords)
        # for square in self.squares:
        #     if square.coords == (3,5):
        #         square.piece = Pawn('pawn', 'black', square.coords)
    def set_rooks(self):
        for square in self.squares:
            if square.coords == (0,0):
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
            # if square.coords == (5,4):
            #     square.piece = Knight('knight', 'black', square.coords)                
    def set_bishops(self):
        for square in self.squares:
            if square.coords == (2, 7):
                square.piece = Bishop('bishop', 'white', square.coords)
            if square.coords == (5, 7):
                square.piece = Bishop('bishop', 'white', square.coords)
            if square.coords == (5, 0):
                square.piece = Bishop('bishop', 'black', square.coords)
            if square.coords == (2, 0):
                square.piece = Bishop('bishop', 'black', square.coords)
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
            if square.coords == (4, 0):
                square.piece = King('king', 'black', square.coords)
            # if square.coords == (2, 4):
            #     square.piece = King('king', 'black', square.coords)
    ### Set Pieces ###
    def set_pieces(self):
        self.set_pawns()
        self.set_rooks()
        self.set_knights()
        self.set_bishops()
        self.set_queens()
        self.set_kings()
    def flip_board(self):
        for square in board.squares:
            square.coords = self.flip_coords(square.coords)
            self.flip_colors(square)
            if square.piece:
                square.piece.location = self.flip_coords(square.piece.location)
                square.piece.origin = self.flip_coords(square.piece.origin)
                square.piece.possible_moves = self.flip_coords(square.piece.possible_moves)
                square.piece.possible_safe_moves = self.flip_coords(square.piece.possible_safe_moves)
                square.piece.possible_captures = self.flip_coords(square.piece.possible_captures)
        self.flip = True
                
    def flip_colors(self, square):
        if square.color == Board.SQUARE_COLOR_1:
            square.color = Board.SQUARE_COLOR_2
        else:
            square.color = Board.SQUARE_COLOR_1
    def flip_coords(self, obj_in):
        set_out = set()
        if isinstance(obj_in, set):
            for coords_in in obj_in:
                old_x, old_y = coords_in
                new_x, new_y = Board.WIDTH - 1 - old_x, Board.HEIGHT - 1 - old_y
                coords_out = (new_x, new_y)
                set_out.add(coords_out)
            return set_out
        else:
            old_x, old_y = obj_in
            new_x, new_y = Board.WIDTH - 1 - old_x, Board.HEIGHT - 1 - old_y
            coords_out = (new_x, new_y)
            return coords_out
class Square:
    def __init__(self, coords, color):
        self.coords = coords
        self.highlighted = False
        self.color = color
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
        self.possible_safe_moves = set()
        self.possible_captures = set()
        self.selected = False
        self.checked = False
        self.origin_lost = False

    def update_possible_safe_moves(self):
        self.possible_safe_moves = set()
        for square in board.squares:
            if square.coords == self.location:
                moving_piece = square.piece
                moving_square = square
                self.update_possible_moves()
                possible_moves = square.piece.possible_moves.copy()
                for move in possible_moves:
                    for square_destination in board.squares:
                        if square_destination.coords == move:
                            moving_square.piece = None
                            captured_piece = square_destination.piece
                            square_destination.piece = moving_piece # Move
                            square_destination.piece.location = square_destination.coords
                            if not game.is_friendly_king_checked():
                                self.possible_safe_moves.add(move)
                            moving_square.piece = moving_piece
                            square_destination.piece = captured_piece
                            moving_square.piece.location = moving_square.coords

class Pawn(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
            self.possible_moves = set()
            self.possible_captures = set()
            x_piece, y_piece = self.location
            for square in board.squares:
                x_possible_square, y_possible_square = square.coords
                if not square.piece:
                # Adds regular movement
                    if x_piece == x_possible_square and y_piece + self.direction_vertical() == y_possible_square:
                        self.possible_moves.add(square.coords)
                # Adds double movement from origin
                    if not self.is_hop():    
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
    def is_hop(self):
        for square in board.squares:
            if square.piece:
                if square.coords == self.location:
                    origin_square = square
                    origin_x, origin_y = origin_square.coords
                    hopped_x, hopped_y = origin_x, origin_y + self.direction_vertical()
        for square in board.squares:
            hop_x, hop_y = square.coords
            if hopped_x == hop_x:
                if hopped_y == hop_y:
                    if square.piece:
                        return True
        return False
    def direction_vertical(self):
        if board.flip:
            return -1
        if game.turn == 'white':
            return -1
        else:
            return 1
    def diagonal_direction_left(self):
        if board.flip:
            return (-1, -1)
        if game.turn == 'white':
            return (-1, -1)
        else:
            return (-1, 1)
    def diagonal_direction_right(self):
        if board.flip:
            return (1, -1)
        if game.turn == 'white':
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
            for square in board.squares:
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
        factors_set = set()
        #added factors determine by every direction possible.
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0):
                    factors_set.add((x, y))
        def update_possible_move(factors):
            x_factor, y_factor = factors
            for square in board.squares:
                x_possible_square, y_possible_square = square.coords
                if square.piece and square.piece.color == game.turn:
                    pass
                elif x_piece == x_possible_square - x_factor:
                    if y_piece == y_possible_square - y_factor:
                        self.possible_moves.add(square.coords)
        for factors in factors_set:
            update_possible_move(factors)

class Bishop(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
        self.possible_moves = set()
        x_piece, y_piece = self.location
        def update_possible_move(x_coord, y_coord):
            for square in board.squares:
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
            for square in board.squares:
                if square.coords == (x_coord, y_coord):
                    if square.piece and square.piece.color == game.turn:
                        return True
                    self.possible_moves.add(square.coords)
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
        #Creates factors of surrounding directions 
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
            for square in board.squares:
                x_possible_square, y_possible_square = square.coords
                if square.piece and square.piece.color == game.turn:
                    pass
                elif x_piece == x_possible_square - x_factor:
                    if y_piece == y_possible_square - y_factor:
                        self.possible_moves.add(square.coords)
        for factors in factors_set:
            update_possible_move(factors)
        def add_possible_castle(turn, x_rook_pos, y_rook_pos, factor):  # Adds possible castle moves
            if not self.checked:
                if not self.origin_lost:
                    for square in board.squares:
                        if not square.piece:
                            x_square, y_square = square.coords
                            x_piece, y_piece = self.location
                            if game.turn == turn:
                                if x_square == x_piece + factor:
                                    if y_square == y_piece:
                                        for square_rook in board.squares:
                                            if square_rook.piece:
                                                if square_rook.piece.name == 'rook':
                                                    if square_rook.piece.color == game.turn:
                                                        if not square_rook.piece.origin_lost:
                                                            x_rook, y_rook = square_rook.coords
                                                            if y_rook == y_rook_pos:
                                                                if x_rook == x_rook_pos:
                                                                    self.possible_moves.add(square.coords)
        if self.origin == self.location:
            def is_any_piece(turn, side): # checks if there is a piece between king and rook
                if side == 'left':
                    x_squares = [1,2,3]
                else:
                    x_squares = [5,6]
                if turn == 'white':
                    y_square_pos = 7
                else:
                    y_square_pos = 0            
                for square in board.squares:
                    x_square, y_square = square.coords
                    if y_square == y_square_pos:
                        if x_square in x_squares:
                            if square.piece:
                                return True
                ### Lower left side castle ###
            if not is_any_piece('white', 'left'):
                add_possible_castle('white', 0, 7, -2)
                ### Lower right side castle ###
            if not is_any_piece('white', 'right'):
                add_possible_castle('white', 7, 7,  2)
                ### Upper left side castle ###
            if not is_any_piece('black', 'left'):
                add_possible_castle('black', 0, 0, -2)
                ### Upper right side castle ###
            if not is_any_piece('black', 'right'):
                add_possible_castle('black', 7, 0,  2)

def main():
    global game
    game = Game()
    game.run()

if __name__ == "__main__":
    main()