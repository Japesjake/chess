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
    def pixelate(tuple):
        x, y = tuple
        return (Board.SQUARE_SIZE * x, Board.SQUARE_SIZE * y)

class Game:
    objects = {}
    def __init__(self):
        self.running = True
    def run(self):
        graphics = Graphics()
        board = Board()
        self.set_squares()
        board.draw()
        self.set_pieces()
        self.draw_pieces()
        while self.running:
            graphics.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.select_piece()
    def set_squares(self):
        for y_coord in range(Board.HEIGHT):
            for x_coord in range(Board.WIDTH):
                self.objects[Square((x_coord, y_coord))] = None       
    def set_pawns(self):
        y_coord = Board.HEIGHT - 2
        for x_coord in range(Board.WIDTH):
            for square, piece in self.objects.items():
                if square.coords == (x_coord, y_coord):
                    self.objects[square] = Pawn('pawn', 'white', square.coords)
        y_coord = 1
        for x_coord in range(Board.WIDTH):
            for square, piece in self.objects.items():
                if square.coords == (x_coord, y_coord):
                    self.objects[square] = Pawn('pawn', 'black', square.coords)
    def set_pieces(self):
        self.set_pawns()
    def draw_pieces(self):
        for square in self.objects:
            if self.objects[square] != None:
                Graphics.screen.blit(self.objects[square].image, Graphics.pixelate(square.coords))
    def select_piece(self):
        for square, piece in self.objects.items():
            if piece != None and square.is_clicked():
                if piece.selected:
                    selected_before_reset = True
                else:
                    selected_before_reset = False
                # Resets all pieces to unselected status
                for piece_to_be_unselected in self.objects.values():
                    if piece_to_be_unselected != None:
                        piece_to_be_unselected.selected = False
                if selected_before_reset:
                    piece.selected = False
                else:
                    piece.selected = True


class Board:
    WIDTH = 8
    HEIGHT = WIDTH
    SQUARE_SIZE = 100
    BOARD_SIZE = SQUARE_SIZE * WIDTH
    SQUARE_COLOR_1 = Graphics.TAN
    SQUARE_COLOR_2 = Graphics.DARK_GREEN
    def draw(self):
        Graphics.screen.fill(self.SQUARE_COLOR_2)
        for y_coord in range(0,self.HEIGHT,2):
            for x_coord in range(0, self.WIDTH, 2):
                x_pixel, y_pixel = Graphics.pixelate((x_coord, y_coord))
                pg.draw.rect(Graphics.screen,self.SQUARE_COLOR_1,(x_pixel, y_pixel, self.SQUARE_SIZE,self.SQUARE_SIZE))
        for y_coord in range(1,self.HEIGHT,2):
            for x_coord in range(1, self.WIDTH, 2):
                x_pixel, y_pixel = Graphics.pixelate((x_coord, y_coord))
                pg.draw.rect(Graphics.screen,self.SQUARE_COLOR_1,(x_pixel, y_pixel, self.SQUARE_SIZE,self.SQUARE_SIZE))

class Square:
    def __init__(self, coords):
        self.coords = coords
        self.highlighted = False
    def is_clicked(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        # print(pg.mouse.get_pos())
        square_x, square_y = Graphics.pixelate(self.coords)
        if square_x <= mouse_x <= square_x + Board.SQUARE_SIZE and square_y <= mouse_y <= square_y + Board.SQUARE_SIZE:
            return True
        return False
    # def is_forward_square_occupied():
    #     for square, piece in Game.objects.items():
    #         if piece.selected:
    #             if piece.color == 'white':
    #                 direction = -1
    #             else:
    #                 direction = 1
    #             x_selected, y_selected = square.coords
    #             x_forward, y_forward = x_selected, y_selected + direction
    #     for square, piece in Game.objects.items():
    #         if square.coords == (x_forward, y_forward):
    #             if piece != None:
    #                 return True
    #             return False
        


class Piece:
    def __init__(self, name, color, location):
        self.name = name
        self.color = color
        self.image = pg.transform.scale(pg.image.load(os.path.join('pngs', self.name + '_' + self.color + '.png')), (Board.SQUARE_SIZE, Board.SQUARE_SIZE))
        self.location = location
        self.possible_moves = []
        self.selected = False


class Pawn(Piece):
    def __init__(self, name, color, location):
        Piece.__init__(self, name, color, location)



def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()