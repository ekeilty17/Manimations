from manim import *

mobject_type_to_animation_map = {
    BackgroundRectangle: FadeIn,
    Dot: GrowFromCenter,
    Text: Write,
    MathTex: Write,
}
mobject_type_to_unanimation_map = {
    BackgroundRectangle: FadeOut,
    Dot: ShrinkToCenter,
    Text: Unwrite,
    MathTex: Unwrite,
}

def Animate(*mobjects):
    if len(mobjects) == 0:
        raise TypeError("No input provided.")
    if len(mobjects) > 1:
        output = [Animate(mob) for mob in mobjects]
        flatted_output = []
        for anim in output:
            if isinstance(anim, (list, tuple)):
                flatted_output.extend(anim)
            flatted_output.append(anim)
        return flatted_output
    
    mobject = mobjects[0]
    if isinstance(mobject, VGroup):
        first_mob_type = type(mobject[0])
        if not isinstance(mobject[0], VGroup) and all([isinstance(mob, first_mob_type) for mob in mobject]):
            animation_func = mobject_type_to_animation_map.get(first_mob_type, Create)
            return animation_func(mobject)
        return [Animate(mob) for mob in mobject]
    animation_func = mobject_type_to_animation_map.get(type(mobject), Create)
    return animation_func(mobject)

def Unanimate(*mobjects):
    if len(mobjects) == 0:
        raise TypeError("No input provided.")
    if len(mobjects) > 1:
        output = [Unanimate(mob) for mob in mobjects]
        flatted_output = []
        for anim in output:
            if isinstance(anim, (list, tuple)):
                flatted_output.extend(anim)
            flatted_output.append(anim)
        return flatted_output
    
    mobject = mobjects[0]
    if isinstance(mobject, VGroup):
        first_mob_type = type(mobject[0])
        if not isinstance(mobject[0], VGroup) and all([isinstance(mob, first_mob_type) for mob in mobject]):
            animation_func = mobject_type_to_unanimation_map.get(first_mob_type, Uncreate)
            return animation_func(mobject)
        return [Unanimate(mob) for mob in mobject]
    animation_func = mobject_type_to_unanimation_map.get(type(mobject), Uncreate)
    return animation_func(mobject)