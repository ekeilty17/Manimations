import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop17(GreekConstructionScenes):

    title = "Book 1 Proposition 17"
    description = """
        For any triangle, (the sum of) two angles 
        taken together in any (possible way) is 
        less than two right-angles.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DOWN)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DOWN)
        
        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)

        _, line_CD = extend_line_by_length(line_BC, self.D_length.get_value())
        D, label_D = self.get_dot_and_label("D", line_CD.get_end(), DOWN)

        givens = (
            A, B, C,
            label_A, label_B, label_C, 
            line_AB, line_BC, line_CA, 
        )
        intermediaries = (D, label_D, line_CD)
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"<ABC < <ACD", "[Prop. 1.16]"),
            (r"<ABC + <ACB \\ < <ACD + <ACB", "[CN. 2]"),
            (r"<ACD + <ACB = \rightanglesqr + \rightanglesqr", "[Prop. 1.13]"),
            (r"<ABC + <ACB < \rightanglesqr + \rightanglesqr", "[CN. 1]", self.SOLUTION)
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
        self.D_length = ValueTracker(1)

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