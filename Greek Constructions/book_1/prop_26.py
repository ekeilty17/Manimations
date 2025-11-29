import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class BookNPropM(GreekConstructionScenes):

    title = "Book 1 Proposition 26"
    description = """
        If two triangles have two angles equal to 
        two angles, respectively, and one side equal 
        to one side—in fact, either that by the equal 
        angles, or that subtending one of the equal 
        angles—then (the triangles) will also have the 
        remaining sides equal to the [corresponding] 
        remaining sides, and the remaining angle 
        (equal) to the remaining angle.
    """

    def write_givens(self):
        # Triangle ABC
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DL)

        line_BC = polar_to_line(B.get_center(), self.side.get_value(), 0)
        C, label_C = self.get_dot_and_label("C", line_BC.get_end(), DR)

        line_AB_extended = polar_to_line(B.get_center(), 1, self.angle_1.get_value())
        line_CA_extended = polar_to_line(C.get_center(), 1, PI - self.angle_2.get_value())
        
        A_coord = get_line_line_intersection(line_AB_extended, line_CA_extended)
        A, label_A = self.get_dot_and_label("A", A_coord, UP)

        line_AB = Line(A.get_center(), B.get_center())
        line_CA = Line(C.get_center(), A.get_center())

        # Triangle DEF
        E, label_E = self.get_dot_and_label("E", self.Ex.get_value() * RIGHT + self.Ey.get_value() * UP, DL)

        line_EF = polar_to_line(E.get_center(), self.side.get_value(), 0)
        F, label_F = self.get_dot_and_label("F", line_EF.get_end(), DR)

        line_DE_extended = polar_to_line(E.get_center(), 1, self.angle_1.get_value())
        line_FD_extended = polar_to_line(F.get_center(), 1, PI - self.angle_2.get_value())
        
        D_coord = get_line_line_intersection(line_DE_extended, line_FD_extended)
        D, label_D = self.get_dot_and_label("D", D_coord, UP)

        line_DE = Line(D.get_center(), E.get_center())
        line_FD = Line(F.get_center(), D.get_center())

        # marks
        line_BC_marker = get_line_marker(line_BC, marker_type="/")
        line_EF_marker = get_line_marker(line_EF, marker_type="/")

        angle_B_marker = get_angle_marker(line_AB, line_BC, marker_type="(")
        angle_C_marker = get_angle_marker(line_BC, line_CA, marker_type="((")
        angle_E_marker = get_angle_marker(line_DE, line_EF, marker_type="(")
        angle_F_marker = get_angle_marker(line_EF, line_FD, marker_type="((")

        givens = (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD,
        )
        intermediaries = (
            line_BC_marker, line_EF_marker,
            angle_B_marker, angle_C_marker, angle_E_marker, angle_F_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_BC, line_CA, line_DE, line_EF, line_FD,
        ) = givens
        (
            line_BC_marker, line_EF_marker,
            angle_B_marker, angle_C_marker, angle_E_marker, angle_F_marker,
        ) = given_intermediaries
        
        _, G, line_GB = interpolate_line(line_AB, self.G_percentage.get_value())
        line_GB.set_color(self.color_map[self.IMPOSSIBLE])
        G, label_G = self.get_dot_and_label("G", G.get_center(), LEFT, color=self.color_map[self.IMPOSSIBLE])

        line_GB_marker = get_line_marker(line_GB, marker_type="//")
        line_DE_marker = get_line_marker(line_DE, marker_type="//")

        intermediaries = (
            G, label_G,
            line_GB,
            line_DE_marker, line_GB_marker, 
        )
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"<ABC ~= <EDF", "[Givens]", self.GIVEN),
            (r"|BC ~= |EF", "[Givens]", self.GIVEN),
            (r"<ACB ~= <DFE", "[Givens]", self.GIVEN),
            (r"|AB > |DE", "[Assumption]", self.ASSUMPTION),
            (r"|BG ~= |DE", "[Prop. 1.3]", self.PBC_INTERMEDIARY),
            (r"^GBC ~= ^DEF", "[Prop. 1.4]", self.PBC_INTERMEDIARY),
            (r"<GCB ~= <DFE", "[Prop. 1.4]", self.CONTRADICTION),
            (r"<GCB < <ACB", "[Construction]", self.PBC_INTERMEDIARY),
            (r"<GCB < <DFE", "[CN. 1]", self.CONTRADICTION),
            (r"|AB ~= |DE", "[Contradiction]"),
            (r"^ABC ~= ^DEF", "[Prop. 1.4]"),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 2.5*LEFT)
        self.Ex, self.Ey, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 0.25*RIGHT)

        self.angle_1 = ValueTracker(PI/2 - PI/10)
        self.side = ValueTracker(2.5)
        self.angle_2 = ValueTracker(PI/5 + PI/40)

        self.triangle_ABC_angle = ValueTracker(0)
        self.triangle_EDF_angle = ValueTracker(0)

        self.G_percentage = ValueTracker(0.2)

        """ Initialization """
        self.initialize_canvas()
        self.initialize_construction(add_updaters=False)
        title, description = self.initialize_introduction()
        footnotes, footnote_animations = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()

        """ Construction Variables """
        # () = self.givens
        # () = self.given_intermediaries
        # () = self.solution_intermediaries
        # () = self.solution

        """ Animate Introduction """
        self.add(*self.givens, *self.given_intermediaries)
        self.wait()

        self.custom_play(*Animate(title, description))
        self.wait(3)
        self.custom_play(*Unanimate(title, description))
        self.wait()
        
        """ Animate Proof Line Numbers """
        self.animate_proof_line_numbers(proof_line_numbers)
        self.wait()
        
        """ Animation Construction """
        self.add(*self.solution_intermediaries, *self.solution)
        self.add(proof_lines)
        self.wait()