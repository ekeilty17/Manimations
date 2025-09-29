import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop9(GreekConstructionScenes):

    title = "Book 1 Proposition 9"
    description = """
        To cut a given rectilinear angle in half
    """

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, LEFT)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, RIGHT)

        line_AB = Line(A.get_center(), B.get_center())
        line_AC = Line(A.get_center(), C.get_center())

        givens = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_AC
        )
        intermediaries = ()
        return givens, intermediaries

    def get_solution(self, *givens):
        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_AC
        ) = givens

        line_AD, D, line_DB = interpolate_line(line_AB, self.D_percentage.get_value())
        D, label_D = self.get_dot_and_label("D", D.get_center(), LEFT)
        line_AD_marker = get_line_marker(line_AD, "|")

        line_AE, _ = extend_line_by_length(line_AC, line_AD.get_length(), switch_direction=True)
        E, label_E = self.get_dot_and_label("E", line_AE.get_end(), RIGHT)
        line_AE_marker = get_line_marker(line_AE, "|")

        line_DE = Line(D.get_center(), E.get_center())
        _, F = get_equilateral_triangle_apex(line_DE)
        F, label_F = self.get_dot_and_label("F", F.get_center(), DOWN)

        line_DF = Line(D.get_center(), F.get_center())
        line_EF = Line(E.get_center(), F.get_center())
        line_DF_marker = get_line_marker(line_DF, "||")
        line_EF_marker = get_line_marker(line_EF, "||")

        line_AF = Line(A.get_center(), F.get_center())
        line_AF_marker = get_line_marker(line_AF, "|||")

        angle_BAF_marker = get_angle_marker(line_AB.copy().rotate(PI), line_AF, ")", radius=0.6)
        angle_CAF_marker = get_angle_marker(line_AC.copy().rotate(PI), line_AF, "(", radius=0.7)

        intermediaries = (
            D, E, F,
            label_D, label_E, label_F,
            line_AD, line_AE, line_DE, line_DF, line_EF,
            line_AD_marker, line_AE_marker, line_AF_marker, line_DF_marker, line_EF_marker,
            angle_BAF_marker, angle_CAF_marker
        )
        solution = (line_AF)
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ("|AD ~ |AE",   "[Prop. 1.3]"),
            ("|DF ~ |EF",   "[Prop. 1.1]"),
            ("|AF ~ |FA",   "[Reflexivity]"),
            ("^ADF ~ ^AEF", "[Prop. 1.8 (SSS)]"),
            ("<DAF ~ <EAF", "[Prop. 1.8]", self.SOLUTION)
        ]
    def get_proof_color_map(self):
        return {
            "|AF": self.solution_color,
            "|FA": self.solution_color,
        }

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 3*UP)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*DOWN + 1.5*RIGHT)
        self.D_percentage = ValueTracker(0.7)

        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_AC
        ) = givens
        (
            D, E, F,
            label_D, label_E, label_F,
            line_AD, line_AE, line_DE, line_DF, line_EF,
            line_AD_marker, line_AE_marker, line_AF_marker, line_DF_marker, line_EF_marker,
            angle_BAF_marker, angle_CAF_marker
        ) = solution_intermediaries
        line_AF = solution

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