from manim import *

def get_angle_marker(line1, line2, marker_type="(", radius=None, radius_step=0.1, elbow=False):

    if bool(marker_type) and (
        set(marker_type) == {"("} or set(marker_type) == {")"} # marker_type in ["(", "((", "(((", etc] or [")", "))", ")))", etc]
    ):
        if radius is None:
            if len(marker_type) == 1:
                radius = 0.3
            elif len(marker_type) == 2:
                radius = 0.25
            else:
                radius = 0.25
        angle_marker = VGroup([
            Angle(
                line1.copy().rotate(PI), 
                line2, 
                stroke_width=2, 
                radius=radius + radius_step*i, 
                other_angle=(marker_type[i] == "("),
                elbow=elbow
            )
            for i in range(len(marker_type))
        ])
        if len(angle_marker) == 1:
            angle_marker = angle_marker[0]
        return angle_marker
    
    raise ValueError(f"Unexpected value of marker_type - '{marker_type}'")