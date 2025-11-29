import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *
import footnote_text as ft

class Book1Prop12(GreekConstructionScenes):

    title = "Book 1 Proposition 12"
    description = """
        To draw a straight-line perpendicular 
        to a given infinite straight-line from 
        a given point which is not on it
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, UP)

        # Shifting labels A and B to the edges of the screen
        x_center = 0
        x_right_edge = config.frame_width / 2
        label_A.shift((x_center + 0.5 - label_A.get_center()[0]) * RIGHT)
        label_B.shift((x_right_edge - 0.5 - label_B.get_center()[0]) * RIGHT)

        line_AB = Line(A.get_center(), B.get_center())

        givens = (
            C,
            label_A, label_B, label_C,
            line_AB
        )
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        C, label_A, label_B, label_C, line_AB = givens

        _, E, _ = interpolate_line(line_AB, percentage=self.E_percentage.get_value())
        E, label_E = self.get_dot_and_label("E", E.get_center(), DOWN)
        
        line_CE = Line(C.get_center(), E.get_center())
        line_CD = line_CE.copy().rotate(self.D_offset_angle.get_value(), about_point=C.get_center())
        D, label_D = self.get_dot_and_label("D", line_CD.get_end(), DOWN)

        circle_C = OrientedCircle(C.get_center(), D.get_center())

        line_CF = line_CE.copy().scale([-1, 1, 1], about_point=C.get_center())
        F, label_F = self.get_dot_and_label("F", line_CF.get_end(), DOWN)

        line_EF = Line(E.get_center(), F.get_center())

        line_EF = Line(E.get_center(), F.get_center())
        G, label_G = self.get_dot_and_label("G", line_EF.get_center(), DOWN)

        line_CG = Line(C.get_center(), G.get_center())
        line_GE = Line(G.get_center(), E.get_center())
        angle_CGE_marker = get_angle_marker(line_CG, line_GE, ")", radius=0.25)
        angle_CGE_elbow = get_angle_marker(line_CG, line_GE, elbow=True, radius=0.25)

        line_GF = Line(G.get_center(), F.get_center())
        angle_CGF_marker = get_angle_marker(line_CG, line_GF, "(", radius=0.3)
        angle_CGF_elbow = get_angle_marker(line_CG, line_GF, elbow=True, radius=0.3)

        line_CE_marker = get_line_marker(line_CE, "|")
        line_CF_marker = get_line_marker(line_CF, "|", flip_vertically=True)
        line_GE_marker = get_line_marker(line_GE, "//")
        line_GF_marker = get_line_marker(line_GF, "//", rotate=PI)
        line_CG_marker = get_line_marker(line_CG, "///", flip_vertically=True)

        intermediaries = (
            D, E, F, 
            label_D, label_E, label_F,
            line_CE, line_CF, line_EF, line_GE, line_GF,
            circle_C,
            line_CE_marker, line_CF_marker, line_CG_marker, line_GE_marker, line_GF_marker,
            angle_CGE_marker, angle_CGE_elbow, angle_CGF_marker, angle_CGF_elbow, 
        )
        solution = (
            G, label_G, line_CG, 
        )

        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("|CE ~= |CF", "[Def. 15]"),
            ("|EG ~= |FG", "[Prop. 1.10]"),
            ("|CF ~= |FC", "[Reflexivity]"),
            ("^CEG ~= ^CFG", "[Prop. 1.8 (SSS)]"),
            ("<EGC ~= <FGC", "[Prop. 1.8]"),
            (r"<EGC \text{ is right angle}", "[Def. 10]", self.SOLUTION),
            (r"<FGC \text{ is right angle}", "[Def. 10]", self.SOLUTION),
            ("|AB perp |CG", "[Def. 10]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return [
            r"""
            \text{Pick any point on the side of } |AB \text{ opposite of } {C}
            """,
            ft.postulate3(r"()C", r"{C}", r"|CD"),
            r"""
            \text{Let } {E} \text{ and } {F} \text{ be the intersection of}
            \text{line } |AB \text{ and } ()C
            """,
            ft.postulate1_multiple_lines(r"|CE", r"|CF"),
            ft.definition15(r"()C", r"|CE", r"|CF"),
            ft.postulate1(r"|EF"),
            ft.book1.prop10(r"|EF", r"{G}"),
            ft.postulate1(r"|CG"),
            ft.reflexivity(r"|CG"),
            ft.book1.prop8(r"^CEG", r"^CFG", r"|CE ~= |CF", r"|EG ~= |FG", r"|GC ~= |GC"),
            ft.common_notion4_congruent_triangles(r"^CEG", r"^CFG", r"<EGC ~= <FGC"),
            # TODO: ft.definition10()
            r"""
            \text{Since } |AB \text{ and } |CG \text{ form two congruent angles,}
            \text{these angles are by definition } \textbf{right angles}
            """,
            r"""
            \text{Therefore, line } |CG \text{ is } \textbf{perpendicular} \text{ to line } |AB
            """
        ]
    def write_tex_to_color_map(self):
        return {
            "{C}": self.GIVEN,
            "{G}": self.SOLUTION,
            "|AB": self.GIVEN,
            "|CG": self.SOLUTION,
            "|GC": self.SOLUTION,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(1.5*DOWN)
        self.Bx, self.By, _ = get_value_tracker_of_point(1.5*DOWN + (config.frame_width / 2)*RIGHT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.75*UP)
        self.D_offset_angle = ValueTracker(PI/8)
        self.E_percentage = ValueTracker(0.25)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes(shift=DOWN * SMALL_BUFF)
        proof_line_numbers, proof_lines = self.initialize_proof()

        """ Construction Variables """
        C, label_A, label_B, label_C, line_AB = self.givens
        () = self.given_intermediaries
        (
            D, E, F, 
            label_D, label_E, label_F,
            line_CE, line_CF, line_EF, line_GE, line_GF,
            circle_C,
            line_CE_marker, line_CF_marker, line_CG_marker, line_GE_marker, line_GF_marker,
            angle_CGE_marker, angle_CGE_elbow, angle_CGF_marker, angle_CGF_elbow, 
        ) = self.solution_intermediaries
        G, label_G, line_CG = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        tmp = [mob.copy() for mob in [G, label_G, line_CG]]
        angle_CGF_elbow_copy = angle_CGF_elbow.copy()
        self.custom_play(*Animate(title, description, *tmp))
        self.custom_play(Animate(angle_CGF_elbow_copy))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, *tmp, angle_CGF_elbow_copy))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        # Pick random point on AB
        self.custom_play(
            *Animate(D, label_D),
            footnote_animations[0]
        )
        self.wait(2)

        # ()C
        self.custom_play(
            Animate(circle_C),
            footnote_animations[1]
        )
        self.wait(2)

        # Point E and F
        self.custom_play(
            *Animate(E, F, label_E, label_F),
            footnote_animations[2]
        )
        self.wait(2)

        # |CE ~= |CF
        self.custom_play(
            *Animate(line_CE, line_CF),
            footnote_animations[3]
        )
        self.wait(2)
        self.custom_play(
            *Animate(line_CE_marker, line_CF_marker),
            footnote_animations[4]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[0],
            source_mobjects=[
                C, E, F, 
                label_C, label_E, label_F,
                line_CE, line_CF,
                line_CE_marker, line_CF_marker
            ]
        )
        self.wait(2)

        # |EF
        self.custom_play(
            Animate(line_EF),
            footnote_animations[5]
        )
        self.wait(2)
        self.add(line_GE, line_GF)
        self.remove(line_EF)

        # G is the midpoint of |EF
        self.custom_play(
            *Animate(G, label_G),
            footnote_animations[6]
        )
        self.custom_play(*Animate(line_GE_marker, line_GF_marker))
        self.wait(2)
        self.animate_proof_line(
            proof_lines[1],
            source_mobjects=[
                E, F, G,
                label_E, label_F, label_G,
                line_GE, line_GF,
                line_GE_marker, line_GF_marker
            ]
        )
        self.wait(2)

        # |CG
        self.custom_play(
            Animate(line_CG),
            footnote_animations[7]
        )
        self.wait(2)
        self.custom_play(
            Animate(line_CG_marker),
            footnote_animations[8]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[2],
            source_mobjects=[
                C, G, 
                label_C, label_G,
                line_CG,
                line_CG_marker
            ]
        )
        self.wait(2)

        # ^CEG ~= ^CFG
        emphasize_animations = self.emphasize(
            C, E, F, G, 
            label_C, label_E, label_F, label_G,
            line_CE, line_CF, line_CG, line_GE, line_GF,
            line_CE_marker, line_CF_marker, line_CG_marker, line_GE_marker, line_GF_marker
        )
        self.custom_play(
            *emphasize_animations,
            footnote_animations[9]
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[3])
        self.wait(2)

        # <EGC ~= <FGC
        self.custom_play(
            *Animate(angle_CGE_marker, angle_CGF_marker),
            footnote_animations[10]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[4],
            source_mobjects=[
                G, label_G,
                line_CG, line_GE, line_GF,
                angle_CGE_marker, angle_CGF_marker,
            ]
        )
        self.wait(2)

        # <EGC and <FGC are right angles
        self.custom_play(
            ReplacementTransform(angle_CGE_marker, angle_CGE_elbow),
            ReplacementTransform(angle_CGF_marker, angle_CGF_elbow),
            footnote_animations[11]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[5:7],
            source_mobjects=[
                G, label_G,
                line_CG, line_GE, line_GF,
                angle_CGE_elbow, angle_CGF_elbow,
            ]
        )
        self.wait(2)

        # |AB is perpedicular to |CG
        clear_emphasize_animations = self.clear_emphasize()
        self.custom_play(
            *clear_emphasize_animations,
            Unanimate(angle_CGE_elbow),
            footnote_animations[12]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[7],
            source_mobjects=[
                G,
                label_A, label_B, label_G,
                line_AB, line_CG,
                angle_CGF_elbow,
            ]
        )
        self.wait(2)

        self.custom_play(footnote_animations[-1])
        self.wait()

        self.write_QED()
        self.wait()