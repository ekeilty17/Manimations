from manim import *

from mobius_transformation import MobiusTransformation
from conformal_map_scenes import ConformalMapScenes

import cmath

NUM_SAMPLES = 100

class SteinerNetThumbnail(ConformalMapScenes):

    def get_rectangle_label_text(self, variable_name, real, imag):
        return MathTex(
            f"{variable_name} =", 
            f"{real:.2f}",
            "-" if imag < 0 else "+",
            "i ",
            f"{abs(imag):.2f}",
            substrings_to_isolate=variable_name
        )

    def construct(self):
        
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
        self.add(plane)
        
        steiner_nets_text = MathTex(r"\text{Steiner Nets}").scale(2.2).to_corner(UR).set_z_index(51)
        steiner_nets_text_bg = BackgroundRectangle(
            steiner_nets_text, 
            color=BLACK, 
            fill_opacity=1, 
            stroke_color=WHITE,
            stroke_width=4,
            buff=0.2
        ).set_stroke(color=WHITE, width=4).set_z_index(50)
        # IDK why this white boarder doesn't work...whatever
        
        self.add(steiner_nets_text, steiner_nets_text_bg)

        # Polar Grid
        arc_colors = color_gradient([DARK_BLUE, WHITE], 60)
        ray_colors = color_gradient([YELLOW, WHITE], 25)
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=10, num_arc=41, arc_color=arc_colors,
            angle=2*PI, num_ray=21, ray_color=ray_colors,
            num_sample=NUM_SAMPLES
        )
        net = arcs + rays

        # Parameters
        a_real_tracker = ValueTracker(-1)
        a_imag_tracker = ValueTracker(-1)
        # a_mod_tracker = ValueTracker(1)
        # a_arg_tracker = ValueTracker(0)
        
        b_real_tracker = ValueTracker(1)
        b_imag_tracker = ValueTracker(0)
        # b_mod_tracker = ValueTracker(10)
        # b_arg_tracker = ValueTracker(0)

        k_mod_tracker = ValueTracker(1)
        k_arg_tracker = ValueTracker(0)

        def get_a():
            return complex(a_real_tracker.get_value(), a_imag_tracker.get_value())
            # return cmath.rect(a_mod_tracker.get_value(), a_arg_tracker.get_value() * PI)
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

        inverse_steiner_formula_with_k = MathTex(
            r"z = k {w - a \over w - b}",
            substrings_to_isolate=["k", "a", "b"]
        ).scale(1.8).to_corner(DL).shift(LEFT*0.2)
        inverse_steiner_formula_with_k.set_z_index(50)
        inverse_steiner_formula_with_k.set_color_by_tex("a", RED)
        inverse_steiner_formula_with_k.set_color_by_tex("b", RED)
        inverse_steiner_formula_with_k.set_color_by_tex("k", GREEN)
        inverse_steiner_with_k_bg = BackgroundRectangle(inverse_steiner_formula_with_k, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1).set_z_index(49)
        self.add(inverse_steiner_formula_with_k, inverse_steiner_with_k_bg)

        def T(z):
            a = get_a()
            b = get_b()
            k = get_k()
            S = MobiusTransformation(k, -k*a, 1, -b).inverse()
            return S(z)

        # Initial Steiner Net
        transformed_net = [
            mobject.copy().apply_function(lambda p: self.apply_2D_complex_function(T, p)) for mobject in net
        ]
        self.add(*transformed_net)
        

class SteinerNet(ConformalMapScenes):

    def get_rectangle_label_text(self, variable_name, real, imag):
        return MathTex(
            f"{variable_name} =", 
            f"{real:.2f}",
            "-" if imag < 0 else "+",
            "i ",
            f"{abs(imag):.2f}",
            substrings_to_isolate=variable_name
        )

    def preamble(self):
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
            "Actually, a Steiner Net is produced by the inverse of this",
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

    def construct(self):
        
        self.preamble()

        # Do this for good measure
        self.clear()
        
        # Background complex plane
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
        
        w_plane_text = MathTex(r"w\text{-plane}").to_edge(DOWN).shift(DOWN * 0.2).set_z_index(51)
        plane_text_bg = BackgroundRectangle(w_plane_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1).set_z_index(50)
        z_plane_text = MathTex(r"z\text{-plane}").to_edge(DOWN).shift(DOWN * 0.2).set_z_index(51)
        
        self.play(Create(plane), FadeIn(plane_text_bg), Write(w_plane_text))
        self.wait()

        # Polar Grid
        arc_colors = color_gradient([DARK_BLUE, WHITE], 60)
        ray_colors = color_gradient([YELLOW, WHITE], 25)
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=10, num_arc=41, arc_color=arc_colors,
            angle=2*PI, num_ray=21, ray_color=ray_colors,
            num_sample=NUM_SAMPLES
        )
        net = arcs + rays
        self.play(*[Create(mobject) for mobject in net], run_time=1)
        self.wait()

        inverse_steiner_formula = MathTex(
            # r"z = " + r"{w - a", r"\over", r"w - b}",
            r"z = {w - a \over w - b}",
            # r"z = \frac{w - a}{w - b}",
            substrings_to_isolate=["a", "b"]
        ).scale(1).to_corner(UL)
        inverse_steiner_formula.set_z_index(20)
        inverse_steiner_formula.set_color_by_tex("a", RED)
        inverse_steiner_formula.set_color_by_tex("b", RED)
        inverse_steiner_bg = BackgroundRectangle(inverse_steiner_formula, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        inverse_steiner_formula.set_z_index(30)
        inverse_steiner_bg.set_z_index(29)
        self.play(Write(inverse_steiner_formula), Create(inverse_steiner_bg), run_time=1.5)
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
            a_text = self.get_rectangle_label_text("a", a.real, a.imag)
            a_text.to_corner(UR).shift(LEFT * 0.2).set_color_by_tex("a", RED)

            b = get_b()
            if b_real_tracker.get_value() >= 10:
            # if b_mod_tracker.get_value() >= 10:
                b_text = MathTex("b = \infty", substrings_to_isolate="b")
            else:
                b_text = self.get_rectangle_label_text("b", b.real, b.imag)
            b_text.next_to(a_text, DOWN, aligned_edge=LEFT).set_color_by_tex("b", RED)

            ab_text = VGroup(a_text, b_text)
            bg = BackgroundRectangle(ab_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
            
            label = VGroup(bg, a_text, b_text)
            label.set_z_index(50)

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
            zero_and_infinity_points.set_z_index(50)
            return zero_and_infinity_points
        zero_and_infinity_points = always_redraw(get_zero_and_infinity_points)
        a_dot, b_dot = zero_and_infinity_points
        
        def get_k_label():
            # k = get_k()
            # k_text = self.get_rectangle_label_text("k", k.real, k.imag)
            k_mod_text = MathTex(
                r"|k|", " = ", f"{k_mod_tracker.get_value():.2f}"
            )
            k_mod_text.to_corner(UR).shift(LEFT * 1)
            k_mod_text.set_color_by_tex_to_color_map({
                r"|k|": BLUE,
                # "=": WHITE,
            })
            k_arg_text = MathTex(
                r"\arg ", "k", " = ", f"{k_arg_tracker.get_value():.2f}", r"\pi"
            )
            k_arg_text.next_to(k_mod_text, DOWN, aligned_edge=LEFT)
            k_arg_text.set_color_by_tex_to_color_map({
                r"\arg": YELLOW,
                "k": YELLOW,
                "=": WHITE,
            })

            k_text = VGroup(k_mod_text, k_arg_text)
            k_bg = BackgroundRectangle(k_text, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
            
            label = VGroup(k_bg, k_mod_text, k_arg_text)
            label.set_z_index(50)
            
            return label
        k_label = always_redraw(get_k_label)
        k_bg, k_mod_text, k_arg_text = k_label

        inverse_steiner_formula_with_k = MathTex(
            r"z = k {w - a \over w - b}",
            substrings_to_isolate=["k", "a", "b"]
        ).scale(1).to_corner(UL)
        inverse_steiner_formula_with_k.set_z_index(50)
        inverse_steiner_formula_with_k.set_color_by_tex("a", RED)
        inverse_steiner_formula_with_k.set_color_by_tex("b", RED)
        inverse_steiner_formula_with_k.set_color_by_tex("k", GREEN)
        inverse_steiner_with_k_bg = BackgroundRectangle(inverse_steiner_formula_with_k, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1).set_z_index(49)

        # Zero and Infinity Points explanation
        a_explanation = MathTex(
            r"a \text{ determines where } 0 \text{ is mapped}",
            substrings_to_isolate=["a ", "0"]
        ).scale(0.8).to_edge(RIGHT).shift(DOWN).set_color_by_tex("a ", RED).set_color_by_tex("0", RED)
        a_explanation_bg = BackgroundRectangle(a_explanation, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        a_explanation.set_z_index(50)
        a_explanation_bg.set_z_index(49)

        b_explanation = MathTex(
            r"b \text{ determines where } \infty \text{ is mapped}",
            substrings_to_isolate=["b ", "\infty"]
        ).scale(0.8).next_to(a_explanation, DOWN, aligned_edge=LEFT).set_color_by_tex("b ", RED).set_color_by_tex("\infty", RED)
        b_explanation_bg = BackgroundRectangle(b_explanation, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        b_explanation.set_z_index(50)
        b_explanation_bg.set_z_index(49)

        # animate dots
        self.play(
            Create(a_explanation_bg), Write(a_explanation),
            GrowFromCenter(a_dot), GrowFromCenter(b_dot),#, Create(bg), Write(a_text), Write(b_text),
            run_time=3
        )
        self.wait()
        self.play(
            Create(b_explanation_bg), Write(b_explanation),
            b_dot.animate.move_to([1, 0, 0]),
            run_time=3
        )
        self.wait()
        self.play(b_dot.animate.move_to([10, 0, 0]), run_time=1
        )
        self.wait()
        self.play(
            Create(bg), Write(a_text), Write(b_text),
            Unwrite(a_explanation), FadeOut(a_explanation_bg),
            Unwrite(b_explanation), FadeOut(b_explanation_bg),
            run_time=1.5
        )
        self.wait()
        self.remove(a_dot, b_dot, bg, a_text, b_text)
        self.add(zero_and_infinity_points, ab_label)

        # Initial Steiner Net
        initial_transformation = []
        for mobject in net:
            initial_transformation.append(
                mobject.copy().set_z_index(10).animate.apply_function(lambda p: 
                    self.apply_2D_complex_function(lambda z: MobiusTransformation(1, -1, 1, 1).inverse()(z), p)
                )
            )
        self.remove(*net)
        self.play(
            TransformMatchingShapes(w_plane_text, z_plane_text),
            *initial_transformation, 
            a_mod_tracker.animate.set_value(1), 
            b_real_tracker.animate.set_value(-1),  
            run_time=3
        )
        # b_mod_tracker.animate.set_value(1)
        # b_arg_tracker.animate.set_value(1)
        self.wait()

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
            a = get_a()
            b = get_b()
            k = get_k()
            S = MobiusTransformation(k, -k*a, 1, -b).inverse()
            return S(z)

        # animate mobius transformation
        transformed_net = always_redraw(lambda: VGroup(*[
            mobject.copy().set_z_index(10).apply_function(lambda p: self.apply_2D_complex_function(T, p)) for mobject in net
        ]))
        self.remove(*initial_transformation)
        self.add(transformed_net)

        b_coord = get_b_coord()
        arrow = Arrow(start=b_coord + 0.2*UP, end=b_coord + 1*UP, buff=0, color=RED).set_z_index(50)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(
            FadeOut(arrow), 
            b_imag_tracker.animate.set_value(2), 
            run_time=1
        )

        b_coord = get_b_coord()
        arrow = Arrow(start=b_coord + 0.2*DOWN, end=b_coord + 1*DOWN, buff=0, color=RED).set_z_index(50)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(
            FadeOut(arrow), 
            b_imag_tracker.animate.set_value(-1), 
            run_time=2
        )
        self.wait()

        a = get_a()
        a_coord = np.array([a.real, a.imag, 0])
        arrow = Arrow(start=a_coord + 0.2*RIGHT, end=a_coord + 1*RIGHT, buff=0, color=RED).set_z_index(50)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(
            FadeOut(arrow), 
            a_mod_tracker.animate.set_value(3), 
            run_time=2
        )
        
        a = get_a()
        a_coord = np.array([a.real, a.imag, 0])
        arrow = Arrow(start=a_coord + 0.2*LEFT, end=a_coord + 1*LEFT, buff=0, color=RED).set_z_index(50)
        self.play(GrowArrow(arrow), run_time=1)
        self.play(
            FadeOut(arrow), 
            a_mod_tracker.animate.set_value(-5), 
            run_time=2.5
        )
        self.wait()

        self.play(a_arg_tracker.animate.set_value(1), run_time=3)
        self.play(a_mod_tracker.animate.set_value(-1), run_time=2)
        self.wait()

        self.play(FadeOut(zero_and_infinity_points), FadeOut(ab_label))

        # Put K stuff here
        k_explanation = MathTex(r"\text{Let's see how } k \text{ affects the map}", substrings_to_isolate="k").scale(0.8).to_edge(RIGHT).shift(DOWN).set_color_by_tex("k", GREEN)
        k_explanation_bg = BackgroundRectangle(k_explanation, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        k_explanation.set_z_index(50)
        k_explanation_bg.set_z_index(50)

        self.play(
            Create(k_explanation_bg), Write(k_explanation),
            TransformMatchingShapes(inverse_steiner_formula, inverse_steiner_formula_with_k),
            Transform(inverse_steiner_bg, inverse_steiner_with_k_bg)
        )
        self.wait()
        self.play(
            Create(k_bg), Write(k_mod_text), Write(k_arg_text)
        )
        self.wait()
        self.remove(k_mod_text, k_arg_text, k_bg)
        self.add(k_label)
        self.wait()

        k_mod_explanation = MathTex(r"|k|", r"\text{ cycles the blue lines}").scale(0.8).next_to(k_explanation, DOWN, aligned_edge=LEFT)
        k_mod_explanation.set_color_by_tex_to_color_map({
                r"|k|": BLUE,
                r"\text{ cycles the blue lines}": WHITE,
            })
        k_mod_explanation_bg = BackgroundRectangle(k_mod_explanation, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        k_mod_explanation.set_z_index(50)
        k_mod_explanation_bg.set_z_index(49)
        self.play(Create(k_mod_explanation_bg), Write(k_mod_explanation))
        self.wait()

        k_arg_explanation = MathTex(r"\arg", "k", r"\text{ cycles the yellow lines}").scale(0.8).next_to(k_mod_explanation, DOWN, aligned_edge=LEFT)
        k_arg_explanation.set_color_by_tex_to_color_map({
                r"\arg": YELLOW,
                "k": YELLOW,
                r"\text{ cycles the yellow lines}": WHITE,
            })
        k_arg_explanation_bg = BackgroundRectangle(k_arg_explanation, color=BLACK, fill_opacity=1, stroke_width=4, buff=0.1)
        k_arg_explanation.set_z_index(50)
        k_arg_explanation_bg.set_z_index(49)
        self.play(Create(k_arg_explanation_bg), Write(k_arg_explanation))
        self.wait()
        self.play(
            FadeOut(k_explanation_bg), Unwrite(k_explanation),
            FadeOut(k_mod_explanation_bg), Unwrite(k_mod_explanation),
            FadeOut(k_arg_explanation_bg), Unwrite(k_arg_explanation)
        )
        self.wait()

        self.play(k_mod_tracker.animate.set_value(0.6), run_time=3)
        self.wait()

        self.play(k_mod_tracker.animate.set_value(5), run_time=8)
        self.wait()

        self.play(k_arg_tracker.animate.set_value(1), run_time=10)
        self.wait()
        self.wait()

        # End the video
        self.clear()

        thankyou_text = Text("Thanks for Watching!")
        self.play(FadeIn(thankyou_text))
        self.wait()