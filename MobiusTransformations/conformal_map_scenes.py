from manim import *
import numpy as np
from mpmath import mpc

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
            arc.make_smooth()
            arcs.append(arc)
        
        rays = []
        for j, theta in enumerate(ray_func(start_angle, angle, num_ray)):
            if theta == start_angle + angle:
                continue
            start = start_radius*RIGHT*np.cos(theta) + start_radius*UP*np.sin(theta)
            end = radius*RIGHT*np.cos(theta) + radius*UP*np.sin(theta)
            ray = Line(start=start, end=end, color=ray_color[j], stroke_width=1.5)
            ray.insert_n_curves(100)  # Increase the number of Bezier curves (default is 9)
            ray.make_smooth()
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
