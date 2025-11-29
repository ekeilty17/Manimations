from manim import *
from greek_construction_scene import GreekConstructionScene
import numpy as np

# DONE (I just kept this because I already coded it, it's kind of a stupid construction)
class CopySegmentLengthToPoint(GreekConstructionScene):
    def construct(self):
        # The givens
        A = Dot([-3, 0, 0], color=self.default_color)
        B = Dot([0, -0.5, 0], color=self.default_color)
        C = Dot([1, 1, 0], color=self.given_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color)
        self.add(line_AB, C)

        # draw circle centered at B with radius to A
        circle_BA = self.get_oriented_circle(B, A, z_index=C.z_index-1)
        self.play(self.draw(A))
        self.play(self.draw(B))
        self.play(self.draw(circle_BA))

        # draw line from B to C
        line_BC = Line(B.get_center(), C.get_center(), color=self.default_color, z_index=C.z_index-1)
        self.play(self.draw(line_BC))

        circle_BC = self.get_oriented_circle(B, C, z_index=C.z_index-1)
        circle_CB = self.get_oriented_circle(C, B, z_index=C.z_index-1)
        self.play(self.draw(circle_BC))
        self.play(self.draw(circle_CB))
        
        # calculating intersection between circle_BC and circle_CB, which is labeled point D
        length = np.linalg.norm( line_BC.get_vector() )
        normal_direction = line_BC.get_angle() + 90*DEGREES
        unit_normal = np.array([np.cos(normal_direction), np.sin(normal_direction), 0])
        midpoint_coord = (B.get_center() + C.get_center())/2
        coord = midpoint_coord + (length * np.sqrt(3)/2)*unit_normal
        D = Dot(coord, color=self.default_color)
        self.play(self.draw(D))

        self.make_background_object(circle_BC, circle_CB)

        length = np.linalg.norm( line_AB.get_vector() )
        c1, c2 = self.extended_coordinates(D, B, 0, length)
        E = Dot(c2, color=self.default_color)
        line_DE = Line(D.get_center(), E.get_center(), color=self.default_color)
        self.play(self.draw(line_DE))
        self.play(self.draw(E))

        circle_DE = self.get_oriented_circle(D, E)
        self.play(self.draw(circle_DE))

        length = np.linalg.norm( line_AB.get_vector() )
        c1, c2 = self.extended_coordinates(D, C, 0, length)
        F = Dot(c2, color=self.default_color)
        line_DF = Line(D.get_center(), F.get_center(), color=self.default_color, z_index=C.z_index-1)
        self.play(self.draw(line_DF))
        self.play(self.draw(F))

        line_CF = Line(C.get_center(), F.get_center(), color=self.solution_color, z_index=C.z_index-1)
        self.play(self.draw(line_CF))

        self.wait()
        self.remove_objects(A, B, D, E, F, line_BC, line_DE, line_DF, circle_BA, circle_DE, *self.background_objects)
        self.wait()
        self.remove_objects(line_CF)
        self.wait()

# DONE, but I took shortcuts because otherwise it would be gross
class TranslateSegmentToPoint(GreekConstructionScene):
    def construct(self):
        # The givens
        A = Dot([-2, -2.5, 0], color=self.default_color)
        B = Dot([-3, 0.5, 0], color=self.default_color)
        C = Dot([1, -0.5, 0], color=self.given_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color)
        self.add(line_AB, C)

        D = Dot(C.get_center() + (B.get_center() - A.get_center()), color=self.default_color)

        c1, c2 = self.extended_coordinates(C, D, 7, 7)
        E, F = Dot(c1, color=self.default_color), Dot(c2, color=self.default_color)
        line_EF = Line(E.get_center(), F.get_center(), color=self.default_color, z_index=C.z_index-1)
        self.play(self.draw(line_EF))

        line_AC = Line(A.get_center(), C.get_center(), color=self.default_color, z_index=C.z_index-1)
        self.play(self.draw(A))
        self.play(self.draw(line_AC))

        self.play(self.draw(B))
        line_BD = Line(B.get_center(), D.get_center(), color=self.default_color, z_index=C.z_index-1)
        c1, c2 = self.extended_coordinates(B, D, 7, 7)
        G, H = Dot(c1, color=self.default_color), Dot(c2, color=self.default_color)
        line_GH = Line(G.get_center(), H.get_center(), color=self.default_color, z_index=C.z_index-1)
        self.play(self.draw(line_GH))

        self.play(self.draw(D))
        line_CD = Line(C.get_center(), D.get_center(), color=self.solution_color, z_index=C.z_index-1)
        self.play(self.draw(line_CD))

        self.remove_objects(A, B, D, line_AC, line_EF, line_GH)

# TODO: probably not worth
class TranslateAngleToPoint(GreekConstructionScene):
    def construct(self):
        pass

# DONE
class DoubleSegment(GreekConstructionScene):
    def construct(self):
        # the given line
        A = Dot([-1, 0, 0], color=self.default_color)
        B = Dot([1, 0, 0], color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB)
        self.wait()

        # label line
        b1 = Brace(line_AB, color=self.default_color)
        b1text = Text("1 unit", color=self.text_color).next_to(b1, DOWN)
        self.play(GrowFromCenter(b1), Write(b1text))
        self.wait()
        self.play(ShrinkToCenter(b1), Unwrite(b1text))

        # create circle to double the line segment
        self.play(self.draw(B))
        self.play(self.draw(A))
        circle_BA = self.get_oriented_circle(B, A)
        self.play(self.draw(circle_BA))
        self.wait()

        # animate extending the line
        length = np.linalg.norm( line_AB.get_vector() )
        c1, c2 = self.extended_coordinates(A, B, length, length)
        C = Dot(c2, color=self.default_color)
        line_AC = Line(A.get_center(), C.get_center(), color=self.solution_color, z_index=A.z_index-1)
        self.play(self.draw(line_AC))

        # removing objects
        self.wait()
        self.remove_objects(A, B, circle_BA)
        self.wait(0.5)

        # label solution
        b2 = BraceBetweenPoints(A.get_center(), C.get_center(), color=self.default_color)
        b2text = Text("2 units", color=self.text_color).next_to(b2, DOWN)
        #self.play(Transform(b1, b2), Transform(b1text, b2text))
        self.play(GrowFromCenter(b2), Write(b2text))

        # removing objects
        self.wait()
        self.play(ShrinkToCenter(b2), Unwrite(b2text))
        self.remove_objects(line_AC)
        self.wait()

# DONE
class DoubleAngle(GreekConstructionScene):
    def construct(self):
        # the givens
        theta = 27*DEGREES
        A = Dot([-1, -1, 0], color=self.default_color)
        B = Dot([4, 0, 0] + A.get_center(), color=self.default_color)
        C = Dot([4*np.cos(theta), 4*np.sin(theta), 0] + A.get_center(), color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        line_AC = Line(A.get_center(), C.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB, line_AC)

        # drawing angle
        a0 = Angle(line_AB, line_AC, radius=1, other_angle=False, color=self.text_color)
        text0 = MathTex(r"\theta", color=self.text_color).move_to(
            Angle(
                line_AB, line_AC, radius=1 + 3 * SMALL_BUFF, other_angle=False, color=self.text_color
            ).point_from_proportion(0.5)
        )
        self.play(Create(a0))
        self.play(Write(text0))
        self.wait()
        self.play(Uncreate(a0), Unwrite(text0))

        # draw circle
        r = ValueTracker(1.5)
        circle_A = Circle(radius=r.get_value(), color=self.default_color).move_to(A.get_center())
        self.play(self.draw(A))
        self.play(self.draw(circle_A))
        
        # show circle changing radius
        circle_A.add_updater(
            lambda c: c.become( Circle(radius=r.get_value(), color=self.default_color).move_to(c.get_center()) )
        )
        text = Text("any radius can be used", font_size=30, color=self.text_color).move_to([4.1, -2, 0])
        self.play(r.animate.set_value(3), Write(text), run_time=1)
        self.play(r.animate.set_value(1.5))
        self.play(Unwrite(text), run_time=0.5)
        circle_A.clear_updaters()

        # calculating points where circle intersects the given lines
        r = r.get_value()
        D = Dot([r, 0, 0] + A.get_center(), color=self.default_color)
        E = Dot([r*np.cos(theta), r*np.sin(theta), 0] + A.get_center(), color=self.default_color)
        self.play(self.draw(D))
        self.play(self.draw(E))

        # draw circle
        circle_ED = self.get_oriented_circle(E, D)
        self.play(self.draw(circle_ED))

        # get intersection between first circle and the small circle
        F = Dot([r*np.cos(2 * theta), r*np.sin(2 * theta), 0] + A.get_center(), color=self.default_color)
        self.play(self.draw(F))

        # draw double angle line
        G = Dot([4*np.cos(2 * theta), 4*np.sin(2 * theta), 0] + A.get_center(), color=self.default_color)
        line_AG = Line(A.get_center(), G.get_center(), color=self.solution_color, z_index=A.z_index-1)
        self.play(self.draw(line_AG))

        # remove other objects
        self.wait()
        self.remove_objects(A, D, E, F, circle_A, circle_ED)
        
        # drawing angle
        a1 = Angle(line_AB, line_AG, radius=1, other_angle=False, color=self.text_color)
        text1 = MathTex(r"2\theta", color=self.text_color).move_to(
            Angle(
                line_AB, line_AC, radius=1 + 6 * SMALL_BUFF, other_angle=False, color=self.text_color
            ).point_from_proportion(0.5)
        )
        self.play(Create(a1))
        self.play(Write(text1))
        self.wait()
        self.play(Uncreate(a1), Unwrite(text1))

        # remove solution
        self.wait()
        self.remove_objects(line_AG)

# DONE
class PerpendicularBisector(GreekConstructionScene):
    def construct(self):
        # the given line
        A = Dot([-1, 0, 0], color=self.default_color)
        B = Dot([1, 0, 0], color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color)
        line_AB.set_z_index(A.z_index - 1)
        self.add(line_AB)
        self.wait()

        # left circle
        circle_A = Circle(radius=2, color=self.default_color)
        circle_A.move_to(A.get_center())
        self.play(self.draw(A))
        self.play(self.draw(circle_A))
        
        # right circle
        circle_B = Circle(radius=2, color=self.default_color)
        circle_B.move_to(B.get_center())
        circle_B.flip(RIGHT).rotate(180*DEGREES)
        circle_B.set_z_index(A.z_index - 1)
        self.play(self.draw(B))
        self.play(self.draw(circle_B))
        
        # where the circles intersect
        C = Dot([0, np.sqrt(3), 0], color=self.default_color)
        D = Dot([0, -np.sqrt(3), 0], color=self.default_color)
        self.play(self.draw(C))
        self.play(self.draw(D))

        # drawing the line_CM line_CD
        line_CD = Line(C.get_center(), D.get_center(), color=self.solution_color)
        line_CD.set_z_index(C.z_index - 1)
        self.play(self.draw(line_CD))

        # removing all unnecessary objects
        self.wait()
        self.remove_objects(A, circle_A, B, circle_B, C, D)

        text1 = Text("line_CM", font_size=35, color=self.text_color).move_to([3, 0.3, 0])
        text2 = Text("bisector", font_size=35, color=self.text_color).move_to([3, -0.3, 0])

        # drawing right angle thing
        ra = RightAngle(line_AB, line_CD, quadrant=(1, -1), length=0.3, color=self.default_color)
        self.wait()
        self.play(Create(ra), Write(text1))

        # marking midpoint
        E = Dot([0, 0, 0], color=self.default_color)
        text3 = Text("/", font_size=30, color=self.text_color).move_to([0.5, 0, 0])
        text4 = Text("/", font_size=30, color=self.text_color).move_to([-0.5, 0, 0])
        self.play(self.draw(E))
        self.play(Write(text2), GrowFromCenter(text3), GrowFromCenter(text4))

        # remove solution
        self.wait()
        self.remove_objects(line_CD, ra, E, text1, text2, text3, text4)

# DONE
class AngleBisector(GreekConstructionScene):
    def construct(self):
        # the givens
        theta = 54*DEGREES
        A = Dot([-1, -1, 0], color=self.default_color)
        B = Dot([3.5, -1, 0], color=self.default_color)
        C = Dot([3, 3*np.tan(theta), 0] + A.get_center(), color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        line_AC = Line(A.get_center(), C.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AC, line_AB)

        # drawing angle
        a0 = Angle(line_AB, line_AC, radius=0.75, other_angle=False, color=self.text_color)
        text0 = MathTex(r"\theta", color=self.text_color).move_to(
            Angle(
                line_AB, line_AC, radius=0.75 + 3 * SMALL_BUFF, other_angle=False, color=self.text_color
            ).point_from_proportion(0.5)
        )
        self.play(Create(a0))
        self.play(Write(text0))
        self.wait()
        self.play(Uncreate(a0), Unwrite(text0))

        # draw circle
        r = ValueTracker(2)
        circle_A = Circle(radius=r.get_value(), color=self.default_color).move_to(A.get_center())
        self.play(self.draw(A))
        self.play(self.draw(circle_A))
        
        # show circle changing radius
        circle_A.add_updater(
            lambda c: c.become( Circle(radius=r.get_value(), color=self.default_color).move_to(c.get_center()) )
        )
        text = Text("any radius can be used", font_size=30, color=self.text_color).move_to([4.1, -2, 0])
        self.play(r.animate.set_value(3), Write(text), run_time=1)
        #self.play(r.animate.set_value(3.8))
        self.play(r.animate.set_value(1.5))
        self.play(Unwrite(text), run_time=0.5)
        circle_A.clear_updaters()

        # calculating points where circle intersects the given lines
        r = r.get_value()
        D = Dot([r*np.cos(theta), r*np.sin(theta), 0] + A.get_center(), color=self.default_color)
        E = Dot([r, 0, 0] + A.get_center(), color=self.default_color)
        self.play(self.draw(D))
        self.play(self.draw(E))

        # put circle in background
        self.make_background_object(circle_A)

        # we don't actually draw it, but we need the line as an input to the bisect_line function
        line_DE = Line(D.get_center(), E.get_center(), color=self.default_color)
        solution, background = self.bisect_segment(line_DE, draw_solution=False, draw_endpoints=False, draw_midpoint=False)
        F, *_ = solution

        # using the output, we draw the bisector
        self.play(self.draw(F))
        c1, c2 = self.extended_coordinates(A, F, 0, 0.5)
        #G_coord = (F.get_center() - A.get_center())*1.8 + A.get_center()
        extended_line_AF = Line(A.get_center(), c2, color=self.solution_color, z_index=line_AC.z_index-1)
        self.play(self.draw(extended_line_AF))
        
        # remove unneeded objects
        self.wait()
        self.remove_objects(A, D, E, F, circle_A, *background)

        # add some text
        a1 = Angle(line_AB, extended_line_AF, radius=0.7, other_angle=False, color=self.text_color)
        a2 = Angle(extended_line_AF, line_AC, radius=1, other_angle=False, color=self.text_color)
        text1 = MathTex(r"\theta/2", font_size=25, color=self.text_color).move_to(
            Angle(
                line_AB, extended_line_AF, radius=0.7 + 3 * SMALL_BUFF, other_angle=False, color=self.text_color
            ).point_from_proportion(0.5)
        )
        text2 = MathTex(r"\theta/2", font_size=25, color=self.text_color).move_to(
            Angle(
                extended_line_AF, line_AC, radius=1 + 3 * SMALL_BUFF, other_angle=False, color=self.text_color
            ).point_from_proportion(0.5)
        )
        self.play(Create(a1), Create(a2))
        self.play(Write(text1), Write(text2))
        self.wait()

        # remove solution
        self.remove_objects(extended_line_AF, a1, a2, text1, text2)

# DONE
class DropPerpendicularFromPoint(GreekConstructionScene):
    def construct(self):
        # the given line and point
        A = Dot([-5, -1, 0], color=self.default_color)
        B = Dot([5, -1, 0], color=self.default_color)
        C = Dot([1, 1, 0], color=self.given_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB, C)
        self.wait()

        # draw circle
        r = ValueTracker(2.2)
        circle_C = Circle(radius=r.get_value(), color=self.default_color).move_to(C.get_center())
        self.play(self.draw(circle_C))
        
        # show circle changing radius
        circle_C.add_updater(
            lambda c: c.become( Circle(radius=r.get_value(), color=self.default_color).move_to(c.get_center()) )
        )
        text = Text("any radius that intersects the line can be used", font_size=30, color=self.text_color).move_to([-3, -3.5, 0])
        self.play(r.animate.set_value(4), Write(text), run_time=2)
        self.play(r.animate.set_value(2.25))
        self.wait()
        self.play(Unwrite(text), run_time=0.5)
        circle_C.clear_updaters()

        r = r.get_value()
        x = np.sqrt(r**2 - 4)
        D = Dot([-x, -2, 0] + C.get_center(), color=self.default_color)
        E = Dot([x, -2, 0] + C.get_center(), color=self.default_color)
        self.play(self.draw(D))
        self.play(self.draw(E))

        self.make_background_object(circle_C)

        line_DE = Line(D.get_center(), E.get_center(), color=self.default_color)
        solution, background = self.bisect_segment(line_DE, solution_color=self.default_color, draw_endpoints=False, draw_midpoint=True)
        F, G, line_FG, M = solution

        self.make_background_object(D, E, F, G, line_FG, *background)

        line_CM = Line(C.get_center(), M.get_center(), color=self.solution_color, z_index=C.z_index-1)
        self.play(self.draw(line_CM))
        self.wait()

        self.remove_objects(M, *self.background_objects)
        self.wait()

        ra = RightAngle(line_AB, line_CM, quadrant=(1, -1), length=0.3, color=self.default_color)
        self.wait()
        self.play(Create(ra))

        self.wait(1)
        self.remove_objects(line_CM, ra)

# DONE
class RaisePerpendicularFromPoint(GreekConstructionScene):
    def construct(self):
        # the given line and point
        A = Dot([-5, -1, 0], color=self.default_color)
        B = Dot([5, -1, 0], color=self.default_color)
        C = Dot([1, -1, 0], color=self.given_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB, C)
        self.wait()

        # draw circle
        r = ValueTracker(2.2)
        circle_C = Circle(radius=r.get_value(), color=self.default_color).move_to(C.get_center())
        self.play(self.draw(circle_C))
        
        # show circle changing radius
        circle_C.add_updater(
            lambda c: c.become( Circle(radius=r.get_value(), color=self.default_color).move_to(c.get_center()) )
        )
        text = Text("any circle can be used", font_size=30, color=self.text_color).move_to([-3, -3.5, 0])
        self.play(r.animate.set_value(3.7), Write(text), run_time=2)
        self.play(r.animate.set_value(1.5))
        self.wait()
        self.play(Unwrite(text), run_time=0.5)
        circle_C.clear_updaters()

        self.wait()

        # draw circle intersection points
        r = r.get_value()
        D = Dot([-r, 0, 0] + C.get_center(), color=self.default_color)
        E = Dot([r, 0, 0] + C.get_center(), color=self.default_color)
        self.play(self.draw(D))
        self.play(self.draw(E))

        self.make_background_object(circle_C)

        # bisect segment between circle
        line_DE = Line(D.get_center(), E.get_center(), color=self.default_color)
        solution, background = self.bisect_segment(line_DE, draw_endpoints=False, draw_midpoint=False, draw_solution=False)
        self.wait()

        F, *_ = solution
        self.play(self.draw(F))
        self.make_background_object(D, E, *background)
        self.wait()

        line_CF = Line(C.get_center(), F.get_center(), color=self.solution_color, z_index=C.z_index-1)
        self.play(self.draw(line_CF))

        self.wait()
        self.remove_objects(F, *self.background_objects)

        ra = RightAngle(line_AB, line_CF, quadrant=(1, 1), length=0.3, color=self.default_color)
        self.wait()
        self.play(Create(ra))

        self.wait(1)
        self.remove_objects(line_CF, ra)

# DONE
class ParallelLineThroughPoint(GreekConstructionScene):
    def construct(self):
        # the given line and point
        A = Dot([-5, -2, 0], color=self.default_color)
        B = Dot([5, -2, 0], color=self.default_color)
        C = Dot([0.5, 0, 0], color=self.given_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB, C)
        self.wait()
        
        # draw point on line
        x = ValueTracker(-3)
        D = Dot([x.get_value(), -2, 0], color=self.default_color)
        self.play(self.draw(D))
        
        # show the dot moving on line
        D.add_updater(
            lambda d: d.become( Dot([x.get_value(), -2, 0], color=self.default_color) )
        )
        text = Text("any point the line can be used", font_size=30, color=self.text_color).next_to(line_AB, DOWN)
        self.play(x.animate.set_value(4.5), Write(text), run_time=2)
        self.play(x.animate.set_value(-4.5))
        self.play(x.animate.set_value(-2))
        self.wait()
        self.play(Unwrite(text), run_time=0.5)
        D.clear_updaters()

        # draw transversal
        c1, c2 = self.extended_coordinates(D.get_center(), C.get_center(), 2, 2)
        E = Dot(c1, color=self.default_color)
        F = Dot(c1, color=self.default_color)
        line_EF = Line(c1, c2, color=self.default_color, z_index=C.z_index-1)
        self.play(self.draw(line_EF))

        # draw circle
        r = ValueTracker(0.5)
        circle_D = Circle(radius=r.get_value(), color=self.default_color).move_to(D.get_center())
        self.play(self.draw(circle_D))

        # show circle changing radius
        circle_D.add_updater(
            lambda c: c.become( Circle(radius=r.get_value(), color=self.default_color).move_to(c.get_center()) )
        )
        text = Text("any radius between the two points can be used", font_size=30, color=self.text_color).move_to([2, 3, 0])
        self.play(r.animate.set_value(2), Write(text), run_time=2)
        self.play(r.animate.set_value(3))
        self.play(r.animate.set_value(1))
        self.wait()
        self.play(Unwrite(text), run_time=0.5)
        circle_D.clear_updaters()

        # get intersection of line_EF and circle_D and line_AB and circle_D
        unit_vector = line_EF.get_vector() / np.linalg.norm(line_EF.get_vector())
        G = Dot(D.get_center() + r.get_value() * unit_vector, color=self.default_color)
        H = Dot(D.get_center() + r.get_value() * np.array([1, 0, 0]), color=self.default_color)
        self.play(self.draw(G))
        self.play(self.draw(H))

        # draw circle on those intersections
        circle_GH = self.get_oriented_circle(G, H)
        self.play(self.draw(circle_GH))

        # copy circle_D and circle_GH over to point C
        circle_C = circle_D.copy().move_to(C.get_center())
        I = Dot(C.get_center() + r.get_value() * unit_vector, color=self.default_color)
        circle_I = circle_GH.copy().move_to(I.get_center())
        self.play(TransformFromCopy(circle_D, circle_C))
        self.play(self.draw(I))
        self.play(TransformFromCopy(circle_GH, circle_I))

        # get new intersection point
        J = Dot(C.get_center() + r.get_value() * np.array([1, 0, 0]), color=self.default_color)
        self.play(self.draw(J))

        # now we can draw the solution line
        K = Dot([0, 2, 0] + A.get_center(), color=self.default_color)
        L = Dot([0, 2, 0] + B.get_center(), color=self.default_color)
        line_KL = Line(K.get_center(), L.get_center(), color=self.solution_color, z_index=C.z_index-1)
        self.play(self.draw(line_KL))

        # clean up
        self.wait()
        self.remove_objects(D, G, H, I, J, line_EF, circle_C, circle_D, circle_GH, circle_I)
        self.wait()
        self.remove_objects(line_KL)
        self.wait()

# DONE
class ParallelLineThroughPoint2(GreekConstructionScene):
    def construct(self):
        # the given line and point
        A = Dot([-5, -1, 0], color=self.default_color)
        B = Dot([5, -1, 0], color=self.default_color)
        C = Dot([0.5, 1, 0], color=self.given_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB, C)
        self.wait()

        # first we drop the perpendicular from this point to line_AB
        r = 2.25
        circle_C = Circle(radius=r, color=self.default_color).move_to(C.get_center())
        self.play(self.draw(circle_C))

        x = np.sqrt(r**2 - 4)
        D = Dot([-x, -2, 0] + C.get_center(), color=self.default_color)
        E = Dot([x, -2, 0] + C.get_center(), color=self.default_color)
        self.play(self.draw(D))
        self.play(self.draw(E))

        self.make_background_object(circle_C)

        line_DE = Line(D.get_center(), E.get_center(), color=self.default_color)
        solution, background = self.bisect_segment(line_DE, solution_color=self.default_color, draw_solution=False, draw_endpoints=False, draw_midpoint=False)
        F, G, *_ = solution

        c1, c2 = self.extended_coordinates(F, G, 2, 0)
        H = Dot(c1, color=self.default_color)
        line_GH = Line(G.get_center(), H.get_center(), color=self.default_color, z_index=C.z_index-1)
        self.play(self.draw(G))
        self.play(self.draw(line_GH))

        self.make_background_object(D, E, G, *background)
        self.wait()


        # now we raise the perpendicular from the point and line_GH
        r = 1.5
        circle_C2 = Circle(radius=r, color=self.default_color).move_to(C.get_center())
        self.play(self.draw(circle_C2))

        I = Dot([0, -r, 0] + C.get_center(), color=self.default_color)
        J = Dot([0, r, 0] + C.get_center(), color=self.default_color)
        self.play(self.draw(I))
        self.play(self.draw(J))

        self.make_background_object(circle_C2)

        # bisect segment between circle
        line_IJ = Line(I.get_center(), J.get_center(), color=self.default_color, z_index=C.z_index-1)
        solution, background = self.bisect_segment(line_IJ, draw_endpoints=False, draw_midpoint=False, draw_solution=False)
        self.wait()

        K, L, *_ = solution
        self.play(self.draw(K))
        self.play(self.draw(L))
        
        M = Dot([0, 2, 0] + A.get_center(), color=self.default_color)
        N = Dot([0, 2, 0] + B.get_center(), color=self.default_color)
        line_MN = Line(M.get_center(), N.get_center(), color=self.solution_color, z_index=C.z_index-1)
        self.play(self.draw(line_MN))

        self.wait()
        self.remove_objects(I, J, K, L, line_GH, *background, *self.background_objects)
        self.wait()
        self.remove_objects(line_MN)
        self.wait()

