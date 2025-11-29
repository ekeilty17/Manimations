import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop15(GreekConstructionScenes):

    title = "Book 1 Proposition 15"
    description = """
        If two straight-lines cut one another then 
        they make the vertically opposite angles 
        equal to one another.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DL)
        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, DR)
        
        line_AB = Line(A.get_center(), B.get_center())
        line_CD = Line(C.get_center(), D.get_center())

        givens = (
            A, B, C, D,
            label_A, label_B, label_C, label_D,
            line_AB, line_CD
        )
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            A, B, C, D,
            label_A, label_B, label_C, label_D,
            line_AB, line_CD
        ) = givens
        
        E_pos = get_line_line_intersection(line_AB, line_CD)
        E, label_E = self.get_dot_and_label("E", E_pos, DL)

        angle_AEC = get_angle_marker(line_AB, line_CD.copy().rotate(PI), marker_type="))")
        angle_BED = get_angle_marker(line_AB.copy().rotate(PI), line_CD, marker_type="))")

        angle_AED = get_angle_marker(line_AB, line_CD, marker_type="(")
        angle_BEC = get_angle_marker(line_AB.copy().rotate(PI), line_CD.copy().rotate(PI), marker_type="(")

        intermediaries = (
            E, label_E,
            angle_AEC, angle_AED, angle_BED, angle_BEC
        )
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"<CEA + <AED = \rightanglesqr + \rightanglesqr", "[Prop. 1.13]"),
            (r"<AED + <DEB = \rightanglesqr + \rightanglesqr", "[Prop. 1.13]"),
            (r"<CEA + <AED \\ = <AED + <DEB", "[CN. 1]"),
            (r"<CEA = <DEB", "[CN. 3]", self.SOLUTION),
            (r"<BEC + <CEA = \rightanglesqr + \rightanglesqr", "[Prop. 1.13]"),
            (r"<CEA + <AED \\ = <BEC + <CEA", "[CN. 1]"),
            (r"<AED = <BEC", "[CN. 3]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*UP + 2*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2*RIGHT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*LEFT)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*RIGHT)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(0.9, center_horizontally=True)

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