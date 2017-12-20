#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame

def check_events(ship):

    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
              #向右移动飞船
              ship.moving_right = True

            if event.key == pygame.K_LEFT:
                ship.moving_left = True

        elif event.type == pygame.KEYUP:
              if event.key == pygame.K_RIGHT:
                  ship.moving_right = False

              elif event.key == pygame.K_LEFT:
                  ship.moving_left = False

def update_screen(ai_settings, screen, ship):

    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # 让最近绘制的屏幕可见
    pygame.display.flip()