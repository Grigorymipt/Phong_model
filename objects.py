import math as m


# not works
def floor_lift(cor, size, delta, f_button):
    if (cor[0] < size[0]) and (cor[0] > -size[0]) and (cor[1] < size[1]) and (cor[1] > -size[1]) and f_button is True:
        delta[2] = 200
# intersect all rays with given sphere, source_1(cor_x, cor_y, cor_z, k_ambient, k_diffused, k_specular, alpha)
# sphere(cor_x, cor_y, cor_z, c, color, i_ambient, i_diffused, i_specular)


# works
def turn_hor_cam(ray_cor, al, be):
    r_hor = (ray_cor[0]**2 + ray_cor[1]**2)**0.5
    if ray_cor[1] == 0 and ray_cor[2] > 0:
        phi = float(m.pi / 2)
    elif ray_cor[1] == 0 and ray_cor[2] < 0:
        phi = float(-m.pi / 2)
    else:
        phi = float(m.atan(ray_cor[0] / ray_cor[1]))
    ray_cor = [float(m.sin(phi + al)), float(r_hor * m.cos(phi + al)), float(r_hor * ray_cor[2])]

    r_ver = (ray_cor[2]**2 + ray_cor[1]**2)**0.5
    if ray_cor[1] == 0 and ray_cor[0] > 0:
        phi = m.pi / 2
    elif ray_cor[1] == 0 and ray_cor[0] < 0:
        phi = -m.pi / 2
    else:
        phi = m.atan(ray_cor[2] / ray_cor[1])
    turned_cor = [ray_cor[0], r_ver * m.cos(phi + be), r_ver * m.sin(phi + be)]
    return turned_cor


# works
def make_sphere_with_lines(c_vec, c, r, ray):
    d_vec = ray
    d = (d_vec[0] ** 2 + d_vec[1] ** 2 + d_vec[2] ** 2) ** 0.5
    c_d = ((c_vec[0] * d_vec[0]) + (c_vec[1] * d_vec[1]) + (c_vec[2] * d_vec[2]))
    # c_d_mod = (c_d[1] ** 2 + c_d[1] ** 2 + c_d[2] ** 2) ** 0.5
    cos_angle_c_d = c_d / (d * c)
    if (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) >= 0 and\
            (c_d - d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2 > 0:
        t_min = (c_d - d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2
        n_vec = [t_min * d_vec[i] - c_vec[i] for i in range(3)]
        return t_min, n_vec, [127, 0, 255]
    else:
        return -1, [0, 0, 0], [127, 0, 255]


def make_wall_with_hash(ray, hash_cor):
    wall_1 = make_wall(ray, 1, 1, hash_cor[0] + hash_cor[1] - 100, hash_cor[0] - 100, hash_cor[0], -100, 100)
    wall_2 = make_wall(ray, 1, 1, hash_cor[0] + hash_cor[1] + 100, hash_cor[0], hash_cor[0] + 100, -100, 100)
    wall_3 = make_wall(ray, 1, -1, hash_cor[0] + hash_cor[1] - 100, hash_cor[0] - 100, hash_cor[0], -100, 100)
    wall_4 = make_wall(ray, 1, -1, hash_cor[0] + hash_cor[1] + 100, hash_cor[0], hash_cor[0] + 100, -100, 100)
    walls = [wall_1, wall_2, wall_3, wall_4]
    f_wall = []
    for wall in walls:
        if wall[0] != -1:
            f_wall.append(wall)
    v_wall = min(f_wall[0], f_wall[1])
    return v_wall


# not works
def make_square_with_lines(x_0, y_0, size, ray):

    d = (ray[1] * y_0 + ray[1] * x_0 - 8 * x_0 * ray[0] - 8 * y_0 * ray[1])**2 + \
        (size**2 + x_0 * y_0 - 4 * (x_0**2 + y_0 ** 2)) * ((4 * ray[0]**2 - 16 * ray[1] * ray[0] + 4 * ray[1]**2))
    if d >= 0:
        x_sec_1 = (ray[1] * (ray[1] * y_0 + ray[1] * x_0 - 8 * x_0 * ray[0] - 8 * y_0 * ray[1]) - d) / \
                  (4 * ray[1]**2 - 16 * ray[1] * ray[0] + 4 * ray[0]**2)
        #x_sec_2 = (ray[1] * (ray[1] * y_0 + ray[1] * x_0 - 8 * x_0 * ray[0] - 8 * y_0 * ray[1]) + d) / \
        #          (4 * ray[1] ** 2 - 16 * ray[1] * ray[0] + 4 * ray[0] ** 2)
        x_sec_min = x_sec_1  # temporary
        t_3 = x_sec_1 ** 2 * (((ray[0]) ** 2 + (ray[1]) ** 2 + (ray[0]) ** 2) / ray[0] ** 2) ** 0.5
        #t_4 = x_sec_2 ** 2 * (((ray[0]) ** 2 + (ray[1]) ** 2 + (ray[0]) ** 2) / ray[0] ** 2) ** 0.5
        t_min = t_3  # temporary
        if t_3 >= 0 and (x_sec_min > (x_0 - size / 2) - 0.01 * abs(x_0 - size / 2)) \
                and x_sec_min < (x_0 - size / 2) + 0.01 * abs(x_0 - size / 2):
            n_vec = [0, 1, 1]  # should be fixed
        elif t_3 >= 0 and (x_sec_min > (x_0 - size / 2) - 0.01 * abs(x_0 - size / 2)) \
                and x_sec_min < (x_0 - size / 2) + 0.01 * abs(x_0 - size / 2):
            n_vec = [0, -1, 0]  # should be fixed
        elif t_3 >= 0 and (x_sec_min > (x_0 - size / 2) - 0.01 * abs(x_0 - size / 2)) \
                and x_sec_min < (x_0 - size / 2) + 0.01 * abs(x_0 - size / 2):
            n_vec = [0, -1, 0]  # should be fixed
        elif t_3 >= 0 and (x_sec_min > (x_0 - size / 2) - 0.01 * abs(x_0 - size / 2)) \
                and x_sec_min < (x_0 - size / 2) + 0.01 * abs(x_0 - size / 2):
            n_vec = [0, -1, 0]  # should be fixed
        else:
            t_min = -1
            n_vec = [0, 0, 0]
    else:
        t_min = -1
        n_vec = [0, 0, 0]
    return t_min, n_vec


# works
def make_wall(ray, a, b, c, x_min, x_max, z_min, z_max):
    if ray[0] == 0:
        x = -c / b
        y = c/a
        z = y * (ray[2] / ray[1])
        if (x > x_min) and x < x_max:
            t = (x ** 2 + y ** 2 + z ** 2) ** 0.5
            n_vec = [-a, -b, 0]
        else:
            t = -1
            n_vec = [0, 0, 0]
        return (t, n_vec)
    elif (a + (ray[1] / ray[0]) * b) == 0:
        return (-1, [0, 0, 0])
    else:
        x = -c / (a + (ray[1] / ray[0]) * b)
        y = x * (ray[1] / ray[0])
        z = x * (ray[2] / ray[0])
        if (x > x_min) and x < x_max:
            t = (x**2 + y**2 + z**2)**0.5
            n_vec = [-a, -b, 0]
        else:
            t = -1
            n_vec = [0, 0, 0]
        return (t, n_vec)


# works
def phong_model(t_min, d_vec, d, n_vec, source_cor, source_par, color):
    s_a = source_par[0]
    s_d = source_par[1]
    s_s = source_par[2]
    alpha = source_par[3]
    if t_min >= 0:
        l_vec = [source_cor[i] - t_min * d_vec[i] for i in range(3)]
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
            col_ray = [s_a[i] for i in range(3)]
        else:
            col_ray = [0.1 * color[i] + 0.9 * color[i] * cos_l_n + 255 * cos_r_v ** alpha for i in range(3)]
            if col_ray[0] >= 255:
                col_ray[0] = 255
            if col_ray[1] >= 255:
                col_ray[1] = 255
            if col_ray[2] >= 255:
                col_ray[2] = 255
            if col_ray[0] <= 0:
                col_ray[0] = 0
            if col_ray[1] <= 0:
                col_ray[1] = 0
            if col_ray[2] <= 0:
                col_ray[2] = 0
    else:
        col_ray = [100, 150, 250]
    return col_ray


def make_floor(ray, h, a, b, delta):

    if ray[2] > 0 \
            and ray[0] / ((ray[2] ** 2 + ray[0] ** 2)) ** 0.5 <= (
            (a + delta[0]) ** 2 / ((a + delta[0]) ** 2 + (h + delta[2]) ** 2)) ** 0.5 \
            and ray[1] / ((ray[2] ** 2 + ray[1] ** 2)) ** 0.5 <= (
            (b + delta[1]) ** 2 / ((b + delta[1]) ** 2 + (h + delta[2]) ** 2)) ** 0.5 \
            and ray[0] / ((ray[2] ** 2 + ray[0] ** 2)) ** 0.5 >= -((a - delta[0]) ** 2 / (
            (a - delta[0]) ** 2 + (h + delta[2]) ** 2)) ** 0.5 \
            and ray[1] / ((ray[2] ** 2 + ray[1] ** 2)) ** 0.5 >= -((b - delta[1]) ** 2 / (
            (b - delta[1]) ** 2 + (h + delta[2]) ** 2)) ** 0.5:
        t_3 = (100 ** 2 * ((ray[0]) ** 2 + (ray[1]) ** 2 + (ray[0]) ** 2) / ray[2] ** 2) ** 0.5
        n_vec = [0, 0, -1]
        return t_3, n_vec, [50, 50, 50]
    else:
        return -1, [0, 0, 0], [50, 50, 50]


# rotation:
def make_x(t, rad):
    x = rad * m.sin(t)
    return x


def make_y(t, rad):
    y = rad * m.cos(t)
    return y


def make_room(ray, h, a, b, delta):
    if ray[1] > 0 \
            and ray[0] / ((ray[1] ** 2 + ray[0] ** 2)) ** 0.5 <= (
            (a + delta[0]) ** 2 / ((a + delta[0]) ** 2 + (b + delta[1]) ** 2)) ** 0.5 \
            and ray[2] / ((ray[1] ** 2 + ray[2] ** 2)) ** 0.5 <= (
            (h + delta[2]) ** 2 / ((h + delta[2]) ** 2 + (b + delta[1]) ** 2)) ** 0.5 \
            and ray[0] / ((ray[1] ** 2 + ray[0] ** 2)) ** 0.5 >= -((a - delta[0]) ** 2 / (
            (a - delta[0]) ** 2 + (b + delta[2]) ** 2)) ** 0.5 \
            and ray[2] / ((ray[1] ** 2 + ray[2] ** 2)) ** 0.5 >= -((b - delta[0]) ** 2 / (
            (h - delta[2]) ** 2 + (b + delta[1]) ** 2)) ** 0.5:
        t_3 = ((a - delta[0]) ** 2 * ((ray[0]) ** 2 + (ray[1]) ** 2 + (ray[0]) ** 2) / ray[1] ** 2) ** 0.5
        n_vec = [0, -1, 0]
        color = [30, 30, 150]
        return t_3, n_vec, color
    elif ray[1] < 0 \
            and ray[0] / ((ray[1] ** 2 + ray[0] ** 2)) ** 0.5 <= (
            (a + delta[0]) ** 2 / ((a + delta[0]) ** 2 + (b - delta[1]) ** 2)) ** 0.5 \
            and ray[2] / ((ray[1] ** 2 + ray[2] ** 2)) ** 0.5 <= (
            (h + delta[2]) ** 2 / ((h + delta[2]) ** 2 + (b - delta[1]) ** 2)) ** 0.5 \
            and ray[0] / ((ray[1] ** 2 + ray[0] ** 2)) ** 0.5 >= -((a - delta[0]) ** 2 / (
            (a - delta[0]) ** 2 + (b - delta[2]) ** 2)) ** 0.5 \
            and ray[2] / ((ray[1] ** 2 + ray[2] ** 2)) ** 0.5 >= -((b - delta[0]) ** 2 / (
            (h - delta[2]) ** 2 + (b - delta[1]) ** 2)) ** 0.5:
        t_3 = ((a - delta[0]) ** 2 * ((ray[0]) ** 2 + (ray[1]) ** 2 + (ray[0]) ** 2) / ray[1] ** 2) ** 0.5
        n_vec = [0, 1, 0]
        color = [30, 30, 150]
        return t_3, n_vec, color


    else:
        return -1, [0, 0, 0], [50, 50, 50]
