
import copy
from piece import *
import time
from game import Game


class Heuristics:
    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                if board.squares[x][y].has_piece():
                    if board.squares[x][y].piece.color == WHITE:
                        white += board.squares[x][y].piece.value
                    else:
                        black += board.squares[x][y].piece.value

        return white - black

    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                if board.squares[x][y].has_piece():
                    if board.squares[x][y].piece.name == piece_type:
                        if board.squares[x][y].piece.color == WHITE:
                            white += table[x][y]
                        else:
                            black += table[7 - x][y]
        return white - black

    @staticmethod
    def evaluate(board):
        material = Heuristics.get_material_score(board)
        pawns = Heuristics.get_piece_position_score(board, 'pawn', PAWN_TABLE)
        knights = Heuristics.get_piece_position_score(board, 'knight', KNIGHT_TABLE)
        bishops = Heuristics.get_piece_position_score(board, 'bishop', BISHOP_TABLE)
        rooks = Heuristics.get_piece_position_score(board, 'rook', ROOK_TABLE)
        queens = Heuristics.get_piece_position_score(board, 'queen', QUEEN_TABLE)

        return material + pawns + knights + bishops + rooks + queens


class AI:
    boards = 0
    moves = 0
    time = 0
    last_move = (None, None)

    @staticmethod
    def is_last_move(piece1, move1, piece2, move2):
        if piece1 == piece2:
            if move1.initial.row == move2.final.row and move1.initial.col == move2.final.col:
                if move1.final.row == move2.initial.row and move1.final.col == move2.initial.col:
                    return True
        return False

    @staticmethod
    def get_ai_move(board):
        best_move = (None, None)
        best_score = INFINITE
        end_game = False

        AI.boards = 0
        AI.moves = 0
        AI.time = int(time.time()*1000)

        for squares in board.squares:
            for square in squares:
                if square.has_piece():
                    piece = square.piece
                    if piece.color == BLACK:
                        board.calc_moves(piece, square.row, square.col)
                        for move in piece.moves:
                            if not AI.is_last_move(AI.last_move[0], AI.last_move[1], piece.name, move):
                                AI.moves += 1
                                copy_board = copy.deepcopy(board)
                                copy_piece = copy_board.squares[square.row][square.col].piece
                                copy_board.move(copy_piece, move)
                                # recursive call according detph
                                if Game.algorithm == ALPHABETA:
                                    score = AI.alphabeta(copy_board, Game.depth, -INFINITE, INFINITE, MAXIM)
                                else:
                                    score = AI.minmax(copy_board, Game.depth, MAXIM)

                                if score < best_score:
                                    best_score = score
                                    best_move = move

        moved_piece = board.squares[best_move.initial.row][best_move.initial.col].piece
        move_to_square = board.squares[best_move.final.row][best_move.final.col]
        if move_to_square.has_piece():
            if isinstance(move_to_square.piece, King):
                end_game = True
        board.move(moved_piece, best_move)
        AI.last_move = (moved_piece.name, best_move)
        AI.time = int(time.time() * 1000) - AI.time
        return end_game

    @staticmethod
    def alphabeta(board, depth, a, b, maximizing):
        if depth == 0:
            AI.boards += 1
            return Heuristics.evaluate(board)

        move_color = WHITE if maximizing else BLACK
        best_score = -INFINITE if maximizing else INFINITE
        moves_n_squares = []
        for squares in board.squares:
            for square in squares:
                if square.has_piece():
                    piece = square.piece
                    if piece.color == move_color:
                        board.calc_moves(piece, square.row, square.col, True)
                        for move in piece.moves:
                            AI.moves += 1
                            moves_n_squares.append((move, square))

        if maximizing:
            for move_square in moves_n_squares:
                copy_board = copy.deepcopy(board)
                copy_piece = copy_board.squares[move_square[1].row][move_square[1].col].piece
                copy_board.move(copy_piece, move_square[0])
                # recursive call according detph
                best_score = max(AI.alphabeta(copy_board, depth - 1, a, b, True), best_score)
                a = max(a, best_score)
                if b <= a:
                    break
            del copy_board
            del copy_piece
            return best_score

        else:
            for move_square in moves_n_squares:
                copy_board = copy.deepcopy(board)
                copy_piece = copy_board.squares[move_square[1].row][move_square[1].col].piece
                copy_board.move(copy_piece, move_square[0])
                # recursive call according detph
                best_score = min(AI.alphabeta(copy_board, depth - 1, a, b, False), best_score)
                b = min(b, best_score)
                if b <= a:
                    break
            del copy_board
            del copy_piece
            return best_score

    @staticmethod
    def minmax(board, depth, maximizing):
        if depth == 0:
            AI.boards += 1
            return Heuristics.evaluate(board)

        move_color = WHITE if maximizing else BLACK
        best_score = -INFINITE if maximizing else INFINITE
        moves_n_squares = []
        for squares in board.squares:
            for square in squares:
                if square.has_piece():
                    piece = square.piece
                    if piece.color == move_color:
                        board.calc_moves(piece, square.row, square.col, True)
                        for move in piece.moves:
                            AI.moves += 1
                            moves_n_squares.append((move, square))

        if maximizing:
            for move_square in moves_n_squares:
                copy_board = copy.deepcopy(board)
                copy_piece = copy_board.squares[move_square[1].row][move_square[1].col].piece
                copy_board.move(copy_piece, move_square[0])
                # recursive call according detph
                score = AI.minmax(copy_board, depth - 1, False)
                best_score = max(score, best_score)
            del copy_board
            del copy_piece
            return best_score

        else:
            for move_square in moves_n_squares:
                copy_board = copy.deepcopy(board)
                copy_piece = copy_board.squares[move_square[1].row][move_square[1].col].piece
                copy_board.move(copy_piece, move_square[0])
                # recursive call according detph
                score = AI.minmax(copy_board, depth - 1, True)
                best_score = min(score, best_score)
            del copy_board
            del copy_piece
            return best_score
