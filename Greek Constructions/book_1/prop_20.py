import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop20(GreekConstructionScenes):

    title = "Book 1 Proposition 20"
    description = """
        In any triangle, (the sum of) two sides 
        taken together in any (possible way) is 
        greater than the remaining (side).
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)
        
        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)

        line_AD, _ = extend_line_by_length(line_AB, line_CA.get_length())
        D, label_D = self.get_dot_and_label("D", line_AD.get_end(), UP)
        line_DC = Line(D.get_center(), C.get_center())

        line_CA_marker = get_line_marker(line_CA, marker_type="/")
        line_AD_marker = get_line_marker(line_AD, marker_type="/")

        angle_ACD_marker = get_angle_marker(line_DC, line_CA, marker_type=")")
        angle_ADC_marker = get_angle_marker(line_AD, line_DC, marker_type=")")

        givens = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        )
        intermediaries = (
            D, label_D,
            line_AD, line_DC,
            line_AD_marker, line_CA_marker, 
            angle_ACD_marker, angle_ADC_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AC ~= |AD", "[Prop. 1.3]"),
            (r"<ACD ~= <ADC", "[Prop. 1.5]"),
            (r"<BCD > <ACD", "[Construction]"),
            (r"<BCD > <ADC", "[CN. 1]"),
            (r"|BD > |BC", "[Prop. 1.19]"),
            (r"|BD ~= |BA + |AD", "[Construction]"),
            (r"|BA + |AC ~= |BA + |AD", "[CN. 2]"),
            (r"|BD ~= |BA + |AC", "[CN. 1]"),
            (r"|BA + |AC > |BC", "[CN. 1]"),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*DOWN + 0.75*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*DOWN + 1.5*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*DOWN + 1.5*RIGHT)

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