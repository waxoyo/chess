import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config


class Game:
    algorithm = ALPHABETA
    depth = 0

    def __init__(self):
        self.next_player = WHITE
        self.gamemode = PVP
        self.board = Board()
        self.dragger = Dragger()
        self.hovered_sqr = None
        self.config = Config()


    # show methods

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                # labels
                # if col == 0:
                #     color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                #     label = self.config.font.render(str(ROWS-row), 1, color)
                #     label_pos = (5, 5 + row * SQSIZE)
                #     surface.blit(label, label_pos)
                #
                # if row == 7:
                #     color = theme.bg.light if col % 2 == 0 else theme.bg.dark
                #     label = self.config.font.render(chr(65+col), 1, color)
                #     label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                #     surface.blit(label, label_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # dont blit the dragging piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece

            # show the moves
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def next_turn(self):
        if self.next_player is None:
            return

        self.next_player = WHITE if self.next_player == BLACK else BLACK

    def end_game(self):
        self.next_player = None

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color = (180,180,180)
            color = (0,0,0)
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_soud(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()

    @staticmethod
    def change_depth(more):
        if more:
            if Game.depth < 2:
                Game.depth += 1
        else:
            if Game.depth > 0:
                Game.depth -= 1

    @staticmethod
    def change_algor():
        Game.algorithm = MINMAX if Game.algorithm == ALPHABETA else ALPHABETA


