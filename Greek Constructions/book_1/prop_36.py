import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop35(GreekConstructionScenes):

    title = "Book 1 Proposition 36"
    description = """
        Parallelograms which are on equal bases 
        and between the same parallels are equal 
        to one another.
    """

    def write_givens(self):
        # parallelogram ABCD
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DOWN)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DOWN)
        
        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CD = line_AB.copy().shift(C.get_center() - B.get_center())
        line_DA = line_BC.copy().shift(A.get_center() - B.get_center()).rotate(PI)

        D, label_D = self.get_dot_and_label("D", line_DA.get_start(), UP)

        # parallelograph EFGH
        E, label_E = self.get_dot_and_label("E", self.Ex.get_value() * RIGHT + self.Ey.get_value() * UP, UP)
        F, label_F = self.get_dot_and_label("F", self.Fx.get_value() * RIGHT + self.Fy.get_value() * UP, DOWN)

        line_EF = Line(E.get_center(), F.get_center())
        line_FG = line_BC.copy().shift(F.get_center() - B.get_center())
        line_HE = line_FG.copy().shift(E.get_center() - F.get_center()).rotate(PI)
        G, label_G = self.get_dot_and_label("G", line_FG.get_end(), DOWN)
        H, label_H = self.get_dot_and_label("H", line_HE.get_start(), UP)
        line_GH = Line(G.get_center(), H.get_center())

        # Other lines
        line_CF = Line(C.get_center(), F.get_center())
        line_DE = Line(D.get_center(), E.get_center())

        line_BE = Line(B.get_center(), E.get_center())
        line_CH = Line(C.get_center(), H.get_center())

        # markers
        line_BC_marker = get_line_marker(line_BC, marker_type=">")
        line_DA_marker = get_line_marker(line_DA, marker_type="<")
        line_FG_marker = get_line_marker(line_FG, marker_type=">")
        line_HE_marker = get_line_marker(line_HE, marker_type="<")
        line_DE_marker = get_line_marker(line_DE, marker_type=">")
        line_CF_marker = get_line_marker(line_CF, marker_type=">")

        givens = (
            A, B, C, D, E, F, G, H,
            label_A, label_B, label_C, label_D, label_E, label_F, label_G, label_H,
            line_AB, line_BC, line_CD, line_DA,
            line_EF, line_FG, line_GH, line_HE,
        )
        intermediaries = (
            line_BE, line_CF, line_CH, line_DE,
            line_BC_marker, line_CF_marker, line_DA_marker, line_DE_marker, line_FG_marker, line_HE_marker, 
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"ABCD \text{ is a parallelogram}", "[Given]", self.GIVEN),
            (r"EFGH \text{ is a parallelogram}", "[Given]", self.GIVEN),
            (r"|BC ~= |FG", "[Given]", self.GIVEN),
            (r"EBCH \text{ is a parallelogram}", "[??]"),
            (r"ABCD = EBCH", "[Prop. 1.35]"),
            (r"EFGH = EBCH", "[Prop. 1.35]"),
            (r"ABCD = EFGH", "[CN. 1]"),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 2.25*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1*DOWN + 2.75*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1*DOWN + 1.5*LEFT)

        self.Ex, self.Ey, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 0.75*RIGHT)
        self.Fx, self.Fy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1*DOWN + 1.75*RIGHT)

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