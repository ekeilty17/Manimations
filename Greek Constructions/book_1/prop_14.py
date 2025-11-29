import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop14(GreekConstructionScenes):

    title = "Book 1 Proposition 14"
    description = """
        If two straight-lines, not lying on the 
        same side, make adjacent angles (whose sum 
        is) equal to two right-angles with some 
        straight-line, at a point on it, then the 
        two straight-lines will be straight-on 
        (with respect) to one another.
    """

    def write_givens(self):
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)
        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, DL)

        line_CD = Line(C.get_center(), D.get_center())
        
        _, B, _ = interpolate_line(line_CD, percentage=self.B_percentage.get_value())
        B, label_B = self.get_dot_and_label("B", B.get_center(), DOWN)

        line_BC = Line(B.get_center(), C.get_center())
        line_BD = Line(B.get_center(), D.get_center())

        tmp_line = Line(B.get_center(), B.get_center() + self.line_BE_length.get_value() * RIGHT)
        
        line_BA_angle_acute = self.line_BA_angle.get_value() < PI/2
        line_BA = tmp_line.copy().rotate(self.line_BA_angle.get_value(), about_point=B.get_center())
        A, label_A = self.get_dot_and_label("A", line_BA.get_end(), UR if line_BA_angle_acute else UL)

        line_BE_angle_acute = self.line_BE_angle.get_value() < PI/2
        line_BE = tmp_line.copy().rotate(self.line_BE_angle.get_value(), about_point=B.get_center())
        E, label_E = self.get_dot_and_label("E", line_BE.get_end(), UR if line_BE_angle_acute else UL)

        givens = (
            A, B, C, D, E,
            label_A, label_B, label_C, label_D, label_E,
            line_BA, line_BC, line_BD, line_BE,
        )
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            A, B, C, D, E,
            label_A, label_B, label_C, label_D, label_E,
            line_BA, line_BC, line_BD, line_BE,
        ) = givens

        line_CD = Line(C.get_center(), D.get_center())

        angle_ABC_marker = get_angle_marker(line_BA.copy().rotate(PI), line_BC, marker_type=")")
        angle_ABE_marker = get_angle_marker(line_BA.copy().rotate(PI), line_BE, marker_type="((")
        angle_DBE_marker = get_angle_marker(line_BE.copy().rotate(PI), line_BD, marker_type="(((", radius=0.3)

        intermediaries = (
            angle_ABC_marker, angle_ABE_marker, angle_DBE_marker
        )
        solution = line_CD
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"<ABC + <ABE + <DEB \\ = \rightanglesqr + \rightanglesqr", "[Given]", self.GIVEN),
            (r"|BC \text{ is not straight on } |BD", "[Assumption]", self.ASSUMPTION),
            (r"|BE \text{ is straight on } |BC", "[Assumption]", self.ASSUMPTION),
            (r"<ABC + <ABE = \rightanglesqr + \rightanglesqr", "[Prop. 1.13]", self.PBC_INTERMEDIARY),
            (r"<ABC + <ABD = \rightanglesqr + \rightanglesqr", "[1. + Construction]", self.PBC_INTERMEDIARY),
            (r"<ABC + <ABE \\ = <ABC + <ABD", "[CN. 1]", self.PBC_INTERMEDIARY),
            (r"<ABE ~= <ABD", "[CN. 3]", self.CONTRADICTION),
            (r"<ABE !~= <ABD", "[CN. 5]", self.CONTRADICTION),
            (r"|BC \text{ is straight on } |BD", "[By Contradiction]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {
            "{A}": self.GIVEN,
            "{B}": self.GIVEN,
            "{C}": self.GIVEN,
            "{D}": self.GIVEN,
            "{E}": self.GIVEN,
            "|AB": self.GIVEN,
            "|BA": self.GIVEN,
            "|BC": self.GIVEN,
            "|CB": self.GIVEN,
            "|BD": self.GIVEN,
            "|DB": self.GIVEN,
            "|BE": self.GIVEN,
            "|EB": self.GIVEN,
            "|CD": self.SOLUTION,
            "|DC": self.SOLUTION,
            "<ABC": self.GIVEN,
            "<ABE": self.GIVEN,
            "<DEB": self.GIVEN,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2.25*LEFT)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2.25*RIGHT)
        self.B_percentage = ValueTracker(0.4)
        self.line_BA_length = ValueTracker(2.75)
        self.line_BA_angle = ValueTracker(2*PI/3)
        self.line_BE_length = ValueTracker(2.75)
        self.line_BE_angle = ValueTracker(PI/4)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.8, center_horizontally=True)

        """ Construction Variables """
        (
            A, B, C, D, E,
            label_A, label_B, label_C, label_D, label_E,
            line_BA, line_BC, line_BD, line_BE,
        ) = self.givens
        # () = self.given_intermediaries
        angle_ABC_marker, angle_ABE_marker, angle_DBE_marker = self.solution_intermediaries
        line_CD = self.solution

        """ Animate Introduction """
        angle_ABC = VGroup([mob.copy() for mob in [A, B, C, label_A, label_B, label_C, line_BA, line_BC]])
        angle_ABE = VGroup([mob.copy() for mob in [A, B, E, label_A, label_B, label_E, line_BA, line_BE]])
        angle_DBE = VGroup([mob.copy() for mob in [B, D, E, label_B, label_D, label_E, line_BD, line_BE]])
        self.add(angle_ABC, angle_ABE, angle_DBE)

        solution_explanation = self.MathTex(
            r"\text{If } <ABC + <ABE + <DEB = \rightanglesqr + \rightanglesqr",
            r"\text{then } |BC \text{ is straight on } |BD", 
            scale=0.8,
            paragraph_spacing=1
        )
        solution_explanation_line_1, solution_explanation_line_2 = solution_explanation

        line_CD_copy = line_CD.copy()

        self.wait()
        self.custom_play(
            *Animate(title, description),
        )
        self.wait()
        self.custom_play(
            angle_ABC.animate.shift(0.5*LEFT),
            angle_ABE.animate.shift(UP),
            angle_DBE.animate.shift(0.5*RIGHT),
        )
        self.wait()
        self.custom_play(
            angle_ABC.animate.shift(0.5*RIGHT),
            angle_ABE.animate.shift(DOWN),
            angle_DBE.animate.shift(0.5*LEFT),
        )
        self.wait()
        self.custom_play(Animate(solution_explanation_line_1))
        self.wait()
        self.custom_play(*Animate(line_CD_copy, solution_explanation_line_2))
        self.wait(3)
        self.custom_play(
            *Unanimate(title, description, line_CD_copy, solution_explanation_line_1, solution_explanation_line_2),
        )
        self.add(*self.givens, *self.given_intermediaries)
        self.remove(angle_ABC, angle_ABE, angle_DBE)
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        # self.add(*self.solution_intermediaries, *self.solution)
        self.add(proof_lines)
        self.wait()