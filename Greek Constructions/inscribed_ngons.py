from manim import *
from greek_construction_scene import GreekConstructionScene
import numpy as np

class EquilateralTriangle(GreekConstructionScene):
    def construct(self):
        # the given circle
        A = Dot([0, 0, 0], color=self.given_color)
        r = 2
        circle_A = Circle(radius=r, color=self.given_color, z_index=A.z_index-1).move_to(A.get_center())
        self.add(A, circle_A)

        # choose any point on the circle
        theta = ValueTracker(0)
        B = Dot([r*np.cos(theta.get_value()), r*np.sin(theta.get_value()), 0], color=self.default_color)
        self.play(self.draw(B))

        B.add_updater(
            lambda d: d.become( Dot([r*np.cos(theta.get_value()), r*np.sin(theta.get_value()), 0], color=self.default_color) )
        )
        text = Text("choose any point on the circle", font_size=30, color=self.text_color).move_to([-3, -3.5, 0])
        self.play(theta.animate.set_value(2*PI), Write(text), run_time=2)
        self.play(theta.animate.set_value(3*PI/2))
        self.wait()
        self.play(Unwrite(text), run_time=0.5)
        B.clear_updaters()

        # draw circle at new point
        circle_BA = self.get_oriented_circle(B, A, z_index=A.z_index-1)
        self.play(self.draw(circle_BA))

        # get intersections between circle_A and circle_BA (the bottom two triangle points)
        C = Dot([-np.sqrt(3), -1, 0], color=self.default_color)
        D = Dot([ np.sqrt(3), -1, 0], color=self.default_color)
        self.play(self.draw(C))
        self.play(self.draw(D))

        # This circle gets the top of the triangle
        circle_CD = self.get_oriented_circle(C, D, z_index=A.z_index-1)
        self.play(self.draw(circle_CD))

        E = Dot([0, 2, 0], color=self.default_color)
        self.play(self.draw(E))

        self.make_background_object(B, circle_BA, circle_CD)

        # drawing triangle

        triangle_points = [D, C, E]
        triangle_sides = []
        for i in range(len(triangle_points)):
            d1 = triangle_points[i]
            d2 = triangle_points[(i+1)%len(triangle_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=C.z_index-1)
            triangle_sides.append(side)
            self.play(self.draw(side))
        
        self.wait()
        self.remove_objects(C, D, E, *self.background_objects)
        self.wait()
        self.remove_objects(*triangle_sides)
        self.wait()


class Square(GreekConstructionScene):
    def construct(self):
        # the given circle
        A = Dot([0, 0, 0], color=self.given_color)
        r = 2
        circle_A = Circle(radius=r, color=self.given_color, z_index=A.z_index-1).move_to(A.get_center())
        self.add(A, circle_A)

        # choose any point on the circle
        theta = ValueTracker(0)
        B = Dot([r*np.cos(theta.get_value()), r*np.sin(theta.get_value()), 0], color=self.default_color)
        self.play(self.draw(B))
        
        B.add_updater(
            lambda d: d.become( Dot([r*np.cos(theta.get_value()), r*np.sin(theta.get_value()), 0], color=self.default_color) )
        )
        text = Text("choose any point on the circle", font_size=30, color=self.text_color).move_to([-3, -3.5, 0])
        self.play(theta.animate.set_value(2*PI), Write(text), run_time=2)
        self.play(theta.animate.set_value(PI/4))
        self.wait()
        self.play(Unwrite(text), run_time=0.5)
        B.clear_updaters()

        C = Dot([r*np.cos(5*PI/4), r*np.sin(5*PI/4), 0], color=self.default_color)
        line_BC = Line(B.get_center(), C.get_center(), color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_BC))
        self.play(self.draw(C))

        solution, background = self.bisect_segment(line_BC, draw_endpoints=False)
        D, E, line_DE, _ = solution
        _, _, circle_B, circle_C = background

        F = Dot([r*np.cos(3*PI/4), r*np.sin(3*PI/4), 0], color=self.default_color)
        G = Dot([r*np.cos(7*PI/4), r*np.sin(7*PI/4), 0], color=self.default_color)
        self.play(self.draw(F))
        self.play(self.draw(G))
        
        self.make_background_object(D, E, line_BC, line_DE, circle_B, circle_C)

        square_points = [C, F, B, G]
        square_sides = []
        for i in range(len(square_points)):
            d1 = square_points[i]
            d2 = square_points[(i+1)%len(square_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=A.z_index-1)
            square_sides.append(side)
            self.play(self.draw(side))

        self.wait()
        self.remove_objects(*square_points, *self.background_objects)
        self.wait()
        self.remove_objects(*square_sides)
        self.wait()


class Pentagon(GreekConstructionScene):
    def construct(self):
        # the given circle
        A = Dot([0, 0, 0], color=self.given_color)
        r = 2
        circle_A = Circle(radius=r, color=self.given_color, z_index=A.z_index-1).move_to(A.get_center())
        self.add(A, circle_A)

        # the given circle
        A = Dot([0, 0, 0], color=self.given_color)
        r = 2
        circle_A = Circle(radius=r, color=self.given_color, z_index=A.z_index-1).move_to(A.get_center())
        self.add(A, circle_A)

        # choose any line on the circle
        B, C = Dot([-2, 0, 0], color=self.default_color), Dot([2, 0, 0], color=self.default_color)
        line_BC = Line(B.get_center(), C.get_center(), color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_BC))
        
        # show line rotating
        text = Text("choose any diameter of the circle\nwhich is any line through the A", font_size=30, color=self.text_color).move_to([-3, -3.5, 0])
        self.play(Write(text), Rotating(line_BC, radians=-PI/2, about=A.get_center()), run_time=1)
        self.play(Unwrite(text))
        
        # location of the rotated points and rotated line
        D, E = Dot([0, 2, 0], color=self.default_color), Dot([0, -2, 0], color=self.default_color)
        line_DE = Line(D.get_center(), E.get_center(), color=self.default_color)

        solution, background = self.bisect_segment(line_DE)
        F, G, line_FG, _ = solution
        D, E, circle_D, circle_E = background
        
        # the whole point was to get line_AC
        self.play(self.draw(C))
        self.make_background_object(F, G, line_FG, circle_D, circle_E)
        line_AC = Line(A.get_center(), C.get_center(), color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_AC))

        # bisecting line_AC, we have to do it manually because we don't want to redraw the given line
        #solution, background = self.bisect_segment(line_AC, draw)
        #H, I, line_HI, J = solution
        c1, c2 = A.get_center(), C.get_center()
        length = np.linalg.norm(c2-c1)
        normal_direction = line_AC.get_angle() + 90*DEGREES
        unit_normal = np.array([np.cos(normal_direction), np.sin(normal_direction), 0])
        midpoint = (c1 + c2)/2
        
        circle_CA = self.get_oriented_circle(C, A, z_index=A.z_index-1)
        self.play(self.draw(circle_CA))

        H = Dot(midpoint + (length * np.sqrt(3)/2)*unit_normal, color=self.default_color)
        I = Dot(midpoint - (length * np.sqrt(3)/2)*unit_normal, color=self.default_color)
        line_HI = Line(H.get_center(), I.get_center(), color=self.default_color, z_index=H.z_index-1)
        self.play(self.draw(H))
        self.play(self.draw(I))
        self.play(self.draw(line_HI))

        J = Dot([1, 0, 0], color=self.default_color)
        self.play(self.draw(J))
        self.make_background_object(H, I, line_HI, circle_CA)

        # draw circle centered at J and line through J
        circle_J = self.get_oriented_circle(J, A, z_index=A.z_index-1)
        self.play(self.draw(circle_J))

        c1, c2 = self.extended_coordinates(E, J, 0, 2)
        K = Dot(c2, color=self.default_color)
        line_EK = Line(E.get_center(), K.get_center(), color=self.default_color, z_index=J.z_index-1)
        self.play(self.draw(line_EK))

        # getting intersection between circle_J and line_EK
        theta = line_EK.get_angle()
        L = Dot(J.get_center() + [np.cos(theta), np.sin(theta), 0], color=self.default_color)
        self.play(self.draw(L))

        # getting circle_EL
        circle_EL = self.get_oriented_circle(E, L)
        self.play(self.draw(circle_EL))

        # intersection with circle_EL and circle_A
        M = Dot(A.get_center() + [r*np.cos(0*2*PI/5 + PI/10), r*np.sin(0*2*PI/5 + PI/10), 0], color=self.default_color)
        N = Dot(A.get_center() + [r*np.cos(2*2*PI/5 + PI/10), r*np.sin(2*2*PI/5 + PI/10), 0], color=self.default_color)
        self.play(self.draw(M))
        self.play(self.draw(N))

        # move extra lines to background
        self.make_background_object(E, C, J, L, line_BC, line_AC, line_EK, circle_J, circle_EL)

        # getting last two points
        circle_MD = self.get_oriented_circle(M, D)
        circle_ND = self.get_oriented_circle(N, D)
        self.play(self.draw(circle_MD))
        self.play(self.draw(circle_ND))

        O = Dot(A.get_center() + [r*np.cos(3*2*PI/5 + PI/10), r*np.sin(3*2*PI/5 + PI/10), 0], color=self.default_color)
        P = Dot(A.get_center() + [r*np.cos(4*2*PI/5 + PI/10), r*np.sin(4*2*PI/5 + PI/10), 0], color=self.default_color)
        self.play(self.draw(O))
        self.play(self.draw(P))

        # drawing pentagon
        pentagon_points = [P, O, N, D, M]
        pentagon_sides = []
        for i in range(len(pentagon_points)):
            d1 = pentagon_points[i]
            d2 = pentagon_points[(i+1)%len(pentagon_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=A.z_index-1)
            pentagon_sides.append(side)
            self.play(self.draw(side))

        self.wait()
        self.remove_objects(circle_MD, circle_ND, *pentagon_points, *self.background_objects)
        self.wait()
        self.remove_objects(*pentagon_sides)
        self.wait()


class Hexagon(GreekConstructionScene):
    def construct(self):
        # the given circle
        A = Dot([0, 0, 0], color=self.given_color)
        r = 2
        circle_A = Circle(radius=r, color=self.given_color, z_index=A.z_index-1).move_to(A.get_center())
        self.add(A, circle_A)

        # choose any point on the circle
        theta = ValueTracker(0)
        B = Dot(A.get_center() + [r*np.cos(theta.get_value()), r*np.sin(theta.get_value()), 0], color=self.default_color)
        self.play(self.draw(B))

        B.add_updater(
            lambda d: d.become( Dot(A.get_center() + [r*np.cos(theta.get_value()), r*np.sin(theta.get_value()), 0], color=self.default_color) )
        )
        text = Text("choose any point on the circle", font_size=30, color=self.text_color).move_to([-3, -3.5, 0])
        self.play(theta.animate.set_value(2*PI), Write(text), run_time=2)
        self.play(theta.animate.set_value(5*PI/3))
        self.wait()
        self.play(Unwrite(text), run_time=0.5)
        B.clear_updaters()

        circle_BA = self.get_oriented_circle(B, A, z_index=A.z_index-1)
        self.play(self.draw(circle_BA))

        hexagon_points = [B]
        circles = [circle_BA]
        for n in reversed(range(5)):
            dot = Dot(A.get_center() + [r*np.cos(n*PI/3), r*np.sin(n*PI/3), 0], color=self.default_color)
            self.play(self.draw(dot))
            
            circle = self.get_oriented_circle(dot, A, z_index=A.z_index-1)
            self.play(self.draw(circle))

            hexagon_points.append(dot)
            circles.append(circle)

        self.wait()
        self.make_background_object(*circles)

        hexagon_sides = []
        for i in range(len(hexagon_points)):
            d1 = hexagon_points[i]
            d2 = hexagon_points[(i+1)%len(hexagon_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=A.z_index-1)
            hexagon_sides.append(side)
            self.play(self.draw(side))

        self.wait()
        self.remove_objects(*self.background_objects, *hexagon_points)
        self.wait()
        self.remove_objects(*hexagon_sides)
        self.wait()


class Hexagon2(GreekConstructionScene):
    def construct(self):
        # the given circle
        A = Dot([0, 0, 0], color=self.given_color)
        r = 2
        circle_A = Circle(radius=r, color=self.given_color, z_index=A.z_index-1).move_to(A.get_center())
        self.add(A, circle_A)

        # choose any line on the circle
        B, C = Dot([0, 2, 0], color=self.default_color), Dot([0, -2, 0], color=self.default_color)
        line_BC = Line(B.get_center(), C.get_center(), color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_BC))

        # show line rotating
        text = Text("choose any diameter of the circle\nwhich is any line through the A", font_size=30, color=self.text_color).move_to([-3, -3.5, 0])
        self.play(Write(text), Rotating(line_BC, radians=PI/2, about=A.get_center()), run_time=1)
        self.play(Unwrite(text))

        # getting final points of the line
        D = Dot(A.get_center() + [r*np.cos(0*PI/3), r*np.sin(0*PI/3), 0], color=self.default_color)
        E = Dot(A.get_center() + [r*np.cos(3*PI/3), r*np.sin(3*PI/3), 0], color=self.default_color)
        self.play(self.draw(D))
        self.play(self.draw(E))

        # drawing circles from those points
        circle_DA = self.get_oriented_circle(D, A, z_index=A.z_index-1)
        circle_EA = self.get_oriented_circle(E, A, z_index=A.z_index-1)
        self.play(self.draw(circle_DA))
        self.play(self.draw(circle_EA))

        # getting intersection with circle A
        F = Dot(A.get_center() + [r*np.cos(1*PI/3), r*np.sin(1*PI/3), 0], color=self.default_color)
        G = Dot(A.get_center() + [r*np.cos(2*PI/3), r*np.sin(2*PI/3), 0], color=self.default_color)
        H = Dot(A.get_center() + [r*np.cos(4*PI/3), r*np.sin(4*PI/3), 0], color=self.default_color)
        I = Dot(A.get_center() + [r*np.cos(5*PI/3), r*np.sin(5*PI/3), 0], color=self.default_color)
        self.play(self.draw(F))
        self.play(self.draw(G))
        self.play(self.draw(H))
        self.play(self.draw(I))
        hexagon_points = [I, H, E, G, F, D]

        # moving objects to background
        self.make_background_object(line_BC, circle_DA, circle_EA)

        # drawing hexagon
        hexagon_sides = []
        for i in range(len(hexagon_points)):
            d1 = hexagon_points[i]
            d2 = hexagon_points[(i+1)%len(hexagon_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=A.z_index-1)
            hexagon_sides.append(side)
            self.play(self.draw(side))

        # clean up
        self.wait()
        self.remove_objects(*hexagon_points, *self.background_objects)
        self.wait()
        self.remove_objects(*hexagon_sides)
        self.wait()


class Octagon(GreekConstructionScene):
    def construct(self):
        # the given circle
        A = Dot([0, 0, 0], color=self.given_color)
        r = 2
        circle_A = Circle(radius=r, color=self.given_color, z_index=A.z_index-3)
        self.add(A, circle_A)

        # choose any point on the circle
        theta = ValueTracker(0)
        B = Dot(A.get_center() + [r*np.cos(theta.get_value()), r*np.sin(theta.get_value()), 0], color=self.default_color)
        self.play(GrowFromCenter(B))

        B.add_updater(
            lambda d: d.become( Dot(A.get_center() + [r*np.cos(theta.get_value()), r*np.sin(theta.get_value()), 0], color=self.default_color) )
        )
        text = Text("choose any point on the circle", font_size=30, color=self.text_color).move_to([-3, -3.5, 0])
        self.play(theta.animate.set_value(8*PI/4), Write(text), run_time=2)
        self.play(theta.animate.set_value(7*PI/4 + PI/8))
        self.wait()
        self.play(Unwrite(text), run_time=0.5)
        B.clear_updaters()

        # draw line through diameter of circle_A
        C = Dot(A.get_center() + [r*np.cos(3*PI/4 + PI/8), r*np.sin(3*PI/4 + PI/8), 0], color=self.default_color)
        line_BC = Line(B.get_center(), C.get_center(), color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_BC))
        self.play(self.draw(C))

        # bisect the line
        line_CB = Line(C.get_center(), B.get_center(), color=self.default_color, z_index=A.z_index-1)
        solution, background = self.bisect_segment(line_CB, draw_endpoints=False)
        D, E, line_DE, _ = solution
        _, _, circle_C, circle_B = background

        F = Dot(A.get_center() + [r*np.cos(1*PI/4 + PI/8), r*np.sin(1*PI/4 + PI/8), 0], color=self.default_color, z_index=A.z_index-1)
        G = Dot(A.get_center() + [r*np.cos(5*PI/4 + PI/8), r*np.sin(5*PI/4 + PI/8), 0], color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(F))
        self.play(self.draw(G))

        self.make_background_object(D, E, line_BC, line_DE, circle_C, circle_B)

        # We now have a square, so all we have to do is bisect one of the arcs to get the arc for an octogon
        line_GB = Line(G.get_center(), B.get_center(), color=self.default_color, z_index=A.z_index-1)
        solution, background = self.bisect_segment(line_GB, draw_endpoints=False, draw_solution=False)
        H, I, line_HI, J = solution
        _, _, circle_G, circle_B = background
        self.play(self.draw(I))
        self.play(self.draw(H))

        c1, c2 = self.extended_coordinates(H, I, 2, 0)
        K = Dot(c1, color=self.default_color)
        line_IK = Line(I.get_center(), K.get_center(), color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_IK))

        # getting intersection with circle_A
        L = Dot(A.get_center() + [r*np.cos(6*PI/4 + PI/8), r*np.sin(6*PI/4 + PI/8), 0], color=self.default_color)
        M = Dot(A.get_center() + [r*np.cos(2*PI/4 + PI/8), r*np.sin(2*PI/4 + PI/8), 0], color=self.default_color)
        self.play(self.draw(L))
        self.play(self.draw(M))

        # cleaning up
        self.make_background_object(H, I, line_IK, circle_G, circle_B)

        # getting final two points
        circle_CM = self.get_oriented_circle(C, M)
        circle_BL = self.get_oriented_circle(B, L)
        self.play(self.draw(circle_CM))
        self.play(self.draw(circle_BL))

        N = Dot(A.get_center() + [r*np.cos(0*PI/4 + PI/8), r*np.sin(0*PI/4 + PI/8), 0], color=self.default_color)
        O = Dot(A.get_center() + [r*np.cos(4*PI/4 + PI/8), r*np.sin(4*PI/4 + PI/8), 0], color=self.default_color)
        self.play(self.draw(N))
        self.play(self.draw(O))

        self.make_background_object(circle_CM, circle_BL)

        # drawing octagon
        octagon_points = [G, O, C, M, F, N, B, L]
        octagon_sides = []
        for i in range(len(octagon_points)):
            d1 = octagon_points[i]
            d2 = octagon_points[(i+1)%len(octagon_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=F.z_index-1)
            octagon_sides.append(side)
            self.play(self.draw(side))

        # clean up
        self.wait()
        self.remove_objects(*octagon_points, *self.background_objects)
        self.wait()
        self.remove_objects(*octagon_sides)
        self.wait()


class Heptadecagon(GreekConstructionScene):
    def construct(self):
        #########################################################
        #                   Part 1: set up                      #
        #########################################################

        # the given circle
        A = Dot([0, 0, 0], color=self.given_color)
        r = 3.5
        circle_A = Circle(radius=r, color=self.given_color, z_index=A.z_index-1).move_to(A.get_center())
        self.add(A, circle_A)

        # choose any line on the circle
        text = Text("choose any diameter of the circle\nwhich is any line through the origin", font_size=25, color=self.text_color).move_to([-4, -3.5, 0])
        B, C = Dot(A.get_center() + [-r, 0, 0], color=self.default_color), Dot(A.get_center() + [r, 0, 0], color=self.default_color)
        line_BC = Line(B.get_center(), C.get_center(), color=self.default_color, z_index=A.z_index-1)
        self.play(Write(text), self.draw(line_BC), run_time=1.5)
        self.wait(0.5)
        self.play(Unwrite(text))


        #########################################################
        #               Part 2: get sloped line                 #
        #########################################################

        # now we raise the perpendicular of line_BC from the origin A
        circle_A2 = Circle(radius=r/4, color=self.default_color, z_index=A.z_index-1).move_to(A.get_center())
        self.play(self.draw(circle_A2))

        D, E = Dot(A.get_center() + [-r/4, 0, 0], color=self.default_color), Dot(A.get_center() + [r/4, 0, 0], color=self.default_color)
        line_DE = Line(D.get_center(), E.get_center(), color=self.default_color, z_index=A.z_index-1)
        solution, background = self.bisect_segment(line_DE, draw_solution=False)
        F, G, line_FG, _ = solution
        self.play(self.draw(F))
        
        H = Dot(A.get_center() + [0, r, 0], color=self.default_color)
        line_AH = Line(A.get_center(), H.get_center(), color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_AH))
        self.play(self.draw(H))
        
        self.make_background_object(F, circle_A2, *background)

        # now we quarter line_AH
        # we have to do the first halving manually because we don't want to redraw circle_A
        circle_HA = self.get_oriented_circle(H, A, z_index=A.z_index-1)
        self.play(self.draw(circle_HA))

        I, J = Dot(A.get_center() + [-r*np.sqrt(3)/2, r/2, 0], color=self.default_color), Dot([r*np.sqrt(3)/2, r/2, 0], color=self.default_color)
        self.play(self.draw(I))
        self.play(self.draw(J))

        line_IJ = Line(I.get_center(), J.get_center(), color=self.default_color)
        self.play(self.draw(line_IJ))

        K = Dot(A.get_center() + [0, r/2, 0], color=self.default_color)
        self.play(self.draw(K))

        self.make_background_object(circle_HA, I, J, line_IJ)

        # now I half each segment again
        circle_HK = self.get_oriented_circle(H, K, z_index=A.z_index-1)
        circle_KA = self.get_oriented_circle(K, A, z_index=A.z_index-1)
        circle_AK = self.get_oriented_circle(A, K, z_index=A.z_index-1)
        self.play(self.draw(circle_HK))
        self.play(self.draw(circle_KA))
        self.play(self.draw(circle_AK))

        L = Dot(A.get_center() + [-r/2*np.sqrt(3)/2, 3*r/4, 0], color=self.default_color)
        M = Dot(A.get_center() + [ r/2*np.sqrt(3)/2, 3*r/4, 0], color=self.default_color)
        N = Dot(A.get_center() + [-r/2*np.sqrt(3)/2, r/4, 0], color=self.default_color)
        O = Dot(A.get_center() + [ r/2*np.sqrt(3)/2, r/4, 0], color=self.default_color)
        line_LM = Line(L.get_center(), M.get_center(), color=self.default_color)
        line_NO = Line(N.get_center(), O.get_center(), color=self.default_color)
        P = Dot(A.get_center() + [0, 3*r/4, 0], color=self.default_color)
        Q = Dot(A.get_center() + [0, r/4, 0], color=self.default_color)
        self.play(self.draw(L))
        self.play(self.draw(M))
        self.play(self.draw(line_LM))
        self.play(self.draw(N))
        self.play(self.draw(O))
        self.play(self.draw(line_NO))
        self.play(self.draw(P))
        self.play(self.draw(Q))

        self.make_background_object(L, M, N, O, line_LM, line_NO, circle_HK, circle_KA, circle_AK)

        # finally drawing desired line
        self.play(self.draw(C))
        c1, c2 = self.extended_coordinates(C, Q, 0, r)
        R = Dot(c2, color=self.default_color)
        line_CR = Line(C.get_center(), R.get_center(), color=self.default_color)
        self.play(self.draw(line_CR))


        #########################################################
        #               Part 3: quarter the angle               #
        #########################################################

        # This is part of bisecting the angle, we are just doing it from the other side
        circle_QP = self.get_oriented_circle(Q, P)
        self.play(self.draw(circle_QP))
        
        # getting intersection points
        theta = line_CR.get_angle()
        S = Dot(Q.get_center() + [ r/2*np.cos(theta),  r/2*np.sin(theta), 0], color=self.default_color)
        self.play(self.draw(S))

        # bisect the angle
        line_SP = Line(S.get_center(), P.get_center(), color=self.default_color)
        #self.play(self.draw(line_SP))

        solution, background = self.bisect_segment(line_SP, draw_endpoints=False, draw_solution=False)
        T, *_ = solution
        _, _, *bgr = background
        self.play(self.draw(T))
        c1, c2 = self.extended_coordinates(T, Q, 0, r/2)
        U = Dot(c2, color=self.default_color)
        line_TU = Line(T.get_center(), U.get_center(), color=self.default_color)
        self.play(self.draw(line_TU))

        self.make_background_object(S, T, circle_QP, *bgr)

        # quarter the angle
        circle_QK = self.get_oriented_circle(Q, K)
        self.play(self.draw(circle_QK))

        theta = line_TU.get_angle()
        V = Dot(Q.get_center() + [-r/4*np.cos(theta), -r/4*np.sin(theta), 0], color=self.default_color)
        self.play(self.draw(V))

        line_VK = Line(V.get_center(), K.get_center(), color=self.default_color)
        #self.play(self.draw(line_VK))

        solution, background = self.bisect_segment(line_VK, draw_endpoints=False, draw_solution=False)
        W, *_ = solution
        _, _, *bgr = background
        self.play(self.draw(W))
        c1, c2 = self.extended_coordinates(W, Q, 0, r)
        X = Dot(c2, color=self.default_color)
        line_WX = Line(W.get_center(), X.get_center(), color=self.default_color)
        self.play(self.draw(line_WX))

        # get intersection with base-line, I calculated it theoretically to avoid numerical errors
        Y = Dot([r/4*np.tan(np.arctan(4)/4), 0, 0], color=self.default_color)
        self.play(self.draw(Y))

        self.make_background_object(V, W, line_TU, circle_QK, *bgr)
        
        #line_YQ = Line(Y.get_center(), Q.get_center(), color=self.default_color)
        #self.play(self.draw(line_YQ))

        #########################################################
        #           Part 4: make a 45 degree angle              #
        #########################################################

        # since I am running out of letters and most of the variables are in the background now, 
        # I'm going to do some name shuffling to consolodate
        
        # The following will not change: A, circle_A, B, C, and line_BC
        D, E, F, G = H, P, K, Q         # the quarter marks on the perpendicular starting from the top
        line_AD = line_AH
        H = R                           # the long sloped line with coordinates
        line_CH = line_CR
        I, J = W, X                     # the quarter angle coordinates and line
        line_IJ = line_WX
        K = Y                           # the desired point
        # all other variables will be assumed to be free to re-assign

        # with that out of the way, we now need to draw a 45 degree angle from line_JG
        circle_KG = self.get_oriented_circle(K, G)
        self.play(self.draw(circle_KG))

        # get other intersection point
        radius = circle_KG.radius
        theta = line_IJ.get_angle()
        L = Dot(K.get_center() + [radius*np.cos(theta), radius*np.sin(theta), 0], color=self.default_color)
        self.play(self.draw(L))

        # we bisect line_GL
        line_GL = Line(G.get_center(), L.get_center(), color=self.default_color)
        solution, background = self.bisect_segment(line_GL, draw_endpoints=False)
        M, N, line_MN, _ = solution
        _, _, *bgr = background
        
        # get intersection of bisector on circle
        radius = circle_KG.radius
        theta = line_MN.get_angle()
        O = Dot(K.get_center() + [radius*np.cos(theta), radius*np.sin(theta), 0], color=self.default_color)
        self.play(self.draw(O))

        # connect intersection with point G, this gives us the 45 degree angle
        line_OG = Line(O.get_center(), G.get_center(), color=self.default_color)
        self.play(self.draw(line_OG))

        # getting the intersection with the x-axis
        t = np.tan(np.arctan(4)/4)
        P = Dot([-r/4 * (1-t)/(1+t), 0, 0], color=self.default_color)
        self.play(self.draw(P))

        # simplifying
        self.make_background_object(L, M, N, O, line_IJ, line_MN, line_OG, circle_KG, *bgr)
        line_KG = Line(K.get_center(), G.get_center(), color=self.default_color)
        line_GP = Line(G.get_center(), P.get_center(), color=self.default_color)
        self.play(self.draw(line_KG))
        self.play(self.draw(line_GP))

        
        #########################################################
        #               Part 5: some more points                #
        #########################################################

        # again, I'm just going to clean up the variables 
        # because all of that nonsense was only to get 1 point

        # The following will not change: A, B, C, D, E, F, G, H line_BC, line_AD, line_CH, circle_A
        I, J = K, P         # the two points on the x-axis
        line_IG, line_GJ = line_KG, line_GP
        # All other variables will be assumed to be free to re-assign

        # first I'm extending line_AD
        K = Dot([0, -r, 0], color=self.default_color)
        line_AK = Line(A.get_center(), K.get_center(), color=self.default_color, z_index=A.z_index-1)
        #self.play(self.draw(line_AK))
        # I actually decided not to draw it

        # I need to find the midpoint between J and C
        line_JC = Line(J.get_center(), C.get_center(), color=self.default_color, z_index=A.z_index-1)
        solution, background = self.bisect_segment(line_JC, draw_endpoints=False, draw_midpoint=True)
        *sol, K = solution
        _, _, *bgr = background
        self.make_background_object(*sol, *bgr)

        # draw circle centered at K
        circle_KC = self.get_oriented_circle(K, C, z_index=A.z_index-1)
        self.play(self.draw(circle_KC))

        # calculating intersection, again doing it theoretically to avoid numerical error
        t = np.tan(np.arctan(4)/4)
        a = (1-t)/(1+t)
        y = r/2 * np.sqrt(a)
        L = Dot([0, y, 0], color=self.default_color)
        self.play(self.draw(L))

        # I have to get rid of point K, because it's very very very close to point M, but they are not equal
        self.make_background_object(K, circle_KC)

        # drawing more circles
        circle_IL = self.get_oriented_circle(I, L, z_index=A.z_index-1)
        self.play(self.draw(circle_IL))

        x = r/2 * np.sqrt(t**2/4 + (1-t)/(1+t))
        M = Dot(I.get_center() + [x, 0, 0], color=self.default_color)
        N = Dot(I.get_center() + [-x, 0, 0], color=self.default_color)
        self.play(self.draw(M))
        self.play(self.draw(N))

        #self.make_background_object(L, circle_IL)


        #########################################################
        #           Part 6: raise perpendiculars                #
        #########################################################

        # raising perpendicular of M from x-axis
        circle_M = Circle(radius=r/4, color=self.default_color).move_to(M.get_center())
        self.play(self.draw(circle_M))

        line_M = Line(M.get_center() + [r/4, 0, 0], M.get_center() + [-r/4, 0, 0], color=self.default_color)
        solution, background = self.bisect_segment(line_M, draw_solution=False)
        O, *_ = solution
        self.play(self.draw(O))

        c1, c2 = self.extended_coordinates(M, O, 0, 3*r/5)
        P = Dot(c2, color=self.default_color)
        line_MP = Line(M.get_center(), P.get_center(), color=self.default_color)
        self.play(self.draw(line_MP))

        self.make_background_object(O, circle_M, *background)

        # raising perpendicular of N from x-axis
        circle_N = Circle(radius=r/4, color=self.default_color).move_to(N.get_center())
        self.play(self.draw(circle_N))

        line_N = Line(N.get_center() + [r/4, 0, 0], N.get_center() + [-r/4, 0, 0], color=self.default_color)
        solution, background = self.bisect_segment(line_N, draw_solution=False)
        Q, *_ = solution
        self.play(self.draw(Q))

        c1, c2 = self.extended_coordinates(N, Q, 0, 3*r/5)
        R = Dot(c2, color=self.default_color)
        line_NR = Line(N.get_center(), R.get_center(), color=self.default_color)
        self.play(self.draw(line_NR))

        self.make_background_object(Q, circle_N, *background)

        # drawing intersection points
        x, _, _ = M.get_center()
        S = Dot([x, -np.sqrt(r**2-x**2), 0], color=self.default_color)
        self.play(self.draw(S))

        x, _, _ = N.get_center()
        T = Dot([x, -np.sqrt(r**2-x**2), 0], color=self.default_color)
        self.play(self.draw(T))

        self.remove_objects(*self.background_objects)
        self.background_objects = []
        self.wait()
        self.make_background_object(C, D, E, F, G, I, J, L, M, N, line_BC, line_CH, line_AD, line_IG, line_GJ, line_MP, line_NR, circle_IL)
        self.wait()

        #########################################################
        #           Part 7: getting 17-gon points               #
        #########################################################

        line_AS = Line(A.get_center(), S.get_center(), color=self.default_color, z_index=A.z_index-1)
        theta = line_AS.get_angle()
        
        heptadecagon_points = [None]*17
        circles = []
        for i in range(17):
            j = (2*i)%17
            j_prev = (2*(i-1))%17
            
            dot = Dot([r*np.cos(theta - j*2*PI/17), r*np.sin(theta - j*2*PI/17), 0], color=self.default_color)
            heptadecagon_points[j] = dot
            
            if i == 0:      # extra logic because we alrady drew two of the dots
                continue
            if i != 1:
                self.play(self.draw(dot))
            dot_prev = heptadecagon_points[j_prev]
            circle = self.get_oriented_circle(dot, dot_prev, z_index=A.z_index-1)
            self.play(self.draw(circle))
            circles.append(circle)
        
        # for completeness I'm drawing the last circle
        dot = heptadecagon_points[0]
        dot_prev = heptadecagon_points[15]
        circle = self.get_oriented_circle(dot, dot_prev, z_index=A.z_index-1)
        self.play(self.draw(circle))
        circles.append(circle)

        self.wait(1.5)
        self.remove_objects(*circles)

        # finally, we just connect all of the lines
        heptadecagon_sides = []
        for i in range(17):
            d1, d2 = heptadecagon_points[i], heptadecagon_points[(i+1)%17]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=A.z_index-1)
            self.play(self.draw(side))
            heptadecagon_sides.append(side)
        
        self.wait()
        self.remove_objects(S, T, *heptadecagon_points, *self.background_objects)
        self.wait(2)
        self.remove_objects(*heptadecagon_sides)
        self.wait()
