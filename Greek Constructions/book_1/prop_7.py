import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop7(GreekConstructionScenes):

    title = "Book 1 Proposition 7"
    description = """
        If a triangle has two angles equal to one
        On the same straight-line, two other 
        straight-lines equal, respectively, to two 
        (given) straight-lines (which cannot be 
        constructed (meeting) at a different point on 
        the same side (of the straight-line), but 
        having the same ends as the given straight-lines.
    """

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, UP)
        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, UR)

        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        line_BD = Line(B.get_center(), D.get_center())
        line_DA = Line(D.get_center(), A.get_center())

        line_CD = Line(C.get_center(), D.get_center())

        line_CA_marker = get_line_marker(line_CA, "/")
        line_DA_marker = get_line_marker(line_DA, "/")

        line_BC_marker = get_line_marker(line_BC, "//")
        line_BD_marker = get_line_marker(line_BD, "//")

        angle_ACD_marker = get_angle_marker(line_CA, line_CD, ")", radius=0.2)
        angle_ADC_marker = get_angle_marker(line_DA, line_CD.copy().rotate(PI), "(", radius=0.4)

        angle_BCD_marker = get_angle_marker(line_BC.copy().rotate(PI), line_CD, "))", radius=0.4, radius_step=0.05)
        angle_BDC_marker = get_angle_marker(line_BD.copy().rotate(PI), line_CD.copy().rotate(PI), "((", radius=0.2, radius_step=0.05)

        givens = ()
        intermediaries = (
            A, B, C, D, 
            label_A, label_B, label_C, label_D,
            line_AB, line_BC, line_BD, line_CA, line_CD, line_DA,
            line_BC_marker, line_BD_marker, line_CA_marker, line_DA_marker,
            angle_ACD_marker, angle_ADC_marker, angle_BCD_marker, angle_BDC_marker,
        )
        return givens, intermediaries

    def get_solution(self, *givens):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ("|AC ~ |AD", "[Given]", self.GIVEN),
            ("|BC ~ |BD", "[Given]", self.GIVEN),
            ("C != D", "[Assumption]", self.ASSUMPTION),
            ("<ACD ~ <ADC", "[1. + Prop. 1.6]"),
            ("<BCD ~ <BDC", "[2. + Prop. 1.6]"),
            ("<ACD > <BCD", "[Construction]", self.CONTRADICTION),
            ("<ADC < <BDC", "[Construction]"),
            ("<ACD < <BCD", "[4. + 5. + 7.]", self.CONTRADICTION),
            ("C = D", "[By Contradiction]")
        ]
    def get_proof_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2*RIGHT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*RIGHT + 2*UP)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*RIGHT + 1.5*UP)

        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        # A, B, C = givens
        # D, E, F = given_intermediaries
        # G, H, I = solution_intermediaries
        # J, K, L = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        
        # self.play(Animate(title))
        # self.play(Animate(description))
        # self.wait()
        # tmp1 = [mob.copy() for mob in [A, B, C]]
        # tmp2 = [mob.copy() for mob in [D, E, F]]
        # self.play(Animate(*tmp1))
        # self.play(Animate(*tmp2))
        # self.wait()
        # self.play(Unanimate(title, description, *tmp1, *tmp2))
        # self.wait()
        
        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof()
        self.play(Write(proof_line_numbers))
        self.play(Write(proof_lines))
        self.wait()
        
        """ Start of animation """
        # TODO