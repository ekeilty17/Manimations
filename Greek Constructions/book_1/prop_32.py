import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop32(GreekConstructionScenes):

    title = "Book 1 Proposition 32"
    description = """
        In any triangle, (if) one of the sides 
        (is) produced (then) the external angle 
        is equal to the (sum of the) two internal 
        and opposite (angles), and the (sum of 
        the) three internal angles of the triangle 
        is equal to two right-angles.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)

        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)

        _, line_CD = extend_line_by_length(line_BC, self.line_CD_length.get_value())
        D, label_D = self.get_dot_and_label("D", line_CD.get_end(), RIGHT, buff=SMALL_BUFF)

        line_EC = line_AB.copy().shift(C.get_center() - B.get_center())
        E, label_E = self.get_dot_and_label("E", line_EC.get_start(), UR, buff=SMALL_BUFF)

        line_AB_marker = get_line_marker(line_AB, marker_type="<")
        line_CE_marker = get_line_marker(line_EC, marker_type="<")

        angle_BAC_marker = get_angle_marker(line_CA, line_AB, marker_type="(")
        angle_ACE_marker = get_angle_marker(line_EC, line_CA, marker_type=")")

        angle_ABC_marker = get_angle_marker(line_AB, line_BC, marker_type="((")
        angle_ECD_marker = get_angle_marker(line_EC, line_CD, marker_type="((")

        angle_ACB_marker = get_angle_marker(line_BC, line_CA, marker_type="(((")

        givens = (
            A, B, C,
            label_A, label_B, label_C, label_D,
            line_AB, line_BC, line_CA, line_CD,
        )
        intermediaries = (
            label_E,
            line_EC,
            line_AB_marker, line_CE_marker,
            angle_ABC_marker, angle_ACB_marker, angle_ACE_marker, angle_BAC_marker, angle_ECD_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AB ~= |EC", "[Prop. 1.31]"), 
            (r"<BAC ~= <ACE", "[Prop. 1.29]"),
            (r"<ABC ~= <ECD", "[Prop. 1.29]"),
            (r"<BAC + <ABC \\ ~= <ACE + <ECD", "[CN. 2]"),
            (r"<BAC + <ABC ~= <ACD", "[Construction]"),
            (r"<ACB + <ACD ~= \rightanglesqr + \rightanglesqr", "[Prop. 1.13]"),
            (r"<ACB + <BAC + <ABC \\ ~= <ACB + <ACD", "[CN. 2]"),
            (r"<BAC + <ABC + <BCA \\ ~= \rightanglesqr + \rightanglesqr", "[CN. 1]", self.SOLUTION)
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 1*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2.75*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 0*RIGHT)

        self.line_CD_length = ValueTracker(3)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(0.85)

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