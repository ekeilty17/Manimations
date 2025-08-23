from manim import *

from mobius_transformation import MobiusTransformation
from conformal_map_scenes import ConformalMapScenes

import cmath

NUM_SAMPLES = 100

class Preamble(ConformalMapScenes):

    color_map = {
        r"{p}": RED,
        r"{k}": GREEN,
        "Möbius transformation": YELLOW,
        "Möbius transformations": YELLOW,
        r"\text{M\"obius transformation}": YELLOW,
        r"\text{M\"obius transformations}": YELLOW,
        "fixed point": TEAL,
        "fixed points": TEAL,
        "Fixed Point": TEAL,
        "Fixed Points": TEAL,
    }

    def construct(self):
        
        mobius_text = Text(
            "A Möbius transformation is a complex function of the form", 
            t2c=self.color_map,
        ).scale(0.7).to_edge(UP)
        mobius_formula = MathTex(r"w = \frac{az + b}{cz + d}").scale(1.2).next_to(mobius_text, DOWN)
        self.play(Write(mobius_text), run_time=3)
        self.play(Write(mobius_formula))
        self.wait()

        fixed_point_text = MathTex(
            r"\text{A Fixed Point is a point } {p} \text{ such that } T({p}) = {p} \\" +
            r"\text{In particular for a } \text{M\"obius transformation}",
            substrings_to_isolate=["Fixed Point", r"{p}", r"\text{M\"obius transformation}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        fixed_point_text.scale(1).next_to(mobius_formula, 2*DOWN)
        
        self.play(Write(fixed_point_text), run_time=5)
        self.wait()
        
        mobius_fixed_point_formula = MathTex(
            r"{p} = {a {p} + b \over c {p} + d}",
            substrings_to_isolate=[r"{p}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        mobius_fixed_point_formula.scale(1.2).next_to(fixed_point_text, 1.5*DOWN)
        
        self.play(Write(mobius_fixed_point_formula), run_time=3)
        self.wait()

        mobius_fixed_points_text = Text(
            "Every Möbius transformation has either 1 or 2 fixed points", 
            t2c={key: value for key, value in self.color_map.items() if key in ["Möbius transformation", "fixed points"]},
        ).scale(0.7)
        self.wait()

        mobius_fixed_points_exception_text = MathTex(
            r"^*\text{Except } T(z) = z \text{ where all points are fixed points}", 
            substrings_to_isolate=[r"fixed points"]
        ).set_color_by_tex_to_color_map(self.color_map)
        mobius_fixed_points_exception_text.scale(0.8).to_edge(DOWN)
        mobius_fixed_points_text.next_to(mobius_fixed_points_exception_text, UP)

        self.play(Write(mobius_fixed_points_text), run_time=3)
        self.wait()

        self.play(Write(mobius_fixed_points_exception_text), run_time=1.5)
        self.wait()

        self.play(
            Unwrite(mobius_text), Unwrite(mobius_formula),
            Unwrite(fixed_point_text), Unwrite(mobius_fixed_point_formula),
            Unwrite(mobius_fixed_points_text), Unwrite(mobius_fixed_points_exception_text)
        )
        self.wait()

class TwoFixedPoints(ConformalMapScenes):

    color_map = {
        r"{p_{1}}": RED,
        r"{p_{2}}": RED,
        r"{k}": GREEN,
        r"|k|": GREEN,
        r"{\arg k}": GREEN,
        "Möbius transformation": YELLOW,
        "Möbius transformations": YELLOW,
        r"\text{M\"obius transformation}": YELLOW,
        r"\text{M\"obius transformations}": YELLOW,
        "fixed point": TEAL,
        "fixed points": TEAL,
        "Fixed Point": TEAL,
        "Fixed Points": TEAL,
    }

    def initialize_parameters(self):
        self.p1_mod_tracker = ValueTracker(2)
        self.p1_arg_tracker = ValueTracker(1/4)

        self.p2_mod_tracker = ValueTracker(1)
        self.p2_arg_tracker = ValueTracker(7/8)
        
        self.k_mod_tracker = ValueTracker(1)
        self.k_arg_tracker = ValueTracker(0)
    
    def get_p1(self):
        # return complex(self.p1_real_tracker.get_value(), self.p1_imag_tracker.get_value())
        return cmath.rect(self.p1_mod_tracker.get_value(), self.p1_arg_tracker.get_value() * PI)
    def get_p2(self):
        # return complex(self.p2_real_tracker.get_value(), self.p2_imag_tracker.get_value())
        return cmath.rect(self.p2_mod_tracker.get_value(), self.p2_arg_tracker.get_value() * PI)
    def get_k(self):
        # return complex(self.k_real_tracker.get_value(), self.k_imag_tracker.get_value())
        return cmath.rect(self.k_mod_tracker.get_value(), self.k_arg_tracker.get_value() * PI)

    def get_fixed_points(self):
        p1 = self.get_p1()
        p2 = self.get_p2()

        p1_dot = Dot(point=RIGHT*p1.real + UP*p1.imag, color=RED, z_index=50)
        p2_dot = Dot(point=RIGHT*p2.real + UP*p2.imag, color=RED, z_index=50)

        fixed_point_dots = VGroup(p1_dot, p2_dot)
        return fixed_point_dots

    def get_k_label(self):
        # k = get_k()
        # k_text = self.get_rectangle_label_text("k", k.real, k.imag)
        k_mod_text = MathTex(
            r"|k|", " = ", f"{self.k_mod_tracker.get_value():.2f}",
            substrings_to_isolate=[r"|k|"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_mod_text.to_corner(UR).shift(LEFT * 1)
        
        k_arg_text = MathTex(
            r"{\arg k}", " = ", f"{self.k_arg_tracker.get_value():.2f}", r"\pi",
            substrings_to_isolate=[r"{\arg k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_arg_text.next_to(k_mod_text, DOWN, aligned_edge=LEFT)

        k_text = VGroup(k_mod_text, k_arg_text)
        k_bg = BackgroundRectangle(k_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        
        label = VGroup(k_bg, k_mod_text, k_arg_text)
        label.set_z_index(self.LABEL_TEXT_Z_INDEX)
        
        return label

    def preamble(self):
        top_text = MathTex(
            r"&\text{A }",
            r"\text{M\"obius transformation}",
            r"\text{ with }",
            r"\text{fixed points}",
            r"\\",
            r"&p_{1}",
            r"\text{ and }",
            r"p_{2}",
            r"\text{ can be written as}",
            substrings_to_isolate=[r"\text{M\"obius transformation}", r"p_{1}", r"p_{2}", r"\text{fixed points}"]
        ).to_edge(UP)
        top_text.set_color_by_tex(r"\text{M\"obius transformation}", YELLOW)
        top_text.set_color_by_tex(r"p_{1}", RED)
        top_text.set_color_by_tex(r"p_{2}", RED)
        top_text.set_color_by_tex(r"\text{fixed points}", TEAL)
        
        self.play(Write(top_text), run_time=3)
        self.wait()

        formula_text = MathTex(
            r"{w - p_{1} \over w - p_{2} }" + r" = k " + r"{z - p_{1} \over z -  p_{2} }",
            substrings_to_isolate=[r"p_{1}", r"p_{2}", r"k"]
        ).next_to(top_text, 3.5*DOWN)
        formula_text.set_color_by_tex(r"p_{1}", RED)
        formula_text.set_color_by_tex(r"p_{2}", RED)
        formula_text.set_color_by_tex(r"k", GREEN)

        self.play(Write(formula_text))
        self.wait()

        k_text = MathTex(
            r"&\text{Since the mapping of } 3 \text{ point uniquely determine a } \\",
            r"&\text{M\"obius transformation}",
            r"\text{ and }",
            r"p_{1}",
            r",",
            r"p_{2}",
            r"\text{ map to themselves,}\\",
            r"&\text{the parameter }"
            r"k",
            r"\text{ fixes the last degree of freedom}",
            substrings_to_isolate=[r"\text{M\"obius transformation}", r"p_{1}", r"p_{2}", r"k"]
        ).scale(0.9).next_to(formula_text, 3.5*DOWN)
        k_text.set_color_by_tex(r"\text{M\"obius transformation}", YELLOW)
        k_text.set_color_by_tex(r"p_{1}", RED)
        k_text.set_color_by_tex(r"p_{2}", RED)
        k_text.set_color_by_tex(r"k", GREEN)

        self.play(Write(k_text), run_time=7)
        self.wait()
        self.wait()

        bottom_text = Text(
            "Let's see what it looks like!"
        ).scale(0.7).to_edge(DOWN)

        self.play(Write(bottom_text))
        self.wait()

        self.play(
            Unwrite(top_text), Unwrite(k_text), Unwrite(bottom_text)
        )

        formula_text.set_z_index(50)
        return formula_text

    def get_complex_plane(self):
        plane = ComplexPlane(
            axis_config={
                "color": GREY, 
                # "stroke_opacity": 0.75,       # I don't think this is a setting
            },
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                # "stroke_opacity": 1,
            }
        )
        plane.set_opacity(0.75).set_z_index(1)
        plane.add_coordinates()

        return plane

    def get_polar_net(self):
        arc_colors = BLUE # color_gradient([DARK_BLUE, WHITE], 60)
        ray_colors = YELLOW # color_gradient([YELLOW, WHITE], 25)
        arcs, rays = super().get_polar_net(
            start_radius=0, radius=10, num_arc=31, arc_color=arc_colors,
            angle=2*PI, num_ray=33, ray_color=ray_colors,
            num_sample=NUM_SAMPLES
        )
        polar_net = arcs + rays
        return polar_net


    def construct(self):
        
        # Scene 0: Defining Important MObjects
        self.initialize_parameters()
        fixed_point_dots = always_redraw(self.get_fixed_points)
        k_label = always_redraw(self.get_k_label)

        # Scene 1: Preamble
        fixed_point_formula = self.preamble()
        
        
        
        # Transition: Scene 1 --> Scene 2
        fixed_point_formula_bg = self.get_label_background(fixed_point_formula)
        fixed_point_formula_bg.move_to(fixed_point_formula.copy().to_corner(UL).get_center())

        plane = self.get_complex_plane()
        self.play(Create(plane), fixed_point_formula.animate.to_corner(UL), FadeIn(fixed_point_formula_bg))
        self.wait()

        polar_net = self.get_polar_net()
        self.play(*[Create(mobject) for mobject in polar_net])
        self.wait()

        # Draw Fixed Points
        p1_dot, p2_dot = self.get_fixed_points()
        p1_mobs = [mob.copy() for mob in fixed_point_formula if mob.get_tex_string() == "p_{1}"]
        p2_mobs = [mob.copy() for mob in fixed_point_formula if mob.get_tex_string() == "p_{2}"]

        self.play(
            *[Transform(p1_mob, p1_dot) for p1_mob in p1_mobs],
            *[Transform(p2_mob, p2_dot) for p2_mob in p2_mobs],
        )
        self.remove(*p1_mobs, *p2_mobs)
        self.add(fixed_point_dots)
        self.wait()

        # Scene 3: Animate k changing
        
        # Add short explanation
        explanation_text = MathTex(
            r"&\text{As we vary the magnitude and direction of }",
            r"{k}",
            r"\\ &\text{pay attention to the grid lines intersecting }",
            r"{p_{1}}",
            r"\text{ and }",
            r"{p_{2}}",
            substrings_to_isolate=[r"\text{M\"obius transformations}", r"{p_{1}}", r"{p_{2}}", r"{k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        explanation_text.scale(0.8)
        explanation_bg = self.get_label_background(explanation_text)
        explanation_text.to_edge(DOWN).set_z_index(self.LABEL_TEXT_Z_INDEX)
        explanation_bg.move_to(explanation_text.get_center())
        

        self.play(Write(explanation_text), FadeIn(explanation_bg), run_time=3)
        self.wait()
        self.wait()

        # Add k-label
        k_bg, k_mod_text, k_arg_text = self.get_k_label()
        self.play(
            Unwrite(explanation_text), FadeOut(explanation_bg),
            Create(k_bg), Write(k_mod_text), Write(k_arg_text)
        )
        self.wait()
        self.remove(k_mod_text, k_arg_text, k_bg)
        self.add(k_label)
        self.wait()

        # Defined Mobius Transformation
        def T(z):
            p1 = self.get_p1()
            p2 = self.get_p2()
            k = self.get_k()
            S = MobiusTransformation(1, -p1, 1, -p2, safe_evaluation=True)
            S_inv = S.inverse()
            return S_inv(k * S(z))

        # animate mobius transformation
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().apply_function(
                lambda p: self.apply_2D_complex_function(T, p)
            ) for mobject in polar_net
        ]))
        self.remove(*polar_net)
        self.add(transformed_net)
        self.wait()

        # self.play(
        #     p1_mod_tracker.animate.set_value(1), p1_arg_tracker.animate.set_value(0),
        #     p2_mod_tracker.animate.set_value(1), p2_arg_tracker.animate.set_value(1),
        #     run_time=1
        # )

        self.play(self.k_mod_tracker.animate.set_value(0.2), run_time=1)
        self.wait()
        self.play(self.k_arg_tracker.animate.set_value(2), run_time=1)
        self.wait()

        self.play(self.k_mod_tracker.animate.set_value(4), run_time=1)
        self.wait()
        self.play(self.k_arg_tracker.animate.set_value(0), run_time=1)
        self.wait()

        self.play(self.k_mod_tracker.animate.set_value(1), run_time=1)
        self.wait()
        self.play(self.k_arg_tracker.animate.set_value(2), run_time=1)
        self.wait()

        # self.play(
        #     self.k_mod_tracker.animate.set_value(1),
        #     self.k_arg_tracker.animate.set_value(0),
        #     run_time=4
        # )
        self.wait()

class OneFixedPoint(ConformalMapScenes):

    def preamble(self):
        top_text = MathTex(
            r"&\text{A }",
            r"\text{M\"obius transformation}",
            r"\text{ with a single }",
            r"\text{fixed point}",
            r"\\",
            r"&{p}",
            r"\text{ can be written as}",
            substrings_to_isolate=[r"\text{M\"obius transformation}", r"{p}", r"\text{fixed points}"]
        ).to_edge(UP)
        top_text.set_color_by_tex(r"\text{M\"obius transformation}", YELLOW)
        top_text.set_color_by_tex(r"{p}", RED)
        top_text.set_color_by_tex(r"\text{fixed point}", TEAL)
        
        self.play(Write(top_text), run_time=3)
        self.wait()

        formula_text = MathTex(
            r"{1 \over w - {p} }", 
            r" = ",
            r"{1 \over z -  {p} }",
            r" + k",
            substrings_to_isolate=[r"{p}", r"k"]
        ).next_to(top_text, 3.5*DOWN)
        formula_text.set_color_by_tex(r"{p}", RED)
        formula_text.set_color_by_tex(r"k", GREEN)

        self.play(Write(formula_text))
        self.wait()

        # TODO: Fix
        k_text = MathTex(
            r"&\text{Since the mapping of } 3 \text{ point uniquely determine a } \\",
            r"&\text{M\"obius transformation}",
            r"\text{ and }",
            r"{p}",
            r",",
            r"\infty",
            r"\text{ map to themselves,}\\",
            r"&\text{the parameter }"
            r"{k}",
            r"\text{ fixes the last degree of freedom}",
            substrings_to_isolate=[r"\text{M\"obius transformation}", r"{p}", r"\infty", r"{k}"]
        ).scale(0.9).next_to(formula_text, 3.5*DOWN)
        k_text.set_color_by_tex(r"\text{M\"obius transformation}", YELLOW)
        k_text.set_color_by_tex(r"{p}", RED)
        k_text.set_color_by_tex(r"\infty", RED)
        k_text.set_color_by_tex(r"{k}", GREEN)

        self.play(Write(k_text), run_time=7)
        self.wait()
        self.wait()

        bottom_text = Text(
            "Let's see what it looks like!"
        ).scale(0.7).to_edge(DOWN)

        self.play(Write(bottom_text))
        self.wait()

        self.play(
            Unwrite(top_text), Unwrite(k_text), Unwrite(bottom_text)
        )

        formula_text.set_z_index(50)
        return formula_text

    def get_complex_plane(self):
        plane = ComplexPlane(
            axis_config={
                "color": GREY, 
                # "stroke_opacity": 0.75,       # I don't think this is a setting
            },
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                # "stroke_opacity": 1,
            }
        )
        plane.set_opacity(0.75).set_z_index(1)
        plane.add_coordinates()
    
    def construct(self):
        
        fixed_point_formula = self.preamble()

        # Background complex plane
        plane = self.get_complex_plane()

        tmp = fixed_point_formula.copy().to_corner(UL)
        fixed_point_formula_bg = self.get_label_background_bugged(fixed_point_formula)
        #Rectangle(width=4, height=1.3, color=BLACK, fill_opacity=1).move_to(fixed_point_formula)
        self.play(Create(plane), fixed_point_formula.animate.to_corner(UL), FadeIn(fixed_point_formula_bg))
        self.wait()

        # Create polar net
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=10, num_arc=41,
            angle=2*PI, num_ray=21,
        )
        net = arcs + rays
        self.play(*[Create(mobject) for mobject in net])
        self.wait()

        # Define parameters
        p_mod_tracker = ValueTracker(1)
        # p_arg_tracker = ValueTracker(2/10)
        p_arg_tracker = ValueTracker(0)
        
        k_mod_tracker = ValueTracker(0)
        k_arg_tracker = ValueTracker(0)

        def get_p():
            # return complex(p_real_tracker.get_value(), p_imag_tracker.get_value())
            return cmath.rect(p_mod_tracker.get_value(), p_arg_tracker.get_value() * PI)
        def get_p_coord():
            p = get_p()
            return np.array([p.real, p.imag, 0])
        def get_k():
            return cmath.rect(k_mod_tracker.get_value(), k_arg_tracker.get_value() * PI)

        # Draw Fixed Points
        def get_fixed_points():
            p = get_p()
            p_dot = Dot(point=RIGHT*p.real + UP*p.imag, color=RED, z_index=50)
            return p_dot
        p_dot = always_redraw(get_fixed_points)
        
        p_mobs = [mob.copy() for mob in fixed_point_formula if mob.get_tex_string() == r"{p}"]

        self.play(*[Transform(p_mob, p_dot) for p_mob in p_mobs])
        self.remove(*p_mobs)
        self.add(p_dot)
        self.wait()

        # # Add short explanation
        # explanation_text = MathTex(
        #     r"&\text{As we vary the magnitude and direction of }",
        #     r"k",
        #     r"\\ &\text{pay attention to the grid lines intersecting }",
        #     r"p_{1}",
        #     r"\text{ and }",
        #     r"p_{2}",
        #     substrings_to_isolate=[r"\text{M\"obius transformations}", r"p_{1}", r"p_{2}", r"k"]
        # ).scale(1).to_edge(DOWN)
        # explanation_text.set_color_by_tex(r"p_{1}", RED)
        # explanation_text.set_color_by_tex(r"p_{2}", RED)
        # explanation_text.set_color_by_tex(r"k", GREEN)
        # explanation_text.set_z_index(50)
        # explanation_bg = BackgroundRectangle(explanation_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        # explanation_bg.set_z_index(49)

        # self.play(Write(explanation_text), FadeIn(explanation_bg), run_time=3)
        # self.wait()
        # self.wait()

        # Add k-label
        def get_k_label():
            # k = get_k()
            # k_text = self.get_rectangle_label_text("k", k.real, k.imag)
            k_mod_text = MathTex(
                r"|k|", " = ", f"{k_mod_tracker.get_value():.2f}"
            )
            k_mod_text.to_corner(UR).shift(LEFT * 1)
            k_mod_text.set_color_by_tex_to_color_map({
                r"|k|": GREEN,
                # "=": WHITE,
            })
            k_arg_text = MathTex(
                r"\arg ", "k", " = ", f"{k_arg_tracker.get_value():.2f}", r"\pi"
            )
            k_arg_text.next_to(k_mod_text, DOWN, aligned_edge=LEFT)
            k_arg_text.set_color_by_tex_to_color_map({
                r"\arg": GREEN,
                "k": GREEN,
                "=": WHITE,
            })

            k_text = VGroup(k_mod_text, k_arg_text)
            k_bg = BackgroundRectangle(k_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
            
            label = VGroup(k_bg, k_mod_text, k_arg_text)
            label.set_z_index(50)
            
            return label
        k_label = always_redraw(get_k_label)
        k_bg, k_mod_text, k_arg_text = k_label

        self.play(
            # Unwrite(explanation_text), FadeOut(explanation_bg),
            Create(k_bg), Write(k_mod_text), Write(k_arg_text)
        )
        self.remove(k_mod_text, k_arg_text, k_bg)
        self.add(k_label)
        self.wait()

        # Defined Mobius Transformation
        def T(z):
            p = get_p()
            k = get_k()
            # if k.real == 0 and k.imag == 0:
            #     return z
            S = MobiusTransformation(k, 1-k*p, 1, -p, safe_evaluation=True)
            S_inv = MobiusTransformation(0, 1, 1, -p, safe_evaluation=True).inverse()
            return S_inv(S(z))

        # animate mobius transformation
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().apply_function(
                lambda p: self.apply_2D_complex_function(T, p)
            ) for mobject in net
        ]))
        self.remove(*net)
        self.add(transformed_net)
        self.wait()

        self.play(k_mod_tracker.animate.set_value(0.4), run_time=1)
        self.wait()

        self.play(k_arg_tracker.animate.set_value(2), run_time=1)
        self.wait()

        # self.play(p_mod_tracker.animate.set_value(0.1), run_time=1)
        # self.wait()