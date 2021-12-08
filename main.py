import pygame
from pixels_grph import *
import math as m
import pygame.freetype
from pygame.draw import *
from random import randint
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
black = (0, 0, 0)
screen = pygame.display.set_mode((1200, 600))
screen_width = 40
screen_height = 20

GAME_FONT = pygame.freetype.Font(None, 20)
GAME_FONT_1 = pygame.freetype.Font(None, 36)
pixel_size = 30

def mapping(pixels):
    for pixel_num, pixel in enumerate(pixels):
        x_screen = pixel_num % screen_width + screen_width / 2
        z_screen = pixel_num // screen_width + screen_height / 2
        rect(screen, pixel, (x_screen * pixel_size - 600, z_screen * pixel_size - 300, pixel_size, pixel_size))
        pygame.display.update()
        #blacked = (0, 0, 0)
        #screen.fill(blacked)




finished = False
sphere_cor = [0, 400, 0]
source_cor = [400, 400, 0]
while not finished:
    clock.tick(30)

    #rint(sphere_cor[1])
    mapping(out_scr(sphere_cor, source_cor))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                sphere_cor[1] += 5
            elif event.key == pygame.K_s:
                sphere_cor[1] -= 5
        if event.type == pygame.QUIT:
            finished = True
    sphere_cor[1] -= 0
    source_cor[1] += 0
    print(source_cor[1])
pygame.quit()
