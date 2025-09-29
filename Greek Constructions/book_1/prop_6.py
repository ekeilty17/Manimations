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

    def get_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)

        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        angle_B_marker = get_angle_marker(line_AB.copy().rotate(PI), line_BC, "(")
        angle_C_marker = get_angle_marker(line_BC.copy().rotate(PI), line_CA, "(")

        givens = (
            angle_B_marker, angle_C_marker
        )
        intermediaries = (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        )
        return givens, intermediaries

    def get_solution(self, *givens):
        (
            angle_B_marker, angle_C_marker,
            
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA,            
        ) = givens

        D, label_D = self.get_dot_and_label("D", interpolate_between_dots(A, B, 0.35), UL)
        line_CD = Line(C.get_center(), D.get_center())
        
        line_AB_marker = get_line_marker(line_AB, "/")
        line_CA_marker = get_line_marker(line_CA, "/", flip_vertically=True)

        line_BD = Line(B.get_center(), D.get_center())
        line_BD_marker = get_line_marker(line_BD, "//")
        
        line_AB_marker_contradiction = get_line_marker(line_AB, "/").set_color(self.contradiction_color)
        line_CA_marker_contradiction = get_line_marker(line_CA, "//", flip_vertically=True).set_color(self.contradiction_color)
        
        line_BC_marker = get_line_marker(line_BC, "///")

        intermediaries = (
            D, 
            label_D, 
            line_CD,
            line_AB_marker, line_BC_marker, line_BD_marker,
            line_AB_marker_contradiction, line_CA_marker_contradiction,
        )
        solution = (line_AB_marker, line_CA_marker)
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ("<ABC ~ <ACB",     "[Given]",              self.GIVEN),
            ("|AB !~ |AC",      "[Assumption]",         self.ASSUMPTION),
            ("|AC ~ |BD",       "[Prop. 1.3]"),
            ("|BC ~ |CB",       "[Reflexivity]"),
            ("^ABC ~ ^DBA",     "[Prop. 1.4 (SAS)]",      self.CONTRADICTION),
            ("^ABC !~ ^DBA",    "[Construction]",       self.CONTRADICTION),
            ("|AB ~ |AC",       "[By Contradiction]",   self.SOLUTION),
        ]
    def get_proof_color_map(self):
        return {
            "<ABC": self.given_color,
            "<ACB": self.given_color,
        }

    def construct(self):
        
        """ Value Trackers """
        A_pos = self.RIGHT_CENTER + 2*UP
        self.Ax = ValueTracker(A_pos[0])
        self.Ay = ValueTracker(A_pos[1])

        B_pos = self.RIGHT_CENTER + 2*DOWN + 1.5*LEFT
        self.Bx = ValueTracker(B_pos[0])
        self.By = ValueTracker(B_pos[1])

        C_pos = self.RIGHT_CENTER + 2*DOWN + 1.5*RIGHT
        self.Cx = ValueTracker(C_pos[0])
        self.Cy = ValueTracker(C_pos[1])

        """ Initialize Construction """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        angle_B_marker, angle_C_marker = givens
        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        ) = given_intermediaries
        (
            D, 
            label_D, 
            line_CD,
            line_AB_marker, line_BC_marker, line_BD_marker,
            line_AB_marker_contradiction, line_CA_marker_contradiction
        ) = solution_intermediaries
        line_AB_marker, line_CA_marker = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        
        # self.play(Animate(title))
        # self.play(Animate(description))
        # self.wait()
        # tmp1 = [mob.copy() for mob in [A, B, C]]
        # tmp2 = [mob.copy() for mob in [D, E, F]]
        # self.play(Animate(*tmp1))
        # self.play(Animate(*tmp2))
        # self.wait()
        # self.play(Unanimate(title, description, *tmp1, *tmp2))
        # self.wait()
        
        """ Preamble """
        contradiction_explanation_text_1 = MathTex(r"""
            \begin{aligned}
                &\textbf{Proof by Contradiction} \text{ is a proof method} \\
                &\text{where we assume the negation of a statement,} \\
                &\text{and show that it leads to a contradiction. Thus} \\
                &\text{the assumption must be false, i.e. the target} \\
                &\text{statement must be true.}
            \end{aligned}
        """).scale(0.6).move_to(self.LEFT_CENTER).shift(1.5*UP).set_z_index(self.proof_z_index)

        contradiction_explanation_text_2 = MathTex(r"""
            \begin{aligned}
                &\text{In this context, the } \textit{contradiction} \text{ will be showing} \\
                &\text{that the diagram is impossible.}
            \end{aligned}
        """).scale(0.6).next_to(contradiction_explanation_text_1, 3*DOWN).set_z_index(self.proof_z_index)

        _ = VGroup(contradiction_explanation_text_1, contradiction_explanation_text_2).move_to(self.LEFT_CENTER)
        self.custom_play(contradiction_explanation_text_1)
        self.custom_play(contradiction_explanation_text_2)

        self.play(Unanimate(contradiction_explanation_text_1), Unanimate(contradiction_explanation_text_2))
        self.wait()

        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof()
        self.play(Write(proof_line_numbers))
        self.wait()
        
        self.play(Write(proof_lines))

        """ Start of animation """
        self.custom_play(line_AB_marker_contradiction, line_CA_marker_contradiction)
        self.wait()
        
        self.play(Uncreate(line_AB_marker_contradiction))
        self.custom_play(D, label_D, line_CD)
        self.wait()

        self.custom_play(line_BD_marker)
        self.wait()

        self.custom_play(line_BC_marker)
        self.wait()