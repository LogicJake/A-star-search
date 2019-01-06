# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-06 16:52:35
# @Last Modified time: 2019-01-06 23:00:43
import pygame
import sys
from pygame import locals


WIDTH_NUM = 8    # number of block in width
HEIGHT_NUM = 6   # number of block in height
BLOCK_SIZE = 80  # size of block

SCREEN_WIDTH = WIDTH_NUM * BLOCK_SIZE
SCREEN_HEIGHT = HEIGHT_NUM * BLOCK_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)

cost_1 = 10
cost_2 = 14


class Block():

    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.location_x = x * BLOCK_SIZE
        self.location_y = y * BLOCK_SIZE

        self.fill_color = BLACK
        self.border_color = PURPLE

        # f = g + h
        self.f = 0
        self.g = 0
        self.h = 0

        self.text_size = BLOCK_SIZE // 6
        self.type = 0

    def draw_text(self, text, x, y):
        font = pygame.font.Font('freesansbold.ttf', self.text_size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        pygame.draw.rect(self.screen, self.fill_color, [
            self.location_x, self.location_y, BLOCK_SIZE, BLOCK_SIZE], 0)

        pygame.draw.rect(self.screen, self.border_color, [
            self.location_x, self.location_y, BLOCK_SIZE, BLOCK_SIZE], 5)

        padding_x = 10
        padding_y = 10
        if self.type != 0:
            self.draw_text(str(self.f), self.location_x +
                           padding_x, self.location_y + padding_y)
            self.draw_text(str(self.g), self.location_x + padding_x,
                           self.location_y + BLOCK_SIZE - padding_y)
            self.draw_text(str(self.h), self.location_x + BLOCK_SIZE - padding_x,
                           self.location_y + BLOCK_SIZE - padding_y)

    def set_start(self):
        self.fill_color = GREEN

    def set_obstacle(self):
        if self.fill_color == BLACK:
            self.fill_color = BLUE

    def set_end(self):
        if self.fill_color == BLACK:
            self.fill_color = RED

    def set_open(self):
        self.type = 1
        self.border_color = GREEN

    def set_close(self):
        self.border_color = YELLOW

    def set_g(self, g):
        self.g = g
        self.f = self.g + self.h

    def set_h(self, h):
        self.h = h
        self.f = self.g + self.h

    def set_father(self, father):
        self.father = father


class Screen():

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.blocks = []
        for j in range(HEIGHT_NUM):
            for i in range(WIDTH_NUM):
                self.blocks.append(Block(self.screen, i, j))
        self.start_block_index = None
        self.end_block_index = None
        self.obstacle_blocks_index = []

    def draw(self):
        for block in self.blocks:
            block.draw()

    def get_click_block_index(self, click_x, click_y):
        x = click_x // BLOCK_SIZE
        y = click_y // BLOCK_SIZE

        select_block = y * WIDTH_NUM + x
        return select_block

    def set_start(self, click_x, click_y):
        block_index = self.get_click_block_index(click_x, click_y)
        self.blocks[block_index].set_start()
        self.start_block_index = block_index

    def set_obstacle(self, click_x, click_y):
        block_index = self.get_click_block_index(click_x, click_y)
        self.blocks[block_index].set_obstacle()
        self.obstacle_blocks_index.append(block_index)

    def set_end(self, click_x, click_y):
        block_index = self.get_click_block_index(click_x, click_y)
        self.blocks[block_index].set_end()
        self.end_block_index = block_index


class A_star():

    def __init__(self, screen):
        self.open_list = []
        self.close_list = []

        self.screen = screen

        start_block = screen.start_block_index
        self.cur_block = start_block

        self.screen.blocks[start_block].set_g(0)
        self.screen.blocks[start_block].set_close()
        self.close_list.append(start_block)
        self.add_open_list(start_block)

    def add_open_list(self, block_index):
        block = self.screen.blocks[block_index]
        x = block.x
        y = block.y
        for x_plus in [-1, 0, 1]:
            for y_plus in [-1, 0, 1]:
                if not (x_plus == 0 and y_plus == 0):
                    x_temp = x + x_plus
                    y_temp = y + y_plus

                    temp_index = y_temp * WIDTH_NUM + x_temp

                    if self.is_ok(x_temp, y_temp, x_plus, y_plus):
                        if temp_index in self.open_list:
                            new_g = self.cal_g(temp_index, x_plus, y_plus)
                            if new_g < self.screen.blocks[temp_index].g:
                                self.screen.blocks[temp_index].set_g(new_g)
                                self.screen.blocks[
                                    temp_index].set_father(block_index)
                        else:
                            self.open_list.append(temp_index)
                            self.screen.blocks[temp_index].set_open()
                            self.screen.blocks[
                                temp_index].set_father(block_index)
                            g = self.cal_g(temp_index, x_plus, y_plus)
                            h = self.cal_h(x_temp, y_temp)
                            self.screen.blocks[temp_index].set_h(h)
                            self.screen.blocks[temp_index].set_g(g)

    def cal_g(self, block_index, x_plus, y_plus):
        father_index = self.screen.blocks[block_index].father
        father_g = self.screen.blocks[father_index].g

        if x_plus == 0 or y_plus == 0:
            return father_g + cost_1
        else:
            return father_g + cost_2

    def distance(self, x1, y1, x2, y2):
        return (abs(x2 - x1) + abs(y2 - y1)) * cost_1

    def cal_h(self, x, y):
        end_block_index = self.screen.end_block_index
        end_block = self.screen.blocks[end_block_index]

        end_x = end_block.x
        end_y = end_block.y

        return self.distance(x, y, end_x, end_y)

    def is_ok(self, x, y, x_plus, y_plus):
        index = y * WIDTH_NUM + x

        if abs(x_plus) == 1 and y_plus == 1:
            x_temp = x
            y_temp = y - 1
            temp_index = y_temp * WIDTH_NUM + x_temp
            if temp_index in self.screen.obstacle_blocks_index:
                return False
        elif abs(x_plus) == 1 and y_plus == -1:
            x_temp = x
            y_temp = y + 1
            temp_index = y_temp * WIDTH_NUM + x_temp
            if temp_index in self.screen.obstacle_blocks_index:
                return False

        if x < 0 or x >= WIDTH_NUM or y >= HEIGHT_NUM or y < 0:
            return False
        elif index in self.close_list or index in self.screen.obstacle_blocks_index:
            return False
        else:
            return True

    def step(self):
        min_g = 99999
        min_index = -1
        for index in self.open_list:
            g = self.screen.blocks[index].g
            if g < min_g:
                min_g = min_g
                min_index = index
        self.cur_block = min_index
        self.screen.blocks[min_index].set_close()
        self.close_list.append(min_index)
        self.add_open_list(min_index)


def main():
    pygame.init()
    screen = Screen()

    step = 1
    exit = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and step == 1:
                pygame.display.set_caption('click block to set starting block')
                click_x, click_y = pygame.mouse.get_pos()
                screen.set_start(click_x, click_y)
                step = 2
            elif event.type == pygame.MOUSEBUTTONDOWN and step == 2:
                pygame.display.set_caption(
                    'click block to set obstacle blocks, press enter to next step')
                click_x, click_y = pygame.mouse.get_pos()
                screen.set_obstacle(click_x, click_y)
            elif event.type == pygame.MOUSEBUTTONDOWN and step == 3:
                pygame.display.set_caption(
                    'click block to set finishing block')
                click_x, click_y = pygame.mouse.get_pos()
                screen.set_end(click_x, click_y)
                exit = True
            elif event.type == locals.KEYUP and event.key == locals.K_SPACE:
                step = 3
            elif event.type == locals.QUIT or (event.type == locals.KEYUP and event.key == locals.K_ESCAPE):
                pygame.quit()
                sys.exit()
        screen.draw()
        pygame.display.flip()
        if exit:
            break

    search = A_star(screen)
    while True:
        for event in pygame.event.get():
            if event.type == locals.QUIT or (event.type == locals.KEYUP and event.key == locals.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == locals.KEYUP and event.key == locals.K_SPACE:
                search.step()
        screen.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
