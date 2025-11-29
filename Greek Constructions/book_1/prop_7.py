import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *
import footnote_text as ft

class Book1Prop7(GreekConstructionScenes):

    title = "Book 1 Proposition 7"
    description = """
        On the same straight-line, two other 
        straight-lines equal, respectively, to two 
        (given) straight-lines (which meet) cannot be 
        constructed (meeting) at a different point on 
        the same side (of the straight-line), but having
        the same ends as the given straight-lines.

        (This is essentially a lemma used in the proof
        of Prop. 1.8)
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, UP)

        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        line_BC_given = Line(A.get_center(), A.get_center() + get_unit_direction(line_AB) * line_BC.get_length()).shift(4.5*UP)
        line_CA_given = Line(A.get_center(), A.get_center() + get_unit_direction(line_AB) * line_CA.get_length()).shift(4*UP)
        
        line_CA_marker = get_line_marker(line_CA, "/")
        line_BC_marker = get_line_marker(line_BC, "//")
        
        line_CA_given_marker = get_line_marker(line_CA_given, "/")
        line_BC_given_marker = get_line_marker(line_BC_given, "//")

        givens = (
            A, B,
            label_A, label_B,
            line_AB, line_BC_given, line_CA_given,
        )
        intermediaries = (
            C, label_C,
            line_BC, line_CA,
            line_BC_marker, line_BC_given_marker, line_CA_marker, line_CA_given_marker
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            A, B,
            label_A, label_B,
            line_AB, line_BC_given, line_CA_given,
        ) = givens
        (
            C, label_C,
            line_BC, line_CA,
            line_BC_marker, line_BC_given_marker, line_CA_marker, line_CA_given_marker
        ) = given_intermediaries
        
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, UP)
        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, UR)
        
        line_BD = Line(B.get_center(), D.get_center())
        line_DA = Line(D.get_center(), A.get_center())
        line_CD = Line(C.get_center(), D.get_center())

        line_DA_marker = get_line_marker(line_DA, "/")
        line_BD_marker = get_line_marker(line_BD, "//")

        angle_ACD_marker = get_angle_marker(line_CA.copy().rotate(PI), line_CD, ")", radius=0.2)
        angle_ADC_marker = get_angle_marker(line_DA.copy().rotate(PI), line_CD.copy().rotate(PI), "(", radius=0.4)

        angle_BCD_marker = get_angle_marker(line_BC, line_CD, "))", radius=0.4, radius_step=0.05)
        angle_BDC_marker = get_angle_marker(line_BD, line_CD.copy().rotate(PI), "((", radius=0.2, radius_step=0.05)

        for mobject in [D, label_D, line_BD, line_DA]:
            mobject.set_color(self.color_map[self.IMPOSSIBLE])

        intermediaries = (
            D, label_D,
            line_BD, line_CD, line_DA,
            line_DA_marker, line_BD_marker,
            angle_ACD_marker, angle_ADC_marker, angle_BCD_marker, angle_BDC_marker,
        )
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("{C} != {D}", "[Assumption]", self.ASSUMPTION),
            ("|AC ~= |AD", "[Given]", self.ASSUMPTION),
            ("|BC ~= |BD", "[Given]", self.ASSUMPTION),
            ("<ACD ~= <ADC", "[1. + Prop. 1.5]", self.PBC_INTERMEDIARY),
            ("<BCD ~= <BDC", "[2. + Prop. 1.5]", self.PBC_INTERMEDIARY),
            ("<ACD > <BCD", "[Construction]", self.CONTRADICTION),
            ("<ADC < <BDC", "[Construction]", self.PBC_INTERMEDIARY),
            ("<ACD < <BCD", "[4. + 5. + 7.]", self.CONTRADICTION),
            ("{C} = {D}", "[By Contradiction]", self.SOLUTION)
        ]
    
    def write_footnotes(self):
        return [
            r"""
            \text{In other words, point } {C} \text{ is unique.}
            \text{It is not possible for striaght-lines of the}
            \text{same length to meet at a different point } {D}
            """,
            r"""
            \text{Assume torward a contradiction that}
            \text{such a point } {D} \text{ exists}
            """,
            ft.postulate1(r"|CD"),
            ft.book1.prop6(r"|AC", r"|AD", r"<ACD", r"<ADC"),
            ft.book1.prop6(r"|BC", r"|BD", r"<BCD", r"<BDC"),
            r"""
            <BCD \text{ lies inside } <ACD
            \text{thus, by construction } <ACD > <BCD
            """,
            r"""
            <ADC \text{ lies inside } <BDC
            \text{thus, by construction } <ADC < <BDC
            """,
            r"""
            <ADC < <BDC
            <ADC ~= <ACD \text{ and } <BDC ~= <BCD
            \text{Thus, } <ACD < <BCD
            """,
            r"""
            \text{But now we have show that}
            <ACD > <BCD \text{ and } <ACD < <BCD
            \text{Thus, we have arrived at a contradiction}
            """
        ]
    
    def write_tex_to_color_map(self):
        return {
            #"{C}": self.SOLUTION,
            "{D}": self.IMPOSSIBLE,
            "|AD": self.IMPOSSIBLE,
            "|BD": self.IMPOSSIBLE,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2*RIGHT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*RIGHT + 1.5*UP)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*RIGHT + 1*UP)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.95)

        """ Construction Variables """
        (
            A, B,
            label_A, label_B,
            line_AB, line_BC_given, line_CA_given,
        ) = self.givens
        (
            C, label_C,
            line_BC, line_CA,
            line_BC_marker, line_BC_given_marker, line_CA_marker, line_CA_given_marker
        ) = self.given_intermediaries
        (
            D, label_D,
            line_BD, line_CD, line_DA,
            line_DA_marker, line_BD_marker,
            angle_ACD_marker, angle_ADC_marker, angle_BCD_marker, angle_BDC_marker,
        ) = self.solution_intermediaries
        () = self.solution

        """ Introduction """
        self.add(*self.givens, line_BC_given_marker, line_CA_given_marker)
        self.wait()
        
        self.custom_play(
            *Animate(title, description),
            ReplacementTransform(line_BC_given.copy().rotate(PI), line_BC),
            ReplacementTransform(line_CA_given.copy().rotate(PI), line_CA),
            ReplacementTransform(line_BC_given_marker.copy().rotate(PI), line_BC_marker),
            ReplacementTransform(line_CA_given_marker.copy().rotate(PI), line_CA_marker),
        )
        self.custom_play(*Animate(C, label_C))
        self.wait()

        source_tmp = [mob.copy() for mob in [C, label_C, line_BC, line_CA, line_BC_marker, line_CA_marker]]
        targets = [D, label_D, line_BD, line_DA, line_BD_marker, line_DA_marker]
        self.wait()
        self.custom_play(
            *[ReplacementTransform(source, target) for source, target in zip(source_tmp, targets)],
            footnote_animations[0]
        )
        self.wait(3)

        self.custom_play(*Unanimate(title, description))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        # Assumption
        self.custom_play(footnote_animations[1])
        self.wait()
        self.animate_proof_line(
            proof_lines[0],
            source_mobjects=[C, D, label_C, label_D]
        )
        self.wait(2)

        self.animate_proof_line(
            proof_lines[1:3],
            source_mobjects=[
                A, B, C, D,
                label_A, label_B, label_C, label_D,
                line_BC, line_BD, line_CA, line_DA,
                line_BC_marker, line_BD_marker, line_CA_marker, line_DA_marker,
            ]
        )
        self.wait(2)

        # Draw |CD
        self.custom_play(
            Animate(line_CD),
            footnote_animations[2]
        )
        self.wait(2)

        # ^ACD
        emphasize_animations = self.emphasize(
            A, C, D, 
            label_A, label_C, label_D,
            line_CA, line_CD, line_DA,
            line_CA_marker, line_DA_marker,
            angle_ACD_marker, angle_ADC_marker,
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[3],
        )
        self.wait(2)
        self.custom_play(*Animate(angle_ACD_marker, angle_ADC_marker))
        self.wait(2)
        self.animate_proof_line(proof_lines[3])
        self.wait(2)

        # ^BCD
        emphasize_animations = self.emphasize(
            B, C, D, 
            label_B, label_C, label_D,
            line_BC, line_BD, line_CD,
            line_BC_marker, line_BD_marker,
            angle_BCD_marker, angle_BDC_marker,
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[4],
        )
        self.wait(2)
        self.custom_play(*Animate(angle_BCD_marker, angle_BDC_marker))
        self.wait(2)
        self.animate_proof_line(proof_lines[4])
        self.wait(2)

        # <ACD > <BCD
        emphasize_animations = self.emphasize(
            A, B, C, D, 
            label_A, label_B, label_C, label_D,
            line_BC, line_CA, line_CD,
            angle_ACD_marker, angle_BCD_marker,
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[5],
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[5])
        self.wait(2)

        # <ADC > <BDC
        emphasize_animations = self.emphasize(
            A, B, C, D, 
            label_A, label_B, label_C, label_D,
            line_BD, line_CD, line_DA,
            angle_ADC_marker, angle_BDC_marker,
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[6],
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[6])
        self.wait(2)
        
        # Contradiction
        self.clear_emphasize(play=True)
        self.wait(2)
        self.custom_play(footnote_animations[7])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[7],
            source_mobjects=[
                A, B, C, D,
                label_A, label_B, label_C, label_D,
                line_BC, line_CA, line_CD,
                angle_ACD_marker, angle_ADC_marker, angle_BCD_marker, angle_BDC_marker
            ]
        )
        self.wait(2)
        self.custom_play(footnote_animations[8])
        self.wait(2)
        self.animate_proof_line(proof_lines[8])
        self.wait(2)
        self.custom_play(footnote_animations[-1])
        self.wait()

        self.write_QED()
        self.wait()

        

