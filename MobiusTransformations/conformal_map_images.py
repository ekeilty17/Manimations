from manim import *

from mobius_transformation import MobiusTransformation
from conformal_map_scenes import ConformalMapScenes

import cmath

NUM_SAMPLES = 100

class PolarNetImage(ConformalMapScenes):

    def construct(self):
        arc_colors = BLUE
        ray_colors = YELLOW
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=3.9, num_arc=21, arc_color=arc_colors,
            angle=2*PI, num_ray=21, ray_color=ray_colors,
            num_sample=NUM_SAMPLES
        )
        net = VGroup(*(arcs + rays))
        self.add(net)

class SteinerNetImage(ConformalMapScenes):

    def construct(self):
        
        # Polar Grid
        arc_colors = DARK_BLUE
        ray_colors = YELLOW
        arcs, rays = self.get_polar_net(
            start_radius=0, radius=10, num_arc=41, arc_color=arc_colors,
            angle=2*PI, num_ray=21, ray_color=ray_colors,
            num_sample=NUM_SAMPLES
        )
        net = VGroup(*(arcs + rays))

        # clip_box = Square(4).set_color(WHITE).set_stroke(opacity=0.5)
        # masks = self.create_masks_around_box(clip_box, color=BLACK)

        # # Add the elements in appropriate layering order
        # self.add(clip_box, *masks)

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

        def T(z):
            a = get_a()
            b = get_b()
            k = get_k()
            S = MobiusTransformation(k, -k*a, 1, -b).inverse()
            return S(z)

        # Initial Steiner Net
        transformed_net = VGroup(*[
            mobject.copy().apply_function(lambda p: self.apply_2D_complex_function(T, p)) for mobject in net
        ])
        self.add(*transformed_net)

class SteinerNet2PolarNetImage(ConformalMapScenes):

    def construct(self):
        polar_net_image = ImageMobject("YouTube/PolarNet.png").set(height=4.5)
        polar_net_border = SurroundingRectangle(
            polar_net_image,
            color=WHITE,
            buff=0.1,
            stroke_width=1
        )
        polar_net = Group(polar_net_image, polar_net_border)
        polar_net.move_to(ORIGIN + 4.25*RIGHT)
        self.add(polar_net)


        steiner_net_image = ImageMobject("YouTube/SteinerNet.png").set(height=4.5)
        steiner_net_border = SurroundingRectangle(
            steiner_net_image,
            color=WHITE,
            buff=0.1,
            stroke_width=1
        )
        steiner_net = Group(steiner_net_image, steiner_net_border)
        steiner_net.move_to(ORIGIN + 4.25*LEFT)
        self.add(steiner_net)

        curved_arrow = Arrow(
            start=1*LEFT+SMALL_BUFF*DOWN,
            end=1*RIGHT+SMALL_BUFF*DOWN,
            path_arc=-PI/4,
            stroke_width=4,
            color=WHITE,
            buff=0,
            tip_length=0.3
        )
        self.add(curved_arrow)

        # steiner_equation = MathTex(
        #     r"w = k \frac{z - a}{z - b}"
        # ).next_to(curved_arrow, UP, buff=0.5)
        # self.add(steiner_equation)
