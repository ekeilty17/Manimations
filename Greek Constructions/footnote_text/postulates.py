def postulate1(line, start=None, end=None):
    if start is None and end is None:
        return fr"""
            \text{{By Post. 1, line }} {line} \text{{ can be constructed}}
        """
    return fr"""
        \text{{By Post. 1, line }} {line} \text{{ can be constructed}}
        \text{{between points }} {start} \text{{ and }} {end}
    """

def postulate1_multiple_lines(*lines):
    if len(lines) == 1:
        return postulate1(lines[0])
    
    if len(lines) == 2:
        line1, line2 = lines[0:2]
        return fr"""
            \text{{By Post. 1, lines }} {line1} \text{{ and }} {line2}
            \text{{can be constructed}}
        """
    
    first_lines_string = " , ".join(line for line in lines[:-1])
    last_line = lines[-1]
    return fr"""
            \text{{By Post. 1, lines }} {first_lines_string} , \text{{ and }} {last_line}
            \text{{can be constructed}}
        """

def postulate2(line, intersection_object=None, point=None, line_text_long=False, intersection_object_text_long=False):
    output = fr"\text{{By Post. 2, extend }} {line}"
    if intersection_object is not None:
        if line_text_long:
            output += fr"""
                \text{{ until it intersects }} {intersection_object}"""
        else:
            output += fr"""\text{{ until it}}
                \text{{intersects }} {intersection_object}"""
    if point is not None:
        if intersection_object_text_long:
            output += fr"""
                \text{{at }} {point}"""
        else:
            output += fr"\text{{ at }} {point}"
    
    return output

def postulate3(circle, center, radius):
    return fr"""
        \text{{By Post. 3, }} {circle} \text{{ can be construced}} 
        \text{{at center }} {center} \text{{ with radius }} {radius}
    """

def postulate4():
    pass

def postulate5():
    pass