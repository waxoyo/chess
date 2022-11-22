from const import *
from game import Game
import pygame


class Menu:
    def __init__(self):
        self.title = Title()
        self.status = StatusTag()
        self.pvp_button = StartPvpButton()
        self.pvc_buttom = StartPvcButton()
        self.theme_button = ThemeButton()
        self.algor_button = AlgorButton()
        self.more_depth_button = MoreDepth()
        self.less_depth_button = LessDepth()
        self.gamemode_tag = GamemodeTag()
        self.algorithm_tag = CapValTag((TITLE_POS[0] + MENU_W // 2, 240 + TITLE_POS[1] + MENU_H // 2), Game.algorithm, 'Algorithm: ')
        self.depth_tag = CapValTag((TITLE_POS[0] + MENU_W // 2, 260 + TITLE_POS[1] + MENU_H // 2), Game.depth, 'Depth(0-2): ')
        self.time_tag = CapValTag((TITLE_POS[0] + MENU_W // 2, 290 + TITLE_POS[1] + MENU_H // 2), 0, 'Time(ms): ')
        self.moves_tag = CapValTag((TITLE_POS[0] + MENU_W // 2, 310 + TITLE_POS[1] + MENU_H // 2), 0, 'Moves: ')
        self.boards_tag = CapValTag((TITLE_POS[0] + MENU_W // 2, 330 + TITLE_POS[1] + MENU_H // 2), 0, 'Evaluated Boards: ')
        self.all_clickables = [self.pvp_button, self.theme_button, self.pvc_buttom, self.algor_button, self.more_depth_button, self.less_depth_button]

    def show_menu(self, surface, game):
        self.status.set_value(game)
        self.gamemode_tag.set_value(game)

        MenuBack.show_menu_back(surface)
        if game.gamemode == PVC:
            MenuBack.show_pvc_menu_back(surface)
            self.algorithm_tag.show_tag(surface)
            self.depth_tag.show_tag(surface)
            self.time_tag.show_tag(surface)
            self.moves_tag.show_tag(surface)
            self.boards_tag.show_tag(surface)
            self.algor_button.show_button(surface)
            self.less_depth_button.show_button(surface)
            self.more_depth_button.show_button(surface)

        self.title.show_tag(surface)
        self.status.show_tag(surface)
        self.pvp_button.show_button(surface)
        self.pvc_buttom.show_button(surface)
        self.theme_button.show_button(surface)
        self.gamemode_tag.show_tag(surface)

    def clicked_element(self, y_pos):
        for i in self.all_clickables:
            if i.was_clicked(y_pos) is not None:
                return i.was_clicked(y_pos)
        return None

    def update_pvc(self, time, moves, boards):
        self.time_tag.set_value(time)
        self.moves_tag.set_value(moves)
        self.boards_tag.set_value(boards)

    def refresh_pvc_tags(self, surface):
        self.algorithm_tag.set_value(Game.algorithm)
        self.depth_tag.set_value(Game.depth)
        self.algorithm_tag.show_tag(surface)
        self.depth_tag.show_tag(surface)


class MenuBack:
    def __init__(self):
        pass

    @staticmethod
    def show_menu_back(surface):
        rect = (WIDTH, 0, (2*SPAN) + MENU_W, HEIGHT)
        color = (35, 35, 35)
        pygame.draw.rect(surface, color, rect)

    @staticmethod
    def show_pvc_menu_back(surface):
        rect = (WIDTH, 250, (2 * SPAN) + MENU_W, 250)
        color = (100, 100, 100)
        pygame.draw.rect(surface, color, rect)


class Tag:
    def __init__(self, color, caption, font, pos):
        self.color = color
        self.caption = caption
        self.font = font
        self.pos = pos

    def show_tag(self, surface):
        label = self.font.render(self.caption, 1, self.color)
        label_rect = label.get_rect(center=self.pos)
        surface.blit(label, label_rect)


class Title(Tag):
    def __init__(self):
        font = pygame.font.SysFont('ARIAL', 26, bold=False)
        super().__init__((255, 253, 94), 'CHEESY CHESS', font, (TITLE_POS[0] + MENU_W // 2, TITLE_POS[1] + MENU_H // 2))


# TITLE_POS[0] + MENU_W //2
class StatusTag(Tag):
    def __init__(self):
        self.string = '\'s turn to move'
        self.value = WHITE
        font = pygame.font.SysFont('ARIAL', 16, bold=False)
        super().__init__((225, 225, 225), self.value + self.string, font, (TITLE_POS[0] + MENU_W // 2, 40 + TITLE_POS[1] + MENU_H // 2))

    def set_value(self, game):
        if game.next_player is None:
            self.caption = 'Game Over... ' + self.value + ' wins!'
            return
        self.value = game.next_player
        self.caption = self.value + self.string


class CapValTag(Tag):
    def __init__(self, pos, value, string):
        self.string = string
        self.value = value
        self.pos = pos
        font = pygame.font.SysFont('ARIAL', 16, bold=False)
        super().__init__((225, 225, 225), self.string + str(self.value), font, pos)

    def set_value(self, value):
        self.value = value
        self.caption = self.string + str(self.value)


class GamemodeTag(Tag):
    def __init__(self):
        self.string = 'Game mode: '
        self.value = PVP
        font = pygame.font.SysFont('ARIAL', 16, bold=False)
        super().__init__((225, 225, 225), self.string + self.value, font, (TITLE_POS[0] + MENU_W // 2, HEIGHT - 50 + MENU_H // 2))

    def set_value(self, game):
        self.value = game.gamemode
        self.caption = self.string + self.value


class Button:
    def __init__(self, color, caption, pos):
        self.color = color
        self.caption = caption
        self.pos = pos

    def was_clicked(self, y_pos):
        clicked = y_pos > self.pos[1] - 15 and y_pos < self.pos[1] + 15
        if clicked:
            return self
        return None

    def show_button(self, surface):
        font = pygame.font.SysFont('ARIAL', 16, bold=False)
        label = font.render(self.caption, True, self.color)
        label_rect = label.get_rect(center=(self.pos[0], self.pos[1]))
        surface.blit(label, label_rect)


class StartPvpButton(Button):
    def __init__(self):
        super().__init__((60, 95, 135), 'Start PvP', (TITLE_POS[0] + MENU_W // 2, 100 + TITLE_POS[1] + MENU_H // 2))


class StartPvcButton(Button):
    def __init__(self):
        super().__init__((60, 95, 135), 'Start PvC', (TITLE_POS[0] + MENU_W // 2, 140 + TITLE_POS[1] + MENU_H // 2))


class ThemeButton(Button):
    def __init__(self):
        super().__init__((255, 253, 94), 'Change Theme', (TITLE_POS[0] + MENU_W // 2, HEIGHT - 100 + MENU_H // 2))


class AlgorButton(Button):
    def __init__(self):
        super().__init__((255, 253, 94), 'Change Algorithm', (TITLE_POS[0] + MENU_W // 2, 370 + TITLE_POS[1] + MENU_H // 2))


class MoreDepth(Button):
    def __init__(self):
        super().__init__((255, 253, 94), 'Increase Depth', (TITLE_POS[0] + MENU_W // 2, 400 + TITLE_POS[1] + MENU_H // 2))


class LessDepth(Button):
    def __init__(self):
        super().__init__((255, 253, 94), 'Decrease Depth', (TITLE_POS[0] + MENU_W // 2, 430 + TITLE_POS[1] + MENU_H // 2))
