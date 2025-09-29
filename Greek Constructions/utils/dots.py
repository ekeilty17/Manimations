
def interpolate_between_dots(dot1, dot2, position=0.5):
    return (1-position) * dot1.get_center() + position * dot2.get_center()