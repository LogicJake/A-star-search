# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-06 16:52:35
# @Last Modified time: 2019-01-07 12:30:27
import pygame
import sys
from pygame import locals
from screen import Screen
from search import A_star


def main():
    pygame.init()
    screen = Screen()

    step = 1
    exit = False
    pygame.display.set_caption('click block to set starting block')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and step == 1:
                click_x, click_y = pygame.mouse.get_pos()
                screen.set_start(click_x, click_y)
                step = 2
                pygame.display.set_caption(
                    'click block to set obstacle blocks, press enter to next step')
            elif event.type == pygame.MOUSEBUTTONDOWN and step == 2:
                click_x, click_y = pygame.mouse.get_pos()
                screen.set_obstacle(click_x, click_y)
            elif event.type == pygame.MOUSEBUTTONDOWN and step == 3:
                click_x, click_y = pygame.mouse.get_pos()
                exit = screen.set_end(click_x, click_y)
                # exit = True
            elif event.type == locals.KEYUP and event.key == locals.K_SPACE and step == 2:
                step = 3
                pygame.display.set_caption(
                    'click block to set finishing block')
            elif event.type == locals.QUIT or (event.type == locals.KEYUP and event.key == locals.K_ESCAPE):
                pygame.quit()
                sys.exit()
        screen.draw()
        pygame.display.flip()
        if exit:
            break

    pygame.display.set_caption('press space to step the search')

    search = A_star(screen)
    while True:
        for event in pygame.event.get():
            if event.type == locals.QUIT or (event.type == locals.KEYUP and event.key == locals.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == locals.KEYUP and event.key == locals.K_SPACE and not search.over:
                search.step()
        screen.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
