import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop8(GreekConstructionScenes):

    title = "Book 1 Proposition 8"
    description = """
        If two triangles have two sides equal to two 
        sides, respectively, and also have the base equal 
        to the base, then they will also have equal the 
        angles encompassed by the equal straight-lines
    """

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)

        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        D, label_D = self.get_dot_and_label("D", A.get_center() + self.triangle_DEF_offset_x.get_value() * RIGHT + self.triangle_DEF_offset_y.get_value() * UP, UP)
        E, label_E = self.get_dot_and_label("E", B.get_center() + self.triangle_DEF_offset_x.get_value() * RIGHT + self.triangle_DEF_offset_y.get_value() * UP, DL)
        F, label_F = self.get_dot_and_label("F", C.get_center() + self.triangle_DEF_offset_x.get_value() * RIGHT + self.triangle_DEF_offset_y.get_value() * UP, DR)

        line_DE = Line(D.get_center(), E.get_center())
        line_EF = Line(E.get_center(), F.get_center())
        line_FD = Line(F.get_center(), D.get_center())

        line_AB_marker = get_line_marker(line_AB, "/")
        line_BC_marker = get_line_marker(line_BC, "///")
        line_CA_marker = get_line_marker(line_CA, "//")
        line_DE_marker = get_line_marker(line_DE, "/")
        line_EF_marker = get_line_marker(line_EF, "///")
        line_FD_marker = get_line_marker(line_FD, "//")

        givens = ()
        intermediaries = (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F, 
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD,
            line_AB_marker, line_BC_marker, line_CA_marker, line_DE_marker,line_EF_marker, line_FD_marker,
        )
        return givens, intermediaries

    def get_solution(self, *givens):

        (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F, 
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD,
            line_AB_marker, line_BC_marker, line_CA_marker, line_DE_marker,line_EF_marker, line_FD_marker,
        ) = givens

        G, label_G = self.get_dot_and_label("G", self.Gx.get_value() * RIGHT + self.Gy.get_value() * UP, UR)
        line_EG = Line(E.get_center(), G.get_center())
        line_FG = Line(F.get_center(), G.get_center())

        line_EG_marker = get_line_marker(line_EG, "/")
        line_FG_marker = get_line_marker(line_FG, "//", flip_vertically=True)

        ABC_angle_marker = get_angle_marker(line_AB.copy().rotate(PI), line_BC, "((")
        BCA_angle_marker = get_angle_marker(line_BC.copy().rotate(PI), line_CA, "(")
        CAB_angle_marker = get_angle_marker(line_CA.copy().rotate(PI), line_AB, "(((")

        DEF_angle_marker = get_angle_marker(line_DE.copy().rotate(PI), line_EF, "((")
        EFD_angle_marker = get_angle_marker(line_EF.copy().rotate(PI), line_FD, "(")
        FDE_angle_marker = get_angle_marker(line_FD.copy().rotate(PI), line_DE, "(((")

        intermediaries = (
            G,
            label_G,
            line_EG, line_FG,
            line_EG_marker, line_FG_marker
        )
        solution = (
            ABC_angle_marker, BCA_angle_marker, CAB_angle_marker, DEF_angle_marker, EFD_angle_marker, FDE_angle_marker,
        )
        return intermediaries, solution

    def get_proof_spec(self):
        return [
        ]
    def get_proof_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 3.5*UP + 0.5*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*UP + LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.25*UP + 1.25*RIGHT)
        self.triangle_DEF_offset_x, self.triangle_DEF_offset_y, _ = get_value_tracker_of_point(4*DOWN)
        self.Gx, self.Gy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.75*DOWN + 0.5*RIGHT)

        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        self.add(*solution_intermediaries, *solution)
        return

        # """ Introduction """
        # title, description = self.initialize_introduction(self.title, self.description)
        
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
        
        # """ Proof Initialization """
        # proof_line_numbers, proof_lines = self.initialize_proof()
        # self.play(Write(proof_line_numbers))
        # self.wait()
        
        """ Start of animation """
        # TODO