import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop31(GreekConstructionScenes):

    title = "Book 1 Proposition 31"
    description = """
        To draw a straight-line parallel to a 
        given straight-line, through a given point.
    """

    def write_givens(self):
        
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, LEFT, buff=SMALL_BUFF)
        C, label_C = self.get_dot_and_label("C", B.get_center() + self.parallel_line_length.get_value() * RIGHT, RIGHT, buff=SMALL_BUFF)
        
        line_BC = Line(B.get_center(), C.get_center())
        _, D, _ = interpolate_line(line_BC, self.D_percentage.get_value())
        D, label_D = self.get_dot_and_label("D", D.get_center(), DOWN)

        line_DA = Line(D.get_center(), A.get_center())

        y_shift = (A.get_center() - D.get_center())[1]
        line_EF = line_BC.copy().shift(y_shift*UP)

        E, label_E = self.get_dot_and_label("E", line_EF.get_start(), LEFT, buff=SMALL_BUFF)
        F, label_F = self.get_dot_and_label("F", line_EF.get_end(), RIGHT, buff=SMALL_BUFF)

        angle_ADC = get_angle_marker(line_DA.copy().rotate(PI), line_BC, marker_type="(")
        angle_DAE = get_angle_marker(line_DA, line_EF.copy().rotate(PI), marker_type="(")

        line_BC_marker = get_line_marker(line_BC, marker_type=">", position=0.7)
        line_EF_marker = get_line_marker(line_EF, marker_type=">", position=0.7)

        givens = (
            A,
            label_A, label_B, label_C,
            line_BC,
        )
        intermediaries = (
            D,
            label_D, label_E, label_F,
            line_DA, line_EF,
            angle_ADC, angle_DAE,
            line_BC_marker, line_EF_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"<ADC ~= <DAE", "[Prop. 1.23]"),
            (r"|BC || |EF", "[Prop. 1.27]", self.SOLUTION)
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*UP + 0.5*RIGHT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1*DOWN + 3*LEFT)
        
        self.parallel_line_length = ValueTracker(6)
        self.D_percentage = ValueTracker(0.3)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()

        """ Construction Variables """
        # () = self.givens
        # () = self.given_intermediaries
        # () = self.solution_intermediaries
        # () = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        self.custom_play(*Animate(title, description))
        self.wait(3)
        self.custom_play(*Unanimate(title, description))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        self.add(*self.solution_intermediaries, *self.solution)
        self.add(proof_lines)
        self.wait()