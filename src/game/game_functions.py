#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame

from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) <= ai_settings.bullet_allow_total:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False



def check_events(ai_settings, screen, ship, bullets):

    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def update_screen(ai_settings, screen, ship, bullets):

    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bulltes):
    bulltes.update()
    for bullte in bulltes.copy():
        if bullte.rect.bottom <= 0:
            bulltes.remove(bullte)