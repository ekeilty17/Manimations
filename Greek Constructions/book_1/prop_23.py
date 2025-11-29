import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop23(GreekConstructionScenes):

    title = "Book 1 Proposition 23"
    description = """
        To construct a rectilinear angle equal to a given 
        rectilinear angle at a (given) point on a given 
        straight-line.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DOWN)

        x_right_edge = config.frame_width / 2
        line_AB = Line(A.get_center(), A.get_center() + x_right_edge*RIGHT)
        _, label_B = self.get_dot_and_label("B", line_AB.get_end(), DOWN)
        label_B.shift((x_right_edge - 0.5 - label_B.get_center()[0]) * RIGHT)

        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, LEFT)

        line_CD_extended = polar_to_line(C.get_center(), self.angle_C_length.get_value(), self.line_CD_angle.get_value())
        line_CE_extended = polar_to_line(C.get_center(), self.angle_C_length.get_value(), self.line_CD_angle.get_value() + self.angle_C.get_value())
        
        line_CD, D, _ = interpolate_line(line_CD_extended, self.D_percentage.get_value())
        line_CE, E, _ = interpolate_line(line_CE_extended, self.E_percentage.get_value())

        D, label_D = self.get_dot_and_label("D", line_CD.get_end(), UP)
        E, label_E = self.get_dot_and_label("E", line_CE.get_end(), DOWN)

        line_DE = Line(D.get_center(), E.get_center())

        line_AG, _ = extend_line_by_length(line_AB, line_CE.get_length(), switch_direction=True)
        G, label_G = self.get_dot_and_label("G", line_AG.get_end(), UR)

        offset_angle = line_AG.get_angle() - line_CE.get_angle()
        line_AF = line_CD.copy().shift(A.get_center() - C.get_center()).rotate(offset_angle, about_point=A.get_center())
        F, label_F = self.get_dot_and_label("F", line_AF.get_end(), UP)

        line_FG = line_DE.copy().shift(F.get_center() - D.get_center()).rotate(offset_angle, about_point=F.get_center())

        line_CD_marker = get_line_marker(line_CD, marker_type="/")
        line_DE_marker = get_line_marker(line_DE, marker_type="///")
        line_CE_marker = get_line_marker(line_CE, marker_type="//")
        line_AF_marker = get_line_marker(line_AF, marker_type="/")
        line_FG_marker = get_line_marker(line_FG, marker_type="///")
        line_AG_marker = get_line_marker(line_AG, marker_type="//")

        angle_C_marker = get_angle_marker(line_CD.copy().rotate(PI), line_CE, marker_type="(")
        angle_A_marker = get_angle_marker(line_AF.copy().rotate(PI), line_AG, marker_type="(")

        givens = (
            A, C,
            label_A, label_B, label_C,
            line_AB, line_CD_extended, line_CE_extended,
        )
        intermediaries = (
            D, E, G, F,
            label_D, label_E, label_G, label_F,
            line_AF, line_AG, line_CD, line_CE, line_DE, line_FG,
            line_AF_marker, line_AG_marker, line_CD_marker, line_CE_marker, line_DE_marker, line_FG_marker,
            angle_A_marker, angle_C_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|CD ~= |AF", "[Prop. 1.22]"),
            (r"|DE ~= |FG", "[Prop. 1.22]"),
            (r"|CE ~= |AG", "[Prop. 1.22]"),
            (r"^CDE ~= ^AFG", "[Prop. 1.8]"),
            (r"<C ~= <A", "[Prop. 1.8]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {
            "<C": self.GIVEN,
            "<A": self.SOLUTION,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(ORIGIN + 1*DOWN + 0.8*LARGE_BUFF*RIGHT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 2*LEFT)
        
        self.line_CD_angle = ValueTracker(PI/7)
        self.angle_C_length = ValueTracker(3.25)
        self.angle_C = ValueTracker(-PI/5)

        self.D_percentage = ValueTracker(0.7)
        self.E_percentage = ValueTracker(0.8)

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