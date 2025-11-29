import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop24(GreekConstructionScenes):

    title = "Book 1 Proposition 24"
    description = """
        If two triangles have two sides equal to two sides, 
        respectively, but (one) has the angle encompassed 
        by the equal straight-lines greater than the 
        (corresponding) angle (in the other), then (the 
        former triangle) will also have a base greater than 
        the base (of the latter).
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        
        line_AB = polar_to_line(A.get_center(), self.side_length_1.get_value(), self.line_AB_angle.get_value())
        line_AC = polar_to_line(A.get_center(), self.side_length_2.get_value(), self.line_AB_angle.get_value() + self.angle_A.get_value())
        B, label_B = self.get_dot_and_label("B", line_AB.get_end(), RIGHT)
        C, label_C = self.get_dot_and_label("C", line_AC.get_end(), DL)
        line_BC = Line(B.get_center(), C.get_center())

        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, UP)
        line_DE = polar_to_line(D.get_center(), self.side_length_1.get_value(), self.line_DE_angle.get_value())
        line_DF = polar_to_line(D.get_center(), self.side_length_2.get_value(), self.line_DE_angle.get_value() + self.angle_D.get_value())
        E, label_E = self.get_dot_and_label("E", line_DE.get_end(), RIGHT)
        F, label_F = self.get_dot_and_label("F", line_DF.get_end(), DR)
        line_EF = Line(E.get_center(), F.get_center())

        line_AB_marker = get_line_marker(line_AB, marker_type="/")
        line_AC_marker = get_line_marker(line_AC, marker_type="//")
        line_DE_marker = get_line_marker(line_DE, marker_type="/")
        line_DF_marker = get_line_marker(line_DF, marker_type="//")

        line_DG = polar_to_line(D.get_center(), self.side_length_2.get_value(), self.line_DE_angle.get_value() + self.angle_A.get_value())
        _, line_DG_extended = extend_line_by_length(line_DG, 1)
        line_DG_marker = get_line_marker(line_DG, marker_type="//")
        G, label_G = self.get_dot_and_label("G", line_DG.get_end(), DL)

        angle_A_marker = get_angle_marker(line_AB.copy().rotate(PI), line_AC, marker_type="(")
        angle_EDG_marker = get_angle_marker(line_DE.copy().rotate(PI), line_DG, marker_type="(")

        line_GF = Line(G.get_center(), F.get_center())
        line_GE = Line(G.get_center(), E.get_center())
        
        line_BC_marker = get_line_marker(line_BC, marker_type="///")
        line_EG_marker = get_line_marker(line_GE, marker_type="///")
        angle_DFG_marker = get_angle_marker(line_DF, line_GF.copy().rotate(PI), marker_type="))", radius=0.15)
        angle_DGF_marker = get_angle_marker(line_DG, line_GF, marker_type="((", radius=0.15)

        givens = (
            A, B, C, D, E, F, 
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_AC, line_BC, line_DE, line_DF, line_EF,
        )
        intermediaries = (
            G,
            label_G,
            line_DG_extended, line_DG, line_GE, line_GF,
            line_AB_marker, line_AC_marker, line_BC_marker, line_DE_marker, line_DF_marker, line_DG_marker, line_EG_marker,
            angle_A_marker, angle_DFG_marker, angle_DGF_marker, angle_EDG_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AB ~= |DE", "[Given]", self.GIVEN),
            (r"|AC ~= |DF", "[Given]", self.GIVEN),
            (r"<A > <EDF", "[Given]", self.GIVEN),
            (r"<A ~= <EDG", "[Prop. 1.23]"),
            (r"|AC ~= |DG", "[Prop. 1.3]"),
            (r"^ABC ~= ^DEG", "[Prop. 1.4]"),
            (r"|BC ~= |EG", "[Prop. 1.4]"),
            (r"<DGF ~= <DFG", "[Prop. 1.5]"),
            (r"<DGF > <EGF", "[Construction]"),
            (r"<DGF > <DFG", "[CN. 1]"),
            (r"|EG > |EF", "[Prop. 1.19]"),
            (r"|BC > |EF", "[CN. 1]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.side_length_1 = ValueTracker(2.5)
        self.side_length_2 = ValueTracker(3.25)
        self.line_AB_angle = ValueTracker(-11*PI/30)
        self.line_DE_angle = ValueTracker(-8*PI/30)
        self.angle_A = ValueTracker(-PI/6)
        self.angle_D = ValueTracker(-PI/10)
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 2*LEFT)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + RIGHT)

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