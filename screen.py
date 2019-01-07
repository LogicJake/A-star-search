# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-07 12:12:05
# @Last Modified time: 2019-01-07 12:30:08
import pygame
from block import Block
from block import WIDTH_NUM, HEIGHT_NUM, BLOCK_SIZE


SCREEN_WIDTH = WIDTH_NUM * BLOCK_SIZE
SCREEN_HEIGHT = HEIGHT_NUM * BLOCK_SIZE


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
        if self.blocks[block_index].set_obstacle():
            self.obstacle_blocks_index.append(block_index)

    def set_end(self, click_x, click_y):
        block_index = self.get_click_block_index(click_x, click_y)
        if self.blocks[block_index].set_end():
            self.end_block_index = block_index
            return True
        else:
            return False
