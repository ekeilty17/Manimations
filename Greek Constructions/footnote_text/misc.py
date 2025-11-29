def reflexivity(geometric_object):
    return fr"{geometric_object} \text{{ is congruent to itself (Reflexivity)}}"

def random_point_on_line(line, point=None):
    if point is None:
        return fr"""
            \text{{Pick any point along line }} {line}
        """
    return fr"""
        \text{{Let }} {point} \text{{ be any point along line }} {line}
    """