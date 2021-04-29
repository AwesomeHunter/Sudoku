from sudoku import Sudoku
import pygame as pg
from pygame.math import Vector2
from math import sqrt

class App:
    
    TILE_SIZE   = Vector2(64, 64)
    SPACE       = Vector2(2, 2)
    FONT_SIZE   = 32
    SIZE        = 3
    NUMBERS     = SIZE ** 2
    SCREEN_SIZE = NUMBERS * TILE_SIZE + (NUMBERS + 1) * SPACE
    
    KEYS = {
        pg.K_BACKSPACE: 0,
        pg.K_1: 1,
        pg.K_2: 2,
        pg.K_3: 3,
        pg.K_4: 4,
        pg.K_5: 5,
        pg.K_6: 6,
        pg.K_7: 7,
        pg.K_8: 8,
        pg.K_9: 9,
    }
    
    def __init__(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption("Sudoku")
        self.font = pg.font.SysFont("arial", self.FONT_SIZE)
        self.screen = pg.display.set_mode((int(self.SCREEN_SIZE.x), int(self.SCREEN_SIZE.y)))
        self.running = True
        self.sudoku = Sudoku(self.SIZE)
        self.active_cell = None
        self.solving = False
        self.changed_tiles = []
        
    def draw_rect(self, size, position, color):
        rect = pg.Rect(position, size)
        pg.draw.rect(self.screen, color, rect)
        
    def blit_text(self, val, box):
        text_render = self.font.render(str(val), True, pg.Color("black"))
        text_rect = text_render.get_rect(center=box.center)
        self.screen.blit(text_render, text_rect)
        
    def get_tile_color(self, coords):
        sudoku_color = self.sudoku.check_position(coords)
        if coords == self.active_cell:
            return pg.Color("azure3")
        if sudoku_color == self.sudoku.WRONG:
            return pg.Color("red")
        if sudoku_color == self.sudoku.CORRECT:
            return pg.Color("green")
        return pg.Color("azure4")

    def draw_board(self):
        self.screen.fill(pg.Color("dimgray"))
        shift = self.TILE_SIZE + self.SPACE
        for i in range(0, self.NUMBERS + 1, self.SIZE):
            left_top = Vector2(i * shift.x, 0)
            size = Vector2(self.SPACE.x, self.SCREEN_SIZE.y)
            self.draw_rect(size, left_top, pg.Color("black"))
        for i in range(0, self.NUMBERS + 1, self.SIZE):
            left_top = Vector2(0, i * shift.y)
            size = Vector2(self.SCREEN_SIZE.x, self.SPACE.y)
            self.draw_rect(size, left_top, pg.Color("black"))

    def draw_tile_number(self, position):
        coords = position.elementwise() // (self.TILE_SIZE + self.SPACE)
        value_at_position = self.sudoku.get_at_position(coords)
        if value_at_position != 0:
            self.blit_text(value_at_position, pg.Rect(position, self.TILE_SIZE))

    def draw_tiles(self):
        for y in range(self.NUMBERS):
            for x in range(self.NUMBERS):
                coords = Vector2(x, y)
                left_top = coords.elementwise() * (self.SPACE + self.TILE_SIZE) + self.SPACE
                color = self.get_tile_color(coords)
                self.draw_rect(self.TILE_SIZE, left_top, color)
                self.draw_tile_number(left_top)
      
    def clicked_mouse(self, position):
        if self.solving is False:
            tile_position = Vector2(position).elementwise() // (self.TILE_SIZE + self.SPACE)
            if self.active_cell == tile_position:
                self.active_cell = None
            else:
                self.active_cell = tile_position
            
    def clicked_keboard(self, key):
        if self.active_cell is not None and key in self.KEYS and self.solving is False:
            self.sudoku.set_at_position(self.active_cell, self.KEYS[key])
        elif key == pg.K_s:
            self.solving = True
            
    def check_board(self):
        for y in range(self.NUMBERS):
            for x in range(self.NUMBERS):
                if self.sudoku.check_position(Vector2(x, y)) == self.sudoku.WRONG:
                    return False
        return True
    
    def find_empty_tile(self):
        for y in range(self.NUMBERS):
            for x in range(self.NUMBERS):
                position = Vector2(x, y)
                if self.sudoku.get_at_position(position) == 0:
                    return position
        return None
    
    def end_solving(self):
        self.solving = False
        self.changed_tiles = []
        self.active_cell = None
        
    def process_empty_tile(self, tile):
        self.changed_tiles.append(tile)
        self.sudoku.set_at_position(tile, 1)
        self.active_cell = self.changed_tiles[-1]
        
    def solve_step_forward(self):
        empty_tile = self.find_empty_tile()
        if empty_tile is None:
            self.end_solving()
        else:
            self.process_empty_tile(empty_tile)
            
    def increase_last_tile(self):
        position = self.changed_tiles[-1]
        old_value = self.sudoku.get_at_position(position)
        self.sudoku.set_at_position(position, old_value + 1)
        self.active_cell = position
        
    def wrong_last_tile(self):
        while len(self.changed_tiles) > 0 and self.sudoku.get_at_position(self.changed_tiles[-1]) == self.NUMBERS:
            self.sudoku.set_at_position(self.changed_tiles[-1], 0)
            self.changed_tiles.pop()
        if len(self.changed_tiles) == 0:
            self.end_solving()
        else:
            self.increase_last_tile()
    
    def solve_step_back(self):
        if len(self.changed_tiles) > 0:
            self.wrong_last_tile()
        else:
            self.end_solving()
    
    def make_solve_step(self):
        if self.solving:
            if self.check_board():
                self.solve_step_forward()
            else:
                self.solve_step_back()
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.clicked_mouse(pg.mouse.get_pos())
            elif event.type == pg.KEYDOWN:
                self.clicked_keboard(event.key)
          
    def run(self):
        self.draw_board()
        while self.running:
            self.handle_events()
            self.draw_tiles()
            self.make_solve_step()
            pg.display.flip()
        pg.quit()