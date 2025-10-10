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
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
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

    def write_solution(self, *givens):
        (
            angle_B_marker, angle_C_marker,
            
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA,            
        ) = givens

        if self.D_position.get_value() == 0:
            D, label_D = self.get_dot_and_label("", A.get_center(), UL)
        else:
            D, label_D = self.get_dot_and_label("D", interpolate_between_dots(A, B, self.D_position.get_value()), UL)
        line_CD = Line(C.get_center(), D.get_center())
        
        line_AB_marker = get_line_marker(line_AB, "/")
        line_CA_marker = get_line_marker(line_CA, "/", flip_vertically=True)

        line_BD = Line(B.get_center(), D.get_center())
        line_BD_marker = get_line_marker(line_BD, "//")
        
        line_AB_marker_contradiction = get_line_marker(line_AB, "/").set_color(self.color_map[self.GIVEN])
        line_CA_marker_contradiction = get_line_marker(line_CA, "//", flip_vertically=True).set_color(self.color_map[self.GIVEN])
        
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

    def write_proof_spec(self):
        return [
            ("<ABC ~= <ACB",     "[Given]",              self.GIVEN),
            ("|AB !~= |AC",      "[Assumption]",         self.ASSUMPTION),
            ("|AC ~= |BD",       "[Prop. 1.3]"),
            ("|BC ~= |CB",       "[Reflexivity]"),
            ("^ABC ~= ^DBA",     "[Prop. 1.4 (SAS)]",    self.CONTRADICTION),
            ("^ABC !~= ^DBA",    "[Construction]",       self.CONTRADICTION),
            ("|AB ~= |AC",       "[By Contradiction]",   self.SOLUTION),
        ]
    def write_proof_color_map(self):
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
        proof_line_numbers, proof_lines = self.initialize_proof()

        """ Construction Variables """
        angle_B_marker, angle_C_marker = self.givens
        print("1", any(angle_B_marker is x for x in self.givens))
        (
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        ) = self.given_intermediaries
        (
            D, 
            label_D, 
            line_CD,
            line_AB_marker, line_BC_marker, line_BD_marker,
            line_AB_marker_contradiction, line_CA_marker_contradiction
        ) = self.solution_intermediaries
        line_AB_marker, line_CA_marker = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()
        print("2", any(angle_B_marker is x for x in self.givens))
        tmp = [mob.copy() for mob in self.solution]
        self.custom_play(*Animate(title, description, *tmp))
        print("3", any(angle_B_marker is x for x in self.givens))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, *tmp))
        print("4", any(angle_B_marker is x for x in self.givens))
        self.wait()
        print("5", any(angle_B_marker is x for x in self.givens))

        """ Contradiction Explanation """
        contradiction_explanation = self.MathTex(
            r"""
            \textbf{Proof by Contradiction} \text{ is a proof method}
            \text{where we assume the negation of a statement,}
            \text{and show that it leads to a contradiction. Thus}
            \text{the assumption must be false, i.e. the target}
            \text{statement must be true.}
            """,
            r"""
            \text{In this context, the } \textit{contradiction} \text{ will be showing}
            \text{that the diagram is impossible.}
            """
        )
        contradiction_explanation.move_to(self.LEFT_CENTER)
        self.custom_play(*Animate(contradiction_explanation))
        self.wait(3)
        self.custom_play(*Unanimate(contradiction_explanation))
        self.wait()

        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        print("4", angle_B_marker in self.givens)
        self.animate_proof_line(
            proof_lines[0],
            # source_mobjects=[A, B, C]
        )
        self.wait()

        return
        
        """ Start of animation """
        self.custom_play(*Animate(line_AB_marker_contradiction, line_CA_marker_contradiction))
        self.wait()
        
        self.custom_play(Unanimate(line_AB_marker_contradiction))
        self.custom_play(*Animate(D, label_D, line_CD))
        self.wait()

        self.custom_play(Animate(line_BD_marker))
        self.wait()

        self.custom_play(Animate(line_BC_marker))
        self.wait()

        self.animate_proof_line(proof_lines[1:])
        self.wait()

        self.custom_play(self.D_position.animate.set_value(0))
        self.wait()