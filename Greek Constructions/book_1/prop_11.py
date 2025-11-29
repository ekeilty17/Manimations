import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *
import footnote_text as ft

class Book1Prop11(GreekConstructionScenes):

    title = "Book 1 Proposition 11"
    description = """
        To draw a straight-line at right-angles
        to a given straight-line from a given 
        point on it
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        
        # Shifting labels A and B to the edges of the screen
        x_center = 0
        x_right_edge = config.frame_width / 2
        label_A.shift((x_center + 0.25 - label_A.get_center()[0]) * RIGHT)
        label_B.shift((x_right_edge - 0.25 - label_B.get_center()[0]) * RIGHT)
        
        line_AB = Line(A.get_center(), B.get_center())
        
        line_AC, C, line_CB = interpolate_line(line_AB, self.C_percentage.get_value())
        C, label_C = self.get_dot_and_label("C", C.get_center(), DOWN)

        givens = (
            C,
            label_A, label_B, label_C,
            line_AB,
        )
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        C, label_A, label_B, label_C, line_AB = givens

        line_AC = Line(line_AB.get_start(), C.get_center())
        _, D, line_DC = interpolate_line(line_AC, self.D_percentage.get_value())
        D, label_D = self.get_dot_and_label("D", D.get_center(), DOWN)

        _, line_CE = extend_line_by_length(line_DC, line_DC.get_length())
        E, label_E = self.get_dot_and_label("E", line_CE.get_end(), DOWN)

        line_DE = Line(D.get_center(), E.get_center())
        F, _ = get_equilateral_triangle_apex(line_DE)
        F, label_F = self.get_dot_and_label("F", F.get_center(), UP)

        line_CE_marker = get_line_marker(line_CE, "/")
        line_DC_marker = get_line_marker(line_DC, "/")
        
        line_EF = Line(E.get_center(), F.get_center())
        line_FD = Line(F.get_center(), D.get_center())
        line_EF_marker = get_line_marker(line_EF, "||")
        line_FD_marker = get_line_marker(line_FD, "||")

        line_FC = Line(F.get_center(), C.get_center())
        line_FC_marker = get_line_marker(line_FC, "///", flip_vertically=True)

        angle_FCD_marker = get_angle_marker(line_FC, line_DC.copy().rotate(PI), ")", radius=0.25)
        angle_FCE_marker = get_angle_marker(line_FC, line_CE, "(", radius=0.3)
        angle_FCD_elbow = get_angle_marker(line_FC, line_DC.copy().rotate(PI), radius=0.25, elbow=True)
        angle_FCE_elbow = get_angle_marker(line_FC, line_CE, radius=0.3, elbow=True)

        intermediaries = (
            D, E, F,
            label_D, label_E, label_F,
            line_CE, line_DC, line_EF, line_FD,
            line_CE_marker, line_DC_marker, line_EF_marker, line_FC_marker, line_FD_marker,
            angle_FCD_marker, angle_FCE_marker, angle_FCD_elbow, angle_FCE_elbow
        )
        solution = (
            line_FC
        )
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("|DC ~= |EC", "[Prop. 1.3]"),
            ("|DF ~= |EF", "[Prop. 1.1]"),
            ("|CF ~= |CF", "[Reflexivity]"),
            ("^DCF ~= ^ECF", "[Prop. 1.8 (SSS)]"),
            ("<DCF ~= <ECF", "[Prop. 1.8]"),
            (r"<DCF \text{ is right angle}", "[Def. 10]", self.SOLUTION),
            (r"<ECF \text{ is right angle}", "[Def. 10]", self.SOLUTION),
            ("|CF perp |AB", "[Def. 10]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return [
            ft.random_point_on_line(r"|AC", r"{D}"),
            ft.postulate1(r"|DC"),
            ft.book1.prop3(r"|DC", r"|CB", r"{C}"),
            ft.book1.prop1(r"^DEF", r"|DE"),
            ft.postulate1(r"|FC", r"{F}", r"{C}"),
            ft.reflexivity(r"|CF"),
            ft.book1.prop8(r"^DCF", r"^ECF", r"|DC ~= |EC", r"|CF ~= |CF", r"|FD ~= |FE"),
            ft.common_notion4_congruent_triangles(r"^DCF", r"^ECF", r"<DCF ~= <ECF"),
            # TODO:
            r"""
            \text{Since } |AB \text{ and } |CF \text{ form two congruent angles,}
            \text{these angles are by definition } \textbf{right angles}
            """,
            r"""
            \text{Therefore, line } |CF \text{ is } \textbf{perpendicular} \text{ to line } |AB
            """
        ]
    def write_tex_to_color_map(self):
        return {
            "|AB": self.GIVEN,
            "|CF": self.SOLUTION,
            "|FC": self.SOLUTION,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(DOWN)
        self.Bx, self.By, _ = get_value_tracker_of_point(DOWN + (config.frame_width / 2)*RIGHT)
        self.C_percentage = ValueTracker(0.5)
        self.D_percentage = ValueTracker(0.55)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.95)

        """ Construction Variables """
        C, label_A, label_B, label_C, line_AB = self.givens
        () = self.given_intermediaries
        (
            D, E, F,
            label_D, label_E, label_F,
            line_CE, line_DC, line_EF, line_FD,
            line_CE_marker, line_DC_marker, line_EF_marker, line_FC_marker, line_FD_marker,
            angle_FCD_marker, angle_FCE_marker, angle_FCD_elbow, angle_FCE_elbow
        ) = self.solution_intermediaries
        line_FC = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        line_FC_copy = line_FC.copy().rotate(PI)
        angle_FCE_elbow_copy = angle_FCE_elbow.copy()
        self.custom_play(*Animate(title, description, line_FC_copy))
        self.custom_play(Animate(angle_FCE_elbow_copy))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, line_FC_copy, angle_FCE_elbow_copy))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        # Draw D
        self.custom_play(
            *Animate(D, label_D),
            footnote_animations[0]
        )
        self.wait(2)

        # Draw |DC
        self.custom_play(
            Animate(line_DC),
            footnote_animations[1]
        )
        self.wait(2)

        # Copy |DC to |BC at point C
        self.custom_play(
            *Animate(line_CE, E, label_E),
            footnote_animations[2]
        )
        self.custom_play(*Animate(line_DC_marker, line_CE_marker))
        self.wait(2)
        self.animate_proof_line(
            proof_lines[0],
            source_mobjects=[
                C, D, E,
                label_C, label_D, label_E,
                line_DC, line_CE,
                line_DC_marker, line_CE_marker
            ]
        )
        self.wait(2)

        # Draw equilateral triangle ^DEF
        self.custom_play(
            *Animate(F, label_F),
            footnote_animations[3]
        )
        self.custom_play(
            *Animate(line_EF, line_FD, line_EF_marker, line_FD_marker)
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[1],
            source_mobjects=[
                D, E, F,
                label_D, label_E, label_F,
                line_EF, line_FD, 
                line_EF_marker, line_FD_marker, 
            ]
        )
        self.wait(2)

        # |FC
        self.custom_play(
            Animate(line_FC),
            footnote_animations[4]
        )
        self.wait(2)
        self.custom_play(
            Animate(line_FC_marker),
            footnote_animations[5]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[2],
            source_mobjects=[
                C, F,
                label_C, label_F,
                line_FC,
                line_FC_marker
            ]
        )
        self.wait(2)

        # ^DCF ~= ^ECF
        self.custom_play(footnote_animations[6])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[3],
            source_mobjects=[
                C, D, E, F,
                label_C, label_D, label_E, label_F,
                line_CE, line_DC, line_EF, line_FC, line_FD,
                line_CE_marker, line_DC_marker, line_EF_marker, line_FC_marker, line_FD_marker,
            ]
        )
        self.wait(2)

        # <DCF ~= <ECF
        self.custom_play(
            *Animate(angle_FCD_marker, angle_FCE_marker),
            footnote_animations[7]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[4],
            source_mobjects=[
                C,
                label_C,
                line_CE, line_DC, line_FC,
                angle_FCD_marker, angle_FCE_marker
            ]
        )
        self.wait(2)

        # <DCF and <ECF are right angles
        self.custom_play(
            ReplacementTransform(angle_FCD_marker, angle_FCD_elbow),
            ReplacementTransform(angle_FCE_marker, angle_FCE_elbow),
            footnote_animations[8]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[5:7],
            source_mobjects=[
                C,
                label_C,
                line_CE, line_DC, line_FC,
                angle_FCD_marker, angle_FCE_marker
            ]
        )
        self.wait(2)

        # |DC is perpedicular to |CF
        self.custom_play(
            Unanimate(angle_FCD_elbow),
            footnote_animations[9]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[7],
            source_mobjects=[
                C,
                label_A, label_B, label_C,
                line_AB, line_FC,
                angle_FCE_elbow
            ]
        )
        self.wait(2)

        self.custom_play(footnote_animations[-1])
        self.wait()

        self.write_QED()
        self.wait()