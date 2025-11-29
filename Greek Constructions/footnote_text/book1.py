def prop1(triangle, base=None):
    if base is None:
        return fr"""
            \text{{Using the procedure in Prop. 1.1,}}
            \text{{construct equilateral triangle }} {triangle}
        """
    return fr"""
        \text{{Using the procedure in Prop. 1.1, construct}}
        \text{{equilateral triangle }} {triangle} \text{{ with base }} {base}
    """
    
def prop2(line, point):
    return fr"""
        \text{{Using the procedure in Prop. 1.2,}}
        \text{{copy line }} {line} \text{{ to point }} {point}
    """

def prop3(source_line, target_line, point):
    return fr"""
        \text{{Using the procedure in Prop 1.3}}, 
        \text{{copy line }} {source_line} \text{{ onto line }} {target_line} \text{{ starting at }} {point}
    """

def prop4(triangle1, triangle2, congruency1=None, congruency2=None, congruency3=None):
    if congruency1 is None or congruency2 is None or congruency3 is None:
        return fr"""
            \text{{By SAS (Prop. 1.4), }} {triangle1} ~= {triangle2}
        """
    return fr"""
        {congruency1} , {congruency2} , {congruency3}
        \text{{therefore by SAS (Prop. 1.4), }} {triangle1} ~= {triangle2}
    """

def prop5(angle1, angle2, side1, side2):
    return fr"""
        \text{{Since }} {angle1} ~= {angle2} , \text{{by Prop. 1.5 }} {side1} ~= {side2}
    """

def prop6(side1, side2, angle1, angle2):
    return fr"""
        \text{{Since }} {side1} ~= {side2} , \text{{by Prop. 1.6 }} {angle1} ~= {angle2}
    """

def prop7():
    pass

def prop8(triangle1, triangle2, congruency1=None, congruency2=None, congruency3=None):
    if congruency1 is None or congruency2 is None or congruency3 is None:
        return fr"""
            \text{{By SSS (Prop. 1.8), }} {triangle1} ~= {triangle2}
        """
    return fr"""
        {congruency1} , {congruency2} , {congruency3}
        \text{{therefore by SSS (Prop. 1.8), }} {triangle1} ~= {triangle2}
    """

def prop9(angle):
    return fr"""
        \text{{Using the procedure in Prop. 1.9,}}
        \text{{construct the bisector of angle }} {angle}
    """

def prop10(line, midpoint):
    return fr"""
        \text{{Using the procedure in Prop. 1.10,}}
        \text{{construct midpoint }} {midpoint} \text{{ of line }} {line}
    """

def prop11(base_line, perp_line):
    return fr"""
        \text{{Using the procedure in Prop 1.11,}}
        \text{{construct }} {perp_line} \text{{ perpendicular to }} {base_line}
    """

def prop12():
    pass

def prop13():
    pass