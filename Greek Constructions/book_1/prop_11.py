import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop11(GreekConstructionScenes):

    title = "Book 1 Proposition 11"
    description = """
        To draw a straight-line at right-angles
        to a given straight-line from a given 
        point on it
    """

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        line_AB = Line(A.get_center(), B.get_center())
        
        line_AC, C, line_CB = interpolate_line(line_AB, self.C_percentage.get_value())
        C, label_C = self.get_dot_and_label("C", C.get_center(), DOWN)

        givens = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB,
        )
        intermediaries = ()
        return givens, intermediaries

    def get_solution(self, *givens):
        A, B, C, label_A, label_B, label_C, line_AB, = givens

        line_AC = Line(A.get_center(), C.get_center())
        _, D, line_DC = interpolate_line(line_AC, self.D_percentage.get_value())
        D, label_D = self.get_dot_and_label("D", D.get_center(), DOWN)

        _, line_CE = extend_line_by_length(line_DC, line_DC.get_length())
        E, label_E = self.get_dot_and_label("E", line_CE.get_end(), DOWN)

        line_DE = Line(D.get_center(), E.get_center())
        F, _ = get_equilateral_triangle_apex(line_DE)
        F, label_F = self.get_dot_and_label("F", F.get_center(), UP)

        line_CE_marker = get_line_marker(line_CE, "/")
        line_DC_marker = get_line_marker(line_DC, "/")
        
        line_EF = Line(E.get_center(), F.get_center())
        line_FD = Line(F.get_center(), D.get_center())
        line_EF_marker = get_line_marker(line_EF, "||")
        line_FD_marker = get_line_marker(line_FD, "||")

        line_FC = Line(F.get_center(), C.get_center())
        line_FC_marker = get_line_marker(line_FC, "///", flip_vertically=True)

        angle_FCD_marker = get_angle_marker(line_FC, line_DC.copy().rotate(PI), ")", radius=0.25)
        angle_FCE_marker = get_angle_marker(line_FC, line_CE, "(", radius=0.3)
        elbow_FCE_marker = get_angle_marker(line_FC, line_CE, elbow=True)

        intermediaries = (
            D, E, F,
            label_D, label_E, label_F,
            line_CE, line_DC, line_EF, line_FD,
            line_CE_marker, line_DC_marker, line_EF_marker, line_FC_marker, line_FD_marker,
            angle_FCD_marker, angle_FCE_marker, elbow_FCE_marker
        )
        solution = (
            line_FC, 
        )
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ("|DC ~ |EC", "[Prop. 1.3]"),
            ("|DF ~ |EF", "[Prop. 1.1]"),
            ("|CF ~ |FC", "[Reflexivity]"),
            ("^DCF ~ ^ECF", "[Prop. 1.8 (SSS)]"),
            ("<DCF ~ <ECF", "[Prop. 1.8]"),
            ("|FC perp |AB", "[Def. 10]"),
        ]
    def get_proof_color_map(self):
        return {
            "|AB": self.given_color,
            "|CF": self.solution_color,
            "|FC": self.solution_color,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2.5*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2.5*RIGHT)
        self.C_percentage = ValueTracker(0.4)
        self.D_percentage = ValueTracker(0.2)

        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

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