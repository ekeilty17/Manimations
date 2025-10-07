import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

import random

class Book1Definitions(GreekConstructionScenes):

    def interpolate(self, start, end, alpha):
        return start + alpha * (end - start)

    def wiggle_line_func(self, alpha, a=-0.25, b=3, c=0.1):
        return (
            a * np.sin(np.pi * alpha)
            + b * (alpha ** 3 - alpha ** 2)
            + c * (np.sin(6 * np.pi * alpha))
        )

    def wiggly_line_point(self, start, end, alpha, a, b, c):
        direction = end - start
        length = np.linalg.norm(direction)
        unit_dir = direction / length
        perp = np.array([-unit_dir[1], unit_dir[0], 0])  # perpendicular in 2D
        base_point = self.interpolate(start, end, alpha)
        offset = self.wiggle_line_func(alpha, a, b, c)
        return base_point + offset * perp

    def get_wiggly_line_points(self, start, end, num_points, a=-0.25, b=3, c=0.1):
        return [self.wiggly_line_point(start, end, i / (num_points - 1), a, b, c) for i in range(num_points)]

    def wiggle_surface_func(self, start1, start2, end1, end2, u, v, a=-0.25, b=3, c=0.1):
        p1 = self.wiggly_line_point(start1, end1, u, a, b, c)
        p2 = self.wiggly_line_point(start2, end2, v, a, b, c)
        
        return p1 + (p2 - start2)

    def create_wiggly_line(self, start, end, num_points=100, a=-0.25, b=3, c=0.1):
        points = self.get_wiggly_line_points(start, end, num_points, a, b, c)
        wiggly_line = VMobject(fill_opacity=0, stroke_opacity=1)
        wiggly_line.set_points_smoothly(points)
        return wiggly_line

    def create_wiggly_surface(self, start1, start2, end1, end2, a=-0.25, b=3, c=0.1):
        surface = Surface(
            lambda u, v: self.wiggle_surface_func(start1, start2, end1, end2, u, v, a, b, c),
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(50, 50)
        )
        surface.set_style(
            fill_color=GREY,
            fill_opacity=1.0,
            stroke_color=GREY,
            stroke_opacity=1.0,
        )
        return surface

    def definition_1_2_3_4_5_6_7(self):
        descriptions = [
            "A point is that of which there is no part",
            "A line is a length without breadth",
            "The extremities of a line are points",
            "A straight-line is (any) one which\nlies evenly with points on itself",
            "A surface is that which has\nlength and breadth only",
            "The extremities of a surface are lines",
            "A plane surface is (any) one which lies\nevenly with the straight-lines on itself"
        ]
        titles = [f"Defintion {i+1}" for i in range(len(descriptions))]
        explainations = [self.get_explanation(description, title=title) for title, description in zip(titles, descriptions)]

        B, _ = self.get_dot_and_label("B", self.RIGHT_CENTER+2*LEFT+0.5*DOWN, DOWN)
        C, _ = self.get_dot_and_label("C", self.RIGHT_CENTER+3*RIGHT+0.5*UP, DOWN)

        line_BC = Line(B.get_center(), C.get_center())
        line_BA, A, line_AC = interpolate_line(line_BC)
        line_AB = line_BA.copy().rotate(PI)
        
        wiggly_line_AB = self.create_wiggly_line(A.get_center(), B.get_center())
        wiggly_line_AC = self.create_wiggly_line(A.get_center(), C.get_center())

        D, _ = self.get_dot_and_label("D", self.RIGHT_CENTER+2.5*LEFT+2*DOWN, DOWN)
        E, _ = self.get_dot_and_label("E", self.RIGHT_CENTER+2*RIGHT+2*DOWN, DOWN)
        F, _ = self.get_dot_and_label("F", self.RIGHT_CENTER+2*LEFT+2.5*UP, DOWN)
        G, _ = self.get_dot_and_label("G", self.wiggle_surface_func(D.get_center(), D.get_center(), E.get_center(), F.get_center(), 1, 1) )

        wiggly_line_DE = self.create_wiggly_line(D.get_center(), E.get_center())
        wiggly_line_DF = self.create_wiggly_line(D.get_center(), F.get_center())
        wiggly_line_EG = self.create_wiggly_line(E.get_center(), G.get_center())
        wiggly_line_FG = self.create_wiggly_line(F.get_center(), G.get_center())
        wiggly_surface = self.create_wiggly_surface(D.get_center(), D.get_center(), E.get_center(), F.get_center())

        line_DE = self.create_wiggly_line(D.get_center(), E.get_center(), a=0, b=0, c=0)
        line_DF = self.create_wiggly_line(D.get_center(), F.get_center(), a=0, b=0, c=0)
        line_EG = self.create_wiggly_line(E.get_center(), G.get_center(), a=0, b=0, c=0)
        line_FG = self.create_wiggly_line(F.get_center(), G.get_center(), a=0, b=0, c=0)
        surface = self.create_wiggly_surface(D.get_center(), D.get_center(), E.get_center(), F.get_center(), a=0, b=0, c=0)

        self.custom_play(*Animate(explainations[0]), Animate(A))
        self.wait()
        self.custom_play(
            ReplacementTransform(explainations[0], explainations[1]),
            Create(wiggly_line_AB), Create(wiggly_line_AC),
            ShrinkToCenter(A)
        )
        self.wait()
        self.custom_play(
            ReplacementTransform(explainations[1], explainations[2]),
            *Animate(B, C)
        )
        self.wait()
        self.custom_play(
            ReplacementTransform(explainations[2], explainations[3]),
            ReplacementTransform(wiggly_line_AB, line_AB),
            ReplacementTransform(wiggly_line_AC, line_AC)
        )
        self.wait()
        self.add(line_BC)
        self.remove(line_AB, line_AC)
        self.custom_play(
            ReplacementTransform(explainations[3], explainations[4]),
            ReplacementTransform(line_BC, wiggly_surface),
            ShrinkToCenter(B), ShrinkToCenter(C)
        )
        self.wait()
        self.custom_play(
            ReplacementTransform(explainations[4], explainations[5]),
            Create(wiggly_line_DE), Create(wiggly_line_DF), Create(wiggly_line_EG), Create(wiggly_line_FG), 
            # GrowFromCenter(D), GrowFromCenter(E), GrowFromCenter(F), GrowFromCenter(G)
        )

        self.wait()
        self.custom_play(
            ReplacementTransform(explainations[5], explainations[6]),
            ReplacementTransform(wiggly_surface, surface),
            ReplacementTransform(wiggly_line_DE, line_DE), 
            ReplacementTransform(wiggly_line_DF, line_DF), 
            ReplacementTransform(wiggly_line_EG, line_EG),
            ReplacementTransform(wiggly_line_FG, line_FG),
        )

        self.wait()

    def construct(self):
        self.definition_1_2_3_4_5_6_7()