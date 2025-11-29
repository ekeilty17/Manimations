import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop16(GreekConstructionScenes):

    title = "Book 1 Proposition 16"
    description = """
        For any triangle, when one of the sides is 
        produced, the external angle is greater than 
        each of the internal and opposite angles
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)
        
        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())
        
        _, line_CD = extend_line_by_length(line_BC, self.line_CD_length.get_value())
        D, label_D = self.get_dot_and_label("D", line_CD.get_end(), DR)

        line_CG, _ = extend_line_by_length(line_CA, self.line_CG_length.get_value())
        G, label_G = self.get_dot_and_label("G", line_CG.get_end(), DOWN)

        givens = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        )
        intermediaries = (
            D, G,
            label_D, label_G,
            line_CD, line_CG
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        ) = givens
        (
            D, G,
            label_D, label_G,
            line_CD, line_CG
        ) = given_intermediaries
        
        line_CE, E, line_EA = interpolate_line(line_CA, 0.5)
        E, label_E = self.get_dot_and_label("E", E.get_center(), DL)
        line_CE_marker = get_line_marker(line_CE, marker_type="/")
        line_EA_marker = get_line_marker(line_EA, marker_type="/")

        line_BE = Line(B.get_center(), E.get_center())
        _, line_EF = extend_line_by_length(line_BE, line_BE.get_length())
        F, label_F = self.get_dot_and_label("F", line_EF.get_end(), UR)

        line_BE_marker = get_line_marker(line_BE, marker_type="//")
        line_EF_marker = get_line_marker(line_EF, marker_type="//")

        line_CF = Line(C.get_center(), F.get_center())

        line_BH, H, line_HC = interpolate_line(line_BC, 0.5)
        H, label_H = self.get_dot_and_label("H", H.get_center(), DL)
        line_BH_marker = get_line_marker(line_BH, marker_type="///")
        line_HC_marker = get_line_marker(line_HC, marker_type="///")

        line_AH = Line(A.get_center(), H.get_center())
        _, line_HI = extend_line_by_length(line_AH, line_AH.get_length())
        I, label_I = self.get_dot_and_label("I", line_HI.get_end(), DL)

        line_CI = Line(C.get_center(), I.get_center())

        line_AH_marker = get_line_marker(line_AH, marker_type="////")
        line_HI_marker = get_line_marker(line_HI, marker_type="////")

        angle_AEB_marker = get_angle_marker(line_BE, line_EA, marker_type="(")
        angle_CEF_marker = get_angle_marker(line_CE, line_EF, marker_type=")")

        angle_BAE_marker = get_angle_marker(line_EA, line_AB, marker_type="((")
        angle_ECF_marker = get_angle_marker(line_CF.copy().rotate(PI), line_CE, marker_type="))")

        angle_AHB_marker = get_angle_marker(line_BH, line_AH.copy().rotate(PI), marker_type="(((")
        angle_CHI_marker = get_angle_marker(line_HI.copy().rotate(PI), line_HC, marker_type=")))")

        angle_ABC_marker = get_angle_marker(line_AB, line_BC, marker_type="((((")
        angle_HCI_marker = get_angle_marker(line_HC, line_CI, marker_type="))))", radius=0.2)
        # angle_DCF_marker = get_angle_marker(line_CD.copy().rotate(PI), line_CF, marker_type="))))", radius=0.2)

        intermediaries = (
            E, F, G, H, I,
            label_E, label_F, label_G, label_H, label_I,
            line_AH, line_BE, line_BH, line_CF, line_CG, line_CI, line_EF, line_HC, line_HI,
            line_AH_marker, line_BE_marker, line_BH_marker, line_CE_marker, line_EA_marker, line_EF_marker, line_HC_marker, line_HI_marker,
            angle_ABC_marker, angle_AEB_marker, angle_AHB_marker, angle_BAE_marker, angle_CEF_marker, angle_CHI_marker, angle_ECF_marker, angle_HCI_marker
        )
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AE ~= |CE", "[Prop. 1.10]"),
            (r"|BE ~= |FE", "[Prop. 1.3]"),
            (r"<AEB ~= <CEF", "[Prop. 1.15]"),
            (r"^ABE ~= ^FEC", "[Prop. 1.4]"),
            (r"<BAE ~= <ECF", "[Prop. 1.4]"),
            (r"<ECD > <ECF", "[Construction]"),
            (r"<ECD > <BAE", "[5. + 6.]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP + 0.5*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*DOWN + 2.5*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*DOWN + 0.5*RIGHT)
        self.line_CD_length = ValueTracker(2)
        self.line_CG_length = ValueTracker(2)

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