import pygame
#from pixels_grph import *
import math as m
import pygame.freetype
from pygame.draw import *
from random import randint
#from numba import njit, prange
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
black = (0, 0, 0)
screen = pygame.display.set_mode((1200, 600))
screen_width = 400
screen_height = screen_width // 2

# Use Numba to get better results 



GAME_FONT = pygame.freetype.Font(None, 20)
GAME_FONT_1 = pygame.freetype.Font(None, 36)
pixel_size = 1200 / screen_width

#@njit(fastmath=True, cache=True,parallel=True)

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
		



def out_scr(sphere_cor, source_cor):
    #screen_width = 40
    #screen_height = 20
    #pixel_size = 30
    # source:
    source = (255, 255, 255)
    #source_cor = [100, 200, 0]

    # sphere:
    #sphere_cor = [0, 150, 0]
    r = 100
    color = (127, 0, 255)
    objects = [sphere_cor, r]
    alpha = 10 # here mustn't be numbers like: 2*n, n in N
    k_a = 0.1
    k_d = 0.9
    k_s = 1
    s_a = [color[i] * k_a for i in range(3)]
    s_s = [source[i] * k_s for i in range(3)]
    s_d = [color[i] * k_d for i in range(3)]
    # s_a = k_a * i_a e.t.c.

    # rays:
    death_length = 10000

    rays = [0, 0, 0] * screen_height * screen_width
    col_rays = [0, 0, 0] * screen_height * screen_width
    i = 0
    while i < screen_width * screen_height:
        x = i % screen_width - screen_width/2
        y = (screen_width / 2) * 3 ** 0.5
        z = i // screen_width + screen_height / 2 - screen_height
        des = [x / (x ** 2 + y ** 2 + z ** 2)**0.5, y / (x ** 2 + y ** 2 + z ** 2)**0.5, z / (x ** 2 + y ** 2 + z ** 2)**0.5]
        rays[i] = des
        i += 1
    i = 0

    # intersection for sphere:
    imk = 0
    while imk == 0:  # stupid FIXME
        c = (sphere_cor[0] ** 2 + sphere_cor[1] ** 2 + sphere_cor[2] ** 2) ** 0.5
        c_vec = sphere_cor
        num = 0
        while num < screen_width * screen_height:
            
            d_vec = rays[num]
            d = (d_vec[0] ** 2 + d_vec[1] ** 2 + d_vec[2] ** 2) ** 0.5
            c_d = ((c_vec[0] * d_vec[0]) + (c_vec[1] * d_vec[1]) + (c_vec[2] * d_vec[2]))
            #c_d_mod = (c_d[1] ** 2 + c_d[1] ** 2 + c_d[2] ** 2) ** 0.5
            cos_angle_c_d = c_d / (d * c)
            
            if (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) >= 0:
                t_1 = (c_d - d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2
                t_2 = (c_d + d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2

                # here we choose t_1 cause it's the nearest.
                # FIXME
                # should be smth about back mapping, but i'm very lazy.
                # Phong reflection:
                # Intensity (RGB):

                l_vec = [source_cor[i] - t_1 * d_vec[i] for i in range(3)]
                n_vec = [t_1 * d_vec[i] - sphere_cor[i] for i in range(3)]
                n = ((n_vec[0])**2 + (n_vec[1])**2 + (n_vec[2])**2)**0.5
                l_n = l_vec[0] * n_vec[0] + l_vec[1] * n_vec[1] + l_vec[2] * n_vec[2]
                           
                cos_l_n = l_n / ((l_vec[0]**2 + l_vec[1]**2 + l_vec[2]**2)**0.5 * (n_vec[0]**2 + n_vec[1]**2 + n_vec[2]**2)**0.5)
                
                	 

                r_vec = [2 * cos_l_n * n_vec[i] / n - l_vec[i] / (l_vec[0]**2 + l_vec[1]**2 + l_vec[2]**2)**0.5 for i in range(3)]
                v_vec = [-d_vec[i] / d for i in range(3)]
                r_v = r_vec[0] * v_vec[0] + r_vec[1] * v_vec[1] + r_vec[2] * v_vec[2]
                cos_r_v = r_v
                if cos_r_v < 0:
                	cos_r_v = 0
                if cos_l_n <= 0:
                	col_rays[num] = [s_a[i] for i in range(3)]
                else:
                	col_rays[num] = [1*s_a[i] + s_d[i] * cos_l_n + s_s[i] * cos_r_v ** alpha for i in range(3)]  
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
            #elif :
             
            else:
                #pass
                col_rays[num] = [50, 50, 50]
                #print('inf', d_vec, source_cor, num)
                #print('NOOO', t_1, d_vec, source_cor, num)
            num += 1
        imk += 1
    col_rays[301] = [255, 255, 255]  # broken pixel
    
    #print(col_rays[419])
    return col_rays


def make_x(t, rad):
    x = rad * m.sin(t)
    return x
def make_y(t, rad):
    y = rad * m.cos(t)
    return y



def mapping(pixels):
    for pixel_num, pixel in enumerate(pixels):
        x_screen = pixel_num % screen_width + screen_width / 2
        z_screen = pixel_num // screen_width + screen_height / 2
        rect(screen, pixel, (x_screen * pixel_size - 600, z_screen * pixel_size - 300, pixel_size, pixel_size))
    #GAME_FONT.render_to(screen, (10,10), f"{col_rays[419]}", (255, 255, 255))

    pygame.display.update()
    #blacked = (0, 0, 0)
    #screen.fill(blacked)




finished = False

t = 3 * m.pi / 4
rad = 400  
while not finished:
    clock.tick(30)
    sphere_cor = [0, 400, 0]
    source_cor = [make_x(t, rad), 400 + make_y(t, rad), 0]

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
    t += 0
    print(source_cor[1])
pygame.quit()