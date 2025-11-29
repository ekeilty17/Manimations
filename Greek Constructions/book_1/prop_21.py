import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop21(GreekConstructionScenes):

    title = "Book 1 Proposition 21"
    description = """
        If two internal straight-lines are constructed 
        on one of the sides of a triangle, from its 
        ends, the constructed (straight-lines) will be 
        less than the two remaining sides of the 
        triangle, but will encompass a greater angle.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)
        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, UL)
        
        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)
        line_DB, _, line_CD = get_triangle_edges(D, B, C)

        E_coord = get_line_line_intersection(line_DB, line_CA)
        E, label_E = self.get_dot_and_label("E", E_coord, UR)
        line_DE = Line(D.get_center(), E.get_center())

        givens = (
            A, B, C, D,
            label_A, label_B, label_C, label_D, 
            line_AB, line_BC, line_CA, line_CD, line_DB,
        )
        intermediaries = (E, label_E, line_DE)
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AB + |AE > |BE", "[Prop. 1.20]"),
            (r"|AB + |AE + |EC \\ > |BE + |EC", "[CN. 2]"),
            (r"|AB + |AC > |BE + |EC", "[Construction]"),
            (r"|CE + |ED > |CD", "[Prop. 1.20]"),
            (r"|CE + |ED + |DB \\ > |CD + |DB", "[CN. 2]"),
            (r"|CE + |EB > |CD + |DB", "[Construction]"),
            (r"|AB + |AC > |CD + |DB", "[CN. 1]", self.SOLUTION),
            (r"<BDC > <CED", "[Prop. 1.16]"),
            (r"<CED > <BAC", "[Prop. 1.16]"),
            (r"<BDC > <BAC", "[CN. 1]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*UP + LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2.25*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2.25*RIGHT)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.25*UP + 0.75*LEFT)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(0.95)

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