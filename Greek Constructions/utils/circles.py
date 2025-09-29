from manim import *

def OrientedCircle(center, start, other_direction=False, **kwargs):

    # we create this temporary line so we can use its methods
    radius_line = Line(center, start)

    # create circle
    radius = radius_line.get_length()
    circle = Circle(radius=radius, **kwargs).move_to(center)

    # rotate so the animation starts at the start point
    a, b = 0, 2*PI
    theta = radius_line.get_angle()
    angle = ((theta+b)%(b-a))+a
    if PI/2 <= angle <= 3*PI/2:         # TODO: maybe change this behavior, idk
        circle.flip(RIGHT)
    if other_direction:
        circle.flip(RIGHT)
    circle.rotate(angle)

    return circle