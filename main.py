
import sys

from game import Game
from move import Move
from menu import *
from cpu import *
from square import Square


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH + 200 + (2 * SPAN), HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.menu = Menu()

    def mainloop(self):

        game = self.game
        board = self.game.board
        screen = self.screen
        dragger = self.game.dragger
        menu = self.menu

        while True:

            game.show_bg(screen)
            game.show_moves(screen)
            game.show_hover(screen)
            game.show_pieces(screen)
            menu.show_menu(screen, game)

            if dragger.dragging:
                dragger.update_blit(screen)

            # Handle player's turn or PvP
            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.pos[0] > WIDTH:
                        # handle menu
                        clicked_button = menu.clicked_element(event.pos[1])
                        if isinstance(clicked_button, StartPvpButton):
                            game.reset()
                            game = self.game
                            game.gamemode = PVP
                            board = self.game.board
                            dragger = self.game.dragger
                        elif isinstance(clicked_button, StartPvcButton):
                            game.reset()
                            game = self.game
                            game.gamemode = PVC
                            board = self.game.board
                            dragger = self.game.dragger
                        elif isinstance(clicked_button, ThemeButton):
                            game.change_theme()
                        elif isinstance(clicked_button, MoreDepth):
                            Game.change_depth(True)
                            menu.refresh_pvc_tags(screen)
                        elif isinstance(clicked_button, LessDepth):
                            Game.change_depth(False)
                            menu.refresh_pvc_tags(screen)
                        elif isinstance(clicked_button, AlgorButton):
                            Game.change_algor()
                            menu.refresh_pvc_tags(screen)
                        continue

                        # ends handle menu

                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            # print(piece.moves[1].final.row,piece.moves[1].final.col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # showing methods
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # move mouse
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    if motion_row < 8 and motion_col < 8:
                        game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        # game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_hover(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        finial = Square(released_row, released_col)
                        move = Move(initial, finial)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()

                            game.play_soud(captured)
                            # end game
                            if captured:
                                killed_piece = board.squares[released_row][released_col].piece
                                if isinstance(killed_piece, King):
                                    print('Game Finished')
                                    game.end_game()

                            # move
                            board.move(dragger.piece, move)
                            # Show
                            game.show_bg(screen)
                            # game.show_last_move(screen)
                            game.show_pieces(screen)

                            game.next_turn()

                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # if event.key == pygame.K_r:
                    #     game.reset()
                    #     game = self.game
                    #     board = self.game.board
                    #     dragger = self.game.dragger

                # quit app
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Handle AI move if PvC
            if game.gamemode == PVC and game.next_player == BLACK:

                end_game = AI.get_ai_move(board)
                # Show
                game.show_bg(screen)
                # game.show_last_move(screen)
                game.show_pieces(screen)
                if end_game:
                    game.end_game()
                else:
                    game.next_turn()
                menu.update_pvc(AI.time, AI.moves, AI.boards)
                print(AI.moves, AI.boards, AI.time)
                continue

            pygame.display.update()


main = Main()
main.mainloop()
