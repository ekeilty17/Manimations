import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *
import footnote_text as ft

class Book1Prop10(GreekConstructionScenes):

    title = "Book 1 Proposition 10"
    description = """
        To cut a given finite straight-line in half
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)

        line_AB = Line(A.get_center(), B.get_center())

        givens = (
            A, B,
            label_A, label_B,
            line_AB
        )
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        A, B, label_A, label_B, line_AB = givens

        C, _ = get_equilateral_triangle_apex(line_AB)
        C, label_C = self.get_dot_and_label("C", C.get_center(), UP)

        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())
        
        line_AB_marker = get_line_marker(line_AB, "|")
        line_BC_marker = get_line_marker(line_BC, "|")
        line_CA_marker = get_line_marker(line_CA, "|")

        D, label_D = self.get_dot_and_label("D", (A.get_center() + B.get_center())/2, DOWN)
        
        line_CD = Line(C.get_center(), D.get_center())
        line_CD_marker = get_line_marker(line_CD, "||", flip_vertically=True)

        angle_ACD_marker = get_angle_marker(line_CA.copy().rotate(PI), line_CD, ")", radius=0.4)
        angle_BCD_marker = get_angle_marker(line_BC, line_CD, "(", radius=0.5)

        line_AD = Line(A.get_center(), D.get_center())
        line_DB = Line(D.get_center(), B.get_center())
        line_AD_marker = get_line_marker(line_AD, "///", flip_horizontally=True, flip_vertically=True)
        line_DB_marker = get_line_marker(line_DB, "///", flip_horizontally=True, flip_vertically=True)

        intermediaries = (
            C, 
            label_C,
            line_AD, line_BC, line_CA, line_CD, line_DB,
            line_AB_marker, line_AD_marker, line_BC_marker, line_CA_marker, line_CD_marker, line_DB_marker,
            angle_ACD_marker, angle_BCD_marker,
        )
        solution = (
            D,
            label_D,
        )
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("|AC ~= |BC", "[Prop. 1.1]"),
            ("<ACD ~= <BCD", "[Prop. 1.9]"),
            ("|CD ~= |DC", "[Reflexivity]"),
            ("^ACD ~= ^BCD", "[Prop. 1.4 (SAS)]"),
            ("|AD ~= |BD", "[Prop. 1.4]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return [
            ft.book1.prop1(r"^ABC", r"|AB"),
            ft.book1.prop9(r"<ACB"),
            r"""
            \text{Extend the bisector of angle } <ACB
            \text{until it intersects line } |AB
            """,
            ft.reflexivity(r"\text{Line } |CD"),
            ft.book1.prop4(r"|AC ~= |BC", r"<ACD ~= <BCD", r"|CD ~= |DC", r"^ACD", r"^BCD"),
            ft.corresponding_parts_of_congruent_triangles_are_congruent(r"^ADF", r"^AEF"),
        ]
    def write_proof_color_map(self):
        return {
            "{A}": self.GIVEN,
            "{B}": self.GIVEN,
            "|AB": self.GIVEN,
            "{D}": self.SOLUTION,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.5*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.5*RIGHT)
        
        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()

        """ Construction Variables """
        A, B, label_A, label_B, line_AB = self.givens
        (
            C, 
            label_C,
            line_AD, line_BC, line_CA, line_CD, line_DB,
            line_AB_marker, line_AD_marker, line_BC_marker, line_CA_marker, line_CD_marker, line_DB_marker,
            angle_ACD_marker, angle_BCD_marker,
        ) = self.solution_intermediaries
        D, label_D = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        tmp1 = [mob.copy() for mob in [D, label_D]]
        tmp2 = [mob.copy() for mob in [line_AD_marker, line_DB_marker]]
        self.custom_play(*Animate(title, description, *tmp1))
        self.custom_play(*Animate(*tmp2))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, *tmp1, *tmp2))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        # Draw equivalateral ^ABC
        self.custom_play(
            *Animate(C, label_C),
            footnote_animations[0]
        )
        self.custom_play(
            *Animate(line_BC, line_CA, line_AB_marker, line_BC_marker, line_CA_marker)
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[0],
            source_mobjects=[
                A, B, C,
                label_A, label_B, label_C,
                line_BC, line_CA, 
                line_BC_marker, line_CA_marker,
            ]
        )
        self.wait(2)

        # Bisect angle C
        self.custom_play(
            Animate(line_CD),
            Unanimate(line_AB_marker),
            footnote_animations[1]
        )
        self.custom_play(*Animate(angle_ACD_marker, angle_BCD_marker))
        self.wait(2)
        self.animate_proof_line(
            proof_lines[1],
            source_mobjects=[
                C,
                label_C,
                line_BC, line_CA, line_CD,
                angle_ACD_marker, angle_BCD_marker,
            ]
        )
        self.wait(2)

        # Draw intersection point D
        self.custom_play(
            *Animate(D, label_D),
            footnote_animations[2]
        )
        self.wait(2)

        # |CD is congruent to itself
        self.custom_play(
            Animate(line_CD_marker),
            footnote_animations[3]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[2],
            source_mobjects=[
                C, D,
                label_C, label_D,
                line_CD,
                line_CD_marker,
            ]
        )
        self.wait(2)

        # ^ACD ~= ^BCD
        self.custom_play(footnote_animations[4])
        self.wait(2)
        self.animate_proof_line(proof_lines[3])
        self.wait(2)

        # Thus, |AD ~= |BD
        self.custom_play(
            *Animate(line_AD_marker, line_DB_marker),
            footnote_animations[5]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[4],
            source_mobjects=[
                A, B, D,
                label_A, label_B, label_D,
                line_AD, line_DB,
                line_AD_marker, line_DB_marker
            ]
        )
        self.wait(2)

        self.custom_play(footnote_animations[-1])
        self.wait()

        self.write_QED()
        self.wait()