#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings, screen)
    alien = Alien(ai_settings, screen)
    #创建子弹存储数组
    bullets = Group()
    #创建外星人编组
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_aliens(ai_settings, aliens)
        gf.update_bullets(bullets, aliens)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()