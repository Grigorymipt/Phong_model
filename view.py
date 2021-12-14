import math as m
import pygame
from pygame.draw import *
import pygame.freetype
pygame.font.init()
pygame.init()
black = (0, 0, 0)
screen = pygame.display.set_mode((1200, 600))

GAME_FONT = pygame.freetype.Font(None, 20)
GAME_FONT_1 = pygame.freetype.Font(None, 36)

"""
def turn_hor_cam(ray_cor, al, be):
    r_hor = (ray_cor[0] ** 2 + ray_cor[1] ** 2) ** 0.5
    if ray_cor[1] == 0 and ray_cor[2] > 0:
        phi = (m.pi / 2)
    elif ray_cor[1] == 0 and ray_cor[2] < 0:
        phi = -m.pi / 2
    else:
        phi = m.atan(ray_cor[0] / ray_cor[1])
    ray_cor = [m.sin(phi + al), 1 * m.cos(phi + al), ray_cor[2]]
    
    r_ver = (ray_cor[2] ** 2 + ray_cor[1] ** 2) ** 0.5
    if ray_cor[1] == 0 and ray_cor[0] > 0:
        phi = m.pi / 2
    elif ray_cor[1] == 0 and ray_cor[0] < 0:
        phi = -m.pi / 2
    elif ray_cor[1] > 0:
        phi = m.atan(ray_cor[2] / ray_cor[1])
    else:
        phi = m.pi + m.atan(ray_cor[2] / ray_cor[1])
    ray_cor = [ray_cor[0], r_ver * m.cos(phi + be), r_ver * m.sin(phi + be)]
    
    
    return ray_cor
"""


def mapping(pixels, screen_width, screen_height, pixel_size, screen):
    for pixel_num, pixel in enumerate(pixels):
        x_screen = pixel_num % screen_width + screen_width / 2
        z_screen = pixel_num // screen_width + screen_height / 2
        rect(screen, pixel, (x_screen * pixel_size - 600, z_screen * pixel_size - 300, pixel_size, pixel_size))
    pygame.display.update()