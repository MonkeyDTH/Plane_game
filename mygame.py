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


def text_mid(text, screen, width, height, language='eng'):
    if language == 'eng':
        my_font = pygame.font.Font('./resource/LT_55869.TTF', 70)
        text_surface = my_font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (width / 2 - len(text) * 20, height / 2 - 120))
    elif language == 'chs':  # chinese
        my_font = pygame.font.Font('./resource/FZShenYMXSJW.TTF', 40)
        text_surface = my_font.render("玩这么久，休息一会吧！", True, (255, 255, 255))
        screen.blit(text_surface, (width / 2 - len(text) * 20, height / 2 - 120))
    else:
        pass


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

    # set background music and sound effect
    pygame.mixer.init()
    sound_effect = pygame.mixer.Sound("./resource/hit.wav")
    pygame.mixer.music.load("./resource/brave_heart.mp3")
    pygame.mixer.music.play(-1)

    # load image
    bkg_img = pygame.image.load(bkg_img_fname).convert()
    plane_img = pygame.image.load(plane_fname).convert_alpha()
    bullet_img = pygame.image.load(bullet_fname).convert_alpha()
    monster_img = pygame.image.load(monster_fname).convert_alpha()

    bullet_list = []
    monster_list = []
    score = 0
    num = 0
    pause = False

    # main loop
    while True:
        for event in pygame.event.get():
            # QUIT event
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pause = ~pause

        # draw background
        screen.blit(bkg_img, (0, 0))

        # display score
        my_font = pygame.font.Font('./resource/LT_55869.TTF', 40)
        text_surface = my_font.render("score: {0}".format(score), True, (255, 255, 255))
        screen.blit(text_surface, (width_bkg / 2 - 80, height_bkg / 2 - 50))

        # handle pause
        if pause:
            text_mid("Pause!", screen, width_bkg, height_bkg)
            pygame.display.update()
            continue

        # get mouse position
        x, y = pygame.mouse.get_pos()
        # draw mouse cursor img
        x_plane = x - width_plane / 2
        y_plane = y - height_plane / 2
        plane = Plane(x_plane, y_plane, width_plane, height_plane)
        # plane crash
        for monster in monster_list:
            if plane.touch(monster):  # game over
                text_mid("Game Over!", screen, width_bkg, height_bkg)
                pygame.display.update()
                time.sleep(2)
                exit()
        screen.blit(plane_img, (x_plane, y_plane))

        # bullet fire control
        if num % 150 == 0:
            bullet_list.append(Bullet(x, y - 80, width_bullet, height_bullet))
        # monster appear rate
        if random.randint(0, 300) == num % 300:
            monster_list.append(Monster(random.randint(0, width_bkg-width_monster), 0, width_monster, height_monster))

        # draw bullet
        for bullet in bullet_list:
            screen.blit(bullet_img, (bullet.leftUp.x, bullet.leftUp.y))
            bullet.move(1)
            # destroy monster
            for monster in monster_list:
                if monster.touch(bullet):
                    score += 1
                    sound_effect.play()
                    monster_list.remove(monster)
                    bullet_list.remove(bullet)
                    break

        # draw monster
        for monster in monster_list:
            screen.blit(monster_img, (monster.leftUp.x, monster.leftUp.y))
            if num % 2 == 0:
                monster.move(1)

        # count time and rest
        num += 1
        if num == 10000:
            text_mid("玩这么久，休息一会吧！", screen, width_bkg, height_bkg, language="chs")
            pygame.display.update()
            time.sleep(2)
            exit()

        # update window
        pygame.display.update()
        time.sleep(0.001)


if __name__ == "__main__":
    main()
