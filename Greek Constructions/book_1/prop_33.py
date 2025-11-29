import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop33(GreekConstructionScenes):

    title = "Book 1 Proposition 33"
    description = """
        Straight-lines joining equal and parallel 
        (straight-lines) on the same sides are 
        themselves also equal and parallel.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, UP)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DOWN)
        
        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)

        line_CD = line_AB.copy().shift(C.get_center() - A.get_center())
        D, label_D = self.get_dot_and_label("D", line_CD.get_end(), DOWN)

        line_DB = Line(D.get_center(), B.get_center())

        line_AB_parallel_marker = get_line_marker(line_AB, marker_type="<", position=0.675)
        line_CD_parallel_marker = get_line_marker(line_CD, marker_type="<", position=0.675)
        line_CA_parallel_marker = get_line_marker(line_CA, marker_type=">>", position=0.475)
        line_DB_parallel_marker = get_line_marker(line_DB, marker_type=">>", position=0.475)

        line_AB_marker = get_line_marker(line_AB, marker_type="/", position=0.475)
        line_CD_marker = get_line_marker(line_CD, marker_type="/", position=0.475)
        line_CA_marker = get_line_marker(line_CA, marker_type="///", position=0.675)
        line_DB_marker = get_line_marker(line_DB, marker_type="///", position=0.675)

        line_BC_marker = get_line_marker(line_BC, marker_type="//")

        angle_ABC_marker = get_angle_marker(line_AB, line_BC, marker_type="(")
        angle_DCB_marker = get_angle_marker(line_BC, line_CD, marker_type=")")

        angle_ACB_marker = get_angle_marker(line_BC, line_CA, marker_type="((")
        angle_CBD_marker = get_angle_marker(line_DB, line_BC, marker_type="))")

        givens = (
            A, B, C, D,
            label_A, label_B, label_C, label_D,
            line_AB, line_CA, line_CD, line_DB
        )
        intermediaries = (
            line_BC,
            line_AB_marker, line_BC_marker, line_CA_marker, line_CD_marker, line_DB_marker, 
            line_AB_parallel_marker, line_CA_parallel_marker, line_CD_parallel_marker, line_DB_parallel_marker,
            angle_ABC_marker, angle_ACB_marker, angle_CBD_marker, angle_DCB_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AB ~= |CD", "[Given]", self.GIVEN),
            (r"|AB || |CD", "[Given]", self.GIVEN),
            (r"<ABC ~= <BCD", "[Prop. 1.29]"),
            (r"|BC ~= |CB", "[Reflexivity]"),
            (r"^ABC ~= ^DCB", "[Prop. 1.4]"), 
            (r"|AC ~= |BD", "[Prop. 1.4]", self.SOLUTION),
            (r"<ACB ~= CBD", "[Prop. 1.4]"), 
            (r"|AC || |BD", "[Prop. 1.27]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + UP + 2.25*RIGHT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + UP + 1.25*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.25*RIGHT)

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