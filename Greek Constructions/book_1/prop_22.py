import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop22(GreekConstructionScenes):

    title = "Book 1 Proposition 22"
    description = """
        To construct a triangle from three straight-lines 
        which are equal to three given [straight-lines]. 

        It is necessary for (the sum of) two (of the 
        straight-lines) taken together in any (possible 
        way) to be greater than the remaining (one)
    """

    def write_givens(self):
        A_start = ORIGIN + LARGE_BUFF * RIGHT
        line_A = Line(A_start, A_start + self.A_length.get_value() * RIGHT).to_edge(UP)

        B_start = line_A.get_start() + MED_LARGE_BUFF * DOWN
        line_B = Line(B_start, B_start + self.B_length.get_value() * RIGHT)

        C_start = line_B.get_start() + MED_LARGE_BUFF * DOWN
        line_C = Line(C_start, C_start + self.C_length.get_value() * RIGHT)

        _, A_label = self.get_dot_and_label("A", line_A.get_start(), LEFT)
        _, B_label = self.get_dot_and_label("B", line_B.get_start(), LEFT)
        _, C_label = self.get_dot_and_label("C", line_C.get_start(), LEFT)

        givens = (
            A_label, B_label, C_label,
            line_A, line_B, line_C,
        )
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            A_label, B_label, C_label,
            line_A, line_B, line_C,
        ) = givens
        
        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, LEFT)
        
        x_right_edge = config.frame_width / 2
        line_DE = Line(D.get_center(), D.get_center() + x_right_edge*RIGHT)
        _, label_E = self.get_dot_and_label("E", line_DE.get_end(), DOWN)
        label_E.shift((x_right_edge - 0.5 - label_E.get_center()[0]) * RIGHT)

        line_DF, _ = extend_line_by_length(line_DE, line_A.get_length(), switch_direction=True)
        _, line_FG = extend_line_by_length(line_DF, line_B.get_length())
        _, line_GH = extend_line_by_length(line_FG, line_C.get_length())

        F, label_F = self.get_dot_and_label("F", line_DF.get_end(), DOWN)
        G, label_G = self.get_dot_and_label("G", line_FG.get_end(), DOWN)
        H, label_H = self.get_dot_and_label("H", line_GH.get_end(), DR)

        circle_F = OrientedCircle(F.get_center(), D.get_center())
        circle_G = OrientedCircle(G.get_center(), H.get_center())

        K_coord, L_coord = get_circle_circle_intersection(circle_F, circle_G)
        if K_coord[1] < L_coord[1]:
            K_coord, L_coord = L_coord, K_coord
        
        K, label_K = self.get_dot_and_label("K", K_coord, UR)
        line_FG, line_GK, line_KF = get_triangle_edges(F, G, K)
        
        line_A_marker = get_line_marker(line_A, marker_type="/")
        line_B_marker = get_line_marker(line_B, marker_type="//")
        line_C_marker = get_line_marker(line_C, marker_type="///")

        line_DF_marker = get_line_marker(line_DF, marker_type="/")
        line_GH_marker = get_line_marker(line_GH, marker_type="///")

        line_FG_marker = get_line_marker(line_FG, marker_type="//")
        line_GK_marker = get_line_marker(line_GK, marker_type="///")
        line_KF_marker = get_line_marker(line_KF, marker_type="/")

        intermediaries = (
            D, F, G, H, K,
            label_D, label_E, label_F, label_F, label_G, label_H, label_K,
            line_DE, 
            circle_F, circle_G,
            line_A_marker, line_B_marker, line_C_marker, line_DF_marker, line_FG_marker, line_GH_marker, line_GK_marker, line_KF_marker
        )
        solution = (
            line_FG, line_GK, line_KF
        )
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|A ~= |DF", "[Prop. 1.3]"),
            (r"|B ~= |FG", "[Prop. 1.3]", self.SOLUTION),
            (r"|C ~= |GH", "[Prop. 1.3]"),
            (r"|DF ~= |FK", "[Def. 15]"),
            (r"|A ~= |FK", "[CN. 1]", self.SOLUTION),
            (r"|GH ~= |GK", "[Def. 15]"),
            (r"|C ~= |GK", "[CN. 1]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {
            "|A": self.GIVEN,
            "|B": self.GIVEN,
            "|C": self.GIVEN,
        }

    def construct(self):
        
        """ Value Trackers """
        self.A_length = ValueTracker(2.25)
        self.B_length = ValueTracker(1.85)
        self.C_length = ValueTracker(1.25)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(ORIGIN + 0*DOWN + 0.8*LARGE_BUFF*RIGHT)

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