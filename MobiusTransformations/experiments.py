from mobius_transformation import MobiusTransformation
from conformal_map_scenes import ConformalMapScenes

from manim import *
import numpy as np
from mpmath import mp, mpc, arg, cos, sin
mp.dps = 100  # Set number of decimal digits (you can raise this as needed)

import math
import cmath

def get_rectangle_label_text(variable_name, real, imag):
    return MathTex(
        f"{variable_name} =", 
        f"{real:.2f}",
        "-" if imag < 0 else "+",
        "i ",
        f"{abs(imag):.2f}",
        substrings_to_isolate=variable_name
    )


class SteinerTransformation(MobiusTransformation):

    def __init__(self, k, f1, f2=None):
        self.k = mpc(k)
        self.f1 = mpc(f1)
        self.f2 = None if f2 is None else mpc(f2)

        if self.f2 is None:
            pass
            # TODO
        else:
            A = self.k
            B = -self.k * self.f1
            C = 1
            D = -self.f2

        super().__init__(A, B, C, D)

class ConformalMapScenes(Scene):

    def apply_2D_complex_function(self, T, p):
        x, y = p[0], p[1]
        z = mpc(x, y)  # high-precision complex number
        w = T(z)
        return np.array([float(w.real), float(w.imag), 0])

    def get_cartesian_net(
        self, 
        start_x=-5,
        end_x=5,
        num_x=None,
        x_color=BLUE,
        x_func=None,

        start_y=-5,
        end_y=5,
        num_y=None,
        y_color=YELLOW,
        y_func=None,

        num_sample=100,
        ):

        if num_x is None:
            num_x = end_x - start_x + 1
        if x_func is None:
            x_func = np.linspace

        if num_y is None:
            num_y = end_y - start_y + 1
        if y_func is None:
            y_func = np.linspace

        x_lines = []
        for x in x_func(start_x, end_x, num_x):
            x_line = Line(start=RIGHT*start_y+UP*x, end=RIGHT*end_y+UP*x, color=x_color)
            x_lines.append(x_line)

        y_lines = []
        for y in y_func(start_y, end_y, num_y):
            y_line = Line(start=UP*start_x+RIGHT*y, end=UP*end_x+RIGHT*y, color=y_color)
            y_lines.append(y_line)
        
        return x_lines, y_lines

    def get_polar_net(
        self, 
        start_radius=0,
        radius=10, 
        num_arc=None, 
        arc_func=None,
        arc_color=BLUE,

        start_angle=0, 
        angle=2*PI,
        num_ray=None,
        ray_func=None,
        ray_color=YELLOW,

        num_sample=100, 
        ):
        
        if num_arc is None:
            num_arc = (radius - start_radius + 1) * 10
        if arc_func is None:
            arc_func = np.linspace
        if not isinstance(arc_color, list) and not isinstance(arc_color, tuple):
            arc_color = [arc_color]*num_arc
        
        
        if num_ray is None:
            num_ray = int((angle - start_angle) / PI) + 1
        if ray_func is None:
            ray_func = np.linspace
        if not isinstance(ray_color, list) and not isinstance(ray_color, tuple):
            ray_color = [ray_color]*num_ray

        arcs = []
        for i, r in enumerate(arc_func(start_radius, radius, num_arc)):
            if r == 0:
                continue
            arc = Arc(radius=r, start_angle=start_angle, angle=angle, color=arc_color[i], stroke_width=1.75)
            arc.insert_n_curves(num_sample)  # Increase the number of Bezier curves (default is 9)
            arc.make_smooth()         # Ensures the added curves are connected smoothly
            arcs.append(arc)
        
        rays = []
        for j, theta in enumerate(ray_func(start_angle, angle, num_ray)):
            if theta == start_angle + angle:
                continue
            start = start_radius*RIGHT*np.cos(theta) + start_radius*UP*np.sin(theta)
            end = radius*RIGHT*np.cos(theta) + radius*UP*np.sin(theta)
            ray = Line(start=start, end=end, color=ray_color[j], stroke_width=1.5)
            ray.insert_n_curves(100)  # Increase the number of Bezier curves (default is 9)
            ray.make_smooth()         # Ensures the added curves are connected smoothly
            rays.append(ray)
        
        return arcs, rays

    def create_and_animate_net(self, net, T):
        self.play(*[Create(mobject) for mobject in net])
        
        animations = []
        for mobject in net:
            animations.append(mobject.animate.apply_function(lambda p: self.apply_2D_complex_function(T, p)))
        self.play(*animations, run_time=3)

        return animations

    def construct(self):
            
        a = mpc(1, 0)
        b = mpc(0, 1)
        k = mpc(1, 0)
        # S = self.get_Steiner_transformation(a, b, k)
        S = lambda z: z**0.5
        # S = self.get_inverse_Mobius_transformation(1, complex(0, -1), 1, complex(0, 1))
        # S = MobiusTransformation(1, complex(0, -1), 1, complex(0, 1)).inverse()
        # S = lambda z: (z + 1/z)/2
        # S = SteinerTransformation(1, 1, -1)

        def ray_func(start, end, step):
            linear = np.linspace(0, 1, step)
            nonlinear = linear ** 8
            return (nonlinear + start) * (end - start)

        arcs, rays = self.get_polar_net(
            num_arc=10, start_radius=0, radius=5, 
            angle=PI, num_ray=10, ray_func=None
        )
        self.create_and_animate_net(arcs + rays, S)

        # x_lines, y_lines = self.get_cartesian_net()
        # self.create_and_animate_net(x_lines + y_lines, S)


class UnitDisc2HalfPlane(ConformalMapScenes):
    
    def construct(self):
        T = MobiusTransformation(1, complex(0, -1), 1, complex(0, 1)).inverse()
        arcs, rays = self.get_polar_net(
            arc_num=50, 
            radius=1, 
            ray_num=50
        )
        self.create_and_animate_net(arcs + rays, T)

class HalfPlane2UnitDisc(ConformalMapScenes):
    
    def construct(self):
        T = MobiusTransformation(1, complex(0, -1), 1, complex(0, 1))

        arcs, rays = self.get_polar_net(
            start_radius=0, radius=50, num_arc=100, 
            angle=PI, num_ray=20
        )
        self.create_and_animate_net(arcs + rays, T)
    
class HalfDisc2Disc(ConformalMapScenes):
    
    def construct(self):
        T = lambda z: z**2

        arcs, rays = self.get_polar_net(
            start_radius=0, radius=5, num_arc=10,
            angle=PI, num_ray=10,
        )
        self.create_and_animate_net(arcs + rays, T)

class Disc2HalfDisc(ConformalMapScenes):
    
    def construct(self):
        T = lambda z: complex(0, 1) * z**0.5

        arcs, rays = self.get_polar_net(
            start_radius=0, radius=5, num_arc=10,
            angle=2*PI, num_ray=10,
        )
        self.create_and_animate_net(arcs + rays, T)


class LineSegment2Disc(ConformalMapScenes):
    
    # Doesn't really work probably for numerical stability reasons

    def construct(self):
        T = lambda z: 1_000_000 if z == 0 else (z + 1/z)/2

        arcs, rays = self.get_polar_net(
            start_radius=0, radius=5, num_arc=10,
            angle=2*PI, num_ray=10,
        )
        self.create_and_animate_net(arcs + rays, T)


class FixedPointMobiusMap(ConformalMapScenes):

    def construct(self):

        # Fixed Points
        f1 = complex(1*np.cos(PI/3), 1*np.sin(PI/3))
        f2 = complex(-2, 0)
        f1_dot = Dot(point=RIGHT*f1.real + UP*f1.imag, color=RED, z_index=10)
        f2_dot = Dot(point=RIGHT*f2.real + UP*f2.imag, color=RED, z_index=10)
        self.play(GrowFromCenter(f1_dot), GrowFromCenter(f2_dot))

        # Value tracker for k
        k_real_tracker = ValueTracker(1)
        k_imag_tracker = ValueTracker(0)

        # Mobius Transformation
        S = MobiusTransformation(1, -f1, 1, -f2)
        S_inv = S.inverse()
        def T(z):
            k = complex(k_real_tracker.get_value(), k_imag_tracker.get_value())
            return S_inv(k * S(z))

        # Create polar net
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=10, num_arc=41,
            angle=2*PI, num_ray=20,
        )
        net = arcs + rays
        self.play(*[Create(mobject) for mobject in net])

        # Add k-label
        def get_k_label():
            tex = MathTex(
                r"k =", 
                f"{k_real_tracker.get_value():.2f}", 
                "+ i", 
                f"{k_imag_tracker.get_value():.2f}"
            ).to_corner(UR)
            background = BackgroundRectangle(tex, color=BLACK, fill_opacity=0.1, stroke_width=0)
            label = VGroup(background, tex)
            label.set_z_index(5)
            return label
        k_label = always_redraw(get_k_label)
        self.add(k_label)

        # animate mobius transformation
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().apply_function(
                lambda p: self.apply_2D_complex_function(T, p)
            ) for mobject in net
        ]))
        self.remove(*net)
        self.add(transformed_net)
        self.wait()

        self.play(k_real_tracker.animate.set_value(0.1), run_time=4)
        self.wait()

        # self.play(k_real_tracker.animate.set_value(3), run_time=4)
        # self.wait()

        # self.play(k_imag_tracker.animate.set_value(1), run_time=4)
        # self.wait()

        # self.play(k_imag_tracker.animate.set_value(-2), run_time=4)
        # self.wait()

        # self.play(
        #     k_real_tracker.animate.set_value(0.5),
        #     k_imag_tracker.animate.set_value(2),
        #     run_time=4
        # )
        # self.wait()

        # self.play(
        #     k_real_tracker.animate.set_value(1),
        #     k_imag_tracker.animate.set_value(0),
        #     run_time=4
        # )
        # self.wait()

class FixedPointMobiusMap2(ConformalMapScenes):

    def construct(self):

        # Fixed Points
        f1 = complex(1*np.cos(PI/3), 1*np.sin(PI/3))
        f2 = complex(-2, 0)
        f1_dot = Dot(point=RIGHT*f1.real + UP*f1.imag, color=RED, z_index=10)
        f2_dot = Dot(point=RIGHT*f2.real + UP*f2.imag, color=RED, z_index=10)
        self.play(GrowFromCenter(f1_dot), GrowFromCenter(f2_dot))

        # Value tracker for k
        k_mod_tracker = ValueTracker(1)
        k_arg_tracker = ValueTracker(0)

        # Mobius Transformation
        S = MobiusTransformation(1, -f1, 1, -f2)
        S_inv = S.inverse()
        def T(z):
            k = cmath.rect(k_mod_tracker.get_value(), k_arg_tracker.get_value() * PI)
            return S_inv(k * S(z))

        # Create polar net
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=10, num_arc=41,
            angle=2*PI, num_ray=20,
        )
        net = arcs + rays
        self.play(*[Create(mobject) for mobject in net])

        # Add k-label
        def get_k_label():
            mod_text = MathTex(
                r"|k| =", 
                f"{k_mod_tracker.get_value():.2f}"
            ).to_corner(UR)

            arg_text = MathTex(
                r"\arg k =",
                f"{k_arg_tracker.get_value():.2f}",
                "\pi"
            ).next_to(mod_text, DOWN, aligned_edge=LEFT)

            mod_bg = BackgroundRectangle(mod_text, color=BLACK, fill_opacity=0.9, stroke_width=0)
            arg_bg = BackgroundRectangle(arg_text, color=BLACK, fill_opacity=0.9, stroke_width=0)
            
            label = VGroup(mod_bg, arg_bg, mod_text, arg_text)
            label.set_z_index(5)
            return label
        k_label = always_redraw(get_k_label)
        self.add(k_label)

        # animate mobius transformation
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().apply_function(
                lambda p: self.apply_2D_complex_function(T, p)
            ) for mobject in net
        ]))
        self.remove(*net)
        self.add(transformed_net)
        self.wait()

        self.play(k_mod_tracker.animate.set_value(0.1), run_time=4)
        self.wait()

        self.play(k_mod_tracker.animate.set_value(3), run_time=4)
        self.wait()

        self.play(k_arg_tracker.animate.set_value(2), run_time=4)
        self.wait()

        self.play(k_arg_tracker.animate.set_value(1), run_time=4)
        self.wait()

        self.play(
            k_mod_tracker.animate.set_value(0.5),
            k_arg_tracker.animate.set_value(0.5),
            run_time=4
        )
        self.wait()

        self.play(
            k_mod_tracker.animate.set_value(1),
            k_arg_tracker.animate.set_value(0),
            run_time=4
        )
        self.wait()

class SteinerNet(ConformalMapScenes):

    def construct(self):
        
        plane = ComplexPlane(
            axis_config={"color": GREY},
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        )
        plane.add_coordinates()
        self.play(Create(plane))

        a_real_tracker = ValueTracker(1)
        a_imag_tracker = ValueTracker(0)
        
        b_real_tracker = ValueTracker(-1)
        b_imag_tracker = ValueTracker(0)

        def get_fixed_points():
            a = complex(a_real_tracker.get_value(), a_imag_tracker.get_value())
            b = complex(b_real_tracker.get_value(), b_imag_tracker.get_value())
            a_dot = Dot(point=RIGHT*a.real + UP*a.imag, color=RED, z_index=10)
            b_dot = Dot(point=RIGHT*b.real + UP*b.imag, color=ORANGE, z_index=10)

            fixed_points = VGroup(a_dot, b_dot)
            fixed_points.set_z_index(5)
            return fixed_points

        fixed_points = always_redraw(get_fixed_points)
        a_dot, b_dot = fixed_points
        self.play(GrowFromCenter(a_dot), GrowFromCenter(b_dot))
        self.remove(a_dot, b_dot)
        self.add(fixed_points)

        def get_ab_label():
            a_text = get_rectangle_label_text("a", a_real_tracker.get_value(), a_imag_tracker.get_value()).to_corner(UR)
            b_text = get_rectangle_label_text("b", b_real_tracker.get_value(), b_imag_tracker.get_value()).next_to(a_text, DOWN, aligned_edge=RIGHT)

            a_bg = BackgroundRectangle(a_text, color=BLACK, fill_opacity=0.7, stroke_width=0)
            b_bg = BackgroundRectangle(b_text, color=BLACK, fill_opacity=0.7, stroke_width=0)
            
            label = VGroup(a_bg, b_bg, a_text, b_text)
            label.set_z_index(10)
            return label
        
        ab_label = always_redraw(get_ab_label)
        a_bg, b_bg, a_text, b_text = ab_label
        self.play(Create(a_bg), Create(b_bg), Write(a_text), Write(b_text))
        self.remove(a_bg, b_bg, a_text, b_text)
        self.add(ab_label)

        def T(z):
            a = complex(a_real_tracker.get_value(), a_imag_tracker.get_value())
            b = complex(b_real_tracker.get_value(), b_imag_tracker.get_value())
            k = complex(1, 0)
            S = MobiusTransformation(k, -k*a, 1, -b).inverse()
            return S(z)

        # Create polar net
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=10, num_arc=41,
            angle=2*PI, num_ray=20,
        )
        net = arcs + rays
        self.play(*[Create(mobject) for mobject in net])

        # animate mobius transformation
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().apply_function(
                lambda p: self.apply_2D_complex_function(T, p)
            ) for mobject in net
        ]))
        self.remove(*net)
        self.add(transformed_net)
        self.wait()

        self.play(a_real_tracker.animate.set_value(3), run_time=1)
        self.wait()


class SteinerNet2(ConformalMapScenes):

    def construct(self):
        
        # Preamble
        mobius_text = Text(
            "A Möbius transformation is a complex function of the form", 
            # alignment="center",
            t2c={"Möbius transformation": YELLOW},
        ).scale(0.7).to_edge(UP)
        mobius_formula = MathTex(r"w = \frac{az + b}{cz + d}").scale(1.2).next_to(mobius_text, DOWN)
        self.play(Write(mobius_text), run_time=3)
        self.play(Write(mobius_formula))
        self.wait()

        steiner_text = Text(
            "A Steiner Net is a special case of a Möbius transformation of the form", 
            # alignment="center",
            t2c={"Möbius transformation": YELLOW, "Steiner Net": TEAL},
        ).scale(0.7).next_to(mobius_formula, 5*DOWN)
        steiner_formula = MathTex(r"w = k \frac{z - a}{z - b}").scale(1.2).next_to(steiner_text, DOWN)

        self.play(Write(steiner_text), run_time=3)
        self.play(Write(steiner_formula))
        self.wait()

        inverse_steiner_text = Text(
            "Actually, we want to consider the inverse Steiner Net",
            t2c={"Steiner Net": TEAL}
        ).scale(0.7).next_to(steiner_formula, 2*DOWN)
        inverse_steiner_formula = MathTex(r"z = k \frac{w - a}{w - b}").scale(1.2).move_to(steiner_formula.get_center())

        self.play(Write(inverse_steiner_text), run_time=2)
        self.wait()
        self.play(TransformMatchingShapes(steiner_formula, inverse_steiner_formula))
        self.wait()

        bottom_text = Text("Let's see what this looks like!").scale(0.7).to_edge(DOWN)
        self.play(Write(bottom_text), run_time=2)
        self.wait()

        self.play(
            Unwrite(mobius_text), Unwrite(mobius_formula),
            Unwrite(steiner_text),
            Unwrite(inverse_steiner_text), Unwrite(inverse_steiner_formula),
            Unwrite(bottom_text)
        )
        self.wait()
        
        # Do this for good measure
        self.clear()
        
        # Background complex plane
        plane = ComplexPlane(
            axis_config={
                "color": GREY, 
                # "stroke_opacity": 0.75,       # I don't think this is a setting
            },
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                # "stroke_opacity": 1,
            }
        )
        plane.set_opacity(0.75)
        plane.add_coordinates()
        
        w_plane_text = MathTex(r"w\text{-plane}").to_edge(DOWN).shift(DOWN * 0.2).set_z_index(20)
        plane_text_bg = BackgroundRectangle(w_plane_text, color=BLACK, fill_opacity=0.9, stroke_width=0).set_z_index(19)
        z_plane_text = MathTex(r"z\text{-plane}").to_edge(DOWN).shift(DOWN * 0.2).set_z_index(20)
        
        self.play(Create(plane), FadeIn(plane_text_bg), Write(w_plane_text))
        self.wait()

        # Parameters
        # a_real_tracker = ValueTracker(0)
        # a_imag_tracker = ValueTracker(0)
        a_mod_tracker = ValueTracker(0)
        a_arg_tracker = ValueTracker(0)
        
        b_real_tracker = ValueTracker(10)
        b_imag_tracker = ValueTracker(0)
        # b_mod_tracker = ValueTracker(10)
        # b_arg_tracker = ValueTracker(0)

        k_mod_tracker = ValueTracker(1)
        k_arg_tracker = ValueTracker(0)

        # Polar Grid
        arc_colors = color_gradient([DARK_BLUE, WHITE], 60)
        ray_colors = color_gradient([YELLOW, WHITE], 25)
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=10, num_arc=41, arc_color=arc_colors,
            angle=2*PI, num_ray=21, ray_color=ray_colors
        )
        net = arcs + rays
        self.play(*[Create(mobject) for mobject in net], run_time=1)

        inverse_steiner_formula = MathTex(
            r"z = k" + r"{w - a", r"\over", r"w - b}",
            # r"z = k \frac{w - a}{w - b}",
            substrings_to_isolate=["a", "b"]
        ).scale(1).to_corner(UL)
        inverse_steiner_formula.set_z_index(20)
        inverse_steiner_formula.set_color_by_tex("a", RED)
        inverse_steiner_formula.set_color_by_tex("b", RED)
        inverse_steiner_bg = BackgroundRectangle(inverse_steiner_formula, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        self.play(Write(inverse_steiner_formula), Create(inverse_steiner_bg))

        def get_a():
            # return complex(a_real_tracker.get_value(), a_imag_tracker.get_value())
            return cmath.rect(a_mod_tracker.get_value(), a_arg_tracker.get_value() * PI)
        def get_a_coord():
            a = get_a()
            return np.array([a.real, a.imag, 0])
        def get_b():
            return complex(b_real_tracker.get_value(), b_imag_tracker.get_value())
            # return cmath.rect(b_mod_tracker.get_value(), b_arg_tracker.get_value() * PI)
        def get_b_coord():
            b = get_b()
            return np.array([b.real, b.imag, 0])
        def get_k():
            return cmath.rect(k_mod_tracker.get_value(), k_arg_tracker.get_value() * PI)

        def get_ab_label():
            
            a = get_a()
            a_text = get_rectangle_label_text("a", a.real, a.imag)
            a_text.to_corner(UR).shift(LEFT * 0.2).set_color_by_tex("a", RED)

            b = get_b()
            if b_real_tracker.get_value() >= 10:
            # if b_mod_tracker.get_value() >= 10:
                b_text = MathTex("b = \infty", substrings_to_isolate="b")
            else:
                b_text = get_rectangle_label_text("b", b.real, b.imag)
            b_text.next_to(a_text, DOWN, aligned_edge=LEFT).set_color_by_tex("b", RED)

            ab_text = VGroup(a_text, b_text)
            bg = BackgroundRectangle(ab_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
            
            label = VGroup(bg, a_text, b_text)
            label.set_z_index(10)

            return label
        ab_label = always_redraw(get_ab_label)
        bg, a_text, b_text = ab_label

        # Zero and Infinity Points
        def get_zero_and_infinity_points():
            a = get_a()
            a_dot = Dot(point=RIGHT*a.real + UP*a.imag, color=RED, z_index=10)

            b = get_b()
            b_dot = Dot(point=RIGHT*b.real + UP*b.imag, color=ORANGE, z_index=10)

            zero_and_infinity_points = VGroup(a_dot, b_dot)
            zero_and_infinity_points.set_z_index(5)
            return zero_and_infinity_points
        zero_and_infinity_points = always_redraw(get_zero_and_infinity_points)
        a_dot, b_dot = zero_and_infinity_points
        
        # animate dots
        self.play(
            GrowFromCenter(a_dot), Create(bg), Write(a_text), Write(b_text),
            run_time=1.5
        )
        self.wait()
        self.remove(a_dot, b_dot, bg, a_text, b_text)
        self.add(zero_and_infinity_points, ab_label)

        # Initial Steiner Net
        initial_transformation = []
        for mobject in net:
            initial_transformation.append(
                mobject.copy().animate.apply_function(lambda p: 
                    self.apply_2D_complex_function(lambda z: MobiusTransformation(1, -1, 1, 1).inverse()(z), p)
                )
            )
        self.remove(*net)
        self.play(
            TransformMatchingShapes(w_plane_text, z_plane_text),
            *initial_transformation, 
            a_mod_tracker.animate.set_value(1), 
            b_real_tracker.animate.set_value(-1),  
            run_time=1
        )
        # b_mod_tracker.animate.set_value(1), 
        # b_arg_tracker.animate.set_value(1),
        self.wait()

        """
        There is a bug that I don't feel like figuring out where there's a lingering copy of the initial transformation
        so I'm just clearing everything and adding it back
        """
        self.clear()
        self.add(plane)
        self.add(w_plane_text)
        self.add(zero_and_infinity_points)
        self.add(ab_label)

        # General Steiner Net
        def T(z):
            a = get_a()
            b = get_b()
            k = get_k()
            S = MobiusTransformation(k, -k*a, 1, -b).inverse()
            return S(z)

        # animate mobius transformation
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().apply_function(lambda p: self.apply_2D_complex_function(T, p)) for mobject in net
        ]))
        self.remove(*initial_transformation)
        self.add(transformed_net)

        b_coord = get_b_coord()
        arrow = Arrow(start=b_coord + 0.2*UP, end=b_coord + 1*UP, buff=0, color=RED)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(FadeOut(arrow), b_imag_tracker.animate.set_value(2), run_time=1)

        b_coord = get_b_coord()
        arrow = Arrow(start=b_coord + 0.2*DOWN, end=b_coord + 1*DOWN, buff=0, color=RED)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(FadeOut(arrow), b_imag_tracker.animate.set_value(-1), run_time=1)
        self.wait()

        a = get_a()
        a_coord = np.array([a.real, a.imag, 0])
        arrow = Arrow(start=a_coord + 0.2*RIGHT, end=a_coord + 1*RIGHT, buff=0, color=RED)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(FadeOut(arrow), a_mod_tracker.animate.set_value(3), run_time=1)
        
        a = get_a()
        a_coord = np.array([a.real, a.imag, 0])
        arrow = Arrow(start=a_coord + 0.2*LEFT, end=a_coord + 1*LEFT, buff=0, color=RED)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(FadeOut(arrow), a_mod_tracker.animate.set_value(-5), run_time=2)
        self.wait()

        self.play(a_mod_tracker.animate.set_value(2), a_arg_tracker.animate.set_value(2), run_time=4)
        self.wait()

        self.play(FadeOut(zero_and_infinity_points), FadeOut(ab_label))

        def get_k_label():
            k = get_k()
            k_text = get_rectangle_label_text("k", k.real, k.imag)
            k_text.to_corner(UR).shift(LEFT * 0.2)
            k_bg = BackgroundRectangle(k_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
            
            label = VGroup(k_text, k_bg)
            label.set_z_index(10)
            
            return label
        k_label = always_redraw(get_k_label)
        k_text, k_bg = k_label
        self.play(Create(k_bg), Write(k_text))
        self.remove(k_text, k_bg)
        self.add(k_label)

        self.play(k_mod_tracker.animate.set_value(0.5), run_time=3)
        self.wait()

        self.play(k_mod_tracker.animate.set_value(10), run_time=3)
        self.wait()

        self.play(k_arg_tracker.animate.set_value(PI/2), run_time=3)
        self.wait()