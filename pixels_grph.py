def out_scr(sphere_cor, source_cor):
    screen_width = 400
    screen_height = 200
    pixel_size = 3
    # source:
    source = (255, 255, 255)
    #source_cor = [100, 200, 0]

    # sphere:
    #sphere_cor = [0, 150, 0]
    r = 100
    color = (127, 0, 255)
    objects = [sphere_cor, r]
    alpha = 15
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
        des = [x / (x ** 2 + y ** 2 + z ** 2), y / (x ** 2 + y ** 2 + z ** 2), z / (x ** 2 + y ** 2 + z ** 2)]
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
            d = (rays[num][0] ** 2 + rays[num][1] ** 2 + rays[num][2] ** 2) ** 0.5
            d_vec = rays[num]
            c_d = [c_vec[i] + d_vec[i] for i in range(3)]
            c_d_mod = (c_d[1] ** 2 + c_d[1] ** 2 + c_d[2] ** 2) ** 0.5
            cos_angle_c_d = (c_vec[0] * d_vec[0] + c_vec[1] * d_vec[1] + c_vec[2] * d_vec[2]) / (d * c)
            if (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) < 0:
                pass
                # col_rays[num] = [0, 0, 0]
                #print('inf', d_vec, source_cor, num)
            else:
                t_1 = (c_d_mod - d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2
                t_2 = (c_d_mod + d * (((cos_angle_c_d ** 2 - 1) * c ** 2) + r ** 2) ** 0.5) / d ** 2

                # here we choose t_1 cause it's the nearest.
                # FIXME
                # should be smth about back mapping, but i'm very lazy.
                # Phong reflection:
                # Intensity (RGB):

                l_vec = [source_cor[i] - t_1 * d_vec[i] for i in range(3)]
                n_vec = [t_1 * d_vec[i] - sphere_cor[i] for i in range(3)]
                l_n = l_vec[0] * n_vec[0] + l_vec[1] * n_vec[1] + l_vec[2] * n_vec[2]

                r_vec = [2 * l_n * n_vec[i] - l_vec[i] for i in range(3)]
                v_vec = [-t_1 * d_vec[i] for i in range(3)]
                r_v = r_vec[0] * v_vec[0] + r_vec[1] * v_vec[1] + r_vec[2] * v_vec[2]

                il = [0*s_a[i] - 0*s_d[i] * l_n * 0.00000000005 + 1*s_s[i] * (r_v * 0.0000000000000000000000004) ** alpha for i in range(3)]
                col_rays[num] = il
                #print('NOOO', t_1, d_vec, source_cor, num)
            num += 1
        imk += 1
    col_rays[301] = [255, 255, 255]  # broken pixel
    return col_rays


