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

    def write_givens(self):
        
        center = self.center_x.get_value() * RIGHT + self.center_y.get_value() * UP
        A, label_A = self.get_dot_and_label("A", center + LEFT * self.triangle_side_length.get_value()/2, DL)
        B, label_B = self.get_dot_and_label("B", center + RIGHT * self.triangle_side_length.get_value()/2, DR)
        line_AB = Line(A.get_center(), B.get_center())

        givens = (A, label_A, B, label_B, line_AB)
        intermediaries = ()
        return givens, intermediaries

    def write_solution(self, *givens):
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

    def write_proof_spec(self):
        return [    
            ("|AB ~= |BC",                          "[Def. 15]"),
            ("|AB ~= |AC",                          "[Def. 15]"),
            ("|AC ~= |BC",                          "[CN. 1]"),
            (("^ABC", r"\text{ is equilateral}"),   "[Def. 20]",        self.SOLUTION)
        ]
    
    def write_footnotes(self):
        return [
            r"""
            \text{By Post. 3, } ()A \text{ can be}
            \text{drawn given center } {A} \text{ and radius } |AB
            """,
            r"""
            \text{Likewise by Post. 3, } ()B \text{ can be}
            \text{drawn given center } {B} \text{ and radius } |BA
            """,
            r"""
            \text{Euclid does not explicity state that the}
            \text{intersection of two circles results in a}
            \text{point, this is assumed as self-evident}
            """,
            r"""
            \text{By Post. 1, line } |BC \text{ can be}
            \text{drawn between points } {B} \text{ and } {C}
            """,
            r"""
            \text{Likewise by Post. 1, line } |AC \text{ can be}
            \text{drawn between points } {A} \text{ and } {C}
            """,
            r"""
            \text{Line } |AB \text{ and line } |BC \text{ are both radii}
            \text{of } ()B \text{, thus by Def. 15 they are congruent}
            """,
            r"""
            \text{Likewise, line } |AB \text{ and line } |AC \text{ are both radii}
            \text{of } ()A \text{, thus by Def. 15 they are congruent}
            """,
            r"""
            \text{By CN. 1 (Transitivity Property of Congruence), }
            |AC ~= |AB \text{ and } |AB ~= |BC \ => \ |AC ~= |BC
            """,
            r"""
            \text{Thus all sides of } ^ABC \text{ are congruent,}
            \text{by Def. 20 it is an equilateral triangle}
            """
        ]
    
    def write_tex_to_color_map(self):
        return {
            "{A}": self.GIVEN,
            "{B}": self.GIVEN,
            "{C}": self.SOLUTION,
            # "()A": self.GIVEN,
            # "()B": self.GIVEN,
            "|AB": self.GIVEN,
            "|BA": self.GIVEN,
            "|AC": self.SOLUTION,
            "|BC": self.SOLUTION,
            "^ABC": self.SOLUTION,
        }

    def construct(self):
        
        """ Value Trackers """
        self.center_x, self.center_y, _ = get_value_tracker_of_point(self.RIGHT_CENTER)
        self.triangle_side_length = ValueTracker(2)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, first_footnote_animation, next_footnote_animations, last_footnote_animation = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()
        
        """ Construction Variables """
        A, label_A, B, label_B, line_AB = self.givens
        line_AB_marker, line_BC_marker, line_CA_marker, circle_A, circle_B = self.solution_intermediaries
        C, label_C, line_BC, line_CA = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        tmp = [mob.copy() for mob in [C, label_C, line_BC, line_CA, line_AB_marker, line_BC_marker, line_CA_marker]]
        self.custom_play(*Animate(title, description, *tmp))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, *tmp))
        self.wait()
         
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()

        """ Animate Construction """
        # Circle A and Circle B
        self.custom_play(
            Animate(circle_A), 
            first_footnote_animation
        )
        self.wait(2)
        self.custom_play(
            Animate(circle_B),
            next_footnote_animations[0],
        )
        
        self.wait(2)
        
        # Line AC and BC
        self.custom_play(
            *Animate(C, label_C),
            next_footnote_animations[1],
        )
        self.wait(3)
        self.custom_play(
            Animate(line_BC),
            next_footnote_animations[2],
        )
        self.wait(2)
        self.custom_play(
            Animate(line_CA),
            next_footnote_animations[3],
        )
        
        self.wait(2)
        
        # |AB ~= |BC
        emphasize_animations = self.emphasize(
            A, B, C, 
            label_A, label_B, label_C, 
            line_AB, line_BC,
            circle_B
        )
        self.custom_play(
            *emphasize_animations, 
            next_footnote_animations[4],
        )
        self.wait()
        self.custom_play(*Animate(line_AB_marker, line_BC_marker))
        self.wait(2)
        self.animate_proof_line(proof_lines[0])
        
        self.wait(2)

        # |AB ~= |AC
        emphasize_animations = self.emphasize(
            A, B, C, 
            label_A, label_B, label_C, 
            line_AB, line_CA, 
            line_AB_marker,
            circle_A, 
        )
        self.custom_play(
            *emphasize_animations,
            next_footnote_animations[5],
        )
        self.wait()
        self.custom_play(Animate(line_CA_marker))
        self.wait(2)
        self.animate_proof_line(proof_lines[1])
        
        self.wait(2)

        # |AC ~= |BC
        emphasize_animations = self.emphasize(
            A, B, C, 
            label_A, label_B, label_C, 
            line_BC, line_CA, 
            line_BC_marker, line_CA_marker
        )
        self.custom_play(
            *emphasize_animations,
            next_footnote_animations[6],
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[2])

        self.wait(2)

        # ^ABC is equilateral
        emphasize_animations = self.emphasize(
            A, B, C, 
            label_A, label_B, label_C, 
            line_AB, line_BC, line_CA, 
            line_AB_marker, line_BC_marker, line_CA_marker
        )
        self.custom_play(
            *emphasize_animations,
            next_footnote_animations[7],
        )
        self.wait(2)
        self.animate_proof_line(proof_lines[3])
        self.wait(2)
        clear_emphasize_animations = self.clear_emphasize()
        self.custom_play(
            *clear_emphasize_animations,
            last_footnote_animation
        )

        self.wait()

        self.write_QED()
        self.wait()