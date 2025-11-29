import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop27(GreekConstructionScenes):

    title = "Book 1 Proposition 27"
    description = """
        If a straight-line falling across two straight-lines 
        makes the alternate angles equal to one another 
        then the (two) straight-lines will be parallel to
        one another.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", A.get_center() + self.parallel_line_length.get_value() * RIGHT, UP)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DOWN)
        D, label_D = self.get_dot_and_label("D", C.get_center() + self.parallel_line_length.get_value() * RIGHT, DOWN)
        
        line_AB = Line(A.get_center(), B.get_center())
        line_CD = Line(C.get_center(), D.get_center())

        _, E, _ = interpolate_line(line_AB, self.E_percentage.get_value())
        E, label_E = self.get_dot_and_label("E", E.get_center(), UL)

        _, F, _ = interpolate_line(line_CD, self.F_percentage.get_value())
        F, label_F = self.get_dot_and_label("F", F.get_center(), DR)

        line_EF = Line(E.get_center(), F.get_center())
        temp_line_1, temp_line_2 = extend_line_by_length(line_EF, 1)
        line_EF_extended = Line(temp_line_1.get_end(), temp_line_2.get_end())

        angle_AEF_marker = get_angle_marker(line_AB, line_EF, marker_type=")")
        angle_EFD_marker = get_angle_marker(line_EF, line_CD, marker_type="(")

        G, label_G = self.get_dot_and_label("G", (B.get_center() + D.get_center()) / 2 + 1.5*RIGHT, RIGHT, color=self.color_map[self.IMPOSSIBLE])
        line_BG = Line(B.get_center(), G.get_center(), color=self.color_map[self.IMPOSSIBLE])
        line_DG = Line(D.get_center(), G.get_center(), color=self.color_map[self.IMPOSSIBLE])

        line_AB_marker = get_line_marker(line_AB, marker_type=">", position=0.7)
        line_CD_marker = get_line_marker(line_CD, marker_type=">", position=0.7)

        givens = (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_CD, line_EF_extended,
        )
        intermediaries = (
            G, label_G,
            line_BG, line_DG,
            line_AB_marker, line_CD_marker,
            angle_AEF_marker, angle_EFD_marker
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"<AEF ~= <EFD", "[Given]", self.GIVEN),
            (r"|AB !|| |CD", "[Assumption]", self.ASSUMPTION),
            (r"<AEF > <EFG", "[Prop. 1.16]", self.CONTRADICTION),
            (r"|AB || |CD", "[Contradiction]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + UP + 2.5*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*DOWN + 2.5*LEFT)
        
        self.parallel_line_length = ValueTracker(3.5)
        self.E_percentage = ValueTracker(0.5)
        self.F_percentage = ValueTracker(0.3)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()

        """ Construction Variables """
        # () = self.givens
        # () = self.given_intermediaries
        # () = self.solution_intermediaries
        # () = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        self.custom_play(*Animate(title, description))
        self.wait(3)
        self.custom_play(*Unanimate(title, description))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        self.add(*self.solution_intermediaries, *self.solution)
        self.add(proof_lines)
        self.wait()