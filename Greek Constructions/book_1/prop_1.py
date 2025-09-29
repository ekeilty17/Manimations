import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop1(GreekConstructionScenes):

    title = "Book 1 Proposition 1"
    description = """
        To construct an equilateral triangle 
        on a given finite straight-line
    """

    def get_givens(self):
        
        center = self.center_x.get_value() * RIGHT + self.center_y.get_value() * UP
        A, label_A = self.get_dot_and_label("A", center + LEFT * self.triangle_side_length.get_value()/2, DL)
        B, label_B = self.get_dot_and_label("B", center + RIGHT * self.triangle_side_length.get_value()/2, DR)
        line_AB = Line(A.get_center(), B.get_center())

        givens = (A, label_A, B, label_B, line_AB)
        intermediaries = ()
        return givens, intermediaries

    def get_solution(self, *givens):
        A, label_A, B, label_B, line_AB = givens

        circle_A = OrientedCircle(center=A.get_center(), start=B.get_center())
        circle_B = OrientedCircle(center=B.get_center(), start=A.get_center())

        C, _ = get_equilateral_triangle_apex(line_AB)
        _, label_C = self.get_dot_and_label("C", C.get_center(), UP)

        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        line_AB_marker = get_line_marker(line_AB, marker_type="|", rotate=PI)
        line_BC_marker = get_line_marker(line_BC, marker_type="/", flip_horizontally=True, rotate=PI)
        line_CA_marker = get_line_marker(line_CA, marker_type="/", rotate=PI)

        intermediaries = (line_AB_marker, line_BC_marker, line_CA_marker, circle_A, circle_B)
        solution = (C, label_C, line_BC, line_CA)
        return intermediaries, solution

    def get_proof_spec(self):
        return [    
            ("|AB ~ |BC",                                "[Def. 15]"),
            ("|AB ~ |AC",                                "[Def. 15]"),
            ("|BC ~ |AC",                                "[Transitivity]"),
            (r"\triangle ABC \text{ is equilateral}",   "[Def. 20]",        self.SOLUTION)
        ]
    def get_proof_color_map(self):
        return {
            "|AB": self.given_color,
            "|AC": self.solution_color,
            "|BC": self.solution_color,
        }
    # def get_footnotes(self):
    #     return [
    #         r"\textbf{Def. 15} \text{: } "
    #     ]

    def construct(self):
        
        """ Value Trackers """
        self.center_x, self.center_y, _ = get_value_tracker_of_point(self.RIGHT_CENTER)
        self.triangle_side_length = ValueTracker(2)

        """ Initialize Construction """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        A, label_A, B, label_B, line_AB = givens
        line_AB_marker, line_BC_marker, line_CA_marker, circle_A, circle_B = solution_intermediaries
        C, label_C, line_BC, line_CA = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        tmp1 = [mob.copy() for mob in [C, label_C, line_BC, line_CA]]
        tmp2 = [mob.copy() for mob in [line_AB_marker, line_BC_marker, line_CA_marker]]
        self.wait()
        self.custom_play(title, description, *tmp1, *tmp2)
        self.wait(2)
        self.custom_unplay(title, description, *tmp1, *tmp2)
        self.wait()
        
        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof()
        self.play(Write(proof_line_numbers))

        """ Animation """
        self.custom_play(circle_A)
        self.wait()
        self.custom_play(circle_B)
        self.wait()
        self.custom_play(C, label_C)
        self.wait()
        self.custom_play(line_BC)
        self.custom_play(line_CA)
        
        self.wait()
        
        self.emphasize(A, label_A, B, label_B, C, label_C, circle_B, line_AB, line_BC)
        self.wait()
        self.custom_play(line_AB_marker, line_BC_marker)
        self.wait()
        # self.play(Write(proof_lines[0]))
        self.play_proof_line(proof_lines[0])
        # print(self.mobjects_to_emphasize)
        # self.play(Transform(Group(*self.mobjects_to_emphasize).copy(), proof_lines[0]))
        self.wait(2)
        self.undo_emphasize()

        self.wait()

        self.emphasize(A, label_A, B, label_B, C, label_C, circle_A, line_AB, line_CA, line_AB_marker)
        self.wait()
        self.custom_play(line_CA_marker)
        self.wait()
        # self.play(Write(proof_lines[1]))
        self.play_proof_line(proof_lines[1])
        self.wait(2)
        self.undo_emphasize()

        self.wait()

        self.emphasize(A, label_A, B, label_B, C, label_C, line_BC, line_CA, line_BC_marker, line_CA_marker)
        self.wait()
        # self.play(Write(proof_lines[2]))
        self.play_proof_line(proof_lines[2])
        self.wait(2)
        self.undo_emphasize()

        self.wait()

        self.emphasize(A, label_A, B, label_B, C, label_C, line_AB, line_BC, line_CA, line_AB_marker, line_BC_marker, line_CA_marker)
        self.wait()
        # self.play(Write(proof_lines[3]))
        self.play_proof_line(proof_lines[3])
        self.wait(2)
        self.undo_emphasize()

        self.wait()

        self.write_QED()
        self.wait()