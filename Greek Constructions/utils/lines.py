from manim import *
import numpy as np

def polar_to_line(start, radius, angle):
    end = start + radius * np.cos(angle) * RIGHT + radius * np.sin(angle) * UP
    return Line(start, end)

def get_unit_direction(line):
    return (line.get_end() - line.get_start()) / line.get_length()

def get_unit_perpendicular_direction(line):
    return get_unit_direction(line.copy().rotate(PI/2))

def extend_line_by_length(line, length, switch_direction=False):
    unit_direction = get_unit_direction(line)
    mult = -1 if switch_direction else 1
    line_extended_from_start = Line(line.get_start(), line.get_start() - mult * unit_direction * length)
    line_extended_from_end = Line(line.get_end(), line.get_end() + mult * unit_direction * length)
    return line_extended_from_start, line_extended_from_end

def interpolate_line(line_AB, percentage=0.5):
    C = Dot((1-percentage) * line_AB.get_start() + percentage * line_AB.get_end())
    line_AC = Line(line_AB.get_start(), C.get_center())
    line_CB = Line(C.get_center(), line_AB.get_end())
    return line_AC, C, line_CB 

def get_triangle_edges(A, B, C):
    line_AB = Line(A.get_center(), B.get_center())
    line_BC = Line(B.get_center(), C.get_center())
    line_CA = Line(C.get_center(), A.get_center())
    return line_AB, line_BC, line_CA

def get_line_marker(
        line, 
        marker_type="/", 
        flip_horizontally=False, flip_vertically=False, 
        rotate=0, position=0.5,
        stroke_width=2,
        color=None, z_index=None,
    ):
    
    if bool(marker_type) and (
        set(marker_type) == {"/"} or set(marker_type) == {"|"} # marker_type in ["/", "//", "///", etc] or ["|", "||", "|||", etc]
    ):
        marker_step = SMALL_BUFF
        marker_length = 2*SMALL_BUFF
        marker_list = []
        for i in range(len(marker_type)):
            marker_i = Line(DOWN*marker_length/2 + RIGHT*i*marker_step, UP*marker_length/2 + RIGHT*i*marker_step, stroke_width=stroke_width)
            if marker_type[i] == "/":
                marker_i.rotate(-2*SMALL_BUFF)
            marker_list.append(marker_i)
        marker = VGroup(*marker_list)

    elif bool(marker_type) and (
        set(marker_type) == {"<"} or set(marker_type) == {">"} # marker_type in ["<", "<<", "<<<", etc] or [">", ">>", ">>>", etc]
    ):
        marker_step = SMALL_BUFF
        marker_length = 2*SMALL_BUFF
        marker_angle = PI/6
        marker_list = []
        for i in range(len(marker_type)):
            top_slant = Line(RIGHT*i*marker_step, RIGHT*marker_length + RIGHT*i*marker_step, stroke_width=stroke_width)
            bot_slant = Line(RIGHT*i*marker_step, RIGHT*marker_length + RIGHT*i*marker_step, stroke_width=stroke_width)
            
            top_slant.rotate(marker_angle, about_point=top_slant.get_start() if marker_type[i] == "<" else top_slant.get_end())
            bot_slant.rotate(-marker_angle, about_point=bot_slant.get_start() if marker_type[i] == "<" else bot_slant.get_end())

            marker_list.append(top_slant)
            marker_list.append(bot_slant)
        marker = VGroup(*marker_list)

    else:
        raise ValueError(f"Unknown marker_type '{marker_type}'. Expected one of '/' or '|' or any of those duplicated.")
    
    if flip_horizontally:
        marker.scale([-1, 1, 1])
    if flip_vertically:
        marker.scale([1, -1, 1])
    if rotate:
        marker.rotate(rotate)

    # Orient marker to line
    marker.move_to(line.get_start() * (1 - position) + line.get_end() * position).rotate(line.get_angle())

    if z_index is None:
        marker.set_z_index(10000)
    else:
        marker.set_z_index(z_index)
    
    if color is not None:
        marker.set_color(color)

    if len(marker) == 1:
        marker = marker[0]
    return marker

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

def get_parallel(line_AB, perpendicular_distance, length=None):
    if length is None:
        length = line_AB.get_length()

    _, parallel_line = extend_line_by_length(line_AB, length)
    parallel_line.move_to(line_AB.get_center())

    perp_unit_direction = get_unit_perpendicular_direction(line_AB)
    
    line_1 = parallel_line.copy().shift(-perpendicular_distance * perp_unit_direction)
    line_2 = parallel_line.copy().shift(perpendicular_distance * perp_unit_direction)

    return line_1, line_2

def get_line_line_intersection(line1, line2, tol=1e-9):
    """
    Equation of Line: r(t) = r0 + u * t
        r0 = [x0, y0, z0]^T     (3x1)
        u = direction vector    (3x1)
        t = parameter           (real number)
    
    let 
        r1(s) = r01 + u1 * s
        r2(t) = r02 + u2 * t
    
    An intersection exists if there exists (s, t) such that r1(s) = r2(t), i.e.
        r01 + u1 * t = r02 + u2 * s
        (u1 - u2) * [s, t]^T = (r02 - r01)
    
    We have reduced this to Ax = b
    """
    
    r01 = line1.get_start()
    u1 = get_unit_direction(line1)
    r02 = line2.get_start()
    u2 = get_unit_direction(line2)
    
    A = np.array([u1, u2]).T
    b = (r02 - r01)
    
    # Use Least Squares to solve Ax = b
    sol, residuals, rank, svals = np.linalg.lstsq(A, b, rcond=None)

    if np.linalg.norm(residuals) <= tol:
        return r01 + u1 * sol[0]
        # return r02 + u2 + sol[1]
    
    # If we could only get an approximate solution, then the lines must not intersect
    if np.linalg.norm(np.cross(u1, u2)) <= tol:
        if np.linalg.norm(np.cross(u1, b)) <= tol:
            raise Exception("Infinite solutions, lines are collinear.")
        raise Exception("No solutions, lines are disjoint.")
    raise Exception("No solution, lines are skewed.")