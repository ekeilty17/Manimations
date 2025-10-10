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

    def write_givens(self):
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
            line_AB, line_CA
        )
        intermediaries = (
            line_BC, line_AB_marker, line_CA_marker
        )
        return givens, intermediaries

    def write_solution(self, *givens):
        (
            A, B, C, label_A, label_B, label_C, line_AB, line_CA,

            line_BC, line_AB_marker, line_CA_marker,
        ) = givens

        angle_A_marker = get_angle_marker(line_AB.copy().rotate(PI), line_CA.copy().rotate(PI), ")", radius=0.5)

        _, line_BD = extend_line_by_length(line_AB, self.line_BD_length.get_value())
        line_CE, _ = extend_line_by_length(line_CA, self.line_CE_length.get_value())

        D, label_D = self.get_dot_and_label("D", line_BD.get_end(), DL)
        E, label_E = self.get_dot_and_label("E", line_CE.get_end(), DR)
        
        F_position = self.F_position.get_value()
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

        angle_ABG_marker = get_angle_marker(line_AB, line_BG, "((", radius=0.15, radius_step=0.075)
        angle_ACF_marker = get_angle_marker(line_CA.copy().rotate(PI), line_CF, "))", radius=0.15, radius_step=0.075)
        
        angle_CGB_marker = get_angle_marker(line_CG, line_BG.copy().rotate(PI), ")))", radius_step=0.075)
        angle_BFC_marker = get_angle_marker(line_BF, line_CF.copy().rotate(PI), "(((", radius_step=0.075)
        
        # angle_FBC_marker = get_angle_marker(line_BF.copy().rotate(PI), line_BC, ")))", radius=0.2)
        # angle_GCB_marker = get_angle_marker(line_CG.copy().rotate(PI), line_BC.copy().rotate(PI), "(((", radius=0.2)
        angle_BCF_marker = get_angle_marker(line_BC, line_CF, "))))", radius=0.4, radius_step=0.075)
        angle_CBG_marker = get_angle_marker(line_BC.copy().rotate(PI), line_BG, "((((", radius=0.4, radius_step=0.075)
        
        angle_ABC_marker = get_angle_marker(line_AB, line_BC, "(((((", radius=0.35, radius_step=0.075)
        angle_ACB_marker = get_angle_marker(line_CA.copy().rotate(PI), line_BC.copy().rotate(PI), ")))))", radius=0.35, radius_step=0.075)

        intermediaries = (
            D, E, F, G, 
            label_D, label_E, label_F, label_G,
            line_BD, line_BG, line_BF, line_CE, line_CF, line_CG,
            line_BF_marker, line_BG_marker, line_CF_marker, line_CG_marker,
            angle_A_marker, angle_ABG_marker, angle_ACF_marker, angle_BCF_marker, angle_BFC_marker, angle_CBG_marker, angle_CGB_marker,
        )
        solution = (
            angle_ABC_marker, angle_ACB_marker
        )
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("|AB ~= |AC",      "[Given]",          self.GIVEN),
            ("|BF ~= |CG",      "[Prop. 1.3]"),
            ("|AF ~= |AG",      "[CN. 2 (Addition)]"),
            ("<BAG ~= <CAF",    "[Reflexivity]"),
            ("^AFC ~= ^AGB",    "[Prop. 1.4 (SAS)]"),
            ("|FC ~= |GB",      "[Prop. 1.4]"),
            ("<ABG ~= <ACF",    "[Prop. 1.4]"),
            ("<AFC ~= <AGB",    "[Prop. 1.4]"),
            ("^BFC ~= ^CGB",    "[Prop. 1.4 (SAS)]"),
            ("<BCF ~= <CBG",    "[Prop. 1.4]"),
            ("<ABC ~= <ACB",    "[CN. 3 (Subtraction)]",    self.SOLUTION),
        ]
    
    def write_footnotes(self):
        return [
            r"""
            \text{Extend lines } |AB \text{ and } |AC \text{ by any length,}
            \text{assume } |AD \text{ is shorter than } |AE
            """,
            r"""
            \text{Pick any point along line } |BD
            """,
            r"""
            \text{Using Prop 1.3, copy line } |BF \text{ onto line } |CE
            """,
            r"""
            |AB + |BF = |AF
            |AC + |CG = |AG
            |AB ~= |AC  \text{ and } |BF ~= CG
            \text{Therefore, } |AF ~= |AG \text{ by CN. 2 (Addition)}
            """,
            r"""
            <{A} \text{ is congruent to itself (Reflectivity)}
            """,
            r"""
            \text{By Post. 1 draw lines } |FC \text{ and } |GB
            """,
            r"""
            |BA ~= |CA , <BAG ~= <CAF , \text{and } |AG ~= |AF
            \text{therefore } ^AFC ~= ^AGB \text{ by SAS}
            """,
            r"""
            \text{Since } ^AFC ~= ^AGB \text{ corresponding}
            \text{counterparts are congruent}
            """,
            r"""
            |BF ~= |CG , <BFC ~= <CGB, \text{ and } |FC ~= |GB
            \text{therefore } ^BFC ~= ^CGB \text{ by SAS}
            """,
            r"""
            \text{Since } ^BFC ~= ^CGB \text{ corresponding}
            \text{counterparts are congruent}
            """,
            r"""
            <ABC + <CBG = <ABG
            <ACB + <BCF = <ACF
            <ABG ~= <ACF \text{ and } <BCF ~= <CBG
            \text{Therefore, } <ABC ~= <ACB \text{ by CN. 3 (Subtraction)}
            """,
        ]

    def write_tex_to_color_map(self):
        return {
            "|AB": self.GIVEN,
            "|AC": self.GIVEN,
            "|BA": self.GIVEN,
            "|CA": self.GIVEN,
            "|BC": self.GIVEN,
            "|CB": self.GIVEN,
            # "<{A}": self.GIVEN,
            "<ABC": self.SOLUTION,
            "<ACB": self.SOLUTION,
            # "<BAG": self.GIVEN,
            # "<CAF": self.GIVEN,
        }

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 3.25*UP)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + LEFT + 0.25*UP)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + RIGHT + 0.25*UP)
        self.line_BD_length = ValueTracker(2)
        self.line_CE_length = ValueTracker(2.75)
        self.F_position = ValueTracker(0.65)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes(shift=DOWN * MED_SMALL_BUFF)
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.9)

        """ Construction Variables """
        A, B, C, label_A, label_B, label_C, line_AB, line_CA = self.givens
        line_BC, line_AB_marker, line_CA_marker = self.given_intermediaries
        (
            D, E, F, G, 
            label_D, label_E, label_F, label_G,
            line_BD, line_BG, line_BF, line_CE, line_CF, line_CG,
            line_BF_marker, line_BG_marker, line_CF_marker, line_CG_marker,
            angle_A_marker, angle_ABG_marker, angle_ACF_marker, angle_BCF_marker, angle_BFC_marker, angle_CBG_marker, angle_CGB_marker,
        ) = self.solution_intermediaries
        angle_ABC_marker, angle_ACB_marker = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        angle_ABC_marker_copy = get_angle_marker(line_AB, line_BC, "(").set_color(self.color_map[self.SOLUTION]).set_z_index(self.z_index_map[self.ANGLE])
        angle_ACB_marker_copy = get_angle_marker(line_CA.copy().rotate(PI), line_BC.copy().rotate(PI), ")").set_color(self.color_map[self.SOLUTION]).set_z_index(self.z_index_map[self.ANGLE])
        self.custom_play(*Animate(title, description, angle_ABC_marker_copy, angle_ACB_marker_copy))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, angle_ABC_marker_copy, angle_ACB_marker_copy))
        self.wait()

        """ Proof Initialization """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()

        """ Animation """
        self.animate_proof_line(
            proof_lines[0],
            source_mobjects=[A, B, C, label_A, label_B, label_C, line_AB, line_CA, line_AB_marker, line_CA_marker]
        )
        self.wait(2)

        # Extend AB and AC
        self.custom_play(
            *Animate(line_BD, line_CE),
            footnote_animations[0],
        )
        self.custom_play(*Animate(D, E, label_D, label_E))
        self.wait(2)

        # Pick a random point on |BD, draw |BF and copy it over to |CE
        self.custom_play(
            *Animate(F, label_F),
            footnote_animations[1],
        )
        self.add(line_BF)
        self.wait(2)
        self.custom_play(
            ReplacementTransform(line_BF.copy(), line_CG), 
            ReplacementTransform(F.copy(), G), 
            ReplacementTransform(label_F.copy(), label_G),
            footnote_animations[2],
        )
        self.custom_play(*Animate(line_BF_marker, line_CG_marker))
        self.wait(2)
        self.animate_proof_line(
            proof_lines[1],
            source_mobjects=[B, C, F, G, label_B, label_C, label_F, label_G, line_BF, line_CG, line_BF_marker, line_CG_marker]
        )

        self.wait(2)
        
        # |AF ~= |AG
        self.custom_play(footnote_animations[3])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[2],
            source_mobjects=[
                A, B, C, F, G,
                label_A, label_B, label_C, label_F, label_G,
                line_AB, line_BF, line_CA, line_CG,
                line_AB_marker, line_BF_marker, line_CA_marker, line_CG_marker,
            ]
        )
        
        self.wait(2)

        # <A ~= <A
        self.custom_play(
            Animate(angle_A_marker),
            footnote_animations[4],
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[3],
            source_mobjects=[A, B, C, label_A, label_B, label_C, line_AB, line_CA, angle_A_marker]
        )
        
        self.wait(2)

        # Triangle AFC ~= AGB
        self.custom_play(
            *Animate(line_BG, line_CF),
            footnote_animations[5],
        )
        self.wait(2.5)
        emphasize_animations = self.emphasize(
            A, B, C, F, G, 
            label_A, label_B, label_C, label_F, label_G, 
            line_AB, line_BF, line_BG, line_CA, line_CF, line_CG,
            line_AB_marker, line_BF_marker, line_CA_marker, line_CG_marker,
            angle_A_marker,
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[6]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[4])
        
        self.wait(2)
        
        # Congruent parts of these triangles
        self.custom_play(
            *Animate(line_BG_marker, line_CF_marker),
            *Animate(angle_BFC_marker, angle_CGB_marker),
            *Animate(angle_ABG_marker, angle_ACF_marker),
            footnote_animations[7]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[5:8])
        
        self.wait(2)

        # Triangle BFC ~= CGB
        emphasize_animations = self.emphasize(
            B, C, F, G, 
            label_B, label_C, label_F, label_G, 
            line_BC, line_BF, line_BG, line_CF, line_CG,
            line_BF_marker, line_BG_marker, line_CF_marker, line_CG_marker,
            angle_BFC_marker, angle_CGB_marker
        )
        self.custom_play(
            *emphasize_animations, 
            footnote_animations[8]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[8])

        self.wait(2)

        # Congruent parts of these triangles
        self.custom_play(
            *Animate(angle_BCF_marker, angle_CBG_marker),
            footnote_animations[9]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[9])
        # self.wait()
        # self.clear_emphasize()

        self.wait(2)
        
        # Solution: <ABC ~= <ACB
        self.emphasize(
            A, B, C, F, G, 
            label_A, label_B, label_C, label_F, label_G, 
            line_AB, line_BC, line_BG, line_CA, line_CF,
            angle_ABG_marker, angle_ACF_marker, angle_BCF_marker, angle_CBG_marker,
        play=True)
        self.wait(2)
        self.custom_play(
            *Animate(angle_ABC_marker, angle_ACB_marker),
            footnote_animations[10]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[10])
        
        self.wait(2)

        clear_emphasize_animations = self.clear_emphasize()
        self.wait(2)
        self.custom_play(
            *clear_emphasize_animations,
            footnote_animations[-1]
        )
        
        self.wait()

        self.write_QED()
        self.wait()