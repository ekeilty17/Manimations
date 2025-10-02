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

        angle_A_marker = get_angle_marker(line_AB.copy().rotate(PI), line_CA.copy().rotate(PI), ")")
        angle_D_marker = get_angle_marker(line_DE.copy().rotate(PI), line_FD.copy().rotate(PI), ")")

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
        angle_B_marker = get_angle_marker(line_BC.copy().rotate(PI), line_AB.copy().rotate(PI), "))")
        angle_C_marker = get_angle_marker(line_BC, line_CA, "(((")
        angle_E_marker = get_angle_marker(line_EF.copy().rotate(PI), line_DE.copy().rotate(PI), "))")
        angle_F_marker = get_angle_marker(line_EF, line_FD, "(((")

        superposition_shift = self.superposition_shift_x.get_value() * RIGHT + self.superposition_shift_y.get_value() * UP
        
        A_D, label_A_D = self.get_dot_and_label("A', D'", A.get_center() + superposition_shift, UP)
        B_E, label_B_E = self.get_dot_and_label("B', E'", B.get_center() + superposition_shift, DL)
        C_F, label_C_F = self.get_dot_and_label("C', F'", C.get_center() + superposition_shift, DR)
        
        line_AB_DE = Line(A_D.get_center(), B_E.get_center())
        line_BC_EF = Line(B_E.get_center(), C_F.get_center())
        line_CA_FD = Line(C_F.get_center(), A_D.get_center())
        
        line_AB_DE_marker = get_line_marker(line_AB_DE, marker_type="/")
        line_BC_EF_marker = get_line_marker(line_BC_EF, marker_type="///")
        line_CA_FD_marker = get_line_marker(line_CA_FD, marker_type="//")

        angle_A_D_marker = get_angle_marker(line_AB_DE.copy().rotate(PI), line_CA_FD.copy().rotate(PI), ")")
        angle_B_E_marker = get_angle_marker(line_BC_EF.copy().rotate(PI), line_AB_DE.copy().rotate(PI), "))")
        angle_C_F_marker = get_angle_marker(line_BC_EF, line_CA_FD, "(((")

        intermediaries = (
            A_D, B_E, C_F,
            label_A_D, label_B_E, label_C_F,
            line_AB_DE, line_BC_EF, line_CA_FD, 
            line_AB_DE_marker, line_BC_EF_marker, line_CA_FD_marker, 
            angle_A_D_marker, angle_B_E_marker, angle_C_F_marker
        )
        solution = (
            line_BC_marker, line_EF_marker,
            angle_B_marker, angle_C_marker, angle_E_marker, angle_F_marker,
        )
        return intermediaries, solution

    def get_proof_spec(self):
        return [
            ("|AB ~= |DE",       "[Given]",         self.GIVEN),
            ("|AC ~= |DF",       "[Given]",         self.GIVEN),
            ("<A ~= <D",         "[Given]",         self.GIVEN),
            
            ("A c= D",          "[Superposition]"),
            ("|AB c= |DE",      "[Superposition]"),
            ("<A c= <D",        "[Superposition]"),
            ("|AC c= |DF",      "[Superposition]"),

            ("B c= E",          "[Superposition]"),
            ("C c= F",          "[Superposition]"),

            ("|BC c= |EF",      "[Post. 1]"),

            ("^ABC ~= ^EDF",    "[CN. 4]",          self.SOLUTION),

            ("|BC ~= |EF",      "[CN. 4]",          self.SOLUTION),
            ("<B ~= <E",        "[CN. 4]",          self.SOLUTION),
            ("<C ~= <F",        "[CN. 4]",          self.SOLUTION),
        ]
    def get_proof_color_map(self):
        return {}

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2.75*UP + 2.5*LEFT )
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.75*UP + 3*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.75*UP + 0.5*LEFT)
        self.triangle_DEF_shift_x,  self.triangle_DEF_shift_y, _= get_value_tracker_of_point(3.5*RIGHT)
        self.superposition_shift_x, self.superposition_shift_y, _ = get_value_tracker_of_point(2*RIGHT + 3.75*DOWN)

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
            line_BC_marker, line_EF_marker,
            angle_B_marker, angle_C_marker, angle_E_marker, angle_F_marker,
        ) = solution

        """ Introduction """
        title, description = self.initialize_introduction(self.title, self.description)
        
        tmp = [mob.copy() for mob in [line_BC_marker, line_EF_marker, angle_B_marker, angle_E_marker, angle_C_marker, angle_F_marker]]
        self.custom_play(title, description, *tmp, run_time=1)
        self.wait(3)
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
        self.custom_play(superposition_explanation_text_1, superposition_explanation_text_2, run_time=1)
        self.wait(3)

        self.play(Unanimate(superposition_explanation_text_1), Unanimate(superposition_explanation_text_2))
        self.wait()

        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.8)
        self.play(Write(proof_line_numbers))
        self.play_proof_line(
            *proof_lines[0:3],
            source_mobjects=[
                A, B, C, D, E, F,
                label_A, label_B, label_C, label_D, label_E, label_F,
                line_AB, line_CA, line_DE, line_FD,
                line_AB_marker, line_CA_marker, line_DE_marker, line_FD_marker,
                angle_A_marker, angle_D_marker,
            ]
        )
        self.wait()

        """ Animation """
        # Set A on top of D
        self.play(
            self.ReplaceTransformN2M((A, D), A_D, copy_source=True),
            self.ReplaceTransformN2M((label_A, label_D), label_A_D, copy_source=True),
            run_time=self.default_run_time
        )
        self.ReplaceTransformN2M_cleanup()
        self.wait()
        self.play_proof_line(
            proof_lines[3],
            source_mobjects=[
                A, D, A_D,
                label_A, label_D, label_A_D,
            ]
        )

        # Givens coincide
        self.play(
            self.ReplaceTransformN2M((line_AB, line_DE), line_AB_DE, copy_source=True),
            self.ReplaceTransformN2M((line_CA, line_FD), line_CA_FD, copy_source=True),

            self.ReplaceTransformN2M((line_AB_marker, line_DE_marker), line_AB_DE_marker, copy_source=True),
            self.ReplaceTransformN2M((line_CA_marker, line_FD_marker), line_CA_FD_marker, copy_source=True),
            self.ReplaceTransformN2M((angle_A_marker, angle_D_marker), angle_A_D_marker, copy_source=True),

            run_time=self.default_run_time
        )
        self.ReplaceTransformN2M_cleanup()
        self.wait()
        self.play_proof_line(
            *proof_lines[4:7],
            source_mobjects=[
                line_AB, line_CA, line_EF, line_FD, line_AB_DE, line_CA_FD,
                line_AB_marker, line_CA_marker, line_EF_marker, line_FD_marker, line_AB_DE_marker, line_CA_FD_marker,
                angle_A_marker, angle_D_marker, angle_A_D_marker
            ]
        )
        self.wait()

        # Points B and E coincide
        self.play(
            self.ReplaceTransformN2M((B, E), B_E, copy_source=True),
            self.ReplaceTransformN2M((C, F), C_F, copy_source=True),

            self.ReplaceTransformN2M((label_B, label_E), label_B_E, copy_source=True),
            self.ReplaceTransformN2M((label_C, label_F), label_C_F, copy_source=True),

            run_time=self.default_run_time
        )
        self.ReplaceTransformN2M_cleanup()
        self.play_proof_line(
            *proof_lines[7:9],
            source_mobjects=[
                B, C, E, F, B_E, C_F,
                label_B, label_C, label_E, label_F, label_B_E, label_C_F,
            ]
        )

        # Proving that line_BC must coincide with line_EF
        self.emphasize(
            B, C, E, F, B_E, C_F,
            label_B, label_C, label_E, label_F, label_B_E, label_C_F,
            line_BC, line_EF,
        )
        line_BC_EF_arc = ArcBetweenPoints(B_E.get_center(), C_F.get_center()).set_z_index(line_BC_EF.z_index)
        shaded_region = VMobject(color=RED, fill_opacity=0.5, stroke_width=0)
        shaded_region.set_points_as_corners([
            *line_BC_EF_arc.points,
            B_E.get_center(),
            C_F.get_center(),
        ])
        shaded_region.close_path()
        self.play(
            self.ReplaceTransformN2M((B, E), B_E, copy_source=True), 
            self.ReplaceTransformN2M((C, F), C_F, copy_source=True),
            self.ReplaceTransformN2M((label_B, label_E), label_B_E, copy_source=True), 
            self.ReplaceTransformN2M((label_C, label_F), label_C_F, copy_source=True),
            self.ReplaceTransformN2M(line_BC, line_BC_EF, copy_source=True),
            self.ReplaceTransformN2M(line_BC, line_BC_EF_arc, copy_source=True),
            FadeIn(shaded_region),
            run_time=self.default_run_time
        )
        self.ReplaceTransformN2M_cleanup()
        self.wait()
        
        self.play(
            self.ReplaceTransformN2M((line_BC_EF_arc, shaded_region), line_BC_EF),
            run_time=self.default_run_time
        )
        self.ReplaceTransformN2M_cleanup()
        self.wait()
        self.play_proof_line(proof_lines[9])
        self.undo_emphasize()
        
        # Therefore Triangle ABC is congruent to Triangle DEF
        self.emphasize(
            A, B, C, D, E, F, A_D, B_E, C_F,
            label_A, label_B, label_C, label_D, label_E, label_F, label_A_D, label_B_E, label_C_F,
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD, line_AB_DE, line_BC_EF, line_CA_FD,
        )
        self.play_proof_line(proof_lines[10])
        
        self.wait()

        # And the rest of the triangle parts are congruent
        self.custom_play(
            line_BC_marker, line_EF_marker, line_BC_EF_marker,
            angle_B_marker, angle_C_marker, angle_E_marker, 
            angle_F_marker, angle_B_E_marker, angle_C_F_marker
        )
        self.play_proof_line(*proof_lines[11:14])
        self.undo_emphasize()

        self.wait()
        self.write_QED()