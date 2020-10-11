import pygame as pg
import os

# All icons made by Freepik from www.flaticon.com

# To do: fix bug where pawns jump pieces at origin

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
        if Game.is_piece_selected():
            self.draw_possible_moves()
            self.draw_selection()
        self.update()
    def draw_pieces(self):
        for square in Game.squares:
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
        for square in Game.squares:
            if square.piece and square.piece.selected:
                x_pixel, y_pixel = self.pixelate(square.coords)
                pg.draw.rect(self.screen,self.GREEN,(x_pixel, y_pixel, Board.SQUARE_SIZE,Board.SQUARE_SIZE),5)
    def draw_possible_moves(self):
        for square in Game.squares:
            if square.piece and square.piece.selected:
                for coords in square.piece.possible_moves:
                    x_pixel, y_pixel = self.pixelate(coords)
                    pg.draw.rect(self.screen,self.YELLOW,(x_pixel, y_pixel, Board.SQUARE_SIZE,Board.SQUARE_SIZE),5)

class Game:
    squares = set()
    turn = 'white'    
    def __init__(self):
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
                        # self.move_piece()
                        print(self.is_piece_selected())
                        # self.print_possible_moves()
    def set_squares(self):
        for y_coord in range(Board.HEIGHT):
            for x_coord in range(Board.WIDTH):
                self.squares.add(Square((x_coord, y_coord)))     
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
        for square in self.squares:
            if square.coords == (5,5):
                square.piece = Pawn('pawn', 'black', square.coords)
            if square.coords == (4,5):
                square.piece = Pawn('pawn', 'white', square.coords)
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
            if square.coords == (1,0):
                square.piece = Rook('rook','white', square.coords)
            if square.coords == (4,4):
                square.piece = Rook('rook','white', square.coords)                
    def set_pieces(self):
        # self.set_pawns()
        self.set_rooks()
    def select_piece(self):
        for square in self.squares:
            if square.piece and Game.turn == square.piece.color and square.is_clicked():
                selected_before_reset = square.piece.selected
                self.unselect_pieces()
                square.piece.selected = not selected_before_reset
                square.piece.update_possible_moves()
    def unselect_pieces(self):
        for square in self.squares:
            if square.piece and square.piece.selected == True:
                square.piece.selected = False
    @staticmethod
    def is_piece_selected():
        for square in Game.squares:
            if square.piece and square.piece.selected:
                return True
        return False
    def print_possible_moves(self):
        for square in self.squares:
            if square.piece and square.piece.selected:
                print(square.piece.possible_moves)
    def move_piece(self):
        possible_moves = set()
        for square in self.squares:
            if square.piece and square.piece.selected:
                possible_moves = square.piece.possible_moves
                attacking_piece = square.piece
                attacking_square = square
        for square in self.squares:
            if square.is_clicked() and square.coords in possible_moves and attacking_piece.color == Game.turn:
                attacking_square.piece = None               
                square.piece = attacking_piece
                square.piece.location = square.coords
                self.unselect_pieces()
                self.change_turns()
    def change_turns(self):
        if Game.turn == "white":
            Game.turn = "black"
        else:
            Game.turn = "white"

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

class Pawn(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
            self.possible_moves = set()
            self.possible_captures = set()
            x_piece, y_piece = self.location
            for square in Game.squares:
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
                if square.piece and square.piece.color != Game.turn:
                    if x_piece + direction_x == x_possible_square and y_piece + direction_y == y_possible_square:
                        self.possible_moves.add(square.coords)
                        self.possible_captures.add(square.coords)
                # Adds capture possibilities (Right)
                    direction_x, direction_y = self.diagonal_direction_right()
                    if x_piece + direction_x == x_possible_square and y_piece + direction_y == y_possible_square:
                        self.possible_moves.add(square.coords)
                        self.possible_captures.add(square.coords)
    def is_forward_empty(self):
        for square in Game.squares:
            x_selected, y_selected = square.coords
            x_forward, y_forward = x_selected, y_selected + self.direction_vertical()
            for square in Game.squares:
                if square.coords == (x_forward, y_forward):
                    if square.piece:
                        return False
                    return True 
    def is_behind_empty(self):
        for square in Game.squares:
            x_selected, y_selected = square.coords
            x_forward, y_forward = x_selected, y_selected - self.direction_vertical()
            for square in Game.squares:
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
        x_right_len = Board.WIDTH - x_piece - 1
        x_left_len = Board.WIDTH - x_right_len - 1
        y_up_len = Board.WIDTH - y_piece - 1
        y_down_len = Board.WIDTH - y_up_len - 1
        for square in Game.squares:
            # Adds possible moves to the right
            for x in range(x_piece, x_right_len):
                if square.coords == (x, y_piece):
                    self.possible_moves.add((x, y_piece))
            # Adds possible moves to the left            
            for x in range(x_left_len,x_piece,-1):
                if square.coords == (x,y_piece):
                    self.possible_moves.add((x,y_piece))
            # Adds possible moves up
            for y in range(y_piece, y_up_len):
                if square.coords == (x_piece,y):                
                    self.possible_moves.add((x_piece,y))
            # Adds possible moves down
            for y in range(y_down_len,y_piece,-1):
                if square.coords == (x_piece,y):                
                    self.possible_moves.add((x_piece,y))
        print(self.possible_moves)
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()