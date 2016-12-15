def geometric_key(xyz, precision='3f', tolerance=1e-9, sanitize=True):
    if sanitize:
        tolerance = tolerance ** 2
        if xyz[0] ** 2 < tolerance:
            xyz[0] = 0.0
        if xyz[1] ** 2 < tolerance:
            xyz[1] = 0.0
        if xyz[2] ** 2 < tolerance:
            xyz[2] = 0.0
    return '{0[0]:.{1}},{0[1]:.{1}},{0[2]:.{1}}'.format(xyz, precision)


def geometric_key2(xy, precision='3f', tolerance=1e-9, sanitize=True):
    if sanitize:
        tolerance = tolerance ** 2
        if xy[0] ** 2 < tolerance:
            xy[0] = 0.0
        if xy[1] ** 2 < tolerance:
            xy[1] = 0.0
    return '{0[0]:.{1}},{0[1]:.{1}}'.format(xy, precision)
