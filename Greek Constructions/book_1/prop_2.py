import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop2(GreekConstructionScenes):

    title = "Book 1 Proposition 2"
    description = """
        To place a straight-line equal to a given
        straight-line at a given point as an extremity
        (not necessarily in the same direction)
    """

    def get_givens(self):
        
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, UP)
        
        line_BC = Line(B.get_center(), C.get_center())

        givens = (A, B, C, label_A, label_B, label_C, line_BC)
        intermediaries = ()
        return givens, intermediaries

    def get_solution(self, *givens):
        A, B, C, label_A, label_B, label_C, line_BC = givens
        
        # Base of equilateral triangle
        line_AB = Line(A.get_center(), B.get_center())

        # Compute the apex of the equilateral triangle
        D, _ = get_equilateral_triangle_apex(line_AB)
        _, label_D = self.get_dot_and_label("D", D.get_center(), LEFT)

        # Draw equilateral triangle DAB
        line_BD = Line(B.get_center(), D.get_center())
        line_DA = Line(D.get_center(), A.get_center())

        line_AB_marker = get_line_marker(line_AB, marker_type="|", rotate=PI)
        line_BD_marker = get_line_marker(line_BD, marker_type="|", rotate=PI)
        line_DA_marker = get_line_marker(line_DA, marker_type="|", rotate=PI)

        # Copy line_BC and reorient in direction of line_BD
        circle_B = OrientedCircle(center=B.get_center(), start=C.get_center())

        line_BG, _ = extend_line_by_length(line_BD, line_BC.get_length())
        G, label_G = self.get_dot_and_label("G", line_BG.get_end(), RIGHT)

        line_BC_marker = get_line_marker(line_BC, marker_type="//", flip_horizontally=True)
        line_BG_marker = get_line_marker(line_BG, marker_type="//", rotate=PI)

        # Extend line_DA to circle_D
        circle_D = OrientedCircle(center=D.get_center(), start=G.get_center())

        _, line_AL = extend_line_by_length(line_DA, line_BG.get_length())
        line_AL.set_color(self.solution_color)
        
        L, label_L = self.get_dot_and_label("L", line_AL.get_end(), DR)
        line_AL = Line(A.get_center(), L.get_center())

        line_AL_marker = get_line_marker(line_AL, marker_type="//", rotate=PI)
        
        intermediaries = (
            D, G, 
            label_D, label_G,
            line_AB, line_BD, line_BG, line_DA, 
            line_AB_marker, line_AL_marker, line_BC_marker, line_BD_marker, line_BG_marker, line_DA_marker,
            circle_B, circle_D,
        )
        solution = (L, label_L, line_AL)

        return intermediaries, solution

    def get_proof_spec(self):
        return [    
            (r"\triangle ABD \text{ is equilateral}",   "[Prop. 1.1]"),
            ("|AB ~ |BD ~ |AD",                         "[Def. 20]"),
            ("|BC ~ |BG",                               "[Def. 15]"),
            ("|DL ~ |DG",                               "[Def. 15]"),
            ("|AL ~ |BG",                               "[Subtraction]"),
            ("|AL ~ |BC",                               "[Transitivity]",   self.SOLUTION),
        ]
    def get_proof_color_map(self):
        return {
            "|BC": self.given_color,
            "|AL": self.solution_color,
        }

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(4*RIGHT + 1*DOWN)
        self.Bx, self.By, _ = get_value_tracker_of_point(4.5*RIGHT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(4.5*RIGHT + 2*UP)

        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        A, B, C, label_A, label_B, label_C, line_BC = givens
        (
            D, G, 
            label_D, label_G,
            line_AB, line_BD, line_BG, line_DA, 
            line_AB_marker, line_AL_marker, line_BC_marker, line_BD_marker, line_BG_marker, line_DA_marker,
            circle_B, circle_D,
        ) = solution_intermediaries
        L, label_L, line_AL = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        
        line_BC_tmp = line_BC.copy()
        line_AL_tmp = line_AL.copy()
        C_tmp = C.copy()
        L_tmp = L.copy()
        tmp = [mob.copy() for mob in [line_BC_marker, line_AL_marker]]
        self.play(
            Transform(line_BC_tmp, line_AL_tmp), Transform(C_tmp, L_tmp),
            Animate(title, description, *tmp),
            run_time=self.default_run_time
        )
        self.wait(2)
        self.custom_unplay(title, description, line_BC_tmp, line_AL_tmp, L_tmp, C_tmp, *tmp)
        self.wait()
        

        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof()
        self.play(Write(proof_line_numbers))
        self.wait()


        """ Animation """
        # Equilateral triangle
        self.custom_play(line_AB)
        self.custom_play(D, label_D, line_BD, line_DA)
        self.custom_play(line_AB_marker, line_BD_marker, line_DA_marker)
        self.wait()
        self.emphasize(
            A, B, D, 
            label_A, label_B, label_D,
            line_AB, line_BD, line_DA, 
            line_AB_marker, line_BD_marker, line_DA_marker
        )
        self.wait()
        # self.play(Write(proof_lines[0]))
        # self.play(Write(proof_lines[1]))
        self.play_proof_line(*proof_lines[0:2])
        self.wait()
        self.undo_emphasize()

        self.wait()

        # Copy line_BC and reorient in direction of line_BD
        self.custom_play(circle_B)
        self.custom_play(line_BG)
        self.custom_play(G, label_G)
        self.wait()
        self.emphasize(
            B, C, G, 
            label_B, label_C, label_G,
            line_BC, line_BG, 
            circle_B
        )
        self.wait()
        self.custom_play(line_BC_marker, line_BG_marker)
        self.wait()
        # self.play(Write(proof_lines[2]))
        self.play_proof_line(proof_lines[2])
        self.wait()
        self.undo_emphasize()

        self.wait()

        # Extend line_DA to circle_D
        self.custom_play(circle_D)
        self.custom_play(line_AL)
        self.custom_play(L, label_L)
        self.wait()
        self.emphasize(
            A, B, D, G, L,
            label_A, label_B, label_D, label_G, label_L,
            line_DA, line_AL, line_BD, line_BG, 
            line_DA_marker, line_BD_marker, line_BG_marker, 
            circle_D
        )
        self.wait()
        self.custom_play(line_AL_marker)
        self.wait()
        # self.play(Write(proof_lines[3]))
        # self.play(Write(proof_lines[4]))
        self.play_proof_line(*proof_lines[3:5])
        self.wait()
        self.undo_emphasize()

        self.wait()

        self.emphasize(
            A, B, C, L,
            label_A, label_B, label_C, label_L,
            line_AL, line_BC, 
            line_AL_marker, line_BC_marker
        )
        self.wait()
        # self.play(Write(proof_lines[5]))
        self.play_proof_line(proof_lines[5])
        self.wait()
        self.undo_emphasize()

        self.wait()

        self.write_QED()
        self.wait()

        # self.remove(*givens, *given_intermediaries, *solution_intermediaries, *solution)
        # givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=True)
        # self.add(*givens, *given_intermediaries, *solution_intermediaries, *solution)
        # self.play(
        #     self.Ax.animate.set_value(6)
        # )

        # self.wait()