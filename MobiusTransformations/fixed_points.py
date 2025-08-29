from manim import *

from mobius_transformation import MobiusTransformation
from conformal_map_scenes import ConformalMapScenes

import cmath

NUM_SAMPLES = 100

class FixedPointScenes(ConformalMapScenes):

    color_map = {
        r"{p_{1}}": RED,
        r"{p_{2}}": RED,
        r"{p}": RED,
        r"{k}": GREEN,
        r"|k|": GREEN,
        r"{\arg k}": GREEN,
        "Möbius transformation": YELLOW,
        "Möbius transformations": YELLOW,
        r"\text{M\"obius transformation}": YELLOW,
        r"\text{M\"obius transformations}": YELLOW,
        "fixed point": RED,
        "fixed points": RED,
        r"\text{fixed point}": RED,
        r"\text{fixed points}": RED,
        "Fixed Point": RED,
        "Fixed Points": RED,
        r"\text{grid}": BLUE, 
        r"\text{lines}": YELLOW,
    }

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
        polar_net = [mob.set_z_index(self.NET_Z_INDEX) for mob in polar_net]
        return polar_net

    def get_k_label(self):
        # k = get_k()
        # k_text = self.get_rectangle_label_text("k", k.real, k.imag)
        k_mod_text = MathTex(
            r"|k|", " = ", f"{self.k_mod_tracker.get_value():.2f}",
            substrings_to_isolate=[r"|k|"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_mod_text.to_corner(UR).shift(LEFT * 1).set_z_index(self.LABEL_TEXT_Z_INDEX)
        
        k_arg_text = MathTex(
            r"{\arg k}", " = ", f"{self.k_arg_tracker.get_value():.2f}", r"\pi",
            substrings_to_isolate=[r"{\arg k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_arg_text.next_to(k_mod_text, DOWN, aligned_edge=LEFT).set_z_index(self.LABEL_TEXT_Z_INDEX)

        k_text = VGroup(k_mod_text, k_arg_text)
        k_bg = BackgroundRectangle(k_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        k_bg.set_z_index(self.LABEL_BG_Z_INDEX)

        label = VGroup(k_bg, k_mod_text, k_arg_text)
        
        return label

class FixedPointPreamble(FixedPointScenes):

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
        self.wait(3)

        self.play(
            Unwrite(mobius_text), Unwrite(mobius_formula),
            Unwrite(fixed_point_text), Unwrite(mobius_fixed_point_formula),
            Unwrite(mobius_fixed_points_text), Unwrite(mobius_fixed_points_exception_text)
        )
        self.wait()


class TwoFixedPoints(FixedPointScenes):

    def initialize_parameters(self):
        self.p1_mod_tracker = ValueTracker(2)
        self.p1_arg_tracker = ValueTracker(1/8)

        self.p2_mod_tracker = ValueTracker(3)
        self.p2_arg_tracker = ValueTracker(15/16)
        
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

        p1_dot = Dot(point=RIGHT*p1.real + UP*p1.imag, color=RED, z_index=self.DOT_Z_INDEX)
        p2_dot = Dot(point=RIGHT*p2.real + UP*p2.imag, color=RED, z_index=self.DOT_Z_INDEX)

        fixed_point_dots = VGroup(p1_dot, p2_dot)
        return fixed_point_dots

    def preamble(self):
        top_text = MathTex(
            r"&\text{A }",
            r"\text{M\"obius transformation}",
            r"\text{ with }",
            r"\text{fixed points}",
            r"\\",
            r"&{p_{1}}",
            r"\text{ and }",
            r"{p_{2}}",
            r"\text{ can be written as}",
            substrings_to_isolate=[r"\text{M\"obius transformation}", r"{p_{1}}", r"{p_{2}}", r"\text{fixed points}"]
        ).set_color_by_tex_to_color_map({
            **self.color_map,
            r"\text{fixed points}": TEAL
        })
        top_text.to_edge(UP)
        
        self.play(Write(top_text), run_time=3)
        self.wait()

        formula_text = MathTex(
            r"{w - {p_{1}} \over w - {p_{2}} }" + r" = {k} " + r"{z - {p_{1}} \over z -  {p_{2}} }",
            substrings_to_isolate=[r"{p_{1}}", r"{p_{2}}", r"{k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        formula_text.next_to(top_text, 3.5*DOWN)

        self.play(Write(formula_text))
        self.wait()

        k_text = MathTex(
            r"&\text{Since the mapping of } 3 \text{ point uniquely determines a } \\",
            r"&\text{M\"obius transformation}",
            r"\text{ and }",
            r"{p_{1}}",
            r",",
            r"{p_{2}}",
            r"\text{ map to themselves,}\\",
            r"&\text{the parameter }"
            r"{k}",
            r"\text{ fixes the last degree of freedom}",
            substrings_to_isolate=[r"\text{M\"obius transformation}", r"{p_{1}}", r"{p_{2}}", r"{k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_text.scale(0.9).next_to(formula_text, 3.5*DOWN)

        self.play(Write(k_text), run_time=7)
        self.wait()
        self.wait()

        bottom_text = Text(
            "Let's see what it looks like!"
        ).scale(0.7).to_edge(DOWN)

        self.play(Write(bottom_text))
        self.wait()
        self.wait()

        self.play(
            Unwrite(top_text), Unwrite(k_text), Unwrite(bottom_text)
        )
        self.wait()

        formula_text.set_z_index(50)
        return formula_text

    def explain_and_draw_fixed_points(self, p1_dot, p2_dot, fixed_point_formula):
        
        explanation_text_2 = MathTex(
            r"&\text{As the map changes, pay attention to}\\ &\text{the }",
            r"\text{grid}",
            r"\text{ }",
            r"\text{lines}",
            r"\text{ intersecting at the }",
            r"\text{fixed points}",
            substrings_to_isolate=[r"\text{fixed points}", r"\text{grid}", r"\text{lines}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        explanation_text_2.scale(0.8).set_z_index(self.LABEL_TEXT_Z_INDEX)
        explanation_text_2_bg = self.get_label_background(explanation_text_2)
        explanation_text_2.to_edge(DOWN)
        explanation_text_2_bg.move_to(explanation_text_2.get_center())
        
        explanation_text_1 = MathTex(
            r"\text{Let's pin }", r"{p_{1}}", r"\text{ and }", r"{p_{2}}", r"\text{ to the map}",
            substrings_to_isolate=[r"{p_{1}}", r"{p_{2}}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        explanation_text_1.scale(0.8).set_z_index(self.LABEL_TEXT_Z_INDEX)
        explanation_text_1_bg = self.get_label_background(explanation_text_1)
        explanation_text_1.next_to(explanation_text_2, 2*UP)
        explanation_text_1_bg.move_to(explanation_text_1.get_center())

        self.play(Write(explanation_text_1), FadeIn(explanation_text_1_bg), run_time=1.5)

        # Draw Fixed Points
        p1_mobs = [mob.copy() for mob in fixed_point_formula if mob.get_tex_string() == r"{p_{1}}"]
        p2_mobs = [mob.copy() for mob in fixed_point_formula if mob.get_tex_string() == r"{p_{2}}"]

        self.play(
            *[Transform(p1_mob, p1_dot) for p1_mob in p1_mobs],
            *[Transform(p2_mob, p2_dot) for p2_mob in p2_mobs],
            run_time=2
        )
        self.wait()

        self.play(Write(explanation_text_2), FadeIn(explanation_text_2_bg), run_time=3)
        self.wait(3)
        self.play(
            Unwrite(explanation_text_1), FadeOut(explanation_text_1_bg),
            Unwrite(explanation_text_2), FadeOut(explanation_text_2_bg),
            run_time=2
        )
        self.wait()

        self.remove(*p1_mobs, *p2_mobs)

    def k_mod_toward_0_explanation(self):

        k_mod_towards_0_text = MathTex(
            r"\text{As }",
            r"|k|",
            r"\rightarrow 0",
            r"\text{ the map converges towards }",
            r"{p_{1}}",
            substrings_to_isolate=[r"|k|", r"{p_{1}}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_mod_towards_0_text.scale(0.8)
        k_mod_towards_0_bg = self.get_label_background(k_mod_towards_0_text)
        k_mod_towards_0_text.to_edge(2*DOWN).set_z_index(self.LABEL_TEXT_Z_INDEX)
        k_mod_towards_0_bg.move_to(k_mod_towards_0_text.get_center())

        self.play(Write(k_mod_towards_0_text), FadeIn(k_mod_towards_0_bg))
        self.wait()

        return k_mod_towards_0_text, k_mod_towards_0_bg
    def k_mod_toward_infty_explanation(self, k_mod_towards_0_text):

        k_mod_towards_infty_text = MathTex(
            r"\text{As }",
            r"|k|",
            r"\rightarrow \infty",
            r"\text{ the map converges towards }",
            r"{p_{2}}",
            substrings_to_isolate=[r"|k|", r"{p_{2}}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_mod_towards_infty_text.scale(0.8)
        k_mod_towards_infty_bg = self.get_label_background(k_mod_towards_infty_text)
        k_mod_towards_infty_text.next_to(k_mod_towards_0_text, DOWN).set_z_index(self.LABEL_TEXT_Z_INDEX)
        k_mod_towards_infty_bg.move_to(k_mod_towards_infty_text.get_center())

        self.play(Write(k_mod_towards_infty_text), FadeIn(k_mod_towards_infty_bg))
        self.wait()

        return k_mod_towards_infty_text, k_mod_towards_infty_bg
    def k_arg_explanation(self):

        k_arg_towards_text = MathTex(
            r"\text{ Cycling }"
            r"{\arg k}",
            r"\text{ spins the map around }",
            r"{p_{1}}",
            r"\text{ and }",
            r"{p_{2}}",
            substrings_to_isolate=[r"{\arg k}", r"{p_{1}}", r"{p_{2}}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_arg_towards_text.scale(0.8)
        k_arg_towards_bg = self.get_label_background(k_arg_towards_text)
        k_arg_towards_text.to_edge(DOWN).set_z_index(self.LABEL_TEXT_Z_INDEX)
        k_arg_towards_bg.move_to(k_arg_towards_text.get_center())

        self.play(Write(k_arg_towards_text), FadeIn(k_arg_towards_bg))
        self.wait(2)
        
        return k_arg_towards_text, k_arg_towards_bg
  
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



        # Scene 2: Explain Fixed Points
        p1_dot, p2_dot = self.get_fixed_points()
        self.explain_and_draw_fixed_points(p1_dot, p2_dot, fixed_point_formula)
        self.add(fixed_point_dots)



        # Preparing for Scene 3

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
            mobject.copy().set_z_index(self.NET_Z_INDEX).apply_function(
                lambda p: self.apply_2D_complex_function(T, p)
            ) for mobject in polar_net
        ]))
        self.remove(*polar_net)
        self.add(transformed_net)
        self.wait()


        
        # Scene 3: Animate k changing
        
        # Add k-label
        k_bg, k_mod_text, k_arg_text = self.get_k_label()
        self.play(Write(k_mod_text), Write(k_arg_text), FadeIn(k_bg))
        self.wait()
        self.remove(k_mod_text, k_arg_text, k_bg)
        self.add(k_label)
        self.wait()

        # |k| --> 0
        k_mod_towards_0_text, k_mod_towards_0_bg = self.k_mod_toward_0_explanation()
        self.play(self.k_mod_tracker.animate.set_value(0.2), run_time=3)
        self.wait()
        self.play(self.k_mod_tracker.animate.set_value(1), run_time=3)
        self.wait()
        
        # |k| --> infinity
        k_mod_towards_infty_text, k_mod_towards_infty_bg = self.k_mod_toward_infty_explanation(k_mod_towards_0_text)
        self.play(self.k_mod_tracker.animate.set_value(5), run_time=3)
        self.wait()
        
        self.play(
            self.k_mod_tracker.animate.set_value(1),
            Unwrite(k_mod_towards_0_text), FadeOut(k_mod_towards_0_bg),
            Unwrite(k_mod_towards_infty_text), FadeOut(k_mod_towards_infty_bg),
            run_time=3
        )
        self.wait()
        
        # Showing arg k circling around stuff
        k_arg_towards_text, k_arg_towards_bg = self.k_arg_explanation()
        self.play(self.k_arg_tracker.animate.set_value(2), run_time=7)
        self.wait()
        
        self.play(self.k_mod_tracker.animate.set_value(0.2), run_time=2)
        self.wait(0.5)
        self.play(self.k_arg_tracker.animate.set_value(0), run_time=6)
        self.wait()
        
        self.play(self.k_mod_tracker.animate.set_value(5), run_time=4)
        self.wait(0.5)
        self.play(self.k_arg_tracker.animate.set_value(2), run_time=6)
        self.wait()
        
        self.play(
            self.k_mod_tracker.animate.set_value(1), 
            Unwrite(k_arg_towards_text), FadeOut(k_arg_towards_bg),
            run_time=2
        )
        self.wait()
        

        # Scene 4: animating random stuff
        end_text = MathTex(r"\text{Now for some fun transformations}").scale(0.8)
        end_text_bg = self.get_label_background(end_text)
        end_text.to_edge(DOWN).set_z_index(self.LABEL_TEXT_Z_INDEX)
        end_text_bg.move_to(end_text.get_center())

        self.play(Write(end_text), FadeIn(end_text_bg))
        self.wait()
        self.play(Unwrite(end_text), FadeOut(end_text_bg))
        self.wait()
        
        self.play(
            self.k_mod_tracker.animate.set_value(5), 
            self.k_arg_tracker.animate.set_value(3/4), 
            run_time=3
        )
        self.wait()
        
        self.play(
            self.k_mod_tracker.animate.set_value(0.5),
            run_time=3
        )
        self.wait()

        self.play(
            self.k_arg_tracker.animate.set_value(5/4),
            run_time=3
        )
        self.wait()
        

        self.play(
            self.p1_arg_tracker.animate.set_value(7/16),
            self.p2_arg_tracker.animate.set_value(9/16),
            run_time=3
        )
        self.wait()
        self.play(
            self.p1_arg_tracker.animate.set_value(-9/8),
            self.p2_arg_tracker.animate.set_value(1/8),
            run_time=3
        )
        self.wait()

        self.play(
            self.k_arg_tracker.animate.set_value(1/4),
            run_time=3
        )
        self.wait()

        self.play(
            self.k_mod_tracker.animate.set_value(1), 
            self.k_arg_tracker.animate.set_value(0),
            # self.p1_mod_tracker.animate.set_value(0),
            # self.p1_arg_tracker.animate.set_value(0),
            # self.p2_mod_tracker.animate.set_value(10),
            # self.p2_arg_tracker.animate.set_value(0),
            run_time=3
        )


class OneFixedPoint(FixedPointScenes):

    def initialize_parameters(self):
        self.p_mod_tracker = ValueTracker(2)
        self.p_arg_tracker = ValueTracker(1/8)
        
        self.k_mod_tracker = ValueTracker(0)
        self.k_arg_tracker = ValueTracker(0)

    def get_p(self):
        # return complex(self.p_real_tracker.get_value(), self.p_imag_tracker.get_value())
        return cmath.rect(self.p_mod_tracker.get_value(), self.p_arg_tracker.get_value() * PI)
    def get_k(self):
        # return complex(self.k_real_tracker.get_value(), self.k_imag_tracker.get_value())
        return cmath.rect(self.k_mod_tracker.get_value(), self.k_arg_tracker.get_value() * PI)

    def get_fixed_point(self):
        p = self.get_p()
        p_dot = Dot(point=RIGHT*p.real + UP*p.imag, color=RED, z_index=self.DOT_Z_INDEX)
        return p_dot

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
        ).set_color_by_tex_to_color_map({
            **self.color_map,
            r"\text{fixed points}": TEAL
        })
        top_text.to_edge(UP)
        
        self.play(Write(top_text), run_time=3)
        self.wait()

        formula_text = MathTex(
            r"{1 \over w - {p} }", 
            r" = ",
            r"{1 \over z -  {p} }",
            r" + {k}",
            substrings_to_isolate=[r"{p}", r"{k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        formula_text.next_to(top_text, 3.5*DOWN)

        self.play(Write(formula_text))
        self.wait()

        # TODO: Fix
        k_text = MathTex(
            r"&\text{This is somewhat of a degenerate case where} \\",
            r"&{p}",
            r"\text{ encodes } 2 \text{ degress of freedom.}\\",
            r"&\text{The parameter }"
            r"{k}",
            r"\text{ fixes the last degree of freedom}",
            substrings_to_isolate=[r"{p}", r"{k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_text.scale(0.9).next_to(formula_text, 3.5*DOWN)

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

    def explain_and_draw_fixed_point(self, p_dot, fixed_point_formula):
        
        explanation_text_1 = MathTex(
            r"\text{Let's pin }", r"{p}", r"\text{ to the map}",
            substrings_to_isolate=[r"{p}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        explanation_text_1.scale(0.8).set_z_index(self.LABEL_TEXT_Z_INDEX)
        explanation_text_1_bg = self.get_label_background(explanation_text_1)
        explanation_text_1.to_edge(DOWN)
        explanation_text_1_bg.move_to(explanation_text_1.get_center())

        self.play(Write(explanation_text_1), FadeIn(explanation_text_1_bg), run_time=1.5)

        # Draw Fixed Points
        p_mobs = [mob.copy() for mob in fixed_point_formula if mob.get_tex_string() == r"{p}"]

        self.play(
            *[Transform(p_mob, p_dot) for p_mob in p_mobs],
            run_time=2
        )
        self.wait()

        # self.play(
        #     Unwrite(explanation_text_1), FadeOut(explanation_text_1_bg)
        # )

        self.remove(*p_mobs)

        return explanation_text_1, explanation_text_1_bg

    def construct(self):
        
        # Scene 0: Defining Important MObjects
        self.initialize_parameters()
        fixed_point_dot = always_redraw(self.get_fixed_point)
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



        # Scene 2: Explain Fixed Points
        p_dot = self.get_fixed_point()
        explanation_text_1, explanation_text_1_bg = self.explain_and_draw_fixed_point(p_dot, fixed_point_formula)
        self.add(fixed_point_dot)



        # Preparing for Scene 3

        # Defined Mobius Transformation
        def T(z):
            p = self.get_p()
            k = self.get_k()
            S = MobiusTransformation(k, 1-k*p, 1, -p, safe_evaluation=True)
            S_inv = MobiusTransformation(0, 1, 1, -p, safe_evaluation=True).inverse()
            return S_inv(S(z))

        # animate mobius transformation
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().apply_function(
                lambda p: self.apply_2D_complex_function(T, p)
            ) for mobject in polar_net
        ]))
        self.remove(*polar_net)
        self.add(transformed_net)
        self.wait()


        
        # Scene 3: Animate k changing
        
        # Add k-label
        k_bg, k_mod_text, k_arg_text = self.get_k_label()
        self.play(
            Unwrite(explanation_text_1), FadeOut(explanation_text_1_bg),
            Write(k_mod_text), Write(k_arg_text), FadeIn(k_bg)
        )
        self.wait()
        self.remove(k_mod_text, k_arg_text, k_bg)
        self.add(k_label)
        self.wait()

        # |k| --> infinity
        # k_mod_towards_0_text, k_mod_towards_0_bg = self.k_mod_toward_0_explanation()
        self.play(self.k_mod_tracker.animate.set_value(1.5), run_time=3)
        self.wait()
        self.play(self.k_mod_tracker.animate.set_value(0.75), run_time=3)
        self.wait()
        
        # arg k cycling
        self.play(self.k_arg_tracker.animate.set_value(2), run_time=6)
        self.wait()

        # Moving the fixed point
        self.play(
            self.p_arg_tracker.animate.set_value(1),
            run_time=5
        )
        self.wait()

        # Reset k
        self.play(
            self.k_mod_tracker.animate.set_value(0),
            self.k_arg_tracker.animate.set_value(0),
            run_time=8
        )
        self.wait()

class FixedPointEnd(FixedPointScenes):

    def construct(self):
        thankyou_text = Text("Thanks for Watching!")
        self.play(FadeIn(thankyou_text))
        self.wait()
        self.wait()
        self.wait()

class FixedPointThumbnail(FixedPointScenes):

    def initialize_parameters(self):
        self.p1_mod_tracker = ValueTracker(4)
        self.p1_arg_tracker = ValueTracker(-1/4)

        self.p2_mod_tracker = ValueTracker(3)
        self.p2_arg_tracker = ValueTracker(-9/8)
        
        self.k_mod_tracker = ValueTracker(3)
        self.k_arg_tracker = ValueTracker(0.8)

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

        p1_dot = Dot(point=RIGHT*p1.real + UP*p1.imag, color=RED, z_index=self.DOT_Z_INDEX, radius=0.2)
        p2_dot = Dot(point=RIGHT*p2.real + UP*p2.imag, color=RED, z_index=self.DOT_Z_INDEX, radius=0.2)

        fixed_point_dots = VGroup(p1_dot, p2_dot)
        return fixed_point_dots

    def get_fixed_point_title(self):
        fixed_text = Text("Fixed").scale(2.5).set_z_index(self.LABEL_TEXT_Z_INDEX)
        fixed_bg = self.get_label_background(fixed_text)
        point_text = Text("Points").scale(2.5).next_to(fixed_text, DOWN).shift(RIGHT).set_z_index(self.LABEL_TEXT_Z_INDEX)
        point_bg = self.get_label_background(point_text)

        fixed_point_title = VGroup(fixed_text, fixed_bg, point_text, point_bg)
        fixed_point_title.to_corner(UR)
        return fixed_point_title

    def construct(self):
        self.initialize_parameters()
        
        plane = self.get_complex_plane()
        self.add(plane)

        fixed_point_title = self.get_fixed_point_title()
        self.add(fixed_point_title)

        fixed_point_dots = self.get_fixed_points()
        self.add(fixed_point_dots) 

        def T(z):
            p1 = self.get_p1()
            p2 = self.get_p2()
            k = self.get_k()
            S = MobiusTransformation(1, -p1, 1, -p2, safe_evaluation=True)
            S_inv = S.inverse()
            return S_inv(k * S(z))

        polar_net = self.get_polar_net()
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().set_z_index(self.NET_Z_INDEX).apply_function(
                lambda p: self.apply_2D_complex_function(T, p)
            ) for mobject in polar_net
        ]))
        self.add(transformed_net)