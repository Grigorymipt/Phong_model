import pygame
import objects
import view
import multiprocessing as mp
import numpy as np
import math as m
from pygame import *
screen = pygame.display.set_mode((1200, 600))
pygame.init()

clock = pygame.time.Clock()

screen_width = 100
screen_height = screen_width // 2
pixel_size = 1200 / screen_width


def out_scr(alpha, sphere_cor, source_cor, floor_cor):
    # source_color:
    source = (255, 255, 255)
    # sphere
    color = (127, 0, 255)
    # floor
    color_fl = (40, 40, 40)
    # walls
    color_w_1 = (20, 20, 150)
    color_w_2 = (20, 150, 20)

    # consts for phong model:
    alpha = 10
    k_a = 0.1
    k_d = 0.9
    k_s = 1

    s_a = [color[i] * k_a for i in range(3)]
    s_s = [source[i] * k_s for i in range(3)]
    s_d = [color[i] * k_d for i in range(3)]

    f_a = [color_fl[i] * k_a for i in range(3)]
    f_s = [source[i] * k_s for i in range(3)]
    f_d = [color_fl[i] * k_d for i in range(3)]

    w_1_a = [color_w_1[i] * k_a for i in range(3)]
    w_1_s = [source[i] * k_s for i in range(3)]
    w_1_d = [color_w_1[i] * k_d for i in range(3)]

    w_2_a = [color_w_2[i] * k_a for i in range(3)]
    w_2_s = [source[i] * k_s for i in range(3)]
    w_2_d = [color_w_2[i] * k_d for i in range(3)]

    # s_a = k_a * i_a e.t.c.

    # rays:
    rays = [0, 0, 0] * screen_height * screen_width
    col_rays = [0, 0, 0] * screen_height * screen_width
    i = 0

    # intersection for objects:

    c = (sphere_cor[0] ** 2 + sphere_cor[1] ** 2 + sphere_cor[2] ** 2) ** 0.5
    c_vec = sphere_cor
    num = 0

    # calculations for any rays
    for num in range(screen_width * screen_height):
        x = float(num % screen_width - screen_width / 2)
        y = float((screen_width / 2))
        z = float(num // screen_width + screen_height / 2 - screen_height)
        des = [x / (x ** 2 + y ** 2 + z ** 2) ** 0.5, y / (x ** 2 + y ** 2 + z ** 2) ** 0.5,
               z / (x ** 2 + y ** 2 + z ** 2) ** 0.5]
        rays[num] = np.array(des)

        rays[num] = turn_hor_cam(rays[num], al, be)
        d_vec = rays[num]
        d = (d_vec[0] ** 2 + d_vec[1] ** 2 + d_vec[2] ** 2) ** 0.5
        c_d = ((c_vec[0] * d_vec[0]) + (c_vec[1] * d_vec[1]) + (c_vec[2] * d_vec[2]))

        sphere = objects.make_sphere_with_lines(sphere_cor, c, r, rays[num])
        t_min = sphere[0]
        n_vec = sphere[1]
        color = sphere[2]
        if t_min == - 1:
            floor = objects.make_floor(rays[num], h, a, b, delta)
            t_min = floor[0]
            n_vec = floor[1]
            color = floor[2]
            if t_min == - 1:
                wall_1 = objects.make_room(rays[num], h, a, b, delta)
                t_min = wall_1[0]
                n_vec = wall_1[1]
                color = wall_1[2]
                if t_min == -1:
                    col_rays[num] = [100, 150, 250]
                else:
                    col_rays[num] = objects.phong_model(t_min, d_vec, d, n_vec, source_cor, [s_a, s_d, s_s, alpha],
                                                        color)
            else:
                col_rays[num] = objects.phong_model(t_min, d_vec, d, n_vec, source_cor, [s_a, s_d, s_s, alpha], color)
        else:
            col_rays[num] = objects.phong_model(t_min, d_vec, d, n_vec, source_cor, [s_a, s_d, s_s, alpha], color)

    return col_rays



def turn_hor_cam(ray_cor, al, be):
    r_hor = (ray_cor[0] ** 2 + ray_cor[1] ** 2) ** 0.5
    if ray_cor[1] == 0 and ray_cor[2] > 0:
        phi = float(m.pi / 2)
    elif ray_cor[1] == 0 and ray_cor[2] < 0:
        phi = float(-m.pi / 2)
    else:
        phi = float(m.atan(ray_cor[0] / ray_cor[1]))
    ray_cor = [float(m.sin(phi + al)), float(1 * m.cos(phi + al)), float(1 * ray_cor[2])]
    """
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
    """
    return ray_cor


finished = False

t = 7.5 * m.pi / 4
rad = 300
delta = [0, 0, 0]
global r, fire, al, be
al = 0
be = 0
fire = False
r = 100
a = 500
b = 1000
h = 100
f_button = False
pygame.mouse.set_visible(False)

while not finished:
    clock.tick(30)
    sphere_cor = [100 + delta[0], 400 + delta[1], 0 + delta[2]]
    source_cor = [objects.make_x(t, rad) + delta[0], 0 + objects.make_y(t, rad) + delta[1], -100 + delta[2]]
    #source_cor = [0, 0, -200]
    #source_cor = [200, 200, 0]
    floor_cor = [0 + delta[0], 0 + delta[1], 100 + delta[2]]
    view.mapping(out_scr(al, sphere_cor, source_cor, floor_cor), screen_width, screen_height, pixel_size, screen)

    # interface:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                delta[1] -= 20

            elif event.key == pygame.K_s:
                delta[1] += 20

            if event.key == pygame.K_d:
                delta[0] -= 20

            elif event.key == pygame.K_a:
                delta[0] += 20
            if event.key == pygame.K_p:
                finished = True
            if event.key == pygame.K_p:
                fire = True
            if event.key == pygame.K_g:
                f_button = True
        if event.type == pygame.QUIT:
            finished = True
        global pos
        pos = [600, 300]
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            k = 0.002
            al += k * (pos[0] - 600)
            be += k * (pos[1] - 300)
            pygame.mouse.set_pos(600, 300)

    objects.floor_lift([0, 0], [50, 50], delta, f_button)
    sphere_cor[1] -= 0
    source_cor[1] += 0
    t += 0.1
pygame.quit()
