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

    def write_givens(self):
        
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

    def write_solution(self, *givens):

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

    def write_proof_spec(self):
        return [
            ("|AB ~= |DE",       "[Given]",         self.GIVEN),
            ("<A ~= <D",         "[Given]",         self.GIVEN),
            ("|AC ~= |DF",       "[Given]",         self.GIVEN),
            
            ("A c= D",          "[Superposition]"),
            ("|AB c= |DE",      "[1. + Superposition]"),
            ("<A c= <D",        "[2. + 4. + 5.]"),
            ("|AC c= |DF",      "[3. + 4. + 5. + 6.]"),

            ("B c= E",          "[5. + Def. 3]"),
            ("C c= F",          "[7. + Def. 3]"),

            ("|BC c= |EF",      "[Post. 1]"),

            ("^ABC ~= ^EDF",    "[CN. 4]",          self.SOLUTION),

            ("|BC ~= |EF",      "[CN. 4]",          self.SOLUTION),
            ("<B ~= <E",        "[CN. 4]",          self.SOLUTION),
            ("<C ~= <F",        "[CN. 4]",          self.SOLUTION),
        ]
   
    def write_footnotes(self):
        return [
            r"""
            \text{Using superposition, we ``apply" } ^ABC \text{ to } ^DEF
            """,
            r"""
            \text{Let point } {A} \text{ coincide with point } {D}
            """,
            r"""
            \text{Since } |AB ~= |DE \text{,}
            \text{let line } |AB \text{ coincide with line } |DE
            """,
            r"""
            \text{Since } <A ~= <D \text{ and } |AC ~= |DF \text{,} 
            \text{they must also coincide with eachother}
            \text{(the most hand-wavy part of the argument)}
            """,
            r"""
            \text{Since } |AB c= |DE
            \text{ their endpoints must coincide}
            """,
            r"""
            \text{Likewise, since } |AC c= |DF
            \text{ their endpoints must coincide}
            """,
            r"""
            \text{Thus, line } |BC \text{ must coincide with line } |EF
            """,
            r"""
            \text{If not, then we have created a two-sided}
            \text{polygon which is impossible.}
            """,
            r"""
            \text{Thus all points and lines in } ^ABC 
            \text{ coincide with their counterparts in } ^DEF
            \text{so these triangles must be congruent}
            """,
            r"""
            \text{Thus, all other lines and angles must coincide}
            \text{and therefore must be congruent}
            """
        ]
    
    def write_tex_to_color_map(self):
        return {}

    def construct(self):

        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 3.25*UP + 2.5*LEFT )
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.25*UP + 3*LEFT)
        self.Cx, self.Cy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 1.25*UP + 0.5*LEFT)
        self.triangle_DEF_shift_x,  self.triangle_DEF_shift_y, _= get_value_tracker_of_point(3.5*RIGHT)
        self.superposition_shift_x, self.superposition_shift_y, _ = get_value_tracker_of_point(2*RIGHT + 3.25*DOWN)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes(shift=DOWN * MED_SMALL_BUFF)
        proof_line_numbers, proof_lines = self.initialize_proof(scale=0.85)

        """ Construction Variables """
        (
            line_AB_marker, line_CA_marker, line_DE_marker, line_FD_marker,
            angle_A_marker, angle_D_marker,
        ) = self.givens
        (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_CA, line_DE, line_FD,
            line_BC, line_EF,
        ) = self.given_intermediaries
        (
            A_D, B_E, C_F,
            label_A_D, label_B_E, label_C_F,
            line_AB_DE, line_BC_EF, line_CA_FD, 
            line_AB_DE_marker, line_BC_EF_marker, line_CA_FD_marker, 
            angle_A_D_marker, angle_B_E_marker, angle_C_F_marker
        ) = self.solution_intermediaries
        (
            line_BC_marker, line_EF_marker,
            angle_B_marker, angle_C_marker, angle_E_marker, angle_F_marker,
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
        superposition_explanation = self.MathTex(
        r"""
        \textbf{Superposition} \text{ is a method where two figures}
        \text{are imagined to be placed on top of each other.}
        \text{This is often written as ``applying" one figure}
        \text{to another.}
        """,
        r"""
        \text{By modern standards, superposition constitutes}
        \text{a new axiom. It's essentially equivalent to}
        \text{assuming the Euclidean plane allows for rigid}
        \text{motion. Most modern treatments (such as}
        \text{Hilbert's ``Foundations of Geometry") instead}
        \text{choose to assume SAS as the axiom.}
        """,
        r"""
        \text{While the rigorous axiomatization of Euclidean
        \text{geometry is an interesting topic, the goal}
        \text{here is simply to reproduce Euclid's original}
        \text{reasoning as presented in ``Euclid's Elements}
        \text{of Geometry".}
        """)
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
            label_A_D, label_B_E, label_C_F,
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
                line_AB, line_CA, line_DE, line_FD,
                line_AB_marker, line_CA_marker, line_DE_marker, line_FD_marker,
                angle_A_marker, angle_D_marker,
            ]
        )
        self.wait()

        """ Animation Construction """
        self.custom_play(footnote_animations[0])
        self.wait(2)

        # Let A c= D
        self.custom_play(
            *self.ReplacementTransformN2M((A, D), A_D, copy_source=True),
            *self.ReplacementTransformN2M((label_A, label_D), label_A_D, copy_source=True),
            footnote_animations[1]
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.animate_proof_line(
            proof_lines[3],
            source_mobjects=[
                A, D, A_D,
                label_A, label_D, label_A_D,
            ]
        )

        self.wait(2)

        # Let |AB c= |DE
        self.custom_play(
            *self.ReplacementTransformN2M((line_AB, line_DE), line_AB_DE, copy_source=True),
            *self.ReplacementTransformN2M((line_AB_marker, line_DE_marker), line_AB_DE_marker, copy_source=True),
            footnote_animations[2],
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.custom_play(
            *self.ReplacementTransformN2M((line_CA, line_FD), line_CA_FD, copy_source=True),
            *self.ReplacementTransformN2M((line_CA_marker, line_FD_marker), line_CA_FD_marker, copy_source=True),
            *self.ReplacementTransformN2M((angle_A_marker, angle_D_marker), angle_A_D_marker, copy_source=True),
            footnote_animations[3],
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.animate_proof_line(
            *proof_lines[4:7],
            source_mobjects=[
                line_AB, line_CA, line_EF, line_FD, line_AB_DE, line_CA_FD,
                line_AB_marker, line_CA_marker, line_EF_marker, line_FD_marker, line_AB_DE_marker, line_CA_FD_marker,
                angle_A_marker, angle_D_marker, angle_A_D_marker
            ]
        )

        self.wait(2)

        # Thus, B c= E
        self.custom_play(
            *self.ReplacementTransformN2M((B, E), B_E, copy_source=True),
            *self.ReplacementTransformN2M((label_B, label_E), label_B_E, copy_source=True),
            footnote_animations[4],
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)

        # Thus, C c= D
        self.custom_play(
            *self.ReplacementTransformN2M((C, F), C_F, copy_source=True),
            *self.ReplacementTransformN2M((label_C, label_F), label_C_F, copy_source=True),
            footnote_animations[5],
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.animate_proof_line(
            *proof_lines[7:9],
            source_mobjects=[
                B, C, E, F, B_E, C_F,
                label_B, label_C, label_E, label_F, label_B_E, label_C_F,
            ]
        )
        
        self.wait(2)

        # Proving that line_BC must coincide with line_EF
        self.emphasize(
            B, C, E, F, B_E, C_F,
            label_B, label_C, label_E, label_F, label_B_E, label_C_F,
            line_BC, line_EF, 
        play=True)
        self.wait(2)

        line_BC_EF_arc = ArcBetweenPoints(B_E.get_center(), C_F.get_center()).set_z_index(line_BC_EF.z_index)
        shaded_region = VMobject(color=RED, fill_opacity=0.5, stroke_width=0)
        shaded_region.set_points_as_corners([
            *line_BC_EF_arc.points,
            B_E.get_center(),
            C_F.get_center(),
        ])
        shaded_region.close_path()
        self.custom_play(
            # *self.ReplacementTransformN2M((B, E), B_E, copy_source=True), 
            # *self.ReplacementTransformN2M((C, F), C_F, copy_source=True),
            # *self.ReplacementTransformN2M((label_B, label_E), label_B_E, copy_source=True), 
            # *self.ReplacementTransformN2M((label_C, label_F), label_C_F, copy_source=True),
            *self.ReplacementTransformN2M((line_BC, line_EF), line_BC_EF, copy_source=True),
            footnote_animations[6],
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2.5)
        
        self.custom_play(
            *self.ReplacementTransformN2M(line_BC_EF, line_BC_EF_arc, copy_source=True),
            FadeIn(shaded_region),
            footnote_animations[7],
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait(2)

        self.custom_play(
            *self.ReplacementTransformN2M((line_BC_EF_arc, shaded_region), line_BC_EF),
        )
        self.ReplacementTransformN2M_cleanup()
        self.wait()
        self.animate_proof_line(proof_lines[9])
        self.wait(2)
        self.clear_emphasize(play=True)
        self.wait()
        
        # Therefore Triangle ABC is congruent to Triangle DEF
        self.custom_play(footnote_animations[8])
        self.wait(2)
        self.animate_proof_line(proof_lines[10])
        
        self.wait(2)

        # And the rest of the triangle parts are congruent
        self.custom_play(
            *Animate(angle_B_E_marker, line_BC_EF_marker, angle_C_F_marker),
            footnote_animations[9],
        )
        self.wait(2)
        self.custom_play(
            ReplacementTransform(angle_B_E_marker.copy(), angle_B_marker),
            ReplacementTransform(angle_B_E_marker.copy(), angle_E_marker),
            ReplacementTransform(line_BC_EF_marker.copy(), line_BC_marker),
            ReplacementTransform(line_BC_EF_marker.copy(), line_EF_marker),
            ReplacementTransform(angle_C_F_marker.copy(), angle_C_marker),
            ReplacementTransform(angle_C_F_marker.copy(), angle_F_marker),
            # IDK why this doesn't work
            # *self.ReplacementTransformN2M(angle_B_E_marker, (angle_B_marker, angle_E_marker), copy_source=True),
            # *self.ReplacementTransformN2M(line_BC_EF_marker, (line_BC_marker, line_EF_marker), copy_source=True),
            # *self.ReplacementTransformN2M(angle_C_F_marker, (angle_C_marker, angle_F_marker), copy_source=True),
        )
        # self.ReplacementTransformN2M_cleanup()
        self.wait(2)
        self.animate_proof_line(*proof_lines[11:14])
        self.wait(2)
        self.custom_play(footnote_animations[-1])
        self.wait(2)

        self.write_QED()
        self.wait()