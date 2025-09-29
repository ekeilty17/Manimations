import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop12(GreekConstructionScenes):

    title = "Book 1 Proposition 12"
    description = """
        To draw a straight-line perpendicular to a given infinite straight-line from a given point which is not on it
    """

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, UP)

        # TODO
        # Ax_shift = ORIGIN[0] - A.get_center()[0] + 1
        # label_A.shift(Ax_shift)

        line_AB = Line(A.get_center(), B.get_center())

        givens = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB
        )
        intermediaries = ()
        return givens, intermediaries

    def get_solution(self, *givens):
        A, B, C, label_A, label_B, label_C, line_AB = givens

        _, D, line_DB = interpolate_line(line_AB, percentage=self.D_percentage.get_value())
        D, label_D = self.get_dot_and_label("D", D.get_center(), DOWN)
        
        circle_C = OrientedCircle(C.get_center(), D.get_center())
        # _, E, line_DF = interpolate_line(line_AB, percentage=self.D_percentage.get_value())

        line_CD = Line(C.get_center(), D.get_center())
        line_CE = line_CD.copy().scale([-1, 1, 1], about_point=C.get_center())
        E, label_E = self.get_dot_and_label("E", line_CE.get_end(), DOWN)

        line_DE = Line(D.get_center(), E.get_center())
        F, label_F = self.get_dot_and_label("F", line_DE.get_center(), DOWN)
        line_CF = Line(C.get_center(), F.get_center())
        line_FD = Line(F.get_center(), D.get_center())
        angle_CFD_marker = get_angle_marker(line_CF, line_FD, ")", radius=0.25)

        line_FE = Line(F.get_center(), E.get_center())
        angle_CFE_marker = get_angle_marker(line_CF, line_FE, "(", radius=0.3)
        elbow_CFE_marker = get_angle_marker(line_CF, line_FE, elbow=True)
        

        line_CD_marker = get_line_marker(line_CD, "|")
        line_CE_marker = get_line_marker(line_CE, "|")
        line_FD_marker = get_line_marker(line_FD, "//")
        line_FE_marker = get_line_marker(line_FE, "//")
        line_CF_marker = get_line_marker(line_CF, "///", flip_vertically=True)

        intermediaries = (
            D, E,
            label_D, label_E,
            line_CD, line_CE, line_DE,
            circle_C,
            line_CD_marker, line_CE_marker, line_FD_marker, line_FE_marker, line_CF_marker,
            angle_CFD_marker, angle_CFE_marker, elbow_CFE_marker
        )
        solution = (
            F,
            label_F,
            line_CF,
        )
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ("|CD ~ |CE", "[Def. 15]"),
            ("|DF ~ |ED", "[Prop. 10]"),
            ("|CF ~ |FC", "[Reflexivity]"),
            ("^CDF ~ ^CEF", "[Prop. 1.8 (SSS)]"),
            ("<DFC ~ ^EFC", "[Prop. 1.8]"),
            ("|AB perp |CF", "[??]"),
        ]
    def get_proof_color_map(self):
        return {
            "|AB": self.given_color,
            "|CF": self.solution_color,
            "|FC": self.solution_color,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 10*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 10*RIGHT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*UP)
        self.D_percentage = ValueTracker(0.42)

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