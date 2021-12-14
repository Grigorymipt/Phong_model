import pygame
import objects
import multiprocessing as mp
# from pixels_grph import *
import numpy as np
import math as m
import pygame.freetype
from pygame.draw import *
from random import randint

from numba import *
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
black = (0, 0, 0)
screen = pygame.display.set_mode((1200, 600))
screen_width = 100
screen_height = screen_width // 2

# Use Numba to get better results


GAME_FONT = pygame.freetype.Font(None, 20)
GAME_FONT_1 = pygame.freetype.Font(None, 36)
pixel_size = 1200 / screen_width


# @njit(fastmath=True, cache=True,parallel=True)

class sphere:
    def __int__(self, color, k_a, k_d, k_s, cor):
        self.color = color
        self.k_a = k_a
        self.k_d = k_d
        self.k_s = k_s
        self.cor = cor

    def move(cor, dcor):
        cor = [cor[i] + dcor[i] for i in range(3)]
        return cor


class floor:
    def __int__(self, color, k_a, k_d, k_s, cor):
        self.color = color
        self.k_a = k_a
        self.k_d = k_d
        self.k_s = k_s
        self.cor = cor

    def move(cor, dcor):
        cor = [cor[i] + dcor[i] for i in range(3)]
        return cor

#@jit
def out_scr(alpha, sphere_cor, source_cor, floor_cor):
    # screen_width = 40
    # screen_height = 20
    # pixel_size = 30
    # source:
    source = (255, 255, 255)
    # source_cor = [100, 200, 0]

    # sphere:
    # sphere_cor = [0, 150, 0]

    color = (127, 0, 255)
    color_fl = (40, 40, 40)
    color_w_1 = (20, 20, 150)
    color_w_2 = (20, 150, 20)
    #objects = [sphere_cor, r]
    alpha = 10  # here mustn't be numbers like: 2*n, n in N
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
    death_length = 10000

    rays = [0, 0, 0] * screen_height * screen_width
    col_rays = [0, 0, 0] * screen_height * screen_width
    i = 0

    while i < screen_width * screen_height:
        x = float(i % screen_width - screen_width / 2)
        y = float((screen_width / 2))
        z = float(i // screen_width + screen_height / 2 - screen_height)
        des = [x / (x ** 2 + y ** 2 + z ** 2) ** 0.5, y / (x ** 2 + y ** 2 + z ** 2) ** 0.5, z / (x ** 2 + y ** 2 + z ** 2) ** 0.5]
        rays[i] = np.array(des)
        i += 1
    i = 0

    # intersection for sphere:
    imk = 0
    while imk == 0:  # stupid FIXME
        c = (sphere_cor[0] ** 2 + sphere_cor[1] ** 2 + sphere_cor[2] ** 2) ** 0.5
        c_vec = sphere_cor
        num = 0

        while num < screen_width * screen_height:
            rays[num] = turn_hor_cam(rays[num], al, be)
            d_vec = rays[num]
            d = (d_vec[0] ** 2 + d_vec[1] ** 2 + d_vec[2] ** 2) ** 0.5
            c_d = ((c_vec[0] * d_vec[0]) + (c_vec[1] * d_vec[1]) + (c_vec[2] * d_vec[2]))
            # c_d_mod = (c_d[1] ** 2 + c_d[1] ** 2 + c_d[2] ** 2) ** 0.5
            cos_angle_c_d = c_d / (d * c)
            global r
            if (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) >= 0 and (c_d - d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2 > 0:

                t_1 = (c_d - d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2
                #t_2 = (c_d + d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2

                # here we choose t_1 cause it's the nearest.
                # FIXME
                # should be smth about back mapping, but i'm very lazy.
                # Phong reflection:
                # Intensity (RGB):

                l_vec = [source_cor[i] - t_1 * d_vec[i] for i in range(3)]
                n_vec = [t_1 * d_vec[i] - sphere_cor[i] for i in range(3)]
                n = ((n_vec[0]) ** 2 + (n_vec[1]) ** 2 + (n_vec[2]) ** 2) ** 0.5
                l_n = l_vec[0] * n_vec[0] + l_vec[1] * n_vec[1] + l_vec[2] * n_vec[2]

                cos_l_n = l_n / ((l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5 * (
                            n_vec[0] ** 2 + n_vec[1] ** 2 + n_vec[2] ** 2) ** 0.5)

                r_vec = [2 * cos_l_n * n_vec[i] / n - l_vec[i] / (l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5
                         for i in range(3)]
                v_vec = [-d_vec[i] / d for i in range(3)]
                r_v = r_vec[0] * v_vec[0] + r_vec[1] * v_vec[1] + r_vec[2] * v_vec[2]
                cos_r_v = r_v
                if cos_r_v < 0:
                    cos_r_v = 0
                if cos_l_n <= 0:
                    col_rays[num] = [s_a[i] for i in range(3)]
                else:
                    col_rays[num] = [1 * s_a[i] + s_d[i] * cos_l_n + s_s[i] * cos_r_v ** alpha for i in range(3)]
                    if col_rays[num][0] >= 255:
                        col_rays[num][0] = 255
                    if col_rays[num][1] >= 255:
                        col_rays[num][1] = 255
                    if col_rays[num][2] >= 255:
                        col_rays[num][2] = 255
                    if col_rays[num][0] <= 0:
                        col_rays[num][0] = 0
                    if col_rays[num][1] <= 0:
                        col_rays[num][1] = 0
                    if col_rays[num][2] <= 0:
                        col_rays[num][2] = 0

            elif rays[num][2] > 0 \
                    and rays[num][0] / ((rays[num][2]**2 + rays[num][0]**2))**0.5 <= ((a-delta[0])**2 / ((a-delta[0])**2 + (h + delta[2])**2))**0.5 \
                    and rays[num][1] / ((rays[num][2]**2 + rays[num][1]**2))**0.5 <= ((b-delta[1])**2 / ((b-delta[1])**2 + (h + delta[2])**2))**0.5\
                    and rays[num][0] / ((rays[num][2]**2 + rays[num][0]**2))**0.5 >= -((a+delta[0])**2 / ((a+delta[0])**2 + (h + delta[2])**2))**0.5 \
                    and rays[num][1] / ((rays[num][2]**2 + rays[num][1]**2))**0.5 >= -((b+delta[1])**2 / ((b+delta[1])**2 + (h + delta[2])**2))**0.5:
                t_3 = (100**2 * ((rays[num][0])**2 + (rays[num][1])**2 + (rays[num][0])**2) / rays[num][2]**2)**0.5

                l_vec = [source_cor[i] - t_3 * d_vec[i] for i in range(3)]
                n_vec = [0, 0, -1]
                n = ((n_vec[0]) ** 2 + (n_vec[1]) ** 2 + (n_vec[2]) ** 2) ** 0.5
                l_n = l_vec[0] * n_vec[0] + l_vec[1] * n_vec[1] + l_vec[2] * n_vec[2]

                cos_l_n = l_n / ((l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5 * (
                        n_vec[0] ** 2 + n_vec[1] ** 2 + n_vec[2] ** 2) ** 0.5)

                r_vec = [2 * cos_l_n * n_vec[i] / n - l_vec[i] / (l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5
                         for i in range(3)]
                v_vec = [-d_vec[i] / d for i in range(3)]
                r_v = r_vec[0] * v_vec[0] + r_vec[1] * v_vec[1] + r_vec[2] * v_vec[2]
                cos_r_v = r_v
                if cos_r_v < 0:
                    cos_r_v = 0
                if cos_l_n <= 0:
                    col_rays[num] = [0, 0, 0]
                else:
                    col_rays[num] = [1 * f_a[i] + f_d[i] * cos_l_n + f_s[i] * cos_r_v ** alpha for i in range(3)]
                    if col_rays[num][0] >= 255:
                        col_rays[num][0] = 255
                    if col_rays[num][1] >= 255:
                        col_rays[num][1] = 255
                    if col_rays[num][2] >= 255:
                        col_rays[num][2] = 255
                    if col_rays[num][0] <= 0:
                        col_rays[num][0] = 0
                    if col_rays[num][1] <= 0:
                        col_rays[num][1] = 0
                    if col_rays[num][2] <= 0:
                        col_rays[num][2] = 0

            # walls:
            elif rays[num][1] > 0 and (rays[num][0]**2 / (rays[num][1]**2 + rays[num][0]**2))**0.5 <= (1/5)**0.5 and (rays[num][2]**2 / (rays[num][1]**2 + rays[num][2]**2))**0.5 <= ((a-delta[0])**2 / ((a-delta[0])**2 + (h + delta[2])**2))**0.5:
                t_3 = (500**2 * ((rays[num][0])**2 + (rays[num][1])**2 + (rays[num][0])**2) / rays[num][1]**2)**0.5

                l_vec = [source_cor[i] - t_3 * d_vec[i] for i in range(3)]
                n_vec = [0, -1, 0]
                n = ((n_vec[0]) ** 2 + (n_vec[1]) ** 2 + (n_vec[2]) ** 2) ** 0.5
                l_n = l_vec[0] * n_vec[0] + l_vec[1] * n_vec[1] + l_vec[2] * n_vec[2]

                cos_l_n = l_n / ((l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5 * (
                        n_vec[0] ** 2 + n_vec[1] ** 2 + n_vec[2] ** 2) ** 0.5)

                r_vec = [2 * cos_l_n * n_vec[i] / n - l_vec[i] / (l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5
                         for i in range(3)]
                v_vec = [-d_vec[i] / d for i in range(3)]
                r_v = r_vec[0] * v_vec[0] + r_vec[1] * v_vec[1] + r_vec[2] * v_vec[2]
                cos_r_v = r_v
                if cos_r_v < 0:
                    cos_r_v = 0
                if cos_l_n <= 0:
                    col_rays[num] = [0, 0, 0]
                else:

                    col_rays[num] = [1 * w_1_a[i] + w_1_d[i] * cos_l_n + 0*w_1_s[i] * cos_r_v ** alpha for i in range(3)]
                    if col_rays[num][0] >= 255:
                        col_rays[num][0] = 255
                    if col_rays[num][1] >= 255:
                        col_rays[num][1] = 255
                    if col_rays[num][2] >= 255:
                        col_rays[num][2] = 255
                    if col_rays[num][0] <= 0:
                        col_rays[num][0] = 0
                    if col_rays[num][1] <= 0:
                        col_rays[num][1] = 0
                    if col_rays[num][2] <= 0:
                        col_rays[num][2] = 0

            elif rays[num][1] < 0 and (rays[num][0]**2 / (rays[num][1]**2 + rays[num][0]**2))**0.5 <= (1/5)**0.5 and (rays[num][2]**2 / (rays[num][1]**2 + rays[num][2]**2))**0.5 <= ((a-delta[0])**2 / ((a-delta[0])**2 + (h + delta[2])**2))**0.5:
                t_3 = (500**2 * ((rays[num][0])**2 + (rays[num][1])**2 + (rays[num][0])**2) / rays[num][1]**2)**0.5

                l_vec = [source_cor[i] - t_3 * d_vec[i] for i in range(3)]
                n_vec = [0, 1, 0]
                n = ((n_vec[0]) ** 2 + (n_vec[1]) ** 2 + (n_vec[2]) ** 2) ** 0.5
                l_n = l_vec[0] * n_vec[0] + l_vec[1] * n_vec[1] + l_vec[2] * n_vec[2]

                cos_l_n = l_n / ((l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5 * (
                        n_vec[0] ** 2 + n_vec[1] ** 2 + n_vec[2] ** 2) ** 0.5)

                r_vec = [2 * cos_l_n * n_vec[i] / n - l_vec[i] / (l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5
                         for i in range(3)]
                v_vec = [-d_vec[i] / d for i in range(3)]
                r_v = r_vec[0] * v_vec[0] + r_vec[1] * v_vec[1] + r_vec[2] * v_vec[2]
                cos_r_v = r_v
                if cos_r_v < 0:
                    cos_r_v = 0
                if cos_l_n <= 0:
                    col_rays[num] = [0, 0, 0]
                else:
                    col_rays[num] = [1 * w_1_a[i] + w_1_d[i] * cos_l_n + 0*w_1_s[i] * cos_r_v ** alpha for i in range(3)]
                    if col_rays[num][0] >= 255:
                        col_rays[num][0] = 255
                    if col_rays[num][1] >= 255:
                        col_rays[num][1] = 255
                    if col_rays[num][2] >= 255:
                        col_rays[num][2] = 255
                    if col_rays[num][0] <= 0:
                        col_rays[num][0] = 0
                    if col_rays[num][1] <= 0:
                        col_rays[num][1] = 0
                    if col_rays[num][2] <= 0:
                        col_rays[num][2] = 0

            elif rays[num][0] > 0 and (rays[num][1]**2 / (rays[num][0]**2 + rays[num][1]**2))**0.5 <= (4/5)**0.5 and (rays[num][2]**2 / (rays[num][0]**2 + rays[num][2]**2))**0.5 <= ((b-delta[1])**2 / ((b-delta[1])**2 + (h + delta[2])**2))**0.5:
                t_3 = (500**2 * ((rays[num][0])**2 + (rays[num][1])**2 + (rays[num][0])**2) / rays[num][1]**2)**0.5

                l_vec = [source_cor[i] - t_3 * d_vec[i] for i in range(3)]
                n_vec = [-1, 0, 0]
                n = ((n_vec[0]) ** 2 + (n_vec[1]) ** 2 + (n_vec[2]) ** 2) ** 0.5
                l_n = l_vec[0] * n_vec[0] + l_vec[1] * n_vec[1] + l_vec[2] * n_vec[2]

                cos_l_n = l_n / ((l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5 * (
                        n_vec[0] ** 2 + n_vec[1] ** 2 + n_vec[2] ** 2) ** 0.5)

                r_vec = [2 * cos_l_n * n_vec[i] / n - l_vec[i] / (l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5
                         for i in range(3)]
                v_vec = [-d_vec[i] / d for i in range(3)]
                r_v = r_vec[0] * v_vec[0] + r_vec[1] * v_vec[1] + r_vec[2] * v_vec[2]
                cos_r_v = r_v
                if cos_r_v < 0:
                    cos_r_v = 0
                if cos_l_n <= 0:
                    col_rays[num] = [0, 0, 0]
                else:
                    col_rays[num] = [1 * w_2_a[i] + w_2_d[i] * cos_l_n + 0*w_2_s[i] * cos_r_v ** alpha for i in range(3)]
                    if col_rays[num][0] >= 255:
                        col_rays[num][0] = 255
                    if col_rays[num][1] >= 255:
                        col_rays[num][1] = 255
                    if col_rays[num][2] >= 255:
                        col_rays[num][2] = 255
                    if col_rays[num][0] <= 0:
                        col_rays[num][0] = 0
                    if col_rays[num][1] <= 0:
                        col_rays[num][1] = 0
                    if col_rays[num][2] <= 0:
                        col_rays[num][2] = 0

            elif rays[num][0] < 0 and (rays[num][1]**2 / (rays[num][0]**2 + rays[num][1]**2))**0.5 <= (4/5)**0.5 and (rays[num][2]**2 / (rays[num][0]**2 + rays[num][2]**2))**0.5 <= ((b-delta[1])**2 / ((b-delta[1])**2 + (h + delta[2])**2))**0.5:
                t_3 = (500**2 * ((rays[num][0])**2 + (rays[num][1])**2 + (rays[num][0])**2) / rays[num][1]**2)**0.5

                l_vec = [source_cor[i] - t_3 * d_vec[i] for i in range(3)]
                n_vec = [1, 0, 0]
                n = ((n_vec[0]) ** 2 + (n_vec[1]) ** 2 + (n_vec[2]) ** 2) ** 0.5
                l_n = l_vec[0] * n_vec[0] + l_vec[1] * n_vec[1] + l_vec[2] * n_vec[2]

                cos_l_n = l_n / ((l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5 * (
                        n_vec[0] ** 2 + n_vec[1] ** 2 + n_vec[2] ** 2) ** 0.5)

                r_vec = [2 * cos_l_n * n_vec[i] / n - l_vec[i] / (l_vec[0] ** 2 + l_vec[1] ** 2 + l_vec[2] ** 2) ** 0.5
                         for i in range(3)]
                v_vec = [-d_vec[i] / d for i in range(3)]
                r_v = r_vec[0] * v_vec[0] + r_vec[1] * v_vec[1] + r_vec[2] * v_vec[2]
                cos_r_v = r_v
                if cos_r_v < 0:
                    cos_r_v = 0
                if cos_l_n <= 0:
                    col_rays[num] = [0, 0, 0]
                else:
                    col_rays[num] = [1 * w_2_a[i] + w_2_d[i] * cos_l_n + 0*w_2_s[i] * cos_r_v ** alpha for i in range(3)]
                    if col_rays[num][0] >= 255:
                        col_rays[num][0] = 255
                    if col_rays[num][1] >= 255:
                        col_rays[num][1] = 255
                    if col_rays[num][2] >= 255:
                        col_rays[num][2] = 255
                    if col_rays[num][0] <= 0:
                        col_rays[num][0] = 0
                    if col_rays[num][1] <= 0:
                        col_rays[num][1] = 0
                    if col_rays[num][2] <= 0:
                        col_rays[num][2] = 0
            else:
                # pass
                #col_rays[num] = objects.sphere([screen_width, screen_height], [sphere_cor[0], sphere_cor[1], sphere_cor[2], c, color], r, rays[num], al, be, [source_cor[0], source_cor[1], source_cor[2], k_a, k_d, k_s, alpha])
                col_rays[num] = [100, 150, 250]
                # print('inf', d_vec, source_cor, num)
                # print('NOOO', t_1, d_vec, source_cor, num)
            num += 1

    # aim and shoot:

        if col_rays[screen_width * screen_height // 2 + screen_width // 2 - 1][0] + col_rays[(screen_width - 0) * screen_height // 2 + screen_width // 2 - 1][1] + col_rays[(screen_width - 0) * screen_height // 2 + screen_width // 2 - 1][2] <= 250:
            col_rays[(screen_width - 0) * screen_height // 2 + screen_width // 2 - 1] = [255, 255, 255]
        else:
            col_rays[(screen_width - 0) * screen_height // 2 + screen_width // 2 - 1] = [0, 0, 0]
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    rays[(screen_width - 0) * screen_height // 2 + screen_width // 2 - 1] = turn_hor_cam(rays[(screen_width - 0) * screen_height // 2 + screen_width // 2 - 1], alpha)
                    d_vec = rays[(screen_width - 0) * screen_height // 2 + screen_width // 2 - 1]
                    d = (d_vec[0] ** 2 + d_vec[1] ** 2 + d_vec[2] ** 2) ** 0.5
                    c_d = ((c_vec[0] * d_vec[0]) + (c_vec[1] * d_vec[1]) + (c_vec[2] * d_vec[2]))
                    # c_d_mod = (c_d[1] ** 2 + c_d[1] ** 2 + c_d[2] ** 2) ** 0.5
                    cos_angle_c_d = c_d / (d * c)
                    if (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) >= 0:
                        r = 0
                        col_rays[0] = [255, 255, 255]
                        """
        imk += 1

    #col_rays[(screen_width - 0) * screen_height // 2] = [255, 255, 255]

        # print(col_rays[419])
    return col_rays


def make_x(t, rad):
    x = rad * m.sin(t)
    return x


def make_y(t, rad):
    y = rad * m.cos(t)
    return y

def turn_hor(cor, al, be):
    rad_0 = (cor[0]**2 + cor[1]**2)**0.5
    if cor[1] == 0 and cor[2] > 0:
        phi = m.pi / 2
    elif cor[1] == 0 and cor[2] < 0:
        phi = -m.pi / 2
    else:
        phi = m.atan(cor[0] / cor[1])
    if cor[1] == 0 and cor[2] > 0:
        theta = m.pi / 2
    elif cor[1] == 0 and cor[2] < 0:
        theta = -m.pi / 2
    else:
        theta = m.atan(cor[2] / cor[1])
    turned_cor = [rad_0 * m.sin(phi + be), rad_0 * m.cos(phi + be), cor[2]]
    return turned_cor


#@jit
def turn_hor_cam(ray_cor, al, be):
    r_hor = (ray_cor[0] ** 2 + ray_cor[1] ** 2) ** 0.5
    if ray_cor[1] == 0 and ray_cor[2] > 0:
        phi = float(m.pi / 2)
    elif ray_cor[1] == 0 and ray_cor[2] < 0:
        phi = float(-m.pi / 2)
    else:
        phi = float(m.atan(ray_cor[0] / ray_cor[1]))
    ray_cor = [float(m.sin(phi + al)), float(1 * m.cos(phi + al)), float(1 * ray_cor[2])]
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



def turn_ver_cam(ray_cor):
    if ray_cor[1] == 0 and ray_cor[2] > 0:
        phi = m.pi / 2
    elif ray_cor[1] == 0 and ray_cor[2] < 0:
        phi = -m.pi / 2
    else:
        phi = m.atan(ray_cor[0] / ray_cor[1])
    turned_cor = [ray_cor[0], m.cos(phi + be), m.sin(phi + be)]
    return turned_cor



def mapping(pixels):
    for pixel_num, pixel in enumerate(pixels):
        x_screen = pixel_num % screen_width + screen_width / 2
        z_screen = pixel_num // screen_width + screen_height / 2
        rect(screen, pixel, (x_screen * pixel_size - 600, z_screen * pixel_size - 300, pixel_size, pixel_size))
    # GAME_FONT.render_to(screen, (10,10), f"{col_rays[419]}", (255, 255, 255))

    pygame.display.update()
    # blacked = (0, 0, 0)
    # screen.fill(blacked)


finished = False

t = 7.5 * m.pi / 4
rad = 300
delta = [0, 0, 0]


global r, fire, al, be
al = 0
be = 0
fire = False
r = 50
a = 500
b = 1000
h = 100
f_button = False
pygame.mouse.set_visible(False)

while not finished:
    clock.tick(30)
    sphere_cor = [0 + delta[0], 400 + delta[1], 0 + delta[2]]
    source_cor = [make_x(t, rad) + delta[0], 0 + make_y(t, rad) + delta[1], 0 + delta[2]]
    #source_cor = [200, 200, 0]
    floor_cor = [0 + delta[0], 0 + delta[1], 100 + delta[2]]
    # rint(sphere_cor[1])
    mapping(out_scr(al, sphere_cor, source_cor, floor_cor))
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
    #t += 0.1
    print(source_cor[1])
pygame.quit()
