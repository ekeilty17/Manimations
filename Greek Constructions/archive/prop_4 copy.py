import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Book1Prop4(GreekConstructionScenes):

    title = "Book 1 Proposition 4"
    description = """
        If two triangles have two sides equal to two
        sides, respectively, and have the angle(s)
        enclosed by the equal straight-lines equal,
        then they will also have the base equal to 
        the base, and the triangle will be equal to 
        the triangle, and the remaining angles 
        subtended by the equal sides will be equal 
        to the corresponding remaining angles
        
        (i.e. SAS congruency)
    """

    def get_givens(self):
        
        # A, label_A = self.get_dot_and_label("A", 3*UP+1.25*RIGHT, UP)
        # B, label_B = self.get_dot_and_label("B", A.get_center() + 2*DOWN + 0.75*LEFT, DL)
        # C, label_C = self.get_dot_and_label("C", A.get_center() + 2*DOWN + 1.75*RIGHT, DR)
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, DR)

        triangle_DEF_shift = self.triangle_DEF_shift_x.get_value() * RIGHT + self.triangle_DEF_shift_y.get_value() * UP
        D, label_D = self.get_dot_and_label("D", A.get_center() + triangle_DEF_shift, UP)
        E, label_E = self.get_dot_and_label("E", B.get_center() + triangle_DEF_shift, DL)
        F, label_F = self.get_dot_and_label("F", C.get_center() + triangle_DEF_shift, DR)

        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())
        line_DE = Line(D.get_center(), E.get_center())
        line_EF = Line(E.get_center(), F.get_center())
        line_FD = Line(F.get_center(), D.get_center())
        
        line_AB_marker = get_line_marker(line_AB, marker_type="/")
        line_CA_marker = get_line_marker(line_CA, marker_type="//")
        line_DE_marker = get_line_marker(line_DE, marker_type="/")
        line_FD_marker = get_line_marker(line_FD, marker_type="//")

        angle_A_marker = get_angle_marker(line_AB, line_CA.copy().rotate(PI), ")")
        angle_D_marker = get_angle_marker(line_DE, line_FD.copy().rotate(PI), ")")

        # givens = (
        #     A, B, C, D, E, F,
        #     label_A, label_B, label_C, label_D, label_E, label_F,
        #     line_AB, line_CA, line_DE, line_FD,
        # )
        # intermediaries = (
        #     line_BC, line_EF,
        #     line_AB_marker, line_CA_marker, line_DE_marker, line_FD_marker,
        #     angle_A_marker, angle_D_marker
        # )
        # return givens, intermediaries
        givens = (
            line_AB_marker, line_CA_marker, line_DE_marker, line_FD_marker,
            angle_A_marker, angle_D_marker,
        )
        intermediaries = (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_CA, line_DE, line_FD,
            line_BC, line_EF,
        )
        return givens, intermediaries

    def get_solution(self, *givens):

        # (
        #     A, B, C, D, E, F,
        #     label_A, label_B, label_C, label_D, label_E, label_F,
        #     line_AB, line_CA, line_DE, line_FD,

        #     line_BC, line_EF,
        #     line_AB_marker, line_CA_marker, line_DE_marker, line_FD_marker,
        #     angle_A_marker, angle_D_marker
        # ) = givens
        (
            line_AB_marker, line_CA_marker, line_DE_marker, line_FD_marker,
            angle_A_marker, angle_D_marker,
            
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_CA, line_DE, line_FD,
            line_BC, line_EF,
        ) = givens

        line_BC_marker = get_line_marker(line_BC, marker_type="///")
        line_EF_marker = get_line_marker(line_EF, marker_type="///")
        angle_B_marker = get_angle_marker(line_BC, line_AB.copy().rotate(PI), "))")
        angle_C_marker = get_angle_marker(line_BC.copy().rotate(PI), line_CA, "(((")
        angle_E_marker = get_angle_marker(line_EF, line_DE.copy().rotate(PI), "))")
        angle_F_marker = get_angle_marker(line_EF.copy().rotate(PI), line_FD, "(((")

        superposition_shift = self.superposition_shift_x.get_value() * RIGHT + self.superposition_shift_y.get_value() * UP
        
        A_D, label_A_D = self.get_dot_and_label("A', D", A.get_center() + superposition_shift, UP)
        B_E, label_B_E = self.get_dot_and_label("B', E", B.get_center() + superposition_shift, DL)
        C_F, label_C_F = self.get_dot_and_label("C', F", C.get_center() + superposition_shift, DR)
        
        line_AB_DE = Line(A_D.get_center(), B_E.get_center())
        line_BC_EF = Line(B_E.get_center(), C_F.get_center())
        line_CA_FD = Line(C_F.get_center(), A_D.get_center())
        
        line_AB_DE_marker = get_line_marker(line_AB_DE, marker_type="/")
        line_BC_EF_marker = get_line_marker(line_BC_EF, marker_type="///")
        line_CA_FD_marker = get_line_marker(line_CA_FD, marker_type="//")

        angle_A_D_marker = get_angle_marker(line_AB_DE, line_CA_FD.copy().rotate(PI), ")")
        angle_B_E_marker = get_angle_marker(line_BC_EF, line_AB_DE.copy().rotate(PI), "))")
        angle_C_F_marker = get_angle_marker(line_BC_EF.copy().rotate(PI), line_CA_FD, "(((")

        intermediaries = (
            A_D, B_E, C_F,
            label_A_D, label_B_E, label_C_F,
            line_AB_DE, line_BC_EF, line_CA_FD, 
            line_AB_DE_marker, line_BC_EF_marker, line_CA_FD_marker, 
            angle_A_D_marker, angle_B_E_marker, angle_C_F_marker
        )
        solution = (
            line_BC_marker, line_BC_EF_marker, line_CA_FD_marker, line_EF_marker,
            angle_B_marker, angle_B_E_marker, angle_C_marker, angle_C_F_marker, angle_E_marker, angle_F_marker,
        )
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ((r"\overline{AB}", r"\cong", r"\overline{DE}"),            "[Given]",                  self.GIVEN),
            ((r"\overline{AC}", r"\cong", r"\overline{DF}"),            "[Given]",                  self.GIVEN),
            ((r"\angle BAC", r"\cong", r"\angle EDF"),                  "[Given]",                  self.GIVEN),
            
            ((r"\overline{A'B'}", r"\equiv", r"\overline{DE}", r", \ ", r"\overline{AB}", r"\cong", r"\overline{A'B'}"),    "[1. + Prop. 3]"),
            ((r"A'", r"\equiv", r"D", r",", r"B'", r"\equiv", r"E"),    "[4. + Def. 3]"),
            
            ((r"\overline{A'C'}", r"\equiv", r"\overline{DF}", r", \ ", r"\overline{AC}", r"\cong", r"\overline{A'C'}"),    "[2. + Prop. 3]"),
            ((r"C'", r"\equiv", r"F"),                                   "[6. + Def. 3]"),
            
            ((r"\angle B'A'C'", r"\equiv", r"\angle EDF"),              "[4. + 6. + Def. 8]"),
            ((r"\angle BAC", r"\cong", r"\angle B'A'C'"),               "[3. + 8. + Transitivity]"),

            ((r"\overline{B'C'}", r"\equiv", r"\overline{EF}"),         "[6. + 8. + Post. 1]"),
            ((r"\overline{BC}", r"\cong", r"\overline{EF}"),            "[Superposition]",          self.SOLUTION),

            ((r"\angle A'B'C'", r"\equiv", r"\angle DEF"),              "[Def. 20]"),
            ((r"\angle ABC", r"\cong", r"\angle DEF"),                  "[Superposition]",          self.SOLUTION),

            ((r"\angle A'C'B'", r"\equiv", r"\angle DFE"),              "[Def. 20]"),
            ((r"\angle ACB", r"\cong", r"\angle DFE"),                  "[Superposition]",          self.SOLUTION),

            ((r"\triangle ABC", r"\cong", r"\triangle DEF"),            "[Def. 20]",                self.SOLUTION),
        ]
    def get_proof_color_map(self):
        return {
            # r"\overline{AB}": self.given_color,
            # r"\overline{AC}": self.given_color,
            # r"\overline{DE}": self.given_color,
            # r"\overline{DF}": self.given_color,
            # r"\angle BAC": self.given_color,
            # r"\angle EDF": self.given_color,
            # r"\overline{BC}": self.solution_color,
            # r"\overline{EF}": self.solution_color,
            # r"\angle ABC": self.solution_color,
            # r"\angle DEF": self.solution_color,
            # r"\angle ACB": self.solution_color,
            # r"\angle DFE": self.solution_color,
        }

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.5*LEFT + 2.75*UP)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.75*UP + 1*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.75*UP + 2*RIGHT)
        self.triangle_DEF_shift_x,  self.triangle_DEF_shift_y, _= get_value_tracker_of_point(3.75*DOWN)
        self.superposition_shift_x, self.superposition_shift_y, _ = get_value_tracker_of_point(3.75*DOWN)

        """ Preparation """
        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)
        
        (
            line_AB_marker, line_CA_marker, line_DE_marker, line_FD_marker,
            angle_A_marker, angle_D_marker,
        ) = givens
        (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_CA, line_DE, line_FD,
            line_BC, line_EF,
        ) = given_intermediaries
        (
            A_D, B_E, C_F,
            label_A_D, label_B_E, label_C_F,
            line_AB_DE, line_BC_EF, line_CA_FD, 
            line_AB_DE_marker, line_BC_EF_marker, line_CA_FD_marker, 
            angle_A_D_marker, angle_B_E_marker, angle_C_F_marker
        ) = solution_intermediaries
        (
            line_BC_marker, line_BC_EF_marker, line_CA_FD_marker, line_EF_marker,
            angle_B_marker, angle_B_E_marker, angle_C_marker, angle_C_F_marker, angle_E_marker, angle_F_marker,
        ) = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        
        self.custom_play(title, description)
        self.wait()

        tmp = [mob.copy() for mob in [line_BC_marker, line_EF_marker, angle_B_marker, angle_E_marker, angle_C_marker, angle_F_marker]]
        self.custom_play(*tmp)
        self.wait()
        self.play(Unanimate(title, description, *tmp))
        self.wait()

        """ Preamble """
        superposition_explanation_text_1 = MathTex(r"""
            \begin{aligned}
                &\textbf{Superposition} \text{ is a method where two figures} \\
                &\text{are imagined to be placed on top of each other}
            \end{aligned}
        """).scale(0.6).move_to(self.LEFT_CENTER).shift(UP).set_z_index(self.proof_z_index)

        superposition_explanation_text_2 = MathTex(r"""
            \begin{aligned}
                &\text{Since } \overline{AB} \cong \overline{DE} \text{ and } \overline{AC} \cong \overline{DF}\\
                &\text{the procedure in Prop. 3 justifies this method,}\\
                &\text{i.e. } \overline{AB} \text{ can be placed on } \overline{DE} \text{ via construction}
            \end{aligned}
        """).scale(0.6).next_to(superposition_explanation_text_1, 3*DOWN).set_z_index(self.proof_z_index)

        _ = VGroup(superposition_explanation_text_1, superposition_explanation_text_2).move_to(self.LEFT_CENTER)
        self.custom_play(superposition_explanation_text_1)
        self.custom_play(superposition_explanation_text_2)

        self.play(Unanimate(superposition_explanation_text_1), Unanimate(superposition_explanation_text_2))
        self.wait()

        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.8)
        self.play(Write(proof_line_numbers))
        self.play(Write(proof_lines[0]), Write(proof_lines[1]), Write(proof_lines[2]))
        self.wait()

        """ Animation """

        self.play(
            ReplacementTransform(A.copy(), A_D), Transform(D, A_D),
            ReplacementTransform(label_A.copy(), label_A_D), Transform(label_D, label_A_D),
            ReplacementTransform(B.copy(), B_E), Transform(E, B_E),
            ReplacementTransform(label_B.copy(), label_B_E), Transform(label_E, label_B_E),
            ReplacementTransform(line_AB.copy(), line_AB_DE), Transform(line_DE, line_AB_DE),
            # ReplacementTransform(line_AB_marker.copy(), line_AB_DE_marker), Transform(line_DE_marker, line_AB_DE_marker),
        )
        self.remove(D, E, label_D, label_E, line_DE, line_AB_DE_marker)
        self.wait()
        self.emphasize(
            A, B, A_D, B_E,
            label_A, label_B, label_A_D, label_B_E,
            line_AB, line_AB_DE,
            line_AB_marker, line_DE_marker, line_AB_DE_marker,
        )
        self.wait()
        self.play(Write(proof_lines[3]))
        self.play(Write(proof_lines[4]))
        self.wait()
        self.undo_emphasize()

        self.wait()
        
        self.play(
            ReplacementTransform(line_CA.copy(), line_CA_FD), Transform(line_FD, line_CA_FD),
            ReplacementTransform(C.copy(), C_F), Transform(F.copy(), C_F),
            ReplacementTransform(label_C.copy(), label_C_F), Transform(label_F.copy(), label_C_F)
            # ReplacementTransform(line_CA_marker.copy(), line_CA_FD_marker), Transform(line_FD_marker, line_CA_FD_marker),
        )
        self.remove(F, label_F, line_FD, line_CA_FD_marker)
        self.wait()
        self.emphasize(
            A, C, A_D, C_F,
            label_A, label_C, label_A_D, label_C_F,
            line_CA, line_CA_FD,
            line_CA_marker, line_FD_marker, line_CA_FD_marker,
        )
        self.wait()
        self.play(Write(proof_lines[5]))
        self.play(Write(proof_lines[6]))
        self.wait()
        self.undo_emphasize()

        self.wait()
        
        self.emphasize(
            A, B, C, A_D, B_E, C_F,
            label_A, label_B, label_C, label_A_D, label_B_E, label_C_F,
            line_AB, line_CA, line_AB_DE, line_CA_FD,
            line_AB_marker, line_DE_marker, line_CA_marker, line_FD_marker, line_AB_DE_marker, line_CA_FD_marker,
        )
        self.wait()
        self.play(Write(proof_lines[7]))
        self.play(Write(proof_lines[8]))
        self.wait()
        self.undo_emphasize()

        self.wait()
        
        self.emphasize(
            B, C, B_E, C_F,
            label_B, label_C, label_B_E, label_C_F,
            line_BC, line_EF, line_BC_EF
        )
        self.wait()
        self.remove(line_EF)
        self.add(line_BC_EF)
        self.custom_play(line_BC_marker, line_EF_marker, line_BC_EF_marker)
        self.play(Write(proof_lines[9]))
        self.play(Write(proof_lines[10]))
        self.wait()
        self.undo_emphasize()
        
        self.emphasize(
            A, B, C, A_D, B_E, C_F,
            label_A, label_B, label_C, label_A_D, label_B_E, label_C_F,
            line_AB, line_BC, line_DE, line_EF, line_AB_DE, line_BC_EF
        )
        self.wait()
        self.custom_play(angle_B_marker, angle_E_marker, angle_B_E_marker)
        self.wait()
        self.play(Write(proof_lines[11]))
        self.play(Write(proof_lines[12]))
        self.wait()
        self.undo_emphasize()
        
        self.emphasize(
            A, B, C, A_D, B_E, C_F,
            label_A, label_B, label_C, label_A_D, label_B_E, label_C_F,
            line_BC, line_CA, line_DE, line_EF, line_BC_EF, line_CA_FD, 
        )
        self.wait()
        self.custom_play(angle_C_marker, angle_F_marker, angle_C_F_marker)
        self.wait()
        self.play(Write(proof_lines[13]))
        self.play(Write(proof_lines[14]))
        self.wait()
        self.undo_emphasize()

        self.wait()

        self.play(Write(proof_lines[15]))
        self.wait()