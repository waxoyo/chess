import os
from const import *


class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == WHITE else -1
        self.value = value# * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self,move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == WHITE else 1
        super().__init__('pawn', color, 100)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 300)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 330)


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 500)


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 900)


class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 20000)

