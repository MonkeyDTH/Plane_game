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
import time
import random
from sys import exit
from pygame.locals import *


def load_img_shape(img_fname):
    bkg_img = cv2.imread(img_fname)
    return bkg_img.shape[1], bkg_img.shape[0]


def main():
    bkg_img_fname = './resource/background.jpg'
    plane_fname = './resource/space-rocket.png'
    bullet_fname = './resource/github.png'
    monster_fname = './resource/snowman.png'

    # load img shape
    width_bkg, height_bkg = load_img_shape(bkg_img_fname)
    width_bullet, height_bullet = load_img_shape(bullet_fname)
    width_monster, height_monster = load_img_shape(monster_fname)

    pygame.init()
    # create a window
    screen = pygame.display.set_mode((width_bkg, height_bkg), 0, 32)
    # set title
    pygame.display.set_caption("TH game!")

    # load image
    background = pygame.image.load(bkg_img_fname).convert()
    mouse_cursor = pygame.image.load(plane_fname).convert_alpha()
    bullet = pygame.image.load(bullet_fname).convert_alpha()
    monster = pygame.image.load(monster_fname).convert_alpha()

    bullet_list = []
    monster_list = []
    num = 0

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
        x_plane = x - mouse_cursor.get_width() / 2
        y_plane = y - mouse_cursor.get_height() / 2
        screen.blit(mouse_cursor, (x_plane, y_plane))

        # bullet fire rate
        if num % 250 == 100:
            bullet_list.append([x, y - 80])
        # monster appear rate
        if num == 500:
            num = 0
            monster_list.append([random.randint(0, width_bkg - 64), 0])

        # draw bullet
        for i in range(len(bullet_list)):
            screen.blit(bullet, (bullet_list[i][0], bullet_list[i][1]))
            bullet_list[i][1] -= 1

        # compute monster disappear

        # draw monster
        for i in range(len(monster_list)):
            screen.blit(monster, (monster_list[i][0], monster_list[i][1]))
            if num % 2 == 0:
                monster_list[i][1] += 1

        # update window
        pygame.display.update()
        num += 1
        time.sleep(0.001)


if __name__ == "__main__":
    main()
