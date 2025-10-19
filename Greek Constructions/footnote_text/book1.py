def prop1(triangle, base=None):
    if base is None:
        return fr"""
            \text{{By Prop. 1.1, construct equilateral triangle }} {triangle}
        """
    else:
        return fr"""
            \text{{By Prop. 1.1, construct equilateral}}
            \text{{triangle }} {triangle} \text{{ with base }} {base}
        """
    
def prop2():
    pass

def prop3():
    pass

def prop4(congruency1, congruency2, congruency3, triangle1, triangle2):
    return fr"""
        {congruency1} , {congruency2} , {congruency3}
        \text{{therefore by SAS (Prop. 1.4), }} {triangle1} ~= {triangle2}
    """

def prop5():
    pass

def prop6():
    pass

def prop7():
    pass

def prop8():
    pass

def prop9(angle):
    return fr"""
        \text{{Using Prop. 1.9, construct the bisector}}
        \text{{of angle }} {angle}
    """

def prop10():
    pass