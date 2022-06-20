from pygame.image import load
from pygame.draw import rect
from time import sleep
from math import sqrt
import threading

class Piece:
    def __init__(self, color, type, index, steps, sprite):
        self.type = type
        self.color = color
        self.direction = 1 - 2*color
        self.index = index

        self.moves = []

        steps = [(step[0], self.direction * step[1]) for step in steps]
        self.steps = steps

        self.sprite = load(sprite)
        self.size = self.sprite.get_size()

        self.danger = set()
        self.check = set()

        self.started = False
        self.cache_legal_moves = None

        self.selected = False

        self.animation_pos = index%8, index//8
        self.animation_speed = 0.8
        self.animation_steps = 30

    def legal_moves(self, grid):
        return set()

    def move(self, grid, next_index):
        last_index = self.index
        if next_index not in self.cache_legal_moves:
            return False

        self.moves.append((self.index, next_index, grid.pieces[1 - self.color].get(next_index, None)))
        grid.moves.append(self)

        if next_index in grid.pieces[1 - self.color]:
            grid.pieces[1 - self.color][next_index].reset(grid)
            grid.pieces[1 - self.color].pop(next_index)

        grid.pieces[self.color][next_index] = self
        grid.pieces[self.color].pop(self.index)

        self.index = next_index
        self.update(grid)

        if grid.check_piece[1 - self.color] in self.cache_legal_moves:
            grid.update_color(1 - self.color)

        self.started = True
        self.lerp(last_index, next_index)

        return True

    def reset_danger(self, grid):
        for danger in self.danger:
            grid.danger[1 - self.color][danger] -= 1
        self.danger = set()

    def apply_danger(self, grid):
        for danger in self.danger:
            grid.danger[1 - self.color][danger] += 1

    def reset_check(self, grid):
        for check in self.check:
            grid.check[1 - self.color][check] -= 1
        self.check = set()

    def apply_check(self, grid):
        for check in self.check:
            grid.check[1 - self.color][check] += 1

    def update(self, grid):
        self.reset_danger(grid)
        self.reset_check(grid)

        self.cache_legal_moves = self.legal_moves(grid)

        self.apply_danger(grid)
        self.apply_check(grid)

    def reset(self, grid):
        self.reset_danger(grid)
        self.reset_check(grid)

    def __lerp__(self, old_index, next_index):

        old_x, old_y = old_index%8, old_index//8
        next_x, next_y = next_index % 8, next_index // 8

        Dx, Dy = (next_x - old_x), (next_y - old_y)

        distance = sqrt(Dx*Dx + Dy*Dy)


        dl = distance/self.animation_steps

        dx = Dx * dl / distance
        dy = Dy * dl / distance

        sleep_time = dl/(self.animation_speed*self.animation_steps)

        for step in range(self.animation_steps):
            sleep(sleep_time)
            self.animation_pos = self.animation_pos[0] + dx, self.animation_pos[1] + dy

        self.animation_pos = next_x, next_y

    def lerp(self, old_index, next_index):
        threading.Thread(target=self.__lerp__, args=(old_index, next_index)).start()

    def undo(self, grid):

        if not self.moves:
            return False

        last_move = self.moves.pop()

        old_index, new_index, killed_piece = last_move

        grid.pieces[self.color].pop(new_index)
        grid.pieces[self.color][old_index] = self
        self.index = old_index

        if killed_piece is not None:
            grid.pieces[1 - self.color][killed_piece.index] = killed_piece
            killed_piece.update(grid)

        self.update(grid)

        self.lerp(new_index, old_index)

        return True

    def render(self, screen, board):

        centered_pos = self.animation_pos[0] - 1/2, self.animation_pos[1] + 1/2
        pos = board.coordinate_to_position(centered_pos[0], centered_pos[1])

        screen.blit(self.sprite, (pos[0], pos[1]))

        if self.selected:
            rect(screen, color=(0, 200, 255), rect=(pos[0], pos[1], self.size[0], self.size[1]), width=3)

            for legal_move in self.cache_legal_moves:
                dx, dy = (legal_move%8) - (self.index%8), (legal_move//8) - (self.index//8)
                next_pos = pos[0] + self.size[0] * dx,  pos[1] - self.size[1] * dy

                rect(screen, color=(255,200,0), rect=(next_pos[0], next_pos[1], self.size[0], self.size[1]), width=3)