import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop35(GreekConstructionScenes):

    title = "Book 1 Proposition 35"
    description = """
        Parallelograms which are on the same base 
        and between the same parallels are equal 
        to one another.
    """

    def write_givens(self):
        # parallelogram ABCD
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)
        
        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CD = line_AB.copy().shift(C.get_center() - B.get_center())
        line_DA = line_BC.copy().shift(A.get_center() - B.get_center()).rotate(PI)

        D, label_D = self.get_dot_and_label("D", line_DA.get_start(), UP)

        # parallelograph EBCF
        E, label_E = self.get_dot_and_label("E", self.Ex.get_value() * RIGHT + self.Ey.get_value() * UP, UP)
        line_FE = line_BC.copy().shift(E.get_center() - B.get_center()).rotate(PI)
        F, label_F = self.get_dot_and_label("F", line_FE.get_start(), UP)

        line_EB = Line(E.get_center(), B.get_center())
        line_CF = Line(C.get_center(), F.get_center())

        # Other lines
        G_pos = get_line_line_intersection(line_CD, line_EB)
        G, label_G = self.get_dot_and_label("G", G_pos, RIGHT)

        line_DE = Line(D.get_center(), E.get_center())

        # markers
        line_BC_marker = get_line_marker(line_BC, marker_type=">")
        line_DA_marker = get_line_marker(line_DA, marker_type="<")
        line_DE_marker = get_line_marker(line_DE, marker_type=">")
        line_FE_marker = get_line_marker(line_FE, marker_type="<")

        givens = (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_BC, line_CD, line_DA, line_EB, line_CF, line_FE
        )
        intermediaries = (
            G,
            label_G,
            line_DE,
            line_BC_marker, line_DA_marker, line_DE_marker, line_FE_marker
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"ABCD \text{ is a parallelogram}", "[Given]", self.GIVEN),
            (r"EBCF \text{ is a parallelogram}", "[Given]", self.GIVEN),
            (r"|BC || |AD || |EF", "[Given]", self.GIVEN),
            (r"|BC ~= |AD ~= |EF", "[Prop. 1.34, CN. 1]"),
            (r"|DE ~= |DE", "[Reflexivity]"),
            (r"|AD + |DE ~= |DE + |EF", "[CN. 2]"),
            (r"|AE ~= |DF", "[Construction]"),
            (r"|AB ~= |DC", "[Prop. 1.34]"),
            (r"|EB ~= |FC", "[Prop. 1.34]"),
            (r"<EAB ~= <FDC", "[Prop. 1.29]"),
            (r"^ABE ~= ^ECF", "[Prop. 1.4]"),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 2.5*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1*DOWN + 1.25*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1*DOWN + 0.5*RIGHT)

        self.Ex, self.Ey, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 1.25*RIGHT)

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