#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class GameStates():
    """跟踪游戏信息"""

    def __init__(self, ai_settings):
        """初始化"""
        self.ai_settings = ai_settings
        self.reset_states()

        self.game_active = False

    def reset_states(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit