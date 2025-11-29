import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop28(GreekConstructionScenes):

    title = "Book 1 Proposition 28 (Part 2)"
    description = """
        If a straight-line falling across two straight-lines
        (makes) the (sum of the) internal (angles) on the 
        same side equal to two rightangles, then the (two) 
        straight-lines will be parallel to one another.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP, buff=SMALL_BUFF)
        B, label_B = self.get_dot_and_label("B", A.get_center() + self.parallel_line_length.get_value() * RIGHT, UP, buff=SMALL_BUFF)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DOWN, buff=SMALL_BUFF)
        D, label_D = self.get_dot_and_label("D", C.get_center() + self.parallel_line_length.get_value() * RIGHT, DOWN, buff=SMALL_BUFF)
        
        line_AB = Line(A.get_center(), B.get_center())
        line_CD = Line(C.get_center(), D.get_center())

        _, G, _ = interpolate_line(line_AB, self.G_percentage.get_value())
        G, label_G = self.get_dot_and_label("G", G.get_center(), UL)
        label_G.shift(MED_SMALL_BUFF * LEFT)

        _, H, _ = interpolate_line(line_CD, self.H_percentage.get_value())
        H, label_H = self.get_dot_and_label("H", H.get_center(), DL)

        line_GH = Line(G.get_center(), H.get_center())
        transversal_extend_length = (self.transversal_length.get_value() - line_GH.get_length()) / 2
        line_GE, line_HF = extend_line_by_length(line_GH, transversal_extend_length)
        E, label_E = self.get_dot_and_label("E", line_GE.get_end(), UR)
        F, label_F = self.get_dot_and_label("F", line_HF.get_end(), DR)
        line_EF = Line(E.get_center(), F.get_center())

        line_AB_marker = get_line_marker(line_AB, marker_type=">", position=0.7)
        line_CD_marker = get_line_marker(line_CD, marker_type=">", position=0.7)

        angle_GHD_marker = get_angle_marker(line_GH, line_CD, marker_type="(")
        angle_AGH_marker = get_angle_marker(line_AB, line_GH, marker_type=")")

        givens = (
            G, H,
            label_A, label_B, label_C, label_D, label_E, label_F, label_G, label_H,
            line_AB, line_CD, line_EF,
        )
        intermediaries = (
            line_AB_marker, line_CD_marker,
            angle_AGH_marker, angle_GHD_marker, 
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"<BGH + <GHD = \rightanglesqr + \rightanglesqr", "[Given]", self.GIVEN),
            (r"<AGH + <BGH = \rightanglesqr + \rightanglesqr", "[Prop. 1.13]"),
            (r"<GHD = \rightanglesqr + \rightanglesqr - <BGH", "[CN. 3]"),
            (r"<AGH = \rightanglesqr + \rightanglesqr - <BGH", "[CN. 3]"),
            (r"<AGH = <GHD", "[CN. 1]"),
            (r"|AB || |CD", "[Prop. 1.27]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*UP + 3*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0*DOWN + 3*LEFT)
        
        self.parallel_line_length = ValueTracker(6)
        self.transversal_length = ValueTracker(5)
        self.G_percentage = ValueTracker(0.35)
        self.H_percentage = ValueTracker(0.55)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(0.9)

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