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


def text_display(text, screen, x, y, size=70, language='eng'):
    if language == 'eng':
        my_font = pygame.font.Font('./resource/LT_55869.TTF', size)
    elif language == 'chs':  # chinese
        my_font = pygame.font.Font('./resource/FZShenYMXSJW.TTF', size)
    text_surface = my_font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))


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

    # init params
    bullet_list = []
    monster_list = []
    score = 0
    num = 0
    level = 0
    level_start = True
    pause = False
    fps = 1000

    fcclock = pygame.time.Clock()  # 创建一个时间对象

    # start game
    text_display("TH Game", screen, width_bkg // 2 - 140, height_bkg // 2 - 60)
    pygame.display.update()
    time.sleep(2)
    screen.blit(bkg_img, (0, 0))

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

        # count time and level up
        if num == 7000:
            if level == 10:  # top level
                text_display("玩这么久，休息一会吧！", screen,
                             width_bkg // 2 - 200, height_bkg // 2 - 20, size=40, language="chs")
                pygame.display.update()
                time.sleep(2)
                exit()
            if score >= (level + 1) * (15 + level):  # level up
                level += 1
                level_start = True
                num = 0
                bullet_list = []
                monster_list = []
                screen.blit(bkg_img, (0, 0))
                text_display("Level Up！", screen, width_bkg // 2 - 150, height_bkg // 2 - 120)
                pygame.display.update()
                time.sleep(2)
                continue
            else:  # can't pass the level
                text_display("Time Over！", screen, width_bkg // 2 - 180, height_bkg // 2 - 120)
                pygame.display.update()
                time.sleep(2)
                screen.blit(bkg_img, (0, 0))
                text_display("Game Over!", screen, width_bkg // 2 - 200, height_bkg // 2 - 120)
                pygame.display.update()
                time.sleep(2)
                exit()

        # display level
        if level_start:
            text_display("Level {0}".format(level), screen, width_bkg // 2 - 130, height_bkg // 2 - 120)
            pygame.display.update()
            time.sleep(1.5)
            level_start = False

        # display score
        text_display("score: {0:3d}".format(score), screen, width_bkg / 2 - 100, height_bkg / 2 - 50, size=40)

        # handle pause
        if pause:
            text_display("Pause!", screen, width_bkg // 2 - 105, height_bkg // 2 - 120)
            pygame.display.update()
            continue

        # get mouse position
        if num <= 100:
            x, y = width_bkg / 2 - width_plane / 2, height_bkg - height_plane
        else:
            x, y = pygame.mouse.get_pos()
            # handle border
            x = max(x, width_plane // 2)
            x = min(x, width_bkg - width_plane // 2)
            y = max(y, height_plane // 2)
            y = min(y, height_bkg - height_plane // 2)
            # draw mouse cursor img
            x_plane = x - width_plane / 2
            y_plane = y - height_plane / 2
            plane = Plane(x_plane, y_plane, width_plane, height_plane)
            # plane crash
            for monster in monster_list:
                if plane.touch(monster):  # game over
                    text_display("Game Over!", screen, width_bkg // 2 - 200, height_bkg // 2 - 120)
                    pygame.display.update()
                    time.sleep(2)
                    exit()
            screen.blit(plane_img, (x_plane, y_plane))

        # bullet fire control
        base_speed = 150
        bullet_speed = int(base_speed * (1 - level * 0.1))
        if bullet_speed <= 0:
            bullet_speed = 10
        if num % bullet_speed == 0:
            bullet_list.append(Bullet(x - width_bullet / 2, y - height_bullet / 2, width_bullet, height_bullet))
        # monster appear control
        monster_speed = int(bullet_speed * (1.8 - level * 0.15))
        if random.randint(0, monster_speed) == num % monster_speed:
            monster_list.append(Monster(random.randint(0, width_bkg-width_monster), 0, width_monster, height_monster))

        # draw bullet
        for bullet in bullet_list:
            screen.blit(bullet_img, (bullet.leftUp.x, bullet.leftUp.y))
            bullet.move(2)
            # destroy monster
            for monster in monster_list:
                if monster.leftUp.y > 50 and monster.touch(bullet):
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

        # count time and level up
        num += 1

        # update window
        fcclock.tick(fps)
        pygame.display.update()
        # time.sleep(0.001)


if __name__ == "__main__":
    main()
