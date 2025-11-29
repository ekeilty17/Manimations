import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *
import footnote_text as ft

class Book1Prop13(GreekConstructionScenes):

    title = "Book 1 Proposition 13"
    description = """
        If a straight-line stood on a(nother) 
        straight-line makes angles, it will 
        certainly either make two right angles, 
        or (angles whose sum is) equal to two 
        right angles.
    """

    def write_givens(self):
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)
        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, DL)

        line_CD = Line(C.get_center(), D.get_center())
        
        _, B, _ = interpolate_line(line_CD, percentage=self.B_percentage.get_value())
        B, label_B = self.get_dot_and_label("B", B.get_center(), DOWN)

        tmp_line = Line(B.get_center(), B.get_center() + self.line_BA_length.get_value() * RIGHT)
        
        line_BA = tmp_line.copy().rotate(self.line_BA_angle.get_value(), about_point=B.get_center())
        A, label_A = self.get_dot_and_label("A", line_BA.get_end(), UR)

        line_BC = Line(B.get_center(), C.get_center())
        line_BD = Line(B.get_center(), D.get_center())

        givens = (
            A, B, C, D, 
            label_A, label_B, label_C, label_D, 
            line_CD, line_BA, line_BC, line_BD
        )
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            A, B, C, D, 
            label_A, label_B, label_C, label_D, 
            line_CD, line_BA, line_BC, line_BD
        ) = givens
        () = given_intermediaries
        
        angle_CBA_marker = get_angle_marker(line_CD, line_BA, "))", radius=0.3)
        angle_CBA_elbow = get_angle_marker(line_CD, line_BA, ")", elbow=True, radius=0.3)

        angle_DBA_marker = get_angle_marker(line_CD.copy().rotate(PI), line_BA, "(", radius=0.2)
        angle_DBA_elbow = get_angle_marker(line_CD.copy().rotate(PI), line_BA, "(", elbow=True, radius=0.2)

        line_BE = line_BA.copy().rotate(PI/2 - self.line_BA_angle.get_value(), about_point=B.get_center())
        E, label_E = self.get_dot_and_label("E", line_BE.get_end(), UP)

        angle_CBE_elbow = get_angle_marker(line_CD, line_BE, ")", elbow=True, radius=0.25)
        angle_DBE_elbow = get_angle_marker(line_CD.copy().rotate(PI), line_BE, "(", elbow=True)

        intermediaries = (
            E, 
            label_E,
            line_BE,
            angle_CBA_marker, angle_DBA_marker, 
            angle_CBA_elbow, angle_CBE_elbow, angle_DBA_elbow, angle_DBE_elbow
        )
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"<CBE = \rightanglesqr", "[Prop. 1.11]"),
            (r"<DBE = \rightanglesqr", "[Prop. 1.11]"),
            (r"<CBA + <ABE = <CBE", "[Construction]"),
            (r"<CBA + <ABE + <DBE \\ = <CBE + <DBE", "[3. + CN. 2]"),
            (r"<ABE + <DBE = <DBA", "[Construction]"),
            (r"<CBA + <ABE + <DBE \\ = <CBA + <DBA", "[5. + CN. 2]"),
            (r"<CBA + <DBA \\ = <CBE + <DBE", "[4. + 6. + CN. 1]", self.SOLUTION),
            (r"<CBA + <DBA = \rightanglesqr + \rightanglesqr", "[1. + 2. + 7. + CN. 1]", self.SOLUTION)
        ]
    def write_footnotes(self):
        return [
            r"\text{Suppose } <CBE ~= <DBE",
            # TODO: ft.definition10()
            r"""
            \text{Since } |CD \text{ and } |AB \text{ form two congruent angles,}
            \text{these angles are by definition } \textbf{right angles}
            """,
            r"\text{So let's assume that } <CBE !~= <DBE",
            ft.book1.prop11("|DC", "|BE"),
            r"\text{By construction, } <CBA + <ABE = <CBE",
            # TODO
            r"""
            \text{Add } <DBE \text{ to both sides,}
            \text{by CN. 2 (Addition) they are still equal}
            """,
            r"\text{By construction, } <DBA = <ABE + <DBE",
            ft.common_notion1("CBA + <DBA", "<CBA + <ABE + <DBE", "<CBE + <DBE", long=True),
            r"""
            \text{Since } <CBE \text{ and } <DBE \text{ are right angles}
            <CBA \text{ and } <DBA \text{ sum to two right angles}
            """
        ]
    def write_tex_to_color_map(self):
        return {
            "{A}": self.GIVEN,
            "{B}": self.GIVEN,
            "{C}": self.GIVEN,
            "{D}": self.GIVEN,
            "|AB": self.GIVEN,
            "|CD": self.GIVEN,
            "|DC": self.GIVEN,
            "<ABC": self.GIVEN,
            "<CBA": self.GIVEN,
            "<ABD": self.GIVEN,
            "<DBA": self.GIVEN,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2*RIGHT)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*DOWN + 2*LEFT)
        self.B_percentage = ValueTracker(0.6)
        self.line_BA_angle = ValueTracker(PI/3)
        self.line_BA_length = ValueTracker(3)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.85, center_horizontally=True)#shift=MED_SMALL_BUFF*LEFT)

        """ Construction Variables """
        (
            A, B, C, D, 
            label_A, label_B, label_C, label_D, 
            line_CD, line_BA, line_BC, line_BD
        ) = self.givens
        # () = self.given_intermediaries
        (
            E, 
            label_E,
            line_BE,
            angle_CBA_marker, angle_DBA_marker, 
            angle_CBA_elbow, angle_CBE_elbow, angle_DBA_elbow, angle_DBE_elbow
        ) = self.solution_intermediaries
        # () = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        solution_explanation = self.MathTex(
            r"<CBA + <DBA = \rightanglesqr + \rightanglesqr", 
            scale=0.9
        )

        self.custom_play(*Animate(title, description, *solution_explanation))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, *solution_explanation))
        self.wait()

        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()

        """ Animation Construction """
        # If <CBA = <DBA, then they must be right by Def. 10
        self.custom_play(
            self.line_BA_angle.animate.set_value(PI/2),
            footnote_animations[0]
        )
        self.wait()

        angle_CBA_marker_copy = get_angle_marker(line_CD, line_BA, ")", radius=0.3)
        angle_CBA_elbow_copy = angle_CBA_elbow.copy()
        angle_DBA_marker_copy = angle_DBA_marker.copy()
        angle_DBA_elbow_copy = angle_DBA_elbow.copy()
        self.custom_play(
            *Animate(angle_CBA_marker_copy, angle_DBA_marker_copy),
        )
        self.wait()
        self.custom_play(
            ReplacementTransform(angle_CBA_marker_copy, angle_CBA_elbow_copy),
            ReplacementTransform(angle_DBA_marker_copy, angle_DBA_elbow_copy),
            footnote_animations[1]
        )
        self.wait(3)

        self.custom_play(
            self.line_BA_angle.animate.set_value(PI/3),
            *Unanimate(angle_CBA_elbow_copy, angle_DBA_elbow_copy),
            footnote_animations[2]
        )
        self.wait(3)

        # Construct |BE
        self.custom_play(
            *Animate(E, label_E, line_BE),
            footnote_animations[3]
        )
        self.custom_play(Animate(angle_DBE_elbow))
        self.wait(2)
        self.animate_proof_line(
            proof_lines[0:2],
            source_mobjects=[
                B, label_B,
                line_BC, line_BD, line_BE,
                angle_DBE_elbow
            ]
        )
        self.wait(2)

        # <CBA + <ABE = <CBE
        emphasize_animations = self.emphasize(
            A, B, C, E,
            label_A, label_B, label_C, label_E,
            line_BA, line_BC, line_BE
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[4]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[2])
        self.wait(2)

        # <CBA + <ABE + <DBE = <CBE + <DBE
        emphasize_animations = self.emphasize(
            A, B, C, D, E,
            label_A, label_B, label_C, label_D, label_E,
            line_BA, line_BC, line_BD, line_BE
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[5]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[3],
            source_mobjects=proof_lines[2]
        )
        self.wait(2)

        # <CBA + <DBA = <CBE + <DBE
        emphasize_animations = self.emphasize(
            A, B, D, E,
            label_A, label_B, label_D, label_E,
            line_BA, line_BD, line_BE
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[6]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[4])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[5],
            source_mobjects=proof_lines[3:5]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[6],
            source_mobjects=proof_lines[3:5]
        )
        self.wait(2)
        self.custom_play(
            footnote_animations[7]
        )
        self.wait(2)

        # Therefore, <CBA and <DBA sum to two right angles
        clear_emphasize_animations = self.clear_emphasize()
        self.custom_play(
            *clear_emphasize_animations,
            footnote_animations[8])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[7],
            source_mobjects=[proof_lines[0], proof_lines[1], proof_lines[4]]
        )
        self.wait(2)

        
        self.custom_play(footnote_animations[-1])
        self.wait()

        self.write_QED()
        self.wait()