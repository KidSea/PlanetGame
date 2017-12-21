#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

from pygame.sprite import  Sprite

class Alien(Sprite):
    """外星人类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人的图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #外星人最初的位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外形人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rec = self.screen.get_rect()
        if self.rect.right >= screen_rec.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x