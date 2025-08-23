from manim import *

from mobius_transformation import MobiusTransformation
from conformal_map_scenes import ConformalMapScenes

import cmath

NUM_SAMPLES = 100

class SteinerNet(ConformalMapScenes):

    color_map = {
        r"{p_0}": RED,
        r"{p_{\infty}}": RED,
        r"{k}": GREEN,
        r"\infty": RED,
        r"{0}": RED,
        r"{\arg k}": YELLOW,
        r"|k|": BLUE,
        "Möbius transformation": YELLOW,
        "Möbius transformations": YELLOW,
        "Steiner Net": TEAL,
        "Steiner Nets": TEAL,
    }

    ARROW_Z_INDEX = 30

    def get_steiner_net_formulas(self):
        steiner_formula = MathTex(
            r"w = {z - {p_0} \over z - {p_{\infty}} }",
            substrings_to_isolate=[r"{p_0}", r"{p_{\infty}}"]
        ).set_color_by_tex_to_color_map(self.color_map)

        inverse_steiner_formula = MathTex(
            r"z = {w - {p_0} \over w - {p_{\infty}} }",
            substrings_to_isolate=[r"{p_0}", r"{p_{\infty}}"]
        ).set_color_by_tex_to_color_map(self.color_map)

        steiner_formula_with_k = MathTex(
            r"w = {k} { z - {p_0} \over z - {p_{\infty}} }",
            substrings_to_isolate=[r"{p_0}", r"{p_{\infty}}", r"{k}"]
        ).set_color_by_tex_to_color_map(self.color_map)

        inverse_steiner_formula_with_k = MathTex(
            r"z = {k} { w - {p_0} \over w - {p_{\infty}} }",
            substrings_to_isolate=[r"{p_0}", r"{p_{\infty}}", r"{k}"]
        ).set_color_by_tex_to_color_map(self.color_map)

        steiner_formula.set_z_index(self.LABEL_TEXT_Z_INDEX)
        inverse_steiner_formula.set_z_index(self.LABEL_TEXT_Z_INDEX)
        steiner_formula_with_k.set_z_index(self.LABEL_TEXT_Z_INDEX)
        inverse_steiner_formula_with_k.set_z_index(self.LABEL_TEXT_Z_INDEX)
        return steiner_formula, inverse_steiner_formula, steiner_formula_with_k, inverse_steiner_formula_with_k

    def initialize_parameters(self):
        # self.a_real_tracker = ValueTracker(0)
        # self.a_imag_tracker = ValueTracker(0)
        self.a_mod_tracker = ValueTracker(0)
        self.a_arg_tracker = ValueTracker(0)
        
        self.b_real_tracker = ValueTracker(1)
        self.b_imag_tracker = ValueTracker(0)
        # self.b_mod_tracker = ValueTracker(10)
        # self.b_arg_tracker = ValueTracker(0)

        self.k_mod_tracker = ValueTracker(1)
        self.k_arg_tracker = ValueTracker(0)

    def get_a(self):
        # return complex(self.a_real_tracker.get_value(), self.a_imag_tracker.get_value())
        return cmath.rect(self.a_mod_tracker.get_value(), self.a_arg_tracker.get_value() * PI)
    def get_a_coord(self):
        a = self.get_a()
        return np.array([a.real, a.imag, 0])
    def get_b(self):
        return complex(self.b_real_tracker.get_value(), self.b_imag_tracker.get_value())
        # return cmath.rect(self.b_mod_tracker.get_value(), self.b_arg_tracker.get_value() * PI)
    def get_b_coord(self):
        b = self.get_b()
        return np.array([b.real, b.imag, 0])
    def get_k(self):
        return cmath.rect(self.k_mod_tracker.get_value(), self.k_arg_tracker.get_value() * PI)


    def get_ab_label(self):
        a = self.get_a()
        a_text = self.get_rectangle_label_text(r"{p_0}", a.real, a.imag)
        a_text.set_color_by_tex_to_color_map(self.color_map)
        a_text.to_corner(UR).shift(LEFT * 0.4)

        b = self.get_b()
        if self.b_real_tracker.get_value() >= 10:
        # if b_mod_tracker.get_value() >= 10:
            b_text = MathTex(
                r"{p_{\infty}} = \infty", 
                substrings_to_isolate=[r"{p_{\infty}}"]
            )
        else:
            b_text = self.get_rectangle_label_text(r"{p_{\infty}}", b.real, b.imag)
        b_text.set_color_by_tex_to_color_map({r"{p_{\infty}}": self.color_map[r"{p_{\infty}}"]})
        b_text.next_to(a_text, DOWN, aligned_edge=LEFT)

        ab_text = VGroup(a_text, b_text)
        bg = self.get_label_background(ab_text)

        label = VGroup(bg, a_text, b_text)
        label.set_z_index(self.LABEL_TEXT_Z_INDEX)

        return label
    def get_zero_and_infinity_points(self):
        a = self.get_a()
        a_dot = Dot(point=RIGHT*a.real + UP*a.imag, color=RED, z_index=10)

        b = self.get_b()
        b_dot = Dot(point=RIGHT*b.real + UP*b.imag, color=RED, z_index=10)

        zero_and_infinity_points = VGroup(a_dot, b_dot)
        zero_and_infinity_points.set_z_index(self.LABEL_TEXT_Z_INDEX)
        return zero_and_infinity_points
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

    def preamble(self, steiner_formula_with_k, inverse_steiner_formula_with_k):
        mobius_text = Text(
            "A Möbius transformation is a complex function of the form", 
            t2c=self.color_map,
        ).scale(0.7).to_edge(UP)
        mobius_formula = MathTex(r"w = \frac{az + b}{cz + d}").scale(1.2).next_to(mobius_text, DOWN)
        self.play(Write(mobius_text), run_time=3)
        self.play(Write(mobius_formula))
        self.wait()

        steiner_text = Text(
            "This can be rewritten as", 
            t2c=self.color_map,
        ).scale(0.7).next_to(mobius_formula, 3*DOWN)
        steiner_formula_with_k.scale(1.2).next_to(steiner_text, 3*DOWN)

        self.play(Write(steiner_text), run_time=2)
        self.wait()
        self.play(Write(steiner_formula_with_k))
        self.wait()

        inverse_steiner_text = Text(
            "A Steiner Net is produced by the inverse of this",
            t2c=self.color_map
        ).scale(0.7).next_to(steiner_formula_with_k, 2*DOWN)
        inverse_steiner_formula_with_k.scale(1.2).move_to(steiner_formula_with_k.get_center())

        self.play(Write(inverse_steiner_text), run_time=3)
        self.wait()
        self.play(TransformMatchingShapes(steiner_formula_with_k, inverse_steiner_formula_with_k))
        self.wait()

        bottom_text = Text("Let's see what it looks like!").scale(0.7).to_edge(DOWN)
        self.play(Write(bottom_text), run_time=2)
        self.wait()

        self.play(
            Unwrite(mobius_text), Unwrite(mobius_formula),
            Unwrite(steiner_text),
            Unwrite(inverse_steiner_text),
            Unwrite(bottom_text)
        )
        self.wait()

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
        plane.set_opacity(0.75).set_z_index(self.GRID_LINES_Z_INDEX)
        plane.add_coordinates()
        
        w_plane_text = MathTex(r"w\text{-plane}").to_edge(DOWN).shift(DOWN * 0.2).set_z_index(self.LABEL_TEXT_Z_INDEX)
        plane_text_bg = self.get_label_background(w_plane_text)
        z_plane_text = MathTex(r"z\text{-plane}").to_edge(DOWN).shift(DOWN * 0.2).set_z_index(self.LABEL_TEXT_Z_INDEX)

        return plane, w_plane_text, z_plane_text, plane_text_bg

    def get_polar_net(self):
        arc_colors = BLUE # color_gradient([DARK_BLUE, WHITE], 60)
        ray_colors = YELLOW # color_gradient([YELLOW, WHITE], 25)
        arcs, rays = super().get_polar_net(
            start_radius=0, radius=10, num_arc=32, arc_color=arc_colors,
            angle=2*PI, num_ray=32, ray_color=ray_colors,
            num_sample=NUM_SAMPLES
        )
        polar_net = arcs + rays
        return polar_net

    def initial_transformation_old(self, polar_net, w_plane_text, z_plane_text):
        initial_transformation = []
        for mobject in polar_net:
            initial_transformation.append(
                mobject.copy().set_z_index(self.NET_Z_INDEX).animate.apply_function(lambda p: 
                    self.apply_2D_complex_function(lambda z: MobiusTransformation(1, -1, 1, 1).inverse()(z), p)
                )
            )
        self.remove(*polar_net)
        self.play(
            TransformMatchingShapes(w_plane_text, z_plane_text),
            *initial_transformation, 
            self.a_mod_tracker.animate.set_value(1), 
            self.b_real_tracker.animate.set_value(-1),
            run_time=3
        )
        # b_mod_tracker.animate.set_value(1)
        # b_arg_tracker.animate.set_value(1)
        self.wait()

        return initial_transformation
    def initial_transformation(self, polar_net, w_plane_text, z_plane_text):
        k_tmp_real = ValueTracker(1)
        k_tmp_imag = ValueTracker(0)

        a_final = complex(1, 0)
        b_final = complex(-1, 0)
        A, B, C, D = complex(1, 0), -a_final, complex(1, 0), -b_final

        def get_fixed_points():
            determinant = (A - D)**2 + 4*B*C
            p1 = ((A - D) + cmath.sqrt(determinant)) / (2 * C)
            p2 = ((A - D) - cmath.sqrt(determinant)) / (2 * C)
            return p1, p2

        def T_init(z):
            p1, p2 = get_fixed_points()
            S = MobiusTransformation(1, -p1, 1, -p2)
            S_inv = S.inverse()
            k = complex(k_tmp_real.get_value(), k_tmp_imag.get_value())
            return S_inv(k * S(z))

        p1, p2 = get_fixed_points()
        k_final = -1 * (C*p2 + D) / (C*p1 + D)

        # Initial Steiner Net
        initial_transformation = always_redraw(lambda: VGroup(*[
            mobject.copy().set_z_index(self.NET_Z_INDEX).apply_function(lambda p: self.apply_2D_complex_function(T_init, p)) for mobject in polar_net
        ]))
        
        self.remove(*polar_net)
        self.add(initial_transformation)
        
        self.b_real_tracker.set_value(-11)
        self.play(
            TransformMatchingShapes(w_plane_text, z_plane_text),
            k_tmp_real.animate.set_value(k_final.real),
            k_tmp_imag.animate.set_value(k_final.imag),
            self.a_mod_tracker.animate.set_value(1), 
            self.b_real_tracker.animate.set_value(-1),
            run_time=5
        )
        self.wait()

        return initial_transformation

    def animate_a_and_b_changing(self):
        b_coord = self.get_b_coord()
        arrow = Arrow(start=b_coord + 0.2*UP, end=b_coord + 1*UP, buff=0, color=RED).set_z_index(self.ARROW_Z_INDEX)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(
            FadeOut(arrow), 
            self.b_imag_tracker.animate.set_value(2), 
            run_time=1
        )

        b_coord = self.get_b_coord()
        arrow = Arrow(start=b_coord + 0.2*DOWN, end=b_coord + 1*DOWN, buff=0, color=RED).set_z_index(self.ARROW_Z_INDEX)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(
            FadeOut(arrow), 
            self.b_imag_tracker.animate.set_value(-1), 
            run_time=2
        )
        self.wait()

        a_coord = self.get_a_coord()
        arrow = Arrow(start=a_coord + 0.2*RIGHT, end=a_coord + 1*RIGHT, buff=0, color=RED).set_z_index(self.ARROW_Z_INDEX)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(
            FadeOut(arrow), 
            self.a_mod_tracker.animate.set_value(3), 
            run_time=2
        )
        
        a_coord = self.get_a_coord()
        arrow = Arrow(start=a_coord + 0.2*LEFT, end=a_coord + 1*LEFT, buff=0, color=RED).set_z_index(self.ARROW_Z_INDEX)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(
            FadeOut(arrow), 
            self.a_mod_tracker.animate.set_value(-5), 
            run_time=2.5
        )
        self.wait()

        self.play(self.a_arg_tracker.animate.set_value(1), run_time=3)
        self.play(self.a_mod_tracker.animate.set_value(-1), run_time=2)
        self.wait()

    def k_explanation(self, k_label, inverse_steiner_formula, inverse_steiner_bg, inverse_steiner_formula_with_k):
        k_explanation = MathTex(
            r"\text{Let's see how } {k} \text{ affects the map}", 
            substrings_to_isolate=[r"{k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_explanation.scale(0.8).to_edge(RIGHT).shift(DOWN).set_z_index(self.LABEL_TEXT_Z_INDEX)
        k_explanation_bg = self.get_label_background(k_explanation)

        inverse_steiner_formula_with_k.to_corner(UL)
        inverse_steiner_with_k_bg = self.get_label_background_bugged(inverse_steiner_formula_with_k)
        self.play(
            Create(k_explanation_bg), Write(k_explanation),
            TransformMatchingShapes(inverse_steiner_formula, inverse_steiner_formula_with_k),
            Transform(inverse_steiner_bg, inverse_steiner_with_k_bg)
        )
        self.wait()
        
        k_bg, k_mod_text, k_arg_text = self.get_k_label()
        self.play(
            Create(k_bg), Write(k_mod_text), Write(k_arg_text)
        )
        self.wait()
        self.remove(k_mod_text, k_arg_text, k_bg)
        self.add(k_label)
        self.wait()

        k_mod_explanation = MathTex(
            r"|k|", r"\text{ scales the blue lines}",
            substrings_to_isolate=[r"|k|"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_mod_explanation.scale(0.8).next_to(k_explanation, DOWN, aligned_edge=LEFT).set_z_index(self.LABEL_TEXT_Z_INDEX)
        # k_mod_explanation.set_color_by_tex_to_color_map({
        #         r"|k|": BLUE,
        #         r"\text{ cycles the blue lines}": WHITE,
        #     })
        k_mod_explanation_bg = self.get_label_background(k_mod_explanation)
        self.play(Create(k_mod_explanation_bg), Write(k_mod_explanation))
        self.wait(2)

        k_arg_explanation = MathTex(
            r"{\arg k}", r"\text{ cycles the yellow lines}",
            substrings_to_isolate=[r"{\arg k}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        k_arg_explanation.scale(0.8).next_to(k_mod_explanation, DOWN, aligned_edge=LEFT).set_z_index(self.LABEL_TEXT_Z_INDEX)
        k_arg_explanation_bg = self.get_label_background(k_arg_explanation)
        self.play(Create(k_arg_explanation_bg), Write(k_arg_explanation))
        self.wait(2)

        self.play(
            FadeOut(k_explanation_bg), Unwrite(k_explanation),
            FadeOut(k_mod_explanation_bg), Unwrite(k_mod_explanation),
            FadeOut(k_arg_explanation_bg), Unwrite(k_arg_explanation)
        )
        self.wait()

    def animate_k_changing(self):
        self.play(self.k_mod_tracker.animate.set_value(0.6), run_time=3)
        self.wait()

        self.play(self.k_mod_tracker.animate.set_value(5), run_time=8)
        self.wait()

        self.play(self.k_arg_tracker.animate.set_value(1), run_time=10)
        self.wait()
        self.wait()

    def thank_you_for_watching(self):
        thankyou_text = Text("Thanks for Watching!")
        self.play(FadeIn(thankyou_text))
        self.wait()

    def construct(self):
        

        # Scene 0: Defining Important MObjects
        steiner_formula, inverse_steiner_formula, steiner_formula_with_k, inverse_steiner_formula_with_k = self.get_steiner_net_formulas()
        self.initialize_parameters()

        ab_label = always_redraw(self.get_ab_label)
        zero_and_infinity_points = always_redraw(self.get_zero_and_infinity_points)
        k_label = always_redraw(self.get_k_label)



        # Scene 1: Preamble
        self.preamble(steiner_formula_with_k, inverse_steiner_formula_with_k)



        # Transition: Scene 1 --> Scene 2
        inverse_steiner_formula.to_corner(UL)
        inverse_steiner_bg = self.get_label_background_bugged(inverse_steiner_formula)
        inverse_steiner_bg.set_z_index(self.LABEL_BG_Z_INDEX)
        self.play(
            TransformMatchingShapes(inverse_steiner_formula_with_k, inverse_steiner_formula),
            FadeIn(inverse_steiner_bg)
        )

        plane, w_plane_text, z_plane_text, plane_text_bg = self.get_complex_plane()
        self.play(Create(plane), FadeIn(plane_text_bg), Write(w_plane_text))
        self.wait()

        polar_net = self.get_polar_net()
        self.play(*[Create(mobject) for mobject in polar_net], run_time=1)
        self.wait()
        
        a_dot, b_dot = self.get_zero_and_infinity_points()

        # Explain zero
        a_explanation = MathTex(
            r"{p_0} \text{ determines where } {0} \text{ is mapped}",
            substrings_to_isolate=[r"{p_0}", r"{0}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        a_explanation.scale(0.8).to_edge(RIGHT).shift(DOWN).shift(LEFT*SMALL_BUFF).set_z_index(self.LABEL_TEXT_Z_INDEX)
        a_explanation_bg = self.get_label_background(a_explanation, buff=0.1)

        a_mobs = [mob.copy() for mob in inverse_steiner_formula if mob.get_tex_string() == r"{p_0}"]
        self.play(
            Create(a_explanation_bg), Write(a_explanation),
            *[Transform(a_mob, a_dot) for a_mob in a_mobs], 
            run_time=3
        )
        self.wait()

        # Explain Infinity
        b_explanation = MathTex(
            r"{p_{\infty}} \text{ determines where } \infty \text{ is mapped}",
            substrings_to_isolate=[r"{p_{\infty}}", r"\infty"]
        ).set_color_by_tex_to_color_map(self.color_map)
        b_explanation.scale(0.8).next_to(a_explanation, DOWN, aligned_edge=LEFT).set_z_index(self.LABEL_TEXT_Z_INDEX)
        b_explanation_bg = self.get_label_background(b_explanation, buff=0.1)

        b_mobs = [mob.copy() for mob in inverse_steiner_formula if mob.get_tex_string() == r"{p_{\infty}}"]
        self.play(
            Create(b_explanation_bg), Write(b_explanation),
            *[Transform(b_mob, b_dot) for b_mob in b_mobs], 
            run_time=3
        )
        self.wait()
        
        # Clean up
        self.remove(*a_mobs, *b_mobs)
        self.add(a_dot)
        self.b_real_tracker.set_value(20)
        bg, a_text, b_text = self.get_ab_label()
        self.play(
            b_dot.animate.move_to([20, 0, 0]),
            Create(bg), Write(a_text), Write(b_text),
            Unwrite(a_explanation), FadeOut(a_explanation_bg),
            Unwrite(b_explanation), FadeOut(b_explanation_bg),
            run_time=1.5
        )
        self.wait()
        self.remove(a_dot, b_dot, bg, a_text, b_text)
        self.remove(zero_and_infinity_points, ab_label)

        # For some reason I have to recall this because it adds the initial state to the screen
        # It doesn't add the updated value of b
        ab_label = always_redraw(self.get_ab_label)
        zero_and_infinity_points = always_redraw(self.get_zero_and_infinity_points)
        self.add(zero_and_infinity_points, ab_label)
        
        # Scene 3: Initial Transformation
        self.wait()
        # initial_transformation = self.initial_transformation_old(polar_net, w_plane_text, z_plane_text)
        initial_transformation = self.initial_transformation(polar_net, w_plane_text, z_plane_text)


        
        """
        There is a bug that I don't feel like figuring out where there's a lingering copy of the initial transformation
        so I'm just clearing everything and adding it back
        """
        self.clear()
        self.add(plane)
        self.add(plane_text_bg, z_plane_text)
        self.add(zero_and_infinity_points)
        self.add(ab_label)
        self.add(inverse_steiner_formula, inverse_steiner_bg)

        # General Steiner Net
        def T(z):
            a = self.get_a()
            b = self.get_b()
            k = self.get_k()
            S = MobiusTransformation(k, -k*a, 1, -b).inverse()
            return S(z)

        # Draw the value-tracked Steiner Net
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().set_z_index(self.NET_Z_INDEX).apply_function(lambda p: self.apply_2D_complex_function(T, p)) for mobject in polar_net
        ]))
        self.remove(*initial_transformation)
        self.add(transformed_net)

        # Scene 4: Animate a and b points changing
        self.animate_a_and_b_changing()
        self.play(FadeOut(zero_and_infinity_points), FadeOut(ab_label))


        # Scene 5: Animate k changing
        inverse_steiner_formula_with_k.scale(1/1.2)     # reversing the scaling from the preamble
        self.k_explanation(k_label, inverse_steiner_formula, inverse_steiner_bg, inverse_steiner_formula_with_k)
        self.animate_k_changing()



        # Scene 6: End the video
        self.clear()
        self.thank_you_for_watching()

class SteinerNetThumbnail(SteinerNet):

    def initialize_parameters(self):
        self.a_real_tracker = ValueTracker(-1)
        self.a_imag_tracker = ValueTracker(-1)
        
        self.b_real_tracker = ValueTracker(1)
        self.b_imag_tracker = ValueTracker(0)

        self.k_mod_tracker = ValueTracker(1)
        self.k_arg_tracker = ValueTracker(0)

    def get_a(self):
        return complex(self.a_real_tracker.get_value(), self.a_imag_tracker.get_value())
        # return cmath.rect(self.a_mod_tracker.get_value(), self.a_arg_tracker.get_value() * PI)
    def get_b(self):
        return complex(self.b_real_tracker.get_value(), self.b_imag_tracker.get_value())
        # return cmath.rect(b_mod_tracker.get_value(), b_arg_tracker.get_value() * PI)

    def construct(self):
        
        # Complex plane
        plane, *_ = self.get_complex_plane()
        self.add(plane)
        
        # Steiner Net Title
        steiner_nets_text = MathTex(r"\text{Steiner Nets}").scale(2.2).to_corner(UR).set_z_index(51)
        steiner_nets_text_bg = BackgroundRectangle(
            steiner_nets_text, 
            color=BLACK, 
            fill_opacity=1, 
            stroke_color=WHITE,
            stroke_width=4,
            buff=0.2
        ).set_stroke(color=WHITE, width=4).set_z_index(self.LABEL_BG_Z_INDEX)
        # IDK why this white boarder doesn't work...whatever
        self.add(steiner_nets_text, steiner_nets_text_bg)

        # Polar Net
        polar_net = self.get_polar_net()

        # Parameters
        self.initialize_parameters()

        inverse_steiner_formula_with_k = MathTex(
            r"z = {k} {w - {p_{0}} \over w - {p_{\infty}} }",
            substrings_to_isolate=[r"{k}", r"{p_{0}}", r"{p_{\infty}}"]
        ).set_color_by_tex_to_color_map(self.color_map)
        inverse_steiner_formula_with_k.scale(1.5).set_z_index(self.LABEL_TEXT_Z_INDEX)
        inverse_steiner_with_k_bg = self.get_label_background(inverse_steiner_formula_with_k)
        inverse_steiner_formula_with_k.to_corner(DL).shift(LEFT*0.2)
        inverse_steiner_with_k_bg.move_to(inverse_steiner_formula_with_k.get_center())
        self.add(inverse_steiner_formula_with_k, inverse_steiner_with_k_bg)

        def T(z):
            a = self.get_a()
            b = self.get_b()
            k = self.get_k()
            S = MobiusTransformation(k, -k*a, 1, -b).inverse()
            return S(z)

        # Initial Steiner Net
        transformed_net = [
            mobject.copy().apply_function(lambda p: self.apply_2D_complex_function(T, p)) for mobject in polar_net
        ]
        self.add(*transformed_net)