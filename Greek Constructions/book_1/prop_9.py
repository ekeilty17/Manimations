import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *
import footnote_text as ft

class Book1Prop9(GreekConstructionScenes):

    title = "Book 1 Proposition 9"
    description = """
        To cut a given rectilinear angle in half
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, LEFT)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, RIGHT)

        line_AB = Line(A.get_center(), B.get_center())
        line_AC = Line(A.get_center(), C.get_center())

        givens = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_AC
        )
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_AC
        ) = givens

        line_AD, D, line_DB = interpolate_line(line_AB, self.D_percentage.get_value())
        D, label_D = self.get_dot_and_label("D", D.get_center(), LEFT)
        line_AD_marker = get_line_marker(line_AD, "|")

        line_AE, _ = extend_line_by_length(line_AC, line_AD.get_length(), switch_direction=True)
        E, label_E = self.get_dot_and_label("E", line_AE.get_end(), RIGHT)
        line_AE_marker = get_line_marker(line_AE, "|")

        line_DE = Line(D.get_center(), E.get_center())
        _, F = get_equilateral_triangle_apex(line_DE)
        F, label_F = self.get_dot_and_label("F", F.get_center(), DOWN)

        line_DF = Line(D.get_center(), F.get_center())
        line_EF = Line(E.get_center(), F.get_center())
        line_DE_marker = get_line_marker(line_DE, "||")
        line_DF_marker = get_line_marker(line_DF, "||")
        line_EF_marker = get_line_marker(line_EF, "||")

        line_AF = Line(A.get_center(), F.get_center())
        line_AF_marker = get_line_marker(line_AF, "|||")

        angle_BAF_marker = get_angle_marker(line_AB.copy().rotate(PI), line_AF, ")", radius=0.6)
        angle_CAF_marker = get_angle_marker(line_AC.copy().rotate(PI), line_AF, "(", radius=0.7)

        intermediaries = (
            D, E, F,
            label_D, label_E, label_F,
            line_AD, line_AE, line_DE, line_DF, line_EF,
            line_AD_marker, line_AE_marker, line_AF_marker, line_DE_marker, line_DF_marker, line_EF_marker,
            angle_BAF_marker, angle_CAF_marker
        )
        solution = (line_AF)
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("|AD ~= |AE",   "[Prop. 1.3]"),
            ("|DF ~= |EF",   "[Prop. 1.1]"),
            ("|AF ~= |FA",   "[Reflexivity]"),
            ("^ADF ~= ^AEF", "[Prop. 1.8 (SSS)]"),
            ("<DAF ~= <EAF", "[Prop. 1.8]", self.SOLUTION)
        ]
    def write_footnotes(self):
        return [
            ft.random_point_on_line(r"|AB", r"{D}"),
            ft.postulate1(r"|AD"),
            ft.book1.prop3(r"|AD", r"|AC", r"{A}"),
            ft.postulate1(r"|DE"),
            ft.book1.prop1(r"^ADE", r"|DE"),
            ft.postulate1(r"|AF"),
            ft.reflexivity(r"|AF"),
            ft.book1.prop8(r"^ADF", r"^AEF", r"|AD ~= |AE", r"|DF ~= |EF", r"|AF ~= |FA"),
            ft.common_notion4_congruent_triangles(r"^ADF", r"^AEF", r"<DAF ~= <EAF")
        ]
    def write_tex_to_color_map(self):
        return {
            "|AF": self.SOLUTION,
            "|FA": self.SOLUTION,
        }

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 3*UP)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*DOWN + 1.5*RIGHT)
        self.D_percentage = ValueTracker(0.7)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()

        """ Construction Variables """
        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_AC
        ) = self.givens
        () = self.given_intermediaries
        (
            D, E, F,
            label_D, label_E, label_F,
            line_AD, line_AE, line_DE, line_DF, line_EF,
            line_AD_marker, line_AE_marker, line_AF_marker, line_DE_marker, line_DF_marker, line_EF_marker,
            angle_BAF_marker, angle_CAF_marker
        ) = self.solution_intermediaries
        line_AF = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        tmp = [mob.copy() for mob in [line_AF, angle_BAF_marker, angle_CAF_marker]]
        self.custom_play(*Animate(title, description, *tmp))
        self.wait(2)
        self.custom_play(*Unanimate(title, description, *tmp))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        # Draw point D
        self.custom_play(
            *Animate(D, label_D),
            footnote_animations[0]
        )
        self.wait()
        self.custom_play(
            Animate(line_AD),
            footnote_animations[1]
        )
        self.wait(2)

        # Copy |AD to |AE
        self.custom_play(
            ReplacementTransform(line_AD.copy(), line_AE),
            ReplacementTransform(D.copy(), E),
            ReplacementTransform(label_D.copy(), label_E),
            footnote_animations[2]
        )
        self.custom_play(*Animate(line_AD_marker, line_AE_marker))
        self.wait(2)
        self.animate_proof_line(
            proof_lines[0],
            source_mobjects=[
                A, D, E, F, 
                label_A, label_D, label_E, label_F,
                line_AD, line_AE,
                line_AD_marker, line_AE_marker
            ]
        )
        self.wait(2)

        # Draw |DE
        self.custom_play(
            Animate(line_DE),
            footnote_animations[3]
        )
        self.wait(2)

        # Draw equilateral triangle ^DEF
        self.custom_play(*Animate(F, label_F))
        self.custom_play(
            *Animate(line_DF, line_EF, line_DE_marker, line_DF_marker, line_EF_marker),
            footnote_animations[4]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[1],
            source_mobjects=[
                D, E, F,
                label_D, label_E, label_F,
                line_DF, line_EF,
                line_DF_marker, line_EF_marker
            ]
        )
        self.wait(2)
        
        # |AF ~= |FA
        self.custom_play(
            Animate(line_AF),
            footnote_animations[5]
        )
        self.wait()
        self.custom_play(
            Animate(line_AF_marker),
            footnote_animations[6]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[2],
            source_mobjects=[A, F, label_A, label_F, line_AF, line_AF_marker]
        )
        self.wait(2)

        # ^ADF ~= ^AEF
        emphasize_animations = self.emphasize(
            A, D, E, F, 
            label_A, label_D, label_E, label_F, 
            line_AD, line_AE, line_AF, line_DF, line_EF,
            line_AD_marker, line_AE_marker, line_AF_marker, line_DF_marker, line_EF_marker,
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[7]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[3])
        self.wait(2)

        # Therefore <DAF ~= <EAF
        self.custom_play(
            *Animate(angle_BAF_marker, angle_CAF_marker),
            footnote_animations[8]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[4],
            source_mobjects=[
                A, D, E, 
                label_A, label_D, label_E,
                line_AD, line_AE, line_AF,
                angle_BAF_marker, angle_CAF_marker
            ]
        )
        self.wait(2)

        clear_emphasize_animations = self.clear_emphasize()
        self.custom_play(
            *clear_emphasize_animations,
            footnote_animations[-1]
        )
        self.wait()

        self.write_QED()
        self.wait()