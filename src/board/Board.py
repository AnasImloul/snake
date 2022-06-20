from src.board.Grid import Grid
from os import getcwd
from pygame.image import load
from pygame import MOUSEBUTTONDOWN, KEYDOWN, K_z, K_y
from pygame.mixer import Sound
from pygame.mouse import get_pos
from pygame.draw import rect
import src.Settings as Settings


class Board:

    def __init__(self, center):

        self.grid = Grid()

        self.image = load(getcwd() + "/assets/board.png")
        self.size = self.image.get_size()
        self.slot_size = self.size[0]//8, self.size[1]//8

        self.center = center

        self.selected = None
        self.sound = getcwd() + "/assets/click.wav"

        self.turn = 0

    def coordinate_to_position(self, x, y):
        return (self.center[0] + self.slot_size[0]*(x-4) + 30, self.center[1] + self.slot_size[1]*(4-y) - 30)

    def render(self, screen):
        screen.blit(self.image, (self.center[0] - self.size[0]/2, self.center[1] - self.size[1]/2))

        for index, piece in self.grid.pieces[0].items():
            piece.render(screen, self)

        for index, piece in self.grid.pieces[1].items():
            piece.render(screen, self)

    def input(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.select()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    if self.grid.undo():
                        self.turn = 1 - self.turn


    def click_sound(self):
        self.audio = Sound(self.sound)
        self.audio.play()
        self.audio.set_volume(Settings.volume)

    def get_mouse_index(self):
        x, y = get_pos()
        x -= self.center[0] - self.size[0] / 2
        y = -(y - self.center[1] - self.size[1] / 2)
        x,y = int(x//self.slot_size[0]), int(y//self.slot_size[1])
        if -1 < x < 8 and -1 < y < 8:
            index = 8 * y + x
            return index
        return -1

    def select(self):
        index = self.get_mouse_index()

        if index < 0:
            return

        if self.selected is None:
            if index not in self.grid.pieces[self.turn]:
                return

            self.selected = self.grid.pieces[self.turn][index]
            self.selected.selected = True

        else:
            if index not in self.grid.pieces[self.turn] and index not in self.selected.cache_legal_moves and index != self.selected.index:
                return

            if index == self.selected.index:
                self.selected.selected = False
                self.selected = None

            elif index in self.grid.pieces[self.turn]:
                self.selected.selected = False
                self.selected = self.grid.pieces[self.turn][index]
                self.selected.selected = True

            elif index in self.selected.cache_legal_moves:
                self.selected.move(self.grid,index)
                self.selected.selected = False
                self.selected = None
                self.turn = 1 - self.turn

        if self.selected is not None:
            self.selected.update(self.grid)

        self.click_sound()

    def highlight(self, screen, index, color=(0,255,255)):
        x,y = index%8, index//8

        x,y =self.slot_size[0]*(x-4), self.slot_size[1]*(3-y)

        rect(screen, color=color, rect=(x + self.center[0],y + self.center[1],self.slot_size[0],self.slot_size[1]), width=3)

    def highlight_check(self, screen):
        for color in range(2):
            if self.grid.is_check(color):
                self.highlight(screen, self.grid.check_piece[color], (255,50,50))

    def highlight_checkmate(self, screen):
        if self.grid.is_checkmate(0) or self.grid.is_checkmate(1):
            rect(screen, color=(255,50,50), rect=(-self.size[0]/2 + self.center[0], -self.size[1]/2 +  self.center[1], self.size[0], self.size[1]), width=4)

    def highlight_danger(self, screen, piece_color):
        for index in range(64):
            if self.grid.danger[piece_color][index]:
                self.highlight(screen,index, (0,200,0))

    def highlight_checked(self, screen, piece_color):
        for index in range(64):
            if self.grid.check[piece_color][index]:
                self.highlight(screen,index, (0,200,0))

    def update(self, screen, events):
        self.input(events)

        self.render(screen)
        #self.highlight_danger(screen, 0)
        self.highlight_check(screen)
        self.highlight_checkmate(screen)

        #print(self.grid.moves)