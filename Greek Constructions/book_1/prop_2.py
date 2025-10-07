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
            (("^ABD", r"\text{ is equilateral}"),   "[Prop. 1.1]"),
            ("|AB ~= |BD ~= |AD",                   "[Def. 20]"),
            ("|BC ~= |BG",                          "[Def. 15]"),
            ("|DL ~= |DG",                          "[Def. 15]"),
            ("|AL ~= |BG",                          "[CN. 3]"),
            ("|AL ~= |BC",                          "[CN. 1]",      self.SOLUTION),
        ]
    def get_footnotes(self):
        return [
            r"""
            \text{By Post. 1, line } |AB \text{ can be}
            \text{drawn between points } {A} \text{ and } {B}
            """,
            r"""
            \text{By Prop. 1.1, construct equilateral}
            \text{triangle } ^ABD \text{ with base } |AB
            """,
            r"""
            \text{By Post. 3, construct } ()BC
            \text{with center } {B} \text{ and radius } |BC
            """,
            r"""
            \text{By Post. 1, extend line } |DB \text{ until it}
            \text{intersects } ()BC \text{ at } {G}
            """,
            r"""
            \text{Line } |BC \text{ and line } |BG \text{ are both radii of}
            ()BC \text{, thus by Def. 15 they are congruent}
            """,
            r"""
            \text{By Post. 3, construct } ()DG
            \text{with center } {D} \text{ and radius } |DG
            """,
            r"""
            \text{By Post. 1, extend line } |DA \text{ until it}
            \text{intersects } ()DG \text{ at } {L}
            """,
            r"""
            \text{Both line } |DG \text{ and line } |DL \text{ are radii of } 
            ()DG \text{, thus by Def. 15 they are congruent}
            """,
            r"""
            |DA + |AL = |DL ~= |DG = |DB + |BG \ \text{ and } |DA ~= |DB
            \text{Therefore, } |AL ~= |BG \text{ by CN. 3 (Subtraction)}
            """,
            r"""
            \text{By CN. 1 (Transitivity Property of Congruence), }
            |BG ~= |BC \text{ and } |AL ~= |BG \ => \ |AL ~= |BC
            """,
        ]
    def get_tex_to_color_map(self):
        return {
            "{A}": self.given_color,
            "{B}": self.given_color,
            "{C}": self.given_color,
            "{L}": self.solution_color,
            "|BC": self.given_color,
            "|AL": self.solution_color,
        }

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(3.8*RIGHT + 0.3*DOWN)
        self.Bx, self.By, _ = get_value_tracker_of_point(4.5*RIGHT + 0.5*UP)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(4.5*RIGHT + 2.5*UP)

        """ Variable Initialization """
        title, description = self.initialize_introduction()
        footnotes, first_footnote_animation, next_footnote_animations, last_footnote_animation = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()

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

        """ Animate Introduction """
        self.wait()

        tmp = [mob.copy() for mob in [line_AL_marker, line_BC_marker]]
        line_AL_copy = line_AL.copy()
        L_copy = L.copy()
        self.custom_play(
            *Animate(title, description),
            ReplacementTransform(line_BC.copy(), line_AL_copy), ReplacementTransform(C.copy(), L_copy)
        )
        self.custom_play(*Animate(*tmp))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, *tmp, line_AL_copy, L_copy))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()

        """ Animation Construction """
        # Equilateral triangle ABD
        self.custom_play(
            Animate(line_AB),
            first_footnote_animation
        )
        self.wait(2)
        self.custom_play(*Animate(D, label_D))
        self.custom_play(
            *Animate(line_BD, line_DA, line_AB_marker, line_BD_marker, line_DA_marker),
            next_footnote_animations[0]
        )
        self.wait(2)
        self.animate_proof_line(
            *proof_lines[0:2],
            source_mobjects=[
                A, B, D, 
                label_A, label_B, label_D,
                line_AB, line_BD, line_DA, 
                line_AB_marker, line_BD_marker, line_DA_marker
            ]
        )

        self.wait(2)

        # Draw ()BC
        self.custom_play(
            Animate(circle_B),
            next_footnote_animations[1]
        )
        self.wait(3)

        # Extend |DB to point G
        self.custom_play(
            Animate(line_BG),
            next_footnote_animations[2]
        )
        self.custom_play(*Animate(G, label_G))
        self.wait(2)
        self.custom_play(
            *Animate(line_BC_marker, line_BG_marker),
            next_footnote_animations[3]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[2],
            source_mobjects=[
                B, C, G, 
                label_B, label_C, label_G,
                line_BC, line_BG, 
                circle_B
            ]
        )

        self.wait(2)

        # Draw ()DG
        self.emphasize(
            D, G, 
            label_D, label_G, 
            line_BD, line_BG,
        play=True)
        self.wait()
        self.custom_play(
            Animate(circle_D),
            next_footnote_animations[4]
        )

        self.wait(2)
        
        # Extend |DA to point L
        self.emphasize(
            A, B, D, G, 
            label_A, label_B, label_D, label_G, 
            line_BD, line_BG, line_DA, 
            circle_D, 
            line_BD_marker, line_BG_marker, line_DA_marker,
        play=True)
        self.wait()
        self.custom_play(
            Animate(line_AL),
            next_footnote_animations[5]
        )
        self.custom_play(*Animate(L, label_L))
       
        self.wait(2)
        
        # self.emphasize(
        #     A, B, D, G, L,
        #     label_A, label_B, label_D, label_G, label_L,
        #     line_DA, line_AL, line_BD, line_BG, 
        #     line_DA_marker, line_BD_marker, line_BG_marker, 
        #     circle_D,
        # play=True)
        # self.wait()
        self.custom_play(next_footnote_animations[6])
        self.wait(3)
        self.custom_play(
            Animate(line_AL_marker),
            next_footnote_animations[7]
        )
        self.wait(2)
        self.animate_proof_line(*proof_lines[3:5])

        self.wait(2)

        # Therefore, |AL ~= BC
        emphasize_animations = self.emphasize(
            A, B, C, G, L,
            label_A, label_B, label_C, label_G, label_L,
            line_AL, line_BC, line_BG,
            line_AL_marker, line_BC_marker, line_BG_marker,
        )
        self.custom_play(
            *emphasize_animations,
            next_footnote_animations[8]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[5],
            source_mobjects=[
                A, B, C, L,
                label_A, label_B, label_C, label_L,
                line_AL, line_BC,
                line_AL_marker, line_BC_marker,
            ]
        )
        self.wait(2)
        clear_emphasize_animations = self.clear_emphasize()
        self.custom_play(
            *clear_emphasize_animations,
            last_footnote_animation
        )

        self.wait(2)

        self.write_QED()
        self.wait()

        # self.remove(*givens, *given_intermediaries, *solution_intermediaries, *solution)
        # givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=True)
        # self.add(*givens, *given_intermediaries, *solution_intermediaries, *solution)
        # self.play(
        #     self.Ax.animate.set_value(6)
        # )

        # self.wait()