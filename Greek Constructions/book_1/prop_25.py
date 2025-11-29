import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class BookNPropM(GreekConstructionScenes):

    title = "Book 1 Proposition 25"
    description = """
        If two triangles have two sides equal to two sides,
        respectively, but (one) has a base greater than the 
        base (of the other), then (the former triangle) will 
        also have the angle encompassed by the equal 
        straight-lines greater than the (corresponding) 
        angle (in the latter).
    """

    def write_givens(self):
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, UP)
        D, label_D = self.get_dot_and_label("D", self.Dx.get_value() * RIGHT + self.Dy.get_value() * UP, UP)

        # b^2 = a^2 + c^2 - 2ac cos B
        a = self.side_length_1.get_value()
        b = self.side_length_2.get_value()
        c = self.line_BC_length.get_value()
        angle_B = np.arccos((a**2 + c**2 - b**2) / (2*a*c))

        line_AB = polar_to_line(A.get_center(), -self.side_length_1.get_value(), self.line_BC_angle.get_value() + angle_B)
        B, label_B = self.get_dot_and_label("B", line_AB.get_end(), DL)

        line_BC = polar_to_line(B.get_center(), self.line_BC_length.get_value(), self.line_BC_angle.get_value())
        C, label_C = self.get_dot_and_label("C", line_BC.get_end(), RIGHT)

        line_AC = Line(A.get_center(), C.get_center())
        
        # e^2 = d^2 + f^2 - 2df cos E
        d = self.side_length_1.get_value()
        e = self.side_length_2.get_value()
        f = self.line_EF_length.get_value()
        angle_E = np.arccos((d**2 + f**2 - e**2) / (2*d*f))

        line_DE = polar_to_line(D.get_center(), -self.side_length_1.get_value(), self.line_EF_angle.get_value() + angle_E)
        E, label_E = self.get_dot_and_label("E", line_DE.get_end(), DL)

        line_EF = polar_to_line(E.get_center(), self.line_EF_length.get_value(), self.line_EF_angle.get_value())
        F, label_F = self.get_dot_and_label("F", line_EF.get_end(), DR)

        line_DF = Line(D.get_center(), F.get_center())

        line_AB_marker = get_line_marker(line_AB, marker_type="/")
        line_AC_marker = get_line_marker(line_AC, marker_type="//")
        line_DE_marker = get_line_marker(line_DE, marker_type="/")
        line_DF_marker = get_line_marker(line_DF, marker_type="//")

        givens = (
            A, B, C, D, E, F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            line_AB, line_AC, line_BC, line_DE, line_DF, line_EF,
        )
        intermediaries = (
            line_AB_marker, line_AC_marker, line_DE_marker, line_DF_marker,
        )
        return givens, intermediaries

    def write_solution(self, givens, given_intermediaries):
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def write_proof_spec(self):
        return [
            (r"|AB ~= |DE", "[Given]", self.GIVEN),
            (r"|AC ~= |DF", "[Given]", self.GIVEN),
            (r"|BC > |EF", "[Given]", self.GIVEN),
            (r"<A ~= <D", "[Assumption]", self.ASSUMPTION),
            (r"^ABC ~= ^DEF", "[Prop. 1.4]", self.PBC_INTERMEDIARY),
            (r"|BC ~= |EF", "[Prop. 1.4]", self.CONTRADICTION),
            (r"<A !~= <D", "[Contradiction]"),
            (r"<A < <D", "[Assumption]", self.ASSUMPTION),
            (r"|BC < |EF", "[Prop. 1.14]", self.CONTRADICTION),
            (r"<A !< <D", "[Contradiction]"),
            (r"<A > <D", "[7. + 10.]", self.SOLUTION),
        ]
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    def construct(self):
        
        """ Value Trackers """
        self.side_length_1 = ValueTracker(2)
        self.side_length_2 = ValueTracker(1.5)
        self.line_BC_length = ValueTracker(3)
        self.line_EF_length = ValueTracker(2.5)
        self.line_BC_angle = ValueTracker(PI/6)
        self.line_EF_angle = ValueTracker(0)
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + 2*UP)
        self.Dx, self.Dy, _ = get_value_tracker_of_point(self.RIGHT_CENTER + RIGHT)

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