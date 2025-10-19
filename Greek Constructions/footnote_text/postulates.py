def postulate1(line, start=None, end=None):
    if start is None and end is None:
        return fr"""
        \text{{By Post. 1, construct line }} {line}
        """
    return fr"""
        \text{{By Post. 1, construct line }} {line}
        \text{{between points }} {start} \text{{ and }} {end}
    """

def postulate2():
    pass

def postulate3(circle, center, radius):
    return fr"""
        \text{{By Post. 3, construct }} {circle}
        \text{{given center }} {center} \text{{ and radius }} {radius}
    """

def postulate4():
    pass

def postulate5():
    pass