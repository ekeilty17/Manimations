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
from shapely.geometry import Point
def get_line_circle_intersection(line, circle):
        
    x1, y1, _ = line.get_start()
    x2, y2, _ = line.get_end()
    L = LineString([(x1, y1), (x2, y2)])

    cx, cy, _ = circle.get_center()
    C = Point((cx, cy)).buffer(circle.radius).boundary
    
    inter = L.intersection(C)

    if inter.is_empty:
        return None, None
    elif inter.geom_type == 'Point':
        return Dot([inter.x, inter.y, 0])
    elif inter.geom_type == 'MultiPoint':
        return (Dot([pt.x, pt.y, 0]) for pt in inter.geoms)
    else:
        raise ValueError(f"Unexpected geometry type: {inter.geom_type}")
    
def get_perpendicular(C, line_AB):
    A = line_AB.get_start()
    B = line_AB.get_end()
    C = C.get_center()
    
    AB = B - A
    AC = C - A
    t = np.dot(AC, AB) / np.linalg.norm(AB)**2
    
    D = Dot(A + t * AB)
    line_CD = Line(C, D.get_center())
    return D, line_CD

def Animate(*mobjects):
    if len(mobjects) == 1:
        mobject = mobjects[0]
        if isinstance(mobject, Dot):
            return GrowFromCenter(mobject)
        if isinstance(mobject, Text) or isinstance(mobject, MathTex):
            return Write(mobject)
        return Create(mobject)
    return [Animate(mob) for mob in mobjects]

def Unanimate(*mobjects):
    if len(mobjects) == 1:
        mobject = mobjects[0]
        if isinstance(mobject, Dot):
            return ShrinkToCenter(mobject)
        if isinstance(mobject, Text) or isinstance(mobject, MathTex):
            return Unwrite(mobject)
        return Uncreate(mobject)
    return [Unanimate(mob) for mob in mobjects]

def get_value_tracker_of_point(point):
    return ValueTracker(point[0]), ValueTracker(point[1]), ValueTracker(point[2])