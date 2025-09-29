import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Postulates(GreekConstructionScenes):

    description = """
        1. Let it have been postulated to draw a straight-line from any point to any point.
        2. And to produce a finite straight-line continuously in a straight-line.
        3. And to draw a circle with any center and radius.
        4. And that all right-angles are equal to one another.
        5. And that if a straight-line falling across two (other) straight-lines makes internal angles on the same side
           (of itself whose sum is) less than two right-angles, then the two (other) straight-lines, being produced to infinity,
           meet on that side (of the original straight-line) that the (sum of the internal angles) is less than two right-angles
           (and do not meet on the other side).
    """

    def postulate_1(self):
        title, description = self.initialize_introduction(
            "Postulate 1",
            "A straight-line can be drawn\nbetween any two points"
        )

        A, label_A = self.get_dot_and_label("A", self.RIGHT_CENTER + LEFT + DOWN, DOWN)
        B, label_B = self.get_dot_and_label("B", self.RIGHT_CENTER + RIGHT, DOWN)
        line_AB = Line(A.get_center(), B.get_center())
        line_A, line_B = extend_line_by_length(line_AB, 10)
        extended_line_AB = Line(line_A.get_end(), line_B.get_end())

        self.format_givens(A, label_A, B, label_B)
        self.format_solution(extended_line_AB)

        self.add(A, B, label_A, label_B)
        self.play(Write(title))
        self.play(Write(description))
        self.play(Create(extended_line_AB))
        
        self.wait()
        self.play(Unanimate(*[title, description, A, B, label_A, label_B, line_AB, extended_line_AB]))
        self.wait()

    def postulate_2(self):
        title, description = self.initialize_introduction(
            "Postulate 2",
            "A finite straight-line can be segmented\nwithin a straight-line"
        )

        A, label_A = self.get_dot_and_label("A", self.RIGHT_CENTER + LEFT + DOWN, DOWN, z_index=self.solution_z_index)
        B, label_B = self.get_dot_and_label("B", self.RIGHT_CENTER + RIGHT, DOWN, z_index=self.solution_z_index)
        line_AB = Line(A.get_center(), B.get_center())
        line_A, line_B = extend_line_by_length(line_AB, 10)
        extended_line_AB = Line(line_A.get_end(), line_B.get_end())

        self.format_givens(extended_line_AB)
        self.format_solution(line_AB)

        self.add(extended_line_AB)
        self.play(Write(title))
        self.play(Write(description))
        self.play(Animate(A, B, label_A, label_B))
        self.play(Create(line_AB))
        
        self.wait()
        self.play(Unanimate(*[title, description, A, B, label_A, label_B, line_AB]))
        self.wait()

    def postulate_3(self):
        title, description = self.initialize_introduction(
            "Postulate 3",
            "A circle can be drawn\ngiven a center and a radius"
        )

        A, label_A = self.get_dot_and_label("A", self.RIGHT_CENTER + LEFT + DOWN, DL, z_index=self.solution_z_index)
        B, label_B = self.get_dot_and_label("B", self.RIGHT_CENTER + RIGHT, UR)
        line_AB = Line(A.get_center(), B.get_center())

        circle_A = OrientedCircle(A.get_center(), B.get_center())
        self.format_givens(A, label_A, B, label_B, line_AB)
        self.format_solution(circle_A)

        self.add(A, label_A, B, label_B, line_AB)
        self.play(Write(title))
        self.play(Write(description))
        self.play(Animate(circle_A))
        
        self.wait()
        self.play(Unanimate(*[title, description, A, B, label_A, label_B, line_AB, circle_A]))
        self.wait()

    def postulate_4(self):
        title, description = self.initialize_introduction(
            "Postulate 4",
            "All right-angles are equal"
        )

    def postulate_5(self):
        title, description = self.initialize_introduction(
            "Postulate 5",
            "Two straight-lines whose internal angles\nhave a sum of less than two right angles\neventually meet"
        )

    def postulate_5_modern(self):
        title, description = self.initialize_introduction(
            "Postulate 5 (Modern Version)",
            "Given any straight-line and any point, there is exactly 1 parallel straight-line which goes through that point"
        )

    def construct(self):
        # self.postulate_1()
        # self.postulate_2()
        # self.postulate_3()
        # self.postulate_4()
        self.postulate_5()