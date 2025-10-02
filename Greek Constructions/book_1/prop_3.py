import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop3(GreekConstructionScenes):

    title = "Book 1 Proposition 3"
    description = """
        For two given unequal straight-lines,
        to cut off from the greater a 
        straight-line equal to the lesser
    """

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, RIGHT)

        line_AB = Line(A.get_center(), B.get_center())
        line_C = Line(
            self.line_C_start_x.get_value() * RIGHT + self.line_C_start_y.get_value() * UP, 
            self.line_C_end_x.get_value() * RIGHT + self.line_C_end_y.get_value() * UP
        )
        label_C = Text("C").scale(self.DOT_LABEL_SCALE).next_to(line_C.get_center(), UP, buff=MED_SMALL_BUFF)

        givens = (A, B, label_A, label_B, line_AB, line_C, label_C)
        intermediaries = ()
        return givens, intermediaries

    def get_solution(self, *givens):
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

    def get_proof_spec(self):
        return [
            ("|C ~= |AD",    "[Prop. 1.2]"),
            ("|AD ~= |AE",   "[Def. 15]"),
            ("|C ~= |AE",    "[Transitivity]",       self.SOLUTION),
        ]
    def get_proof_color_map(self):
        return {
            "|C": self.given_color,
            "|AE": self.solution_color,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(3*RIGHT + 0.5*DOWN)
        self.Bx, self.By, _ = get_value_tracker_of_point(6*RIGHT + 0.5*DOWN)
        self.line_C_start_x, self.line_C_start_y, _ = get_value_tracker_of_point(4*RIGHT + 2.75*UP)
        self.line_C_end_x, self.line_C_end_y, _ = get_value_tracker_of_point(2*RIGHT + 2.25*UP)
        self.line_AD_direction = ValueTracker(4*PI/5)

        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        A, B, label_A, label_B, line_AB, line_C, label_C = givens
        D, label_D, line_AD, line_AD_marker, line_AE_marker, line_C_marker, circle_A = solution_intermediaries
        E, label_E, line_AE = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        
        line_C_tmp = line_C.copy()
        line_AE_tmp = line_AE.copy().rotate(PI)
        tmp = [mob.copy() for mob in [E, label_E, line_AE_marker, line_C_marker]]
        self.play(
            Transform(line_C_tmp, line_AE_tmp),
            Animate(title, description, *tmp),
            run_time=self.default_run_time
        )
        self.wait(2)
        self.custom_unplay(title, description, line_C_tmp, line_AE_tmp, *tmp)
        self.wait()

        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof()
        self.play(Write(proof_line_numbers))
        self.wait()

        """ Animation """
        
        # line_C copied to point D in random direction
        line_C_tmp = line_C.copy()
        self.play(Transform(line_C_tmp, line_AD))
        self.remove(line_C_tmp)
        self.add(line_AD)
        self.custom_play(D, label_D)
        self.wait()
        line_AD_direction_text = MathTex(r"\text{The direction of }", r"\overline{AD}", r"\text{ is determined} \\ \text{by the procedure in Prop. 1.2}")
        line_AD_direction_text.scale(0.7).move_to(self.RIGHT_CENTER).shift(2*DOWN)
        self.custom_play(line_AD_direction_text)
        self.wait(2)
        self.custom_unplay(line_AD_direction_text)
        self.wait()
        self.emphasize(A, D, label_A, label_C, label_D, line_C, line_AD)
        self.wait()
        self.custom_play(line_C_marker, line_AD_marker)
        self.wait()
        # self.play(Write(proof_lines[0]))
        self.play_proof_line(proof_lines[0])
        self.wait()
        self.undo_emphasize()

        self.wait()

        self.custom_play(circle_A)
        self.wait()
        self.custom_play(E, label_E)
        self.custom_play(line_AE)
        self.wait()
        self.emphasize(A, D, E, label_A, label_D, label_E, line_AD, line_AE, line_AD_marker, circle_A)
        self.wait()
        self.custom_play(line_AE_marker)
        self.wait()
        # self.play(Write(proof_lines[1]))
        self.play_proof_line(proof_lines[1])
        self.wait()
        self.undo_emphasize()

        self.wait()

        self.emphasize(A, E, label_A, label_C, label_E, line_AE, line_C, line_AE_marker, line_C_marker)
        self.wait()
        # self.play(Write(proof_lines[2]))
        self.play_proof_line(proof_lines[2])
        self.wait()
        self.undo_emphasize()

        self.wait()