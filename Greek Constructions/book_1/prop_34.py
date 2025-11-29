import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop34(GreekConstructionScenes):

    title = "Book 1 Proposition 34"
    description = """
        In parallelogrammic figures the opposite 
        sides and angles are equal to one another, 
        and a diagonal cuts them in half.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, UP)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DOWN)
        
        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)

        line_CD = line_AB.copy().shift(C.get_center() - A.get_center())
        D, label_D = self.get_dot_and_label("D", line_CD.get_end(), DOWN)

        line_DB = Line(D.get_center(), B.get_center())

        line_AB_parallel_marker = get_line_marker(line_AB, marker_type=">")
        line_CD_parallel_marker = get_line_marker(line_CD, marker_type=">")
        line_CA_parallel_marker = get_line_marker(line_CA, marker_type=">>")
        line_DB_parallel_marker = get_line_marker(line_DB, marker_type=">>")

        line_BC_marker = get_line_marker(line_BC, marker_type="/")
        line_AB_marker = get_line_marker(line_AB, marker_type="//", position=0.675)
        line_CD_marker = get_line_marker(line_CD, marker_type="//", position=0.675)
        line_CA_marker = get_line_marker(line_CA, marker_type="///", position=0.675)
        line_DB_marker = get_line_marker(line_DB, marker_type="///", position=0.675)

        angle_ABC_marker = get_angle_marker(line_AB, line_BC, marker_type=")")
        angle_DCB_marker = get_angle_marker(line_BC, line_CD, marker_type="(")
        angle_ACB_marker = get_angle_marker(line_BC, line_CA, marker_type="))")
        angle_CBD_marker = get_angle_marker(line_DB, line_BC, marker_type="((")
        angle_BAC_marker = get_angle_marker(line_CA, line_AB, marker_type=")))")
        angle_BDC_marker = get_angle_marker(line_CD, line_DB, marker_type="(((")

        givens = (
            A, B, C, D,
            label_A, label_B, label_C, label_D,
            line_AB, line_CA, line_CD, line_DB
        )
        intermediaries = (
            line_BC,
            line_AB_marker, line_BC_marker, line_CA_marker, line_CD_marker, line_DB_marker, 
            line_AB_parallel_marker, line_CA_parallel_marker, line_CD_parallel_marker, line_DB_parallel_marker,
            angle_ABC_marker, angle_ACB_marker, angle_BAC_marker, angle_BDC_marker, angle_CBD_marker, angle_DCB_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"ABDC \text{ is a parallelogram}", "[Given]", self.GIVEN),
            (r"|AB || |CD", "[Given]", self.GIVEN),
            (r"|AC || |BD", "[Given]", self.GIVEN),
            (r"<ABC ~= <BCD", "[Prop. 1.29]"),
            (r"<ACB ~= <CBD", "[Prop. 1.29]"),
            (r"|BC ~= |CB", "[Reflexivity]"), 
            (r"^ABC ~= ^DCB", "[Prop. 1.26]", self.SOLUTION),
            (r"|AB ~= |CD", "[Prop. 1.26]", self.SOLUTION),
            (r"|AC ~= |BD", "[Prop. 1.26]", self.SOLUTION),
            (r"<BAC ~= <CDB", "[Prop. 1.29]", self.SOLUTION),
            (r"<ABC + <CBD \\ ~= <ACB + <BCD", "[CN. 2]"),
            (r"<ABD ~= <ACD", "[Construction]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + UP + 1.25*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + UP + 2.25*RIGHT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2.25*LEFT)

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