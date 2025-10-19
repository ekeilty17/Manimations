def reflexivity(geometric_object):
    return fr"{geometric_object} \text{{ is congruent to itself (Reflexivity)}}"

def corresponding_parts_of_congruent_triangles_are_congruent(triangle1, triangle2):
    return fr"""
        \text{{Since }} {triangle1} ~= {triangle2} , \text{{corresponding}}
        \text{{counterparts are congruent}}
    """