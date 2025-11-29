import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop38(GreekConstructionScenes):

    title = "Book 1 Proposition 38"
    description = """
       Triangles which are on equal bases 
       and between the same parallels are 
       equal to one another.
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        F, label_F = self.get_dot_and_label("F", self.Fx.get_value() * RIGHT + self.Fy.get_value() * UP, DR)
        
        line_BF = Line(B.get_center(), F.get_center())

        line_AD, _ = extend_line_by_length(line_BF, self.line_AD_length.get_value(), switch_direction=True)
        line_AD.shift(A.get_center() - B.get_center())
        D, label_D = self.get_dot_and_label("D", line_AD.get_end(), UP)

        line_BC, line_FE = extend_line_by_length(line_BF, self.base_length.get_value(), switch_direction=True)
        line_EF = line_FE.copy().rotate(PI)

        C, label_C = self.get_dot_and_label("C", line_BC.get_end(), DL)
        line_AB, line_BC, line_CA = get_triangle_edges(A, B, C)

        E, label_E = self.get_dot_and_label("E", line_EF.get_start(), DR)
        line_DE, line_EF, line_FD = get_triangle_edges(D, E, F)
        
        line_CE = Line(C.get_center(), E.get_center())

        line_BG = line_CA.copy().shift(B.get_center() - C.get_center())
        G, label_G = self.get_dot_and_label("G", line_BG.get_end(), UP)
        line_AG = Line(A.get_center(), G.get_center())

        line_HF = line_DE.copy().shift(F.get_center() - E.get_center())
        H, label_H = self.get_dot_and_label("H", line_HF.get_start(), UP)
        line_DH = Line(D.get_center(), H.get_center())

        # line_AD_marker = get_line_marker(line_AD, marker_type=">")
        # line_BC_marker = get_line_marker(line_BC, marker_type=">")
        # line_AE_marker = get_line_marker(line_AE, marker_type="<")
        # line_DF_marker = get_line_marker(line_DF, marker_type=">")
        # line_BE_marker = get_line_marker(line_BE, marker_type=">>")
        # line_CA_marker = get_line_marker(line_CA, marker_type=">>")
        # line_FC_marker = get_line_marker(line_FC, marker_type="<<<")
        # line_DB_marker = get_line_marker(line_DB, marker_type="<<<")


        givens = (
            A, B, C, D, E, F, 
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_AD, line_BC, line_CA, line_CE, line_DE, line_EF, line_FD,
        )
        intermediaries = (
            G, H,
            label_G, label_H,
            line_AG, line_BG, line_DH, line_HF, 
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AD || |BF", "[Given]", self.GIVEN),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + UP + 0.75*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2.75*LEFT)
        self.Fx, self.Fy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2.75*RIGHT)

        self.base_length = ValueTracker(1.25)
        self.line_AD_length = ValueTracker(1)

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