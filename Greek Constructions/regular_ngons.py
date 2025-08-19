from manim import *
from greek_construction_scene import GreekConstructionScene

class EquilateralTriangle(GreekConstructionScene):
    def construct(self):
        # the given line
        A = Dot([-1, 0, 0], color=self.default_color)
        B = Dot([1, 0, 0], color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB)

        # left circle
        circle_AB = self.get_oriented_circle(A.get_center(), B.get_center(), z_index=A.z_index-1)
        self.play(self.draw(A))
        self.play(self.draw(circle_AB))
        
        # right circle
        circle_BA = self.get_oriented_circle(B.get_center(), A.get_center(), z_index=A.z_index-1)
        self.play(self.draw(B))
        self.play(self.draw(circle_BA))

        # where the circles intersect
        C = Dot([0, np.sqrt(3), 0], color=self.default_color)
        self.play(self.draw(C))

        # drawing sides of triangle
        triangle_points = [A, C, B]
        triangle_sides = []
        for i in range(len(triangle_points)):
            d1 = triangle_points[i]
            d2 = triangle_points[(i+1)%len(triangle_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=A.z_index-1)
            triangle_sides.append(side)
            self.play(self.draw(side))

        self.wait()
        self.remove_objects(A, B, C, circle_AB, circle_BA)
        self.wait()
        self.remove_objects(*triangle_sides)
        self.wait()


class Square(GreekConstructionScene):
    def construct(self):
        # the given line
        A = Dot([-1, 0, 0], color=self.default_color)
        B = Dot([1, 0, 0], color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB)

        # double the line
        circle_AB = self.get_oriented_circle(A, B, color=self.default_color)
        self.play(self.draw(A))
        self.play(self.draw(B))
        self.play(self.draw(circle_AB))
        
        # extend the line
        C = Dot([-3, 0, 0], color=self.default_color)
        line_AC = Line(A.get_center(), C.get_center(), color=self.default_color)
        self.play(self.draw(line_AC))

        # bisecting extended line
        self.play(self.draw(C))
        line_CB = Line(C.get_center(), B.get_center(), color=self.default_color)
        solution, background = self.bisect_segment(line_CB, draw_endpoints=False)
        
        # draw intersection from the bisector and circle_AB
        D = Dot([-1, 2, 0], color=self.default_color)
        self.play(self.draw(D))

        E, F, line_EF, _ = solution
        _, _, circle1, circle2 = background
        self.make_background_object(C, E, F, line_AC, line_EF, circle_AB, circle1, circle2)

        # getting last vertex
        circle_DA = self.get_oriented_circle(D, A, color=self.default_color)
        circle_BA = self.get_oriented_circle(B, A, color=self.default_color)
        self.play(self.draw(circle_DA))
        self.play(self.draw(circle_BA))

        G = Dot([1, 2, 0], color=self.default_color)
        self.play(self.draw(G))

        self.make_background_object(circle_DA, circle_BA)

        # drawing square
        square_points = [A, D, G, B]
        square_sides = []
        for i in range(len(square_points)):
            d1 = square_points[i]
            d2 = square_points[(i+1)%len(square_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=A.z_index-1)
            square_sides.append(side)
            self.play(self.draw(side))

        self.wait()
        self.remove_objects(*self.background_objects, *square_points)
        self.wait()
        self.remove_objects(*square_sides)
        self.wait()


class Pentagon(GreekConstructionScene):
    def construct(self):
        # the given line
        A = Dot([-1, -1, 0], color=self.default_color)
        B = Dot([1, -1, 0], color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB)

        solution, background = self.bisect_segment(line_AB)
        C, D, line_CD, _ = solution
        A, B, circle_AB, circle_BA = background

        # draw circle below
        circle_D = self.get_oriented_circle(D, A)
        self.play(self.draw(circle_D))

        # draw the intersection of circle_D and line_CD
        E = Dot(D.get_center() + [0, 2, 0], color=self.default_color)
        self.play(self.draw(E))

        # drawing intersection of the three circles
        F = Dot(D.get_center() + [-2, 0, 0], color=self.default_color)
        H = Dot(D.get_center() + [2, 0, 0], color=self.default_color)
        self.play(self.draw(F))
        self.play(self.draw(H))

        # drawing crossing lines
        c1, c2 = self.extended_coordinates(F, E, 0, 3)
        G = Dot(c2, color=self.default_color)
        line_FG = Line(c1, c2, color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_FG))

        c1, c2 = self.extended_coordinates(H, E, 0, 3)
        I = Dot(c2, color=self.default_color)
        line_HI = Line(c1, c2, color=self.default_color, z_index=A.z_index-1)
        self.play(self.draw(line_HI))

        # getting intersection of the crossing lines and the circles
        J = Dot([2*np.cos(3*PI/5)-1, 2*np.sin(3*PI/5)-1, 0], color=self.default_color)
        L = Dot([2*np.cos(2*PI/5)+1, 2*np.sin(2*PI/5)-1, 0], color=self.default_color)
        self.play(self.draw(J))
        self.play(self.draw(L))

        # putting all unnecessary objects in background
        self.make_background_object(C, D, E, F, H, line_CD, line_FG, line_HI, circle_AB, circle_BA, circle_D)

        # getting final pentagon point
        circle_JA = self.get_oriented_circle(J, A)
        circle_LB = self.get_oriented_circle(L, B)
        self.play(self.draw(circle_JA))
        self.play(self.draw(circle_LB))

        height = np.sqrt(5 + 2*np.sqrt(5))
        M = Dot([0, height-1, 0], color=self.default_color)
        self.play(self.draw(M))

        # drawing pentagon
        self.make_background_object(circle_JA, circle_LB)
        pentagon_points = [A, J, M, L, B]
        pentagon_sides = []
        for i in range(len(pentagon_points)):
            d1 = pentagon_points[i]
            d2 = pentagon_points[(i+1)%len(pentagon_points)]
            side = Line(d1.get_center(), d2.get_center(), color=self.solution_color, z_index=A.z_index-1)
            pentagon_sides.append(side)
            self.play(self.draw(side))

        self.wait()
        self.remove_objects(*self.background_objects, *pentagon_points)
        self.wait()
        self.remove_objects(*pentagon_sides)
        self.wait()


class Hexagon(GreekConstructionScene):
    def construct(self):
        # the given line
        A = Dot([-1, -1, 0], color=self.default_color)
        B = Dot([1, -1, 0], color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB)

        # left circle
        circle_AB = self.get_oriented_circle(A, B, z_index=A.z_index-1)
        self.play(self.draw(A))
        self.play(self.draw(circle_AB))
        
        # right circle
        circle_BA = self.get_oriented_circle(B, A, z_index=A.z_index-1)
        self.play(self.draw(B))
        self.play(self.draw(circle_BA))

        # where the circles intersect
        C = Dot([0, np.sqrt(3)-1, 0], color=self.default_color)
        self.play(self.draw(C))

        circle_CA = self.get_oriented_circle(C, A, z_index=A.z_index-1)
        self.play(self.draw(circle_CA))

        D = Dot([-2, np.sqrt(3)-1, 0], color=self.default_color)
        E = Dot([2, np.sqrt(3)-1, 0], color=self.default_color)
        self.play(self.draw(D))
        self.play(self.draw(E))

        circle_DC = self.get_oriented_circle(D, C, z_index=A.z_index-1)
        circle_EC = self.get_oriented_circle(E, C, z_index=A.z_index-1)
        self.play(self.draw(circle_DC))
        self.play(self.draw(circle_EC))

        F = Dot([-1, 2*np.sqrt(3)-1, 0], color=self.default_color)
        G = Dot([1, 2*np.sqrt(3)-1, 0], color=self.default_color)
        self.play(self.draw(F))
        self.play(self.draw(G))
        
        self.wait()
        self.make_background_object(C, circle_AB, circle_BA, circle_CA, circle_DC, circle_EC)
        self.wait()

        # drawing hexagon
        hexagon_points = [A, D, F, G, E, B]
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
        # the given line
        A = Dot([-1, -1, 0], color=self.default_color)
        B = Dot([1, -1, 0], color=self.default_color)
        line_AB = Line(A.get_center(), B.get_center(), color=self.given_color, z_index=A.z_index-1)
        self.add(line_AB)