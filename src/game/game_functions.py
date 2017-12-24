#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) <= ai_settings.bullet_allow_total:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_button(states, button, mouse_x, mouse_y):
    if button.rect.collidepoint(mouse_x, mouse_y):
        states.game_active = True

def check_events(ai_settings, screen, states, button,  ship, bullets):

    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_button(states, button, mouse_x, mouse_y)

def update_screen(ai_settings, screen, ship, aliens, bullets, button, states):
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    if not states.game_active:
        button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bulltes):
    collisions = pygame.sprite.groupcollide(bulltes, aliens, True, True)

    if len(aliens) == 0:
        bulltes.empty()
        create_fleet(ai_settings, screen, aliens, ship)


def update_bullets(ai_settings, screen, ship, bulltes, aliens):
    bulltes.update()
    for bullte in bulltes.copy():
        if bullte.rect.bottom <= 0:
            bulltes.remove(bullte)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bulltes)


def create_fleet(ai_settings, screen, aliens, ship):
    """创建外星人群"""
    # 创建一个人外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度

    alien = Alien(ai_settings, screen)


    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    row_number = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #创建第一行外星人
    for row_number in range(row_number):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return  number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星人并将其加入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘采取对应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, states, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if states.ships_left > 0:
        # 将ships_left减1
        states.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人,并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        states.game_active = False

def check_aliens_bottom(ai_settings, states, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #类似飞船碰撞处理
            ship_hit(ai_settings, states, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings, states, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测飞船和外星人之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, states, screen, ship, aliens, bullets)
        print ("Ship hit !!!!")
        # sys.exit()

    check_aliens_bottom(ai_settings, states, screen, ship, aliens, bullets)