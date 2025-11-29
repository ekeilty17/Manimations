import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *
import footnote_text as ft

class Book1Prop8(GreekConstructionScenes):

    title = "Book 1 Proposition 8"
    description = """
        If two triangles have two sides equal to two 
        sides, respectively, and also have the base equal 
        to the base, then they will also have equal the 
        angles encompassed by the equal straight-lines

        (i.e. SSS congruency)
    """

    def write_givens(self):
        # ^ABC
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, LEFT)
        C, label_C = self.get_dot_and_label("C", self.Cx.get_value() * RIGHT + self.Cy.get_value() * UP, RIGHT)

        line_AB = Line(A.get_center(), B.get_center())
        line_BC = Line(B.get_center(), C.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        line_AB_marker = get_line_marker(line_AB, "/")
        line_BC_marker = get_line_marker(line_BC, "///")
        line_CA_marker = get_line_marker(line_CA, "//", flip_vertically=True)

        # ^DEF
        D, label_D = self.get_dot_and_label("D", A.get_center() + self.triangle_DEF_offset_x.get_value() * RIGHT + self.triangle_DEF_offset_y.get_value() * UP, UP)
        E, label_E = self.get_dot_and_label("E", B.get_center() + self.triangle_DEF_offset_x.get_value() * RIGHT + self.triangle_DEF_offset_y.get_value() * UP, LEFT)
        F, label_F = self.get_dot_and_label("F", C.get_center() + self.triangle_DEF_offset_x.get_value() * RIGHT + self.triangle_DEF_offset_y.get_value() * UP, RIGHT)

        line_DE = Line(D.get_center(), E.get_center())
        line_EF = Line(E.get_center(), F.get_center())
        line_FD = Line(F.get_center(), D.get_center())

        line_DE_marker = get_line_marker(line_DE, "/")
        line_EF_marker = get_line_marker(line_EF, "///")
        line_FD_marker = get_line_marker(line_FD, "//", flip_vertically=True)

        givens = (
            line_AB_marker, line_BC_marker, line_CA_marker, line_DE_marker,line_EF_marker, line_FD_marker
        )
        intermediaries = (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F, 
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            line_AB_marker, line_BC_marker, line_CA_marker, line_DE_marker,line_EF_marker, line_FD_marker,
        ) = givens
        (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F, 
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD,
        ) = given_intermediaries

        # Superposition Triangle
        A_D, label_A_D = self.get_dot_and_label("D'", A.get_center() + self.superposition_shift_x.get_value() * RIGHT + self.superposition_shift_y.get_value() * UP, UP)
        _, label_A_D_2 = self.get_dot_and_label("A', D'", A_D.get_center(), UP)
        B_E, label_B_E = self.get_dot_and_label("B', E'", B.get_center() + self.superposition_shift_x.get_value() * RIGHT + self.superposition_shift_y.get_value() * UP, LEFT)
        C_F, label_C_F = self.get_dot_and_label("C', F'", C.get_center() + self.superposition_shift_x.get_value() * RIGHT + self.superposition_shift_y.get_value() * UP, RIGHT)

        line_AB_DE = Line(A_D.get_center(), B_E.get_center())
        line_BC_EF = Line(B_E.get_center(), C_F.get_center())
        line_CA_FD = Line(C_F.get_center(), A_D.get_center())

        line_AB_DE_marker = get_line_marker(line_AB_DE, "/")
        line_BC_EF_marker = get_line_marker(line_BC_EF, "///")
        line_CA_FD_marker = get_line_marker(line_CA_FD, "//", flip_vertically=True)

        # Point G and associated lines
        G, label_G = self.get_dot_and_label("G", self.Gx.get_value() * RIGHT + self.Gy.get_value() * UP, UR, color=self.color_map[self.IMPOSSIBLE])
        _, label_A_G = self.get_dot_and_label("A', G", G.get_center(), UR, color=self.color_map[self.IMPOSSIBLE])
        line_GE = Line(G.get_center(), B_E.get_center(), color=self.color_map[self.IMPOSSIBLE])
        line_FG = Line(C_F.get_center(), G.get_center(), color=self.color_map[self.IMPOSSIBLE])

        line_GE_marker = get_line_marker(line_GE, "/")
        line_FG_marker = get_line_marker(line_FG, "//", flip_vertically=True)

        # angle markers
        ABC_angle_marker = get_angle_marker(line_AB, line_BC, "((")
        BCA_angle_marker = get_angle_marker(line_BC, line_CA, "(")
        CAB_angle_marker = get_angle_marker(line_CA, line_AB, "(((")

        DEF_angle_marker = get_angle_marker(line_DE, line_EF, "((")
        EFD_angle_marker = get_angle_marker(line_EF, line_FD, "(")
        FDE_angle_marker = get_angle_marker(line_FD, line_DE, "(((")

        intermediaries = (
            A_D, B_E, C_F, G, 
            label_A_D, label_A_D_2, label_A_G, label_B_E, label_C_F, label_G,
            line_AB_DE, line_BC_EF, line_CA_FD, line_DE, line_EF, line_FD, line_FG, line_GE,
            line_AB_DE_marker, line_BC_EF_marker, line_CA_FD_marker, line_FG_marker, line_GE_marker, 
        )
        solution = (
            ABC_angle_marker, BCA_angle_marker, CAB_angle_marker, DEF_angle_marker, EFD_angle_marker, FDE_angle_marker,
        )
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            ("|AB ~= |DE", "[Given]", self.GIVEN),
            ("|AC ~= |DF", "[Given]", self.GIVEN),
            ("|BC ~= |EF", "[Given]", self.GIVEN),
            ("{B} c= {E}", "[Superposition]"),
            ("|BC c= |EF", "[3. + 4. + Superposition]"),
            ("{C} c= {F}", "[5. + Def. 3]"),
            ("{A} c= {D}", "[Prop. 1.7]"),
            ("|AB c= |DE", "[Prop. 1.7]"),
            ("|AC c= |DF", "[Prop. 1.7]"),
            ("^ABC ~= ^DEF", "[CN. 4]", self.SOLUTION),
            ("<A ~= <D", "[CN. 4]", self.SOLUTION),
            ("<B ~= <E", "[CN. 4]", self.SOLUTION),
            ("<C ~= <F", "[CN. 4]", self.SOLUTION)
        ]
    def write_footnotes(self):
        return [
            r"""
            \text{Using superposition, we ``apply" } ^ABC \text{ to } ^DEF
            """,
            r"""
            \text{Let point } {B} \text{ coincide with point } {E}
            """,
            r"""
            \text{Since } |BC ~= |EF \text{,}
            \text{let line } |BC \text{ coincide with line } |EF
            """,
            r"""
            \text{Therefore, point } {C} \text{ coincides with point } {F}
            """,
            r"""
            \text{Suppose that } {A} \text{ does not coincide with } {D}
            \text{but instead coincides with some other point } {G}
            """,
            r"""
            \text{But we showed in Prop. 1.7 that}
            \text{this construction is impossible}
            """,
            r"""
            \text{So in fact } {A} \text{ must coincide with } {D}
            """,
            r"""
            \text{Furthermore by Prop. 1.7, } 
            |AB c= |DE \text{ and } |AC c= |DF
            """,
            r"""
            \text{Thus all points and lines in } ^ABC 
            \text{ coincide with their counterparts in } ^DEF
            \text{so these triangles must be congruent}
            """,
            r"""
            \text{Thus, all corresponding internal angles must}
            \text{coincide and therefore must be congruent}
            """
        ]
    def write_tex_to_color_map(self):
        return {
            "{G}": self.IMPOSSIBLE,
        }

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 3.25*UP + 2*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.75*UP + 2.5*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.5*UP + 0.75*LEFT)
        self.triangle_DEF_offset_x, self.triangle_DEF_offset_y, _ = get_value_tracker_of_point(3.5*RIGHT)
        self.superposition_shift_x, self.superposition_shift_y, _ = get_value_tracker_of_point(3.25*DOWN + 1.75*RIGHT)
        self.Gx, self.Gy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.2*DOWN + 0.4*RIGHT)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes(shift=DOWN * MED_SMALL_BUFF)
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.8, shift=0.1*LEFT)

        """ Construction Variables """
        (
            line_AB_marker, line_BC_marker, line_CA_marker, line_DE_marker,line_EF_marker, line_FD_marker,
        ) = self.givens
        (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F, 
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD,
        ) = self.given_intermediaries
        (
            A_D, B_E, C_F, G, 
            label_A_D, label_A_D_2, label_A_G, label_B_E, label_C_F, label_G,
            line_AB_DE, line_BC_EF, line_CA_FD, line_DE, line_EF, line_FD, line_FG, line_GE, 
            line_AB_DE_marker, line_BC_EF_marker, line_CA_FD_marker, line_FG_marker, line_GE_marker,
        )= self.solution_intermediaries
        (
            ABC_angle_marker, BCA_angle_marker, CAB_angle_marker, DEF_angle_marker, EFD_angle_marker, FDE_angle_marker,
        ) = self.solution

        """ Animate Introduction """
        center_shift = self.get_center_shift(*self.givens, *self.given_intermediaries, *self.solution)
        givens_copy = VGroup(*self.givens, *self.given_intermediaries).copy().shift(center_shift)
        solution_copy = VGroup(*self.solution).copy().shift(center_shift)

        self.add(givens_copy)
        self.wait()
        self.custom_play(*Animate(title, description, *solution_copy))
        self.wait(3)
        self.custom_play(*Unanimate(title, description, *solution_copy))
        self.wait()
        self.custom_play(givens_copy.animate.shift(-center_shift))
        self.add(*self.givens, *self.given_intermediaries)
        self.remove(givens_copy)
        self.wait(2)

        """ Superposition Explanation """
        superposition_explanation = self.MathTex(*superposition_explanation_text())
        superposition_explanation.move_to(self.LEFT_CENTER)
        triangle_ABC = VGroup([
            A, B, C,
            label_A, label_B, label_C,
            line_AB, line_BC, line_CA
        ])
        triangle_DEF = VGroup([
            D, E, F,
            label_D, label_E, label_F,
            line_DE, line_EF, line_FD
        ])
        superposition_triangle = VGroup([
            A_D, B_E, C_F,
            label_A_D_2, label_B_E, label_C_F,
            line_AB_DE, line_BC_EF, line_CA_FD
        ])
        self.custom_play(
            *self.ReplacementTransformN2M((triangle_ABC, triangle_DEF), superposition_triangle, copy_source=True),
            *Animate(superposition_explanation), 
        run_time=1.5)
        self.ReplacementTransformN2M_cleanup()
        self.wait(4)
        self.custom_play(
            FadeOut(superposition_triangle),
            *Unanimate(superposition_explanation), 
        run_time=1.5)
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        self.animate_proof_line(
            *proof_lines[0:3],
            source_mobjects=[
                A, B, C, D, E, F,
                label_A, label_B, label_C, label_D, label_E, label_F,
                line_AB, line_BC, line_CA, line_DE, line_EF, line_FD,
                line_AB_marker, line_BC_marker, line_CA_marker, line_DE_marker, line_EF_marker, line_FD_marker,
            ]
        )
        self.wait()
        
        """ Animation Construction """
        self.custom_play(footnote_animations[0])
        self.wait(2)

        # B c= E
        self.custom_play(
            *self.ReplacementTransformN2M((B, E), B_E, copy_source=True),
            *self.ReplacementTransformN2M((label_B, label_E), label_B_E, copy_source=True),
            footnote_animations[1]
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.animate_proof_line(
            proof_lines[3],
            source_mobjects=[
                B, E, B_E,
                label_B, label_E, label_B_E,
            ]
        )

        self.wait(2)

        # |BC c= |EF
        self.custom_play(
            *self.ReplacementTransformN2M((line_BC, line_EF), line_BC_EF, copy_source=True),
            *self.ReplacementTransformN2M((line_BC_marker, line_EF_marker), line_BC_EF_marker, copy_source=True),
            footnote_animations[2]
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.animate_proof_line(
            *proof_lines[4],
            source_mobjects=[
                line_BC, line_EF, line_BC_EF,
                line_BC_marker, line_EF_marker, line_BC_EF_marker,
            ]
        )

        # C c= F
        self.custom_play(
            *self.ReplacementTransformN2M((C, F), C_F, copy_source=True),
            *self.ReplacementTransformN2M((label_C, label_F), label_C_F, copy_source=True),
            footnote_animations[3]
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.animate_proof_line(
            proof_lines[5],
            source_mobjects=[
                C, F, C_F,
                label_C, label_F, label_C_F,
            ]
        )

        self.wait(2)

        # Suppose A !c= D but instead A c= G
        self.custom_play(
            *self.ReplacementTransformN2M(D, A_D, copy_source=True),
            *self.ReplacementTransformN2M(label_D, label_A_D, copy_source=True),
            *self.ReplacementTransformN2M(A, G, copy_source=True),
            *self.ReplacementTransformN2M(label_A, label_A_G, copy_source=True),
            footnote_animations[4],
        )
        self.wait()
        self.custom_play(
            *self.ReplacementTransformN2M(line_DE, line_AB_DE, copy_source=True),
            *self.ReplacementTransformN2M(line_FD, line_CA_FD, copy_source=True),
            *self.ReplacementTransformN2M(line_DE_marker, line_AB_DE_marker, copy_source=True),
            *self.ReplacementTransformN2M(line_FD_marker, line_CA_FD_marker, copy_source=True),
            
            *self.ReplacementTransformN2M(line_AB, line_GE, copy_source=True),
            *self.ReplacementTransformN2M(line_CA, line_FG, copy_source=True),
            *self.ReplacementTransformN2M(line_AB_marker, line_GE_marker, copy_source=True),
            *self.ReplacementTransformN2M(line_CA_marker, line_FG_marker, copy_source=True),
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)

        self.custom_play(footnote_animations[5])
        self.wait(2)

        # So actually A c= D
        self.custom_play(
            *self.ReplacementTransformN2M(label_A_D, label_A_D_2),
            footnote_animations[6]
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.animate_proof_line(
            proof_lines[6],
            source_mobjects=[
                A, A_D, D, G, 
                label_A, label_A_D_2, label_A_G,  label_D,
                line_GE, line_FG, 
                line_GE_marker, line_FG_marker
            ]
        )
        self.wait(2)

        # Rest of proof
        self.custom_play(footnote_animations[7])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[7:9],
            source_mobjects=[
                A, B, C, D, E, F,
                label_A, label_B, label_C, label_D, label_E, label_F,
                line_AB, line_BC, line_DE, line_EF
            ]
        )
        self.wait(2)

        # ^ABC ~= ^DEF
        self.custom_play(footnote_animations[8])
        self.wait(2)
        self.animate_proof_line(
            proof_lines[9],
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD, 
        )
        self.wait(2)

        # All the interior angles are congruent
        self.custom_play(
            *Animate(
                ABC_angle_marker, BCA_angle_marker, CAB_angle_marker,
                DEF_angle_marker, EFD_angle_marker, FDE_angle_marker
            ),
            footnote_animations[9]
        )
        self.wait(2)
        self.animate_proof_line(
            proof_lines[10:13],
            source_mobjects=[
                ABC_angle_marker, BCA_angle_marker, CAB_angle_marker,
                DEF_angle_marker, EFD_angle_marker, FDE_angle_marker
            ]
        )
        self.wait(2)

        self.custom_play(footnote_animations[-1])
        self.wait(2)

        self.write_QED()
        self.wait()
