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
    def __init__(self):
        self.init = pg.init()
        self.set_caption = pg.display.set_caption("Chess")
    def update(self):
        pg.display.update()
    @staticmethod
    def pixelate(tuple):
        x, y = tuple
        return (Board.SQUARE_SIZE * x, Board.SQUARE_SIZE * y)
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

class Game:
    squares = set()
    def __init__(self):
        self.running = True
        self.turn = 'white'
    def run(self):
        graphics = Graphics()
        board = Board()
        self.set_squares()
        self.set_pieces()
        while self.running:
            graphics.draw_board()
            graphics.draw_pieces()
            if self.is_piece_selected():
                graphics.draw_selection()
            graphics.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.select_piece()
                        # self.print_if_selected()


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
    def set_pieces(self):
        self.set_pawns()
    def select_piece(self):
        for square in self.squares:
            if square.piece and self.turn == square.piece.color and square.is_clicked():
                selected_before_reset = square.piece.selected
                self.unselect_pieces()
                square.piece.selected = not selected_before_reset
                square.piece.update_possible_moves()
    def unselect_pieces(self):
        for square in self.squares:
            if square.piece and square.piece.selected == True:
                square.piece.selected = False
    def is_piece_selected(self):
        for square in self.squares:
            if square.piece and square.piece.selected:
                return True
        return False
    def print_if_selected(self):
        for square in self.squares:
            if square.piece:
                print(square.piece.selected)

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
        # print(pg.mouse.get_pos())
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
        self.possible_moves = set()
        self.selected = False

class Pawn(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)
    def update_possible_moves(self):
        x_piece, y_piece = self.location
        for square in Game.squares:
            x_square, y_square = square.coords
            if self.is_forward_empty() and x_piece == x_square and y_piece + self.direction() == y_square:
                self.possible_moves.add(square.coords)
                print(self.possible_moves)
    def is_forward_empty(self):
        for square in Game.squares:
            x_selected, y_selected = square.coords
            x_forward, y_forward = x_selected, y_selected + self.direction()
            for square in Game.squares:
                if square.coords == (x_forward, y_forward):
                    if square.piece:
                        return False
                    return True 
    def direction(self):
        if self.color == 'white':
            return -1
        else:
            return 1

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()