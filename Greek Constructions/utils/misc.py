from manim import *

def to_coordinate(obj):
    if isinstance(obj, Mobject):
        return obj.get_center()
    elif isinstance(obj, list):
        return np.array(obj)
    elif isinstance(obj, np.ndarray):
        return obj
    else:
        raise TypeError(f"Recieved an unknown type: {type(obj)} from object: {obj}")

def minimize_angle(theta, range=(-PI, PI)):
    a, b = range
    return ((theta+b)%(b-a))+a

def get_equilateral_triangle_apex(line):
    line_perp = line.copy().rotate(PI/2, about_point=line.get_center())
    unit_vector = (line_perp.get_end() - line_perp.get_start()) / line_perp.get_length()
    
    A = Dot(line.get_center() + np.sqrt(3)/2 * line.get_length() * unit_vector)
    B = Dot(line.get_center() - np.sqrt(3)/2 * line.get_length() * unit_vector)
    return A, B

# To compute intersections between lines and circles
from shapely.geometry import LineString
from shapely.geometry import Point as shapely_Point
def get_line_circle_intersection(line, circle):
        
    x1, y1, _ = line.get_start()
    x2, y2, _ = line.get_end()
    L = LineString([(x1, y1), (x2, y2)])

    cx, cy, _ = circle.get_center()
    C = shapely_Point((cx, cy)).buffer(circle.radius).boundary
    
    inter = L.intersection(C)

    if inter.is_empty:
        return None
    
    elif inter.geom_type == 'Point':        # tangent
        return [inter.x, inter.y, 0]
    elif inter.geom_type == 'MultiPoint':   # typical case
        return ([pt.x, pt.y, 0] for pt in inter.geoms)
    else:
        raise ValueError(f"Unexpected geometry type: {inter.geom_type}")

def get_value_tracker_of_point(point):
    return ValueTracker(point[0]), ValueTracker(point[1]), ValueTracker(point[2])