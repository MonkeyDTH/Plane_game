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
from common_types import Bullet, Monster, Plane


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
    width_plane, height_plane = load_img_shape(plane_fname)
    width_bullet, height_bullet = load_img_shape(bullet_fname)
    width_monster, height_monster = load_img_shape(monster_fname)

    pygame.init()
    # create a window
    screen = pygame.display.set_mode((width_bkg, height_bkg), 0, 32)
    # set title
    pygame.display.set_caption("TH game!")

    # load image
    bkg_img = pygame.image.load(bkg_img_fname).convert()
    plane_img = pygame.image.load(plane_fname).convert_alpha()
    bullet_img = pygame.image.load(bullet_fname).convert_alpha()
    monster_img = pygame.image.load(monster_fname).convert_alpha()

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
        screen.blit(bkg_img, (0, 0))

        # get mouse position
        x, y = pygame.mouse.get_pos()
        # draw mouse cursor img
        x_plane = x - width_plane / 2
        y_plane = y - height_plane / 2
        plane = Plane(x_plane, y_plane, width_plane, height_plane)
        # plane crash
        for monster in monster_list:
            if plane.touch(monster):
                exit()
        screen.blit(plane_img, (x_plane, y_plane))

        # bullet fire control
        if num % 150 == 0:
            bullet_list.append(Bullet(x, y - 80, width_bullet, height_bullet))
        # monster appear rate
        if random.randint(0, 500) == num:
            monster_list.append(Monster(random.randint(0, width_bkg-width_monster), 0, width_monster, height_monster))

        # draw bullet
        for bullet in bullet_list:
            screen.blit(bullet_img, (bullet.leftUp.x, bullet.leftUp.y))
            bullet.move(1)
            # destroy monster
            for monster in monster_list:
                if monster.touch(bullet):
                    monster_list.remove(monster)

        # draw monster
        for monster in monster_list:
            screen.blit(monster_img, (monster.leftUp.x, monster.leftUp.y))
            if num % 2 == 0:
                monster.move(1)

        # update window
        pygame.display.update()
        num += 1
        if num == 500:
            num = 0
        time.sleep(0.001)


if __name__ == "__main__":
    main()
