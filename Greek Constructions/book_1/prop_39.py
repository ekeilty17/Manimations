import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop39(GreekConstructionScenes):

    title = "Book 1 Proposition 39"
    description = """
        Equal triangles which are on the same 
        base, and on the same side, are also 
        between the same parallels.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)
        
        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)

        line_AD, _ = extend_line_by_length(line_BC, self.line_AD_length.get_value(), switch_direction=True)
        line_AD.shift(A.get_center() - B.get_center())

        D, label_D = self.get_dot_and_label("D", line_AD.get_end(), UR)
        line_DB = Line(D.get_center(), B.get_center())
        line_CD = Line(C.get_center(), D.get_center())

        _, E, _ = interpolate_line(line_DB, self.E_percentage.get_value())
        E, label_E = self.get_dot_and_label("E", E.get_center(), DOWN, color=self.color_map[self.IMPOSSIBLE])
        line_AE = Line(A.get_center(), E.get_center(), color=self.color_map[self.IMPOSSIBLE])
        line_EC = Line(E.get_center(), C.get_center(), color=self.color_map[self.IMPOSSIBLE])

        line_AD_marker = get_line_marker(line_AD, marker_type=">")
        line_AE_marker = get_line_marker(line_AE, marker_type=">")
        line_BC_marker = get_line_marker(line_BC, marker_type=">")

        givens = (
            A, B, C, D,
            label_A, label_B, label_C, label_D,
            line_AB, line_BC, line_CA, line_CD, line_DB,
        )
        intermediaries = (
            E, 
            label_E,
            line_AD, line_AE, line_EC,
            line_AD_marker, line_AE_marker, line_BC_marker
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"^ABC = ^DBC", "[Given]", self.GIVEN),
            (r"|AD !|| |BC", "[Assumption]", self.ASSUMPTION),
            (r"|AE || |BC", "[Prop. 1.31]", self.PBC_INTERMEDIARY),
            (r"^ABC = ^EBC", "[Prop. 1.37]", self.PBC_INTERMEDIARY),
            (r"^DBC = ^EBC", "[CN. 1]", self.CONTRADICTION),
            (r"^DBC != ^EBC", "[Construction]", self.CONTRADICTION),
            (r"|AD || |BC", "[Contraduction]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.25*UP + 2*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.25*DOWN + 2.25*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.25*DOWN + 2.25*RIGHT)

        self.line_AD_length = ValueTracker(2.75)
        self.E_percentage = ValueTracker(0.15)

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