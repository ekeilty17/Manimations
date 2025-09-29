import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop10(GreekConstructionScenes):

    title = "Book 1 Proposition 10"
    description = """
        To cut a given finite straight-line in half
    """

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)

        line_AB = Line(A.get_center(), B.get_center())

        givens = (
            A, B,
            label_A, label_B,
            line_AB
        )
        intermediaries = ()
        return givens, intermediaries

    def get_solution(self, *givens):
        A, B, label_A, label_B, line_AB = givens

        C, _ = get_equilateral_triangle_apex(line_AB)
        C, label_C = self.get_dot_and_label("C", C.get_center(), UP)

        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())
        line_BC_marker = get_line_marker(line_BC, "|")
        line_CA_marker = get_line_marker(line_CA, "|", flip_vertically=True)

        D, label_D = self.get_dot_and_label("D", (A.get_center() + B.get_center())/2, DOWN)
        
        line_CD = Line(C.get_center(), D.get_center())
        line_CD_marker = get_line_marker(line_CD, "||", flip_vertically=True)

        angle_ACD_marker = get_angle_marker(line_CA.copy().rotate(PI), line_CD, ")", radius=0.4)
        angle_BCD_marker = get_angle_marker(line_BC, line_CD, "(", radius=0.5)

        line_DA = Line(D.get_center(), A.get_center())
        line_DB = Line(D.get_center(), B.get_center())
        line_DA_marker = get_line_marker(line_DA, "///")
        line_DB_marker = get_line_marker(line_DB, "///")

        intermediaries = (
            C, 
            label_C,
            line_BC, line_CA, line_CD,
            line_BC_marker, line_CA_marker, line_CD_marker, line_DA_marker, line_DB_marker,
            angle_ACD_marker, angle_BCD_marker,
        )
        solution = (
            D,
            label_D,
        )
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ("|AC ~ |BC", "[Prop. 1.1]"),
            ("<ACD ~ <BCD", "[Prop. 1.9]"),
            ("|CD ~ |DC", "[Reflexivity]"),
            ("^ACD ~ ^BCD", "[Prop. 1.4 (SAS)]"),
            ("|AD ~ |BD", "[Prop. 1.4]", self.SOLUTION),
        ]
    def get_proof_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.5*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.5*RIGHT)
        
        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        A, B, label_A, label_B, line_AB = givens
        (
            C, 
            label_C,
            line_BC, line_CA, line_CD,
            line_BC_marker, line_CA_marker, line_CD_marker, line_DA_marker, line_DB_marker,
            angle_ACD_marker, angle_BCD_marker,
        ) = solution_intermediaries
        D, label_D = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        
        self.custom_play(title, description)
        self.wait()
        self.custom_unplay(title, description)
        self.wait()
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
        self.wait()
        
        """ Start of animation """
        self.add(*solution_intermediaries, *solution)
        self.play(Write(proof_lines))