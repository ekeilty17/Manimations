import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop6(GreekConstructionScenes):

    title = "Book 1 Proposition 6"
    description = """
        If a triangle has two angles equal to one 
        another then the sides subtending the equal 
        angles will also be equal to one another
    """

    def write_givens(self):
        label_A_text = "A, D" if self.D_position.get_value() == 0 else "A"
        A, label_A = self.get_dot_and_label(label_A_text, self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)

        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        angle_B_marker = get_angle_marker(line_AB, line_BC, "(")
        angle_C_marker = get_angle_marker(line_BC, line_CA, "(")

        givens = (
            angle_B_marker, angle_C_marker
        )
        intermediaries = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            angle_B_marker, angle_C_marker,
        ) = givens
        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA,            
        ) = given_intermediaries

        if self.D_position.get_value() == 0:
            D, label_D = self.get_dot_and_label("", A.get_center(), UL)
        else:
            D, label_D = self.get_dot_and_label("D", interpolate_between_dots(A, B, self.D_position.get_value()), UL)
        line_CD = Line(C.get_center(), D.get_center())
        
        line_AB_marker = get_line_marker(line_AB, "/")
        line_CA_marker = get_line_marker(line_CA, "/", flip_vertically=True, rotate=PI)

        line_BD = Line(B.get_center(), D.get_center()).set_color(self.color_map[self.IMPOSSIBLE])
        line_BD_marker = get_line_marker(line_BD, "//")
        
        line_AD = Line(A.get_center(), D.get_center())#.set_color(self.color_map[self.IMPOSSIBLE])

        line_AB_marker_contradiction = get_line_marker(line_AB, "/")
        line_CA_marker_contradiction = get_line_marker(line_CA, "//", flip_vertically=True, rotate=PI)
        
        line_BC_marker = get_line_marker(line_BC, "///")

        intermediaries = (
            D, 
            label_D, 
            line_AD, line_BD, line_CD,
            line_AB_marker, line_BC_marker, line_BD_marker,
            line_AB_marker_contradiction, line_CA_marker_contradiction,
        )
        solution = (line_AB_marker, line_CA_marker)
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("<ABC ~= <ACB",     "[Given]",             self.GIVEN),
            ("|AB !~= |AC",      "[Assumption]",        self.ASSUMPTION),
            ("|AC ~= |BD",       "[Prop. 1.3]",         self.PBC_INTERMEDIARY),
            ("|BC ~= |CB",       "[Reflexivity]",       self.PBC_INTERMEDIARY),
            ("^ABC ~= ^DBA",     "[Prop. 1.4 (SAS)]",   self.CONTRADICTION),
            ("^ABC !~= ^DBA",    "[Construction]",      self.CONTRADICTION),
            ("|AB ~= |AC",       "[By Contradiction]",  self.SOLUTION),
        ]
    
    def write_footnotes(self):
        return [
            r"""
            \text{Assume towards a contradiction that } |AB !~= |AC
            """,
            r"""
            \text{Suppose } |AB > |AC,
            \text{then using Prop 1.3 we can copy } |AC \text{ onto } |AB
            """,
            r"""
            \text{Note, this is now an impossible diagram,}
            \text{which is evident visually. Now we just}
            \text{have to prove it.}
            """,
            r"""
            \text{By Post. 1, line } |CD \text{ can be}
            \text{drawn between points } {C} \text{ and } {D}
            """,
            r"""
            \text{Line } |BC \text{ is congruent to itself (Reflexivity)}
            """,
            r"""
            |AC ~= |BD , <ABC ~= <ACB , |BC ~= |CB
            \text{therefore by SAS (Prop. 1.4), } ^ABC ~= ^DBA
            """,
            r"""
            \text{But clearly } ^DBA \text{ is contained inside }^ABC
            \text{so they cannot be congruent}
            """,
            r"""
            \text{Thus, we have arrived at a contradiction}
            \text{and it must be the case that } |AB ~= |AC
            """,
        ]

    def write_tex_to_color_map(self):
        return {
            "<ABC": self.GIVEN,
            "<ACB": self.GIVEN,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*DOWN + 1.5*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*DOWN + 1.5*RIGHT)
        self.D_position = ValueTracker(0.35)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.9)

        """ Construction Variables """
        angle_B_marker, angle_C_marker = self.givens
        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        ) = self.given_intermediaries
        (
            D, 
            label_D, 
            line_AD, line_BD, line_CD,
            line_AB_marker, line_BC_marker, line_BD_marker,
            line_AB_marker_contradiction, line_CA_marker_contradiction
        ) = self.solution_intermediaries
        line_AB_marker, line_CA_marker = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()
        tmp = [mob.copy() for mob in self.solution]
        self.custom_play(*Animate(title, description, *tmp))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, *tmp))
        self.wait()

        """ Contradiction Explanation """
        contradiction_explanation = self.MathTex(
            r"""
            \textbf{Proof by Contradiction} \text{ is a proof method}
            \text{where we assume the negation of a statement,}
            \text{and show that it leads to a contradiction. Thus}
            \text{the assumption must be false, and the target}
            \text{statement must be true.}
            """,
            r"""
            \text{We already saw a mini-version of this reasoning}
            \text{in the proof of Prop 1.4, when we showed}
            \text{two points uniquely define a line.}
            """,
            r"""
            \text{In this proof, the } \textit{contradiction} \text{ will be showing}
            \text{that the assumption leads to an impossible}
            \text{diagram.}
            """,
        )
        contradiction_explanation.move_to(self.LEFT_CENTER)
        self.custom_play(*Animate(contradiction_explanation))
        self.wait(3)
        self.custom_play(*Unanimate(contradiction_explanation))
        self.wait()

        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        # Givens
        self.animate_proof_line(
            proof_lines[0],
            source_mobjects=[angle_B_marker, angle_C_marker]
        )
        self.wait(2)

        # Assume |AB !~= |AC
        self.custom_play(
            *Animate(line_AB_marker_contradiction, line_CA_marker_contradiction),
            footnote_animations[0]
        )
        self.wait(2)

        # Copy |AC onto |AB
        self.animate_proof_line(
            proof_lines[1],
            source_mobjects=[line_AB_marker_contradiction, line_CA_marker_contradiction]
        )
        self.wait()
        self.custom_play(
            Unanimate(line_AB_marker_contradiction),
            footnote_animations[1]
        )
        self.wait(2)
        self.custom_play(
            ReplacementTransform(line_CA.copy(), line_BD),
            ReplacementTransform(A.copy(), D),
            ReplacementTransform(label_A.copy(), label_D),
            FadeIn(line_AD)
        )
        self.custom_play(Animate(line_BD_marker))
        self.wait(2)
        self.animate_proof_line(
            proof_lines[2],
            source_mobjects=[line_CA, line_BD, line_CA_marker, line_BD_marker]
        )
        self.wait(2)
        self.custom_play(footnote_animations[2])
        self.wait(2.5)

        # Draw |CD
        self.custom_play(
            Animate(line_CD),
            footnote_animations[3]
        )
        self.wait(2)

        # |BC is congruent to itself
        self.custom_play(
            Animate(line_BC_marker),
             footnote_animations[4]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[3],
            source_mobjects=[line_BC, line_BC_marker]
        )
        self.wait(2)

        self.custom_play(footnote_animations[5])
        self.wait(2)
        self.animate_proof_line(proof_lines[4])
        self.wait(2)
        self.custom_play(footnote_animations[6])
        self.wait(2)
        self.animate_proof_line(proof_lines[5])
        self.wait(2)
        self.custom_play(footnote_animations[7])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[6],
            source_mobjects=[proof_lines[1], proof_lines[4], proof_lines[5]]
        )
        self.wait(2)
        self.custom_play(footnote_animations[-1])
        self.wait()

        self.write_QED()
        self.wait()

        # original_D_position = self.D_position.get_value()
        # self.custom_play(self.D_position.animate.set_value(0))
        # self.wait()
        # self.custom_play(self.D_position.animate.set_value(original_D_position))
        # self.wait()