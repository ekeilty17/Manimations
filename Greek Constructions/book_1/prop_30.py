import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop29(GreekConstructionScenes):

    title = "Book 1 Proposition 2"
    description = """
        (Straight-lines) parallel to the same 
        straight-line are also parallel to one 
        another.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, LEFT, buff=SMALL_BUFF)
        B, label_B = self.get_dot_and_label("B", A.get_center() + self.parallel_line_length.get_value() * RIGHT, RIGHT, buff=SMALL_BUFF)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, LEFT, buff=SMALL_BUFF)
        D, label_D = self.get_dot_and_label("D", C.get_center() + self.parallel_line_length.get_value() * RIGHT, RIGHT, buff=SMALL_BUFF)
        E, label_E = self.get_dot_and_label("E", self.Ex.get_value() * RIGHT + self.Ey.get_value() * UP, LEFT, buff=SMALL_BUFF)
        F, label_F = self.get_dot_and_label("F", E.get_center() + self.parallel_line_length.get_value() * RIGHT, RIGHT, buff=SMALL_BUFF)

        line_AB = Line(A.get_center(), B.get_center())
        line_CD = Line(C.get_center(), D.get_center())
        line_EF = Line(E.get_center(), F.get_center())

        _, G, _ = interpolate_line(line_AB, self.G_percentage.get_value())
        G, label_G = self.get_dot_and_label("G", G.get_center(), UL)

        _, K, _ = interpolate_line(line_CD, self.K_percentage.get_value())
        K, label_K = self.get_dot_and_label("K", K.get_center(), UL)

        line_GK = Line(G.get_center(), K.get_center())
        transversal_extend_length = (self.transversal_length.get_value() - line_GK.get_length()) / 2
        line_G_extended, line_H_extended = extend_line_by_length(line_GK, transversal_extend_length)
        line_GK_extended = Line(line_G_extended.get_end(), line_H_extended.get_end())

        H_pos = get_line_line_intersection(line_EF, line_GK_extended)
        H, label_H = self.get_dot_and_label("H", H_pos, UL)

        line_AB_marker = get_line_marker(line_AB, marker_type=">", position=0.7)
        line_CD_marker = get_line_marker(line_CD, marker_type=">", position=0.7)
        line_EF_marker = get_line_marker(line_EF, marker_type=">", position=0.7)

        line_CD_marker_2 = get_line_marker(line_CD, marker_type=">>", position=0.8)
        line_EF_marker_2 = get_line_marker(line_EF, marker_type=">>", position=0.8)

        line_AB_marker_3 = get_line_marker(line_AB, marker_type=">>>", position=0.9)
        line_CD_marker_3 = get_line_marker(line_CD, marker_type=">>>", position=0.9)

        angle_AGK_marker = get_angle_marker(line_AB, line_GK, marker_type=")")
        angle_GHF_marker = get_angle_marker(line_GK, line_EF, marker_type="(")
        angle_GKD_marker = get_angle_marker(line_GK, line_CD, marker_type="(")

        givens = (
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_CD, line_EF,
        )
        intermediaries = (
            G, H, K,
            label_G, label_H, label_K,
            line_GK_extended,
            line_AB_marker, line_AB_marker_3, line_CD_marker_2, line_CD_marker_3, line_EF_marker, line_EF_marker_2,
            angle_AGK_marker, angle_GHF_marker, angle_GKD_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AB || |EF", "[Given]", self.GIVEN),
            (r"|CD || |EF", "[Given]", self.GIVEN),
            (r"<AGK ~= <GHF", "[Prop. 1.27]"),
            (r"<GHF ~= <GKD", "[Prop. 1.29]"),
            (r"|AB || |CD", "[Prop. 1.27]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 3*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0*UP + 3*LEFT)
        self.Ex, self.Ey, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1*UP + 3*LEFT)
        
        self.parallel_line_length = ValueTracker(6)
        self.transversal_length = ValueTracker(5)
        self.G_percentage = ValueTracker(0.5)
        # self.H_percentage = ValueTracker(0.5)
        self.K_percentage = ValueTracker(0.3)

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