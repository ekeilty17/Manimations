import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop18(GreekConstructionScenes):

    title = "Book 1 Proposition 18"
    description = """
        In any triangle, the greater side subtends 
        the greater angle.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DOWN)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DOWN)
        
        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)

        _, line_AD = extend_line_by_length(line_CA, line_AB.get_length(), switch_direction=True)
        D, label_D = self.get_dot_and_label("D", line_AD.get_end(), UR)
        line_BD = Line(B.get_center(), D.get_center())

        line_AB_marker = get_line_marker(line_AB, marker_type="|")
        line_AD_marker = get_line_marker(line_AD, marker_type="|")

        angle_ABD_marker = get_angle_marker(line_AB, line_BD, marker_type="(")
        angle_ADB_marker = get_angle_marker(line_AD, line_BD.copy().rotate(PI), marker_type=")")

        givens = (
            A, B, C,
            label_A, label_B, label_C, 
            line_AB, line_BC, line_CA, 
        )
        intermediaries = (
            D, label_D, 
            line_BD, 
            line_AB_marker, line_AD_marker,
            angle_ABD_marker, angle_ADB_marker
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AC > |AB", "[Given]", self.GIVEN),
            (r"|AB ~= |AD", "[Prop. 1.3]"),
            (r"<ABD ~= <ADB", "[Prop. 1.5]"),
            (r"<ADB > <C", "[Prop. 1.16]"),
            (r"<ABD > <C", "[CN. 1]"),
            (r"<ABC > <ABD", "[Construction]"),
            (r"<ABC > <C", "[CN. 1]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*UP + 2.5*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.5*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.5*RIGHT)

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