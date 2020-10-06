import pygame as pg

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
    def __init__(self):
        self.running = True
    def run(self):
        graphics = Graphics()
        board = Board()
        board.load_squares_dict()
        board.draw()
        while self.running:
            graphics.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False


class Board:
    WIDTH = 8
    HEIGHT = WIDTH
    SQUARE_SIZE = 100
    BOARD_SIZE = SQUARE_SIZE * WIDTH
    SQUARE_COLOR_1 = Graphics.TAN
    SQUARE_COLOR_2 = Graphics.DARK_GREEN
    squares = {}
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
    def load_squares_dict(self):
        for y_coord in range(self.HEIGHT):
            for x_coord in range(self.WIDTH):
                self.squares[(x_coord, y_coord)] = None
        print(self.squares)

class Piece:
    pass

class Pawn(Piece):
    pass

def main():
    # graphics = Graphics()
    game = Game()
    game.run()
    # board = Board()

if __name__ == "__main__":
    main()