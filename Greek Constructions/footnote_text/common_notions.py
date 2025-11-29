def common_notion1(object1, object2, object3, operation="~=", property_name="Transitivity", long=False):
    property_name_text = f" ({property_name})" if property_name else ""
    line_break = "\n" if long else r"\ "
    return fr"""
        \text{{By CN. 1{property_name_text}, }}
        {object1} {operation} {object2} {line_break} \text{{and }} {object2} {operation} {object3} {line_break} => \ {object1} {operation} {object3}
    """

def common_notion2(conclusion, justification=""):
    return fr"""
        {justification}
        \text{{Therefore, }} {conclusion} \text{{ by CN. 2 (Addition)}}
    """

def common_notion3(conclusion, justification=""):
    return fr"""
        {justification}
        \text{{Therefore, }} {conclusion} \text{{ by CN. 3 (Subtraction)}}
    """

def common_notion4_congruent_triangles(triangle1, triangle2, congruencies=None):
    if congruencies is None:
        return fr"""
            \text{{Since }} {triangle1} ~= {triangle2} , 
            \text{{parts which coincide are congruent (CN. 4)}}
        """
    return fr"""
        \text{{Since }} {triangle1} ~= {triangle2} , 
        \text{{parts which coincide are congruent (CN. 4)}},
        \text{{i.e. }} {congruencies}
    """

def common_notion5():
    pass