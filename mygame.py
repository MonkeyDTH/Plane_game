#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 15:59
# @Author  : TH
# @Site    : 
# @File    : mygame.py
# @Software: PyCharm
"""
"""
import pygame
import cv2
from sys import exit
from pygame.locals import *


def load_img_shape(img_fname):
    bkg_img = cv2.imread(img_fname)
    return bkg_img.shape[1], bkg_img.shape[0]


def main():
    bkg_img_fname = './resource/background.jpg'
    object_fname = './resource/plane.png'

    # load bkg img shape
    width, height = load_img_shape(bkg_img_fname)

    pygame.init()
    # create a window
    screen = pygame.display.set_mode((width, height), 0, 32)
    # set title
    pygame.display.set_caption("TH game!")

    # load image
    background = pygame.image.load(bkg_img_fname).convert()
    mouse_cursor = pygame.image.load(object_fname).convert_alpha()

    # main loop
    while True:
        for event in pygame.event.get():
            # QUIT event
            if event.type == QUIT:
                exit()

        # draw background
        screen.blit(background, (0, 0))

        # get mouse position
        x, y = pygame.mouse.get_pos()
        # draw mouse cursor img
        x -= mouse_cursor.get_width() / 2
        y -= mouse_cursor.get_height() / 2
        screen.blit(mouse_cursor, (x, y))

        # update window
        pygame.display.update()


if __name__ == "__main__":
    main()