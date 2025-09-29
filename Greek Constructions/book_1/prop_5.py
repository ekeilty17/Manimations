import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop5(GreekConstructionScenes):

    title = "Book 1 Proposition 5"
    description = """
        For isosceles triangles, the angles at the base 
        are equal to one another, and if the equal sides 
        are produced then the angles under the base will 
        be equal to one another
    """

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, LEFT)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, RIGHT)

        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        line_AB_marker = get_line_marker(line_AB, marker_type="/")
        line_CA_marker = get_line_marker(line_CA, marker_type="/", flip_vertically=True)

        givens = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        )
        intermediaries = (
            line_AB_marker, line_CA_marker
        )
        return givens, intermediaries

    def get_solution(self, *givens):
        (
            A, B, C, label_A, label_B, label_C, line_AB, line_BC, line_CA,

            line_AB_marker, line_CA_marker,
        ) = givens

        angle_A_marker = get_angle_marker(line_AB, line_CA.copy().rotate(PI), ")", radius=0.5)

        _, line_BD = extend_line_by_length(line_AB, 2.25)
        line_CE, _ = extend_line_by_length(line_CA, 3.5)

        D, label_D = self.get_dot_and_label("D", line_BD.get_end(), DL)
        E, label_E = self.get_dot_and_label("E", line_CE.get_end(), DR)
        
        F_position = 0.65
        F, label_F = self.get_dot_and_label("F", (1-F_position)*B.get_center() + F_position*D.get_center(), DL + 0.5*LEFT, buff=SMALL_BUFF)
        line_BF = Line(B.get_center(), F.get_center())
        
        line_CG, _ = extend_line_by_length(line_CA, line_BF.get_length())
        G, label_G = self.get_dot_and_label("G", line_CG.get_end(), DR + 0.5*RIGHT, buff=SMALL_BUFF)

        line_BG = Line(B.get_center(), G.get_center())
        line_CF = Line(C.get_center(), F.get_center())
        
        line_BF_marker = get_line_marker(line_BF, marker_type="//")
        line_BG_marker = get_line_marker(line_BG, marker_type="///", position=0.55)
        line_CF_marker = get_line_marker(line_CF, marker_type="///", position=0.55, flip_vertically=True)
        line_CG_marker = get_line_marker(line_CG, marker_type="//", flip_vertically=True)

        angle_BFC_marker = get_angle_marker(line_BF.copy().rotate(PI), line_CF.copy().rotate(PI), "((")
        angle_CGB_marker = get_angle_marker(line_CG.copy().rotate(PI), line_BG.copy().rotate(PI), "))")
        angle_FBC_marker = get_angle_marker(line_BF, line_BC, ")))", radius=0.2)
        angle_GCB_marker = get_angle_marker(line_CG, line_BC.copy().rotate(PI), "(((", radius=0.2)
        angle_ABC_marker = get_angle_marker(line_AB.copy().rotate(PI), line_BC, "((((")
        angle_ACB_marker = get_angle_marker(line_CA, line_BC.copy().rotate(PI), "))))")

        intermediaries = (
            D, E, F, G, 
            label_D, label_E, label_F, label_G,
            line_BD, line_BG, line_BF, line_CE, line_CF, line_CG,
            line_BF_marker, line_BG_marker, line_CF_marker, line_CG_marker,
            angle_A_marker, angle_BFC_marker, angle_CGB_marker, angle_GCB_marker, angle_FBC_marker
        )
        solution = (
            angle_ABC_marker, angle_ACB_marker
        )
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ("|AB ~ |AC",    "[Given]",          self.GIVEN),
            ("|BF ~ |CG",    "[Prop. 1.3]"),
            ("<BAG ~ <CAF",          "[Reflexivity]"),
            ("^AFC ~ ^AGB",    "[Prop. 1.4 (SAS)]"),
            ("|FC ~ |GB",    "[Prop. 1.4]"),
            ("<BFC ~ <CGB",          "[Prop. 1.4]"),
            ("^BFC ~ ^CGB",    "[Prop. 1.4 (SAS)]"),
            ("<FBC ~ <GCB",          "[Prop. 1.4]"),
            ("<ABF ~ <ACG",          "[Def. 10 + Post. 4]"),
            ("<ABC ~ <ACB",          "[Subtraction]",    self.SOLUTION),
        ]
    def get_proof_color_map(self):
        return {
            "|AB": self.given_color,
            "|AC": self.given_color,
            "|BC": self.given_color,
            "|CB": self.given_color,
            "<CAF": self.given_color,
            "<BAG": self.given_color,
            "<ABC": self.solution_color,
            "<ACB": self.solution_color,
        }

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 3*UP)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + RIGHT)

        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        A, B, C, label_A, label_B, label_C, line_AB, line_BC, line_CA = givens
        line_AB_marker, line_CA_marker = given_intermediaries
        (
            D, E, F, G, 
            label_D, label_E, label_F, label_G,
            line_BD, line_BG, line_BF, line_CE, line_CF, line_CG,
            line_BF_marker, line_BG_marker, line_CF_marker, line_CG_marker,
            angle_A_marker, angle_BFC_marker, angle_CGB_marker, angle_GCB_marker, angle_FBC_marker
        ) = solution_intermediaries
        angle_ABC_marker, angle_ACB_marker = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        
        self.custom_play(title, description)
        self.wait()

        tmp = [mob.copy() for mob in [angle_ABC_marker, angle_ACB_marker]]
        self.custom_play(*tmp)
        self.wait()
        self.play(Unanimate(title, description, *tmp))
        self.wait()

        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof()
        self.play(Write(proof_line_numbers))
        self.wait()

        """ Animation """
        self.emphasize(A, B, C, label_A, label_B, label_C, line_AB, line_CA, line_AB_marker, line_CA_marker)
        self.wait()
        self.play(Write(proof_lines[0]))
        self.wait()
        self.undo_emphasize()

        self.wait()

        # Extend AB and AC
        self.custom_play(line_BD, line_CE)
        self.custom_play(D, label_D, E, label_E)

        # Pick a random point on BD and copy it over to CE
        random_point_text = MathTex(
            r"\begin{aligned}&\text{Pick any point} \\ &\text{along } \overline{BD}\end{aligned}",
        ).scale(0.6)
        random_point_text.next_to(line_BC.get_center(), DOWN*3.5)
        self.custom_play(random_point_text)
        self.wait()
        self.custom_play(F, label_F)
        self.wait()
        self.play(Unwrite(random_point_text))
        self.wait()
        self.add(line_BF)
        self.play(
            ReplacementTransform(line_BF.copy(), line_CG), 
            ReplacementTransform(F.copy(), G), 
            ReplacementTransform(label_F.copy(), label_G)
        )
        self.custom_play(line_BF_marker, line_CG_marker)
        self.wait()
        self.play(Write(proof_lines[1]))

        self.wait()
        
        # Triangle AFC ~ AGB
        self.custom_play(line_BG, line_CF)
        self.emphasize(
            A, B, C, F, G, 
            label_A, label_B, label_C, label_F, label_G, 
            line_AB, line_BF, line_BG, line_CA, line_CF, line_CG,
            line_AB_marker, line_BF_marker, line_CA_marker, line_CG_marker
        )
        self.wait()
        self.custom_play(angle_A_marker)
        self.wait()
        self.play(Write(proof_lines[2]))
        self.play(Write(proof_lines[3]))
        self.wait()
        # Congruent parts of these triangles
        self.custom_play(line_BG_marker, line_CF_marker)
        self.wait()
        self.custom_play(angle_BFC_marker, angle_CGB_marker)
        self.wait()
        self.play(Write(proof_lines[4]))
        self.play(Write(proof_lines[5]))
        self.wait()
        self.undo_emphasize()

        self.wait()

        # Triangle BFC ~ CGB
        self.emphasize(
            B, C, F, G, 
            label_B, label_C, label_F, label_G, 
            line_BC, line_BF, line_BG, line_CF, line_CG,
            line_BF_marker, line_BG_marker, line_CF_marker, line_CG_marker,
            angle_BFC_marker, angle_CGB_marker
        )
        self.wait()
        self.play(Write(proof_lines[6]))
        self.wait()
        # Congruent parts of these triangles
        self.custom_play(angle_FBC_marker, angle_GCB_marker)
        self.wait()
        self.play(Write(proof_lines[7]))
        self.wait()
        self.undo_emphasize()

        self.wait()

        # Solution
        self.emphasize(
            A, B, C, F, G, 
            label_A, label_B, label_C, label_F, label_G, 
            line_AB, line_BC, line_BF, line_CA, line_CG,
            angle_FBC_marker, angle_GCB_marker
        )
        self.wait()
        self.custom_play(angle_ABC_marker, angle_ACB_marker)
        self.play(Write(proof_lines[8]))
        self.play(Write(proof_lines[9]))
        self.wait()
        self.undo_emphasize()

        self.wait()