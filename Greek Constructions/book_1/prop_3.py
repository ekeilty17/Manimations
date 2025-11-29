import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *
import footnote_text as ft

class Book1Prop3(GreekConstructionScenes):

    title = "Book 1 Proposition 3"
    description = """
        For two given unequal straight-lines,
        to cut off from the greater a 
        straight-line equal to the lesser
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, RIGHT)

        line_AB = Line(A.get_center(), B.get_center())
        line_C = Line(
            self.line_C_start_x.get_value() * RIGHT + self.line_C_start_y.get_value() * UP, 
            self.line_C_end_x.get_value() * RIGHT + self.line_C_end_y.get_value() * UP
        )
        _, label_C = self.get_dot_and_label("C", line_C.get_center(), UP, buff=MED_SMALL_BUFF)

        givens = (A, B, label_A, label_B, line_AB, line_C, label_C)
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        A, B, label_A, label_B, line_AB, line_C, label_C = givens

        line_AD = Line(A.get_center(), A.get_center() + line_C.get_length() * RIGHT).rotate(self.line_AD_direction.get_value(), about_point=A.get_center())

        D, label_D = self.get_dot_and_label("D", line_AD.get_end(), UL)

        line_C_marker = get_line_marker(line_C, marker_type="/")
        line_AD_marker = get_line_marker(line_AD, marker_type="/")

        circle_A = OrientedCircle(center=A.get_center(), start=D.get_center())

        E_tmp, *_ = get_line_circle_intersection(line_AB, circle_A)
        E, label_E = self.get_dot_and_label("E", E_tmp.get_center(), DR)
        line_AE = Line(A.get_center(), E.get_center())

        line_AE_marker = get_line_marker(line_AE, marker_type="/", rotate=PI)

        intermediaries = (
            D, label_D,
            line_AD,
            line_AD_marker, line_AE_marker, line_C_marker,
            circle_A,
        )
        solution = (E, label_E, line_AE)
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("|C ~= |AD",    "[Prop. 1.2]"),
            ("|AD ~= |AE",   "[Def. 15]"),
            ("|C ~= |AE",    "[CN. 1]",         self.SOLUTION),
        ]
    def write_footnotes(self):
        return [
            ft.book1.prop2(r"|C", r"{A}"),
            r"""
            \text{The direction of line } |AD \text{ is determined}
            \text{by the procedure of Prop. 1.2, however}
            \text{we will treat it as pseudo-random}
            """,
            ft.postulate3(r"()AD", r"{A}", r"|AD"),
            ft.postulate1(r"|AE", r"{A}", r"{E}"),
            ft.definition15(r"()AD", r"|AD", r"|AE"),
            ft.common_notion1(r"|C", r"|AD", r"|AE")
        ]
    def write_tex_to_color_map(self):
        return {
            "{A}":  self.GIVEN,
            "{B}":  self.GIVEN,
            "|C":   self.GIVEN,
            "|AE":  self.SOLUTION,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(3*RIGHT)
        self.Bx, self.By, _ = get_value_tracker_of_point(6*RIGHT)
        self.line_C_start_x, self.line_C_start_y, _ = get_value_tracker_of_point(4*RIGHT + 3.25*UP)
        self.line_C_end_x, self.line_C_end_y, _ = get_value_tracker_of_point(2*RIGHT + 2.75*UP)
        self.line_AD_direction = ValueTracker(4*PI/5)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=True)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()

        """ Construction Variables """
        A, B, label_A, label_B, line_AB, line_C, label_C = self.givens
        D, label_D, line_AD, line_AD_marker, line_AE_marker, line_C_marker, circle_A = self.solution_intermediaries
        E, label_E, line_AE = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        line_AE_tmp = line_AE.copy().rotate(PI)
        tmp = [mob.copy() for mob in [E, label_E, line_AE_marker, line_C_marker]]
        self.custom_play(
            ReplacementTransform(line_C.copy(), line_AE_tmp),
            *Animate(title, description, *tmp)
        )
        self.wait(3)
        self.custom_play(*Unanimate(title, description, line_AE_tmp, *tmp))
        self.wait()

        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()

        """ Animation Construction """
        # |C copied to point A in random direction
        # |C ~= |AD
        self.custom_play(
            ReplacementTransform(line_C.copy(), line_AD),
            footnote_animations[0]
        )
        self.custom_play(*Animate(D, label_D))
        self.custom_play(*Animate(line_C_marker, line_AD_marker))
        self.wait(2)
        self.animate_proof_line(
            proof_lines[0],
            source_mobjects=[
                A, D,
                label_A, label_D,
                line_AD, line_C, 
                line_AD_marker, line_C_marker,
            ]
        )
        self.wait(2)

        # The angle of |AD is pseudo-random
        self.custom_play(footnote_animations[1])
        self.wait()
        self.custom_play(
            self.line_AD_direction.animate.set_value(4*PI/5 + 2*PI),
            run_time=2
        )

        self.wait(3)

        # Construct ()A
        self.custom_play(
            Animate(circle_A),
            footnote_animations[2]
        )

        self.wait(2)

        # |AD ~= |AE
        self.custom_play(
            *Animate(E, label_E),
            footnote_animations[3]
        )
        self.custom_play(Animate(line_AE))
        self.wait(2)
        self.custom_play(
            Animate(line_AE_marker),
            footnote_animations[4]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[1],
            source_mobjects=[A, D, E, label_A, label_D, label_E, line_AD, line_AE, line_AD_marker, circle_A]
        )

        self.wait(2)

        # Thus, |C ~= |AE
        self.custom_play(footnote_animations[5])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[2],
            source_mobjects=[A, E, label_A, label_C, label_E, line_AE, line_C, line_AE_marker, line_C_marker]
        )

        self.wait(2)
        self.custom_play(footnote_animations[-1])
        
        self.wait()
        
        self.write_QED()
        self.wait()
