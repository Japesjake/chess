import pygame as pg

class Graphics:
    def __init__(self):
        self.white = (255,255,255)
        self.black = (0,   0,   0)
        self.brown = (165, 42, 42)
        self.screen = pg.display.set_mode((800,800))
        self.init = pg.init()
        self.set_caption = pg.display.set_caption("Chess")

if __name__ == "__main__":
    graphics = Graphics()
    print(graphics.white)