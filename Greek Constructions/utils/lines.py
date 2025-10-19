from manim import *

def get_unit_direction(line):
    return (line.get_end() - line.get_start()) / line.get_length()

def get_unit_perpendicular_direction(line):
    return get_unit_direction(line.rotate(PI))

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

def get_line_marker(
        line, 
        marker_type="/", 
        flip_horizontally=False, flip_vertically=False, 
        rotate=0, position=0.5,
        stroke_width=2,
        color=None, z_index=None,
    ):
    # Create marker
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
        raise NotImplementedError("Not yet implemented.")
    else:
        raise ValueError(f"Unknown marker_type '{marker_type}'. Expected one of '/' or '|' or any of those duplicated.")
    
    if flip_horizontally:
        marker.scale([-1, 1, 1])
    if flip_vertically:
        marker.scale([1, -1, 1])
    if rotate:
        marker.rotate(rotate)

    # Orient marker to line
    marker.rotate(line.get_angle()).move_to(line.get_start() * (1 - position) + line.get_end() * position)

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