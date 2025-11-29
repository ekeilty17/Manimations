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

from shapely.geometry import Point as shapely_Point
def get_circle_circle_intersection(circle1, circle2):
    # Get centers
    x1, y1, _ = circle1.get_center()
    x2, y2, _ = circle2.get_center()

    # Create Shapely circles (as boundaries)
    C1 = shapely_Point(x1, y1).buffer(circle1.radius).boundary
    C2 = shapely_Point(x2, y2).buffer(circle2.radius).boundary

    inter = C1.intersection(C2)

    if inter.is_empty:
        return None

    if inter.geom_type == "Point":          # tangent
        return [inter.x, inter.y, 0]
    elif inter.geom_type == 'MultiPoint':   # typical case
        return ([pt.x, pt.y, 0] for pt in inter.geoms)
    else:
        raise ValueError(f"Unexpected geometry type: {inter.geom_type}")