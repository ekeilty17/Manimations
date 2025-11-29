def definition15(circle, *radii):
    if len(radii) < 2:
        raise ValueError(f"In parameter `*radii`, expected least 2 entries. Instead got {len(radii)}")
    
    if len(radii) == 2:
        radius1, radius2 = radii
        return fr"""
            \text{{Lines }} {radius1} \text{{ and }} {radius2} \text{{ are both radii of }} {circle} ,
            \text{{thus by Def. 15 they are congruent}}
        """
    
    first_radii_str = " , ".join(radius for radius in radii[:-1])
    last_radius = radii[-1]
    return fr"""
            \text{{Lines }} {first_radii_str} , \text{{ and }} {last_radius} \text{{ are all radii of }} {circle} ,
            \text{{thus by Def. 15 they are congruent}}
        """

def definition20_equilateral_triangle(triangle):
    return fr"""
        \text{{Thus all sides of }} {triangle} \text{{ are congruent,}}
        \text{{by Def. 20 it is an equilateral triangle}}
    """