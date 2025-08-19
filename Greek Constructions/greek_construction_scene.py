from manim import *
from config import *
import numpy as np

class GreekConstructionScene(Scene):
    
    """ Most of the init is the color scheme
        Note, there is also a config.py file which mostly is choosing a color palet """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.isBackgroundColor(BLACK):
            self.default_color = WHITE
            self.text_color = WHITE
            self.given_color = BLUE
            self.solution_color = "#FFC200"     # a bright orange
            self.background_object_color = rgb_to_color([0.2, 0.2, 0.2]).get_hex()       # a grey color
        
        elif self.isBackgroundColor(WHITE):  
            self.default_color = rgb_to_color([0.5, 0.5, 0.5]).get_hex()
            self.text_color = BLACK
            self.given_color = BLACK
            self.solution_color = ORANGE
            self.background_object_color = rgb_to_color([0.7, 0.7, 0.7]).get_hex()       # a grey color

        else:   # background is the warm tan color
            self.default_color = BLACK
            self.text_color = BLACK
            self.given_color = rgb_to_color([0.5, 0.5, 0.5]).get_hex()
            self.solution_color = ORANGE
            self.background_object_color = WHITE


        self.background_objects = []

        self.compass_color = rgb_to_color([0.5, 0.5, 0.5])
        self.straight_edge_color = GREY_BROWN
    
    """ Miscellaneous static functions """
    @staticmethod
    def isBackgroundColor(hex_color):
        return all(config["background_color"].get_rgb() == color_to_rgb(hex_color))
    
    @staticmethod
    def to_coordinate(obj):
        if isinstance(obj, Mobject):
            return obj.get_center()
        elif isinstance(obj, list):
            return np.array(obj)
        elif isinstance(obj, np.ndarray):
            return obj
        else:
            raise TypeError(f"Recieved an unknown type: {type(obj)} from object: {obj}")

    @staticmethod
    def draw(obj):
        if isinstance(obj, Dot):
            return GrowFromCenter(obj)
        elif isinstance(obj, Circle):
            return GrowFromCenter(obj)
        elif isinstance(obj, Line):
            return Create(obj)

    # FIXME: I don't think this really gets used
    @staticmethod
    def get_n_gon_coordinates(self, n, center, start):
        center, start = self.to_coordinate(center), self.to_coordinate(start)

        vector = c2 - c1
        radius = np.linalg.norm(vector)
        start_angle = np.arctan2(vector[1], vector[0])#Line(c1, c2, color=self.default_color).get_angle()
        diff_angle = 2*PI/n
        n_gon_coords = [ center + [radius * np.cos(start_angle - i*diff_theta), radius * np.sin(start_angle - i*diff_angle), 0] for i in range(n) ]
        return n_gon_coords

    """ Helpful bookkeeping functions to make animiations less busy """
    def make_background_object(self, *args):
        # change color of each object
        animate = []
        for obj in args:
            animate.append(FadeToColor(obj, self.background_object_color))
            self.background_objects.append(obj)
        self.play(*animate)

        # move it to background layer
        animate = []
        for obj in args:
            obj.set_z_index(-1000)                       # This whole thing is really weird but it's the only way I could figure out to get the desired effect
            new_obj = obj.copy()                        # which is to move this object into the background layer
            animate.append( Transform(obj, new_obj) )
            self.background_objects.append(new_obj)     # obj doesn't exist in the scene anymore, only the copy new_obj
        self.play(*animate)
    
    def remove_objects(self, *args):
        if len(args) == 0:
            args = self.background_objects
        
        animate = []
        for obj in args:
            animate.append(FadeOut(obj))
        self.play(*animate)


    """ Create and manipulate the straight-edge and compass assets """
    def create_compass(self):
        
        # construct hinge
        r1, r2 = 0.25, 0.5
        annulus = Annulus(inner_radius=r1, outer_radius=r2, color=self.compass_color, stroke_width=2)
        circle1 = Circle(radius=r1, color=self.text_color, stroke_width=2)
        circle2 = Circle(radius=r2, color=self.text_color, stroke_width=2)
        handle = RoundedRectangle(corner_radius=0.1, height=0.5, width=0.3, color=self.default_color, fill_color=rgb_to_color([0.2, 0.2, 0.2]), fill_opacity=1, stroke_width=2)
        handle.move_to(annulus.get_top() + [0, 0.1, 0])
        hinge = VGroup(annulus, circle1, circle2, handle)
        
        # putting things in the correct order
        hinge.set_z_index(1000)
        handle.set_z_index(annulus.z_index-1)
        
        # construct arm with pencil
        holder = Polygon(*[
            [0, 0, 0],          # top left
            [0.3, 0, 0],        # top right
            [0.3, -1.75, 0],    # bottom right
            [0, -1.75, 0]       # bottom left
        ], color=self.text_color, fill_color=self.compass_color, fill_opacity=1, stroke_width=2, z_index=hinge.z_index-1)

        pencil_img = ImageMobject("pencil.png")
        pencil_img.set_z_index(holder.z_index-1)
        pencil_img.width = 1.6
        pencil_img.rotate(45*DEGREES)
        pencil_img.move_to(holder.get_bottom() + [-0.56, 0.35, 0])

        pencil_outline = Polygon(*[
            [0, -1.75, 0],      # top left
            [0.3, -1.75, 0],    # top right
            [0.3, -2.2, 0],     # bottom right
            [0.15, -2.5, 0],    # tip
            [0, -2.2, 0]        # bottom left
        ], color=self.text_color, stroke_width=2, z_index=hinge.z_index-1)
        
        arm = Group(holder, pencil_img, pencil_outline)
        arm.move_to(annulus.get_bottom() + arm.get_center() - [0.15, -0.1, 0])

        # construct needle
        needle = Polygon(*[
            [0, 0, 0],          # top left
            [0.3, 0, 0],        # top right
            [0.3, -2, 0],       # bottom right
            [0.15, -2.5, 0],    # tip
            [0, -2, 0]          # bottom left
        ], color=self.text_color, fill_color=self.compass_color, fill_opacity=1, stroke_width=2, z_index=pencil_img.z_index-1)
        needle.move_to(hinge.get_bottom() + [0, needle.get_center()[1] + 0.1, 0])

        # This is needed to easily move the compass
        hinge_angle = ValueTracker(-90*DEGREES)
        leg_angle = ValueTracker(0)

        # group into the compass
        compass = Group(hinge, arm, needle, hinge_angle, leg_angle)
        return compass

    def create_straight_edge(self):
        straight_edge_color = "#B58A00"
        straight_edge = Rectangle(
                            width=8, height=1.25, 
                            color=self.default_color, 
                            fill_color=(LIGHT_BROWN, DARK_BROWN), fill_opacity=1, sheen_direction=np.array([0, -1, 0])
                        )

        straight_edge.set_z_index(1000)
        straight_edge.drawing_angle = 0
        return straight_edge


    """ All these are helper functions for `position_compass()` """
    @staticmethod
    def minimize_angle(theta, range=(-PI, PI)):
        a, b = range
        return ((theta+b)%(b-a))+a
        
    def compass_move_to(self, compass, destination, animate=False, **kwargs):
        hinge, arm, needle, *_ = compass
        annulus, *_ = hinge
        holder, pencil_img, pencil_outline = arm
        center = annulus.get_center()

        destination = np.array(destination)
        if np.all((destination - center) == 0):
            return
        
        if animate:
            self.play(*[
                obj.animate.shift(destination - center) for obj in [hinge, needle, holder, pencil_img, pencil_outline]
            ], **kwargs)
        else:
            for obj in [hinge, needle, holder, pencil_img, pencil_outline]:
                obj.shift(destination - center)
        
    def compass_rotate(self, compass, angle, animate=False, **kwargs):
        if angle == 0:
            return
        
        hinge, arm, needle, hinge_angle, _ = compass
        annulus, *_ = hinge
        holder, pencil_img, pencil_outline = arm
        center = annulus.get_center()
        
        if animate:
            self.play(*[
                Rotating(
                    obj, radians=angle, about_point=center
                ) for obj in [hinge, needle, holder, pencil_img, pencil_outline]
            ], **kwargs)
        else:
            for obj in [hinge, needle, holder, pencil_img, pencil_outline]:
                obj.rotate(angle, about_point=center)
        
        hinge_angle.set_value(self.minimize_angle(hinge_angle.get_value() + angle))

    def compass_open(self, compass, angle, animate=False, **kwargs):
        if angle == 0:
            return
        
        hinge, arm, needle, _, leg_angle = compass
        annulus, *_ = hinge
        holder, pencil_img, pencil_outline = arm
        center = annulus.get_center()

        if animate:
            self.play(*[
                Rotating(needle, radians=-angle, about_point=center), 
                Rotating(holder, radians= angle, about_point=center), 
                Rotating(pencil_img, radians= angle, about_point=center),
                Rotating(pencil_outline, radians= angle, about_point=center)
            ], **kwargs)
        else:
            needle.rotate(-angle, about_point=center)
            holder.rotate( angle, about_point=center)
            pencil_img.rotate( angle, about_point=center)
            pencil_outline.rotate( angle, about_point=center)

        leg_angle.set_value(self.minimize_angle(leg_angle.get_value() + angle))

    """ The needle goes to c1 and the pencil does to c2 """
    def position_compass(self, compass, c1, c2, animate=True, **kwargs):
        hinge, arm, needle, hinge_angle, leg_angle = compass
        annulus, inner_outline, outer_outline, handle = hinge
        holder, pencil_img, pencil_outline = arm

        # need these to be numpy arrays
        c1, c2 = self.to_coordinate(c1), self.to_coordinate(c2)

        # from `create_compass()`, we can see the radius of the hinge is 0.5 units 
        # and the length of the needle is 2.5 units, which gives the total leg length as 3 units
        # we add a small buffer so we can see the thing we are drawing
        length = 3 + SMALL_BUFF/2
        vector = c2 - c1
        width = np.linalg.norm(vector)
        normal_vector = np.array([vector[1], -vector[0], 0])
        midpoint = (c2 + c1)/2
        
        # 1) we rotate the compass in the correct direction
        destination_angle = np.arctan2(normal_vector[1], normal_vector[0])
        diff_angle = self.minimize_angle(destination_angle - hinge_angle.get_value())
        self.compass_rotate(compass, diff_angle, animate=animate, **kwargs)

        # 2) we move the compass to the correct location
        height = np.sqrt(length**2 - (width/2)**2)
        destination = midpoint - (normal_vector / width) * height
        self.compass_move_to(compass, destination, animate=animate, **kwargs)

        # 3) open compass to correct position
        open_angle = np.arcsin(width/length/2)
        diff_angle = self.minimize_angle(open_angle - leg_angle.get_value())
        self.compass_open(compass, diff_angle, animate=animate, **kwargs)

    def draw_circle_with_compass(self, compass, c1, c2, color=None, z_index=None, **kwargs):
        if color is None:
            color = self.default_color
        
        # we first position the compass
        c1, c2 = self.to_coordinate(c1), self.to_coordinate(c2)
        self.position_compass(compass, c1, c2, animate=True, **kwargs)

        self.wait(0.5)

        # Then we rotate it
        hinge, arm, needle, hinge_angle, leg_angle = compass
        holder, pencil_img, pencil_outline = arm
        animations = [
            Rotating(
                obj,
                radians=TAU,
                about_point=c1
            ) for obj in [hinge, needle, holder, pencil_img, pencil_outline]
        ]

        # drawing corresponding circle
        r = np.linalg.norm(c2-c1)
        circle = Circle(radius=r, color=color)
        temp_line = Line(c2, c1)
        circle.move_to(c1).rotate(temp_line.get_angle() + 180*DEGREES)
        if z_index is not None:
            circle.set_z_index(z_index)
        animations.append(Create(circle))

        # playing animations
        self.play(*animations, run_time=2, rate_func=rate_functions.linear)
        return circle

    def position_straight_edge(self, straight_edge, c1, c2):
        c1, c2 = self.to_coordinate(c1), self.to_coordinate(c2)

        vector = c2 - c1
        midpoint = (c2 + c1)/2
        width = np.linalg.norm(vector)
        unit_normal_vector = np.array([-vector[1], vector[0], 0])/width

        # rotating
        destination_angle = np.arctan2(vector[1], vector[0])
        self.play(Rotating(straight_edge, radians=destination_angle - straight_edge.drawing_angle), run_time=1)
        straight_edge.drawing_angle = destination_angle
        straight_edge.sheen_direction = unit_normal_vector
        
        # positioning
        destination = midpoint - (1.25/2 + SMALL_BUFF) * unit_normal_vector
        self.play(straight_edge.animate.move_to(destination))

    def draw_segment_with_straight_edge(self, straight_edge, c1, c2, color=None):
        if color is None:
            color = self.default_color
        
        c1, c2 = self.to_coordinate(c1), self.to_coordinate(c2)
        self.position_straight_edge(straight_edge, c1, c2)
        line = Line(c1, c2, color=color)
        self.play(Create(line))
        return line
    

    """ Animations for things that occur often in greek constructions """
    def extended_coordinates(self, c1, c2, length1, length2):
        # This method draws a line through coordinates c1 and c2, and extend past c1 and c2 by length1 and length2
        c1, c2 = self.to_coordinate(c1), self.to_coordinate(c2)
        vector = c2 - c1
        unit_vector = vector / np.linalg.norm(vector)
        new_c1 = c1 - length1 * unit_vector
        new_c2 = c2 + length2 * unit_vector
        return new_c1, new_c2

    def get_oriented_circle(self, center, start_point, color=None, z_index=None):
        if color is None:
            color = self.default_color

        # we create this temporary line so we can use its methods
        center, start_point = self.to_coordinate(center), self.to_coordinate(start_point)
        line = Line(center, start_point)

        # create circle
        radius = np.linalg.norm(line.get_vector())
        circle = Circle(radius=radius, color=color)
        if z_index is not None:
            circle.set_z_index(z_index)
        
        # center
        circle.move_to(center)

        # rotate so the animation starts at the start point
        angle = self.minimize_angle(line.get_angle(), (0, 2*PI))
        if PI/2 <= angle <= 3*PI/2:         # TODO: maybe change this behavior, idk
            circle.flip(RIGHT)
        circle.rotate(angle)

        return circle

    # TODO: This is somewhat complicated
    def translate_segment(self, line, start, solution_color=None, draw_solution=True):
        if solution_color is None:
            solution_color = self.default_color

        A = Dot(line.start, color=self.default_color)
        B = Dot(line.end, color=self.default_color)
        C = start

        line_AC = Line(A.get_center(), C.get_center(), color=self.defailt_color, z_index=start.z_index-1)
        self.play(self.draw(line_AC))

        circle_AC = self.get_oriented_circle(A, C, z_index=start.z_index-1)
        circle_CA = self.get_oriented_circle(C, A, z_index=start.z_index-1)
        self.play(self.draw(circle_AC))
        self.play(self.draw(circle_CA))

        D = Dot([])

        self.play(self.draw(A))
        self.play(self.draw(B))

        circle = self.get_oriented_circle(line.start, line.end, z_index=start.z_index-1)
        self.play(self.draw(circle))

        radius = np.linalg.norm( B.get_center() - A.get_center() )
        """
        theta = 
        a = Line(A.get_center(), )

        b = Line(A.get_center(), start.get_center(), color=self.default_color, z_index=start.z_index-1)
        self.play(self.draw(b)) 
        """

    # TODO: This is just copying 2 segments
    def translate_angle(self, line1, line2, solution_color=None, draw_solution=True):
        if solution_color is None:
            solution_color = self.default_color
        
        if np.any( line1.start != line2.start ):
            raise ValueError("The lines need to connect at a single point")

        raise NotImplementedError()

        self.copy_segment(line1, solution_color=solution_color, draw_solution=draw_solution)
        self.copy_segment(line2, solution_color=solution_color, draw_solution=draw_solution)

    def double_segment(self, line, solution_color=None, draw_solution=True):
        if solution_color is None:
            solution_color = self.default_color
        
        # given points
        c1, c2 = line.start, line.end
        A = Dot(c1, color=self.default_color)
        B = Dot(c2, color=self.default_color)
        
        # create circle to double the line segment
        self.play(self.draw(B))
        
        circle_BA = self.get_oriented_circle(c2, c1, z_index=line.z_index)
        self.play(self.draw(circle_BA))

        # animate extending the line
        destination = 2*(c2 - c1) + c1
        C = Dot(destination, color=self.default_color)
        line_BC = Line(c2, destination, color=solution_color, z_index=B.z_index-1)
        if draw_solution:
            self.play(self.draw(line_BC))

        solution = (C, line_BC)
        background = (B, circle_BA)
        return solution, background
    
    def double_angle(self, line1, line2, solution_color=None, draw_solution=True):
        if solution_color is None:
            solution_color = self.default_color
        
        # making sure the two lines form an angle
        if np.any( line1.start != line2.start ):
            raise ValueError("The lines need to connect at a single point")

        # we need the circle to intersect both lines, so we take the minimum of the midpoints of each
        mid1, mid2 = line1.get_vector()/2, line2.get_vector()/2
        radius = min( np.linalg.norm(mid1), np.linalg.norm(mid2) )
        
        # draw circle (whose radius is arbitrary, I chose the midpoint)
        A = Dot(line1.start, color=self.default_color)
        self.play(self.draw(A))
        circle_A = Circle(radius=radius, color=self.default_color).move_to(A.get_center())
        self.play(self.draw(circle_A))

        # drawing intersections
        theta1 = line1.get_angle()
        B = Dot([radius*np.cos(theta1), radius*np.sin(theta1), 0] + A.get_center(), color=self.default_color)
        self.play(self.draw(B))

        theta2 = line2.get_angle()
        C = Dot([radius*np.cos(theta2), radius*np.sin(theta2), 0] + A.get_center(), color=self.default_color)
        self.play(self.draw(C))

        # draw circle to double line
        circle_CB = self.get_oriented_circle(C, B)
        self.play(self.draw(circle_CB))

        new_theta = self.minimize_angle( 2*(theta2 - theta1) + theta1 )
        D = Dot([radius*np.cos(new_theta), radius*np.sin(new_theta), 0] + A.get_center(), color=self.default_color)
        self.play(self.draw(D))

        # we extend the bisector a bit
        c1, c2 = self.extended_coordinates(A, D, 0, 1)
        E = Dot(c2, color=self.default_color)

        # drawing solution
        line_AD = Line(A.get_center(), D.get_center(), color=solution_color, z_index=A.z_index-1)
        line_AE = Line(A.get_center(), E.get_center(), color=solution_color, z_index=A.z_index-1)
        if draw_solution:
            self.play(self.draw(line_AE))
        
        # returning solution and background objects
        solution = (line_AD, line_AE)
        background = (A, B, C, D, circle_A, circle_CB)
        return solution, background

    def bisect_segment(self, line_AB, solution_color=None, draw_solution=True, draw_endpoints=True, draw_midpoint=False):
        if solution_color is None:
            solution_color = self.default_color
        
        # given points
        c1, c2 = line_AB.start, line_AB.end
        A, B = Dot(c1, color=self.default_color), Dot(c2, color=self.default_color)
        
        # we need some of this info for our calculations
        length = np.linalg.norm(c2-c1)
        normal_direction = line_AB.get_angle() + 90*DEGREES
        unit_normal = np.array([np.cos(normal_direction), np.sin(normal_direction), 0])
        midpoint_coord = (c1 + c2)/2

        # left circle
        circle_AB = self.get_oriented_circle(A, B, z_index=A.z_index-1)
        if draw_endpoints:
            self.play(self.draw(A))
        self.play(self.draw(circle_AB))
        
        # right circle
        circle_BA = self.get_oriented_circle(B, A, z_index=A.z_index-1)
        if draw_endpoints:
            self.play(self.draw(B))
        self.play(self.draw(circle_BA))
        
        # now we have to calculate the intersection points
        # we do this sorta backwards to what the construction is doing
        u_cord = midpoint_coord + (length * np.sqrt(3)/2)*unit_normal
        b_cord = midpoint_coord - (length * np.sqrt(3)/2)*unit_normal
        C = Dot(u_cord, color=self.default_color)
        D = Dot(b_cord, color=self.default_color)
        
        # drawing the perpendicular bisector
        line_CD = Line(C.get_center(), D.get_center(), color=solution_color, z_index=C.z_index-1)
        M = Dot(midpoint_coord, color=solution_color)
        if draw_solution:
            self.play(self.draw(C))
            self.play(self.draw(D))
            self.play(self.draw(line_CD))
        if draw_midpoint:
            self.play(self.draw(M))

        solution = (C, D, line_CD, M)
        background = (A, B, circle_AB, circle_BA)
        return solution, background

    def bisect_angle(self, line1, line2, solution_color=None, draw_solution=True):
        if solution_color is None:
            solution_color = self.default_color
        
        # making sure the two lines form an angle
        if np.any( line1.start != line2.start ):
            raise ValueError("The lines need to connect at a single point")
        
        # we need the circle to intersect both lines, so we take the minimum of the midpoints of each
        mid1, mid2 = line1.get_vector()/2, line2.get_vector()/2
        radius = min( np.linalg.norm(mid1), np.linalg.norm(mid2) )
        
        # draw circle (whose radius is arbitrary, I chose the midpoint)
        A = Dot(line1.start, color=self.default_color)
        self.play(self.draw(A))
        circle_A = Circle(radius=radius, color=self.default_color).move_to(A.get_center())
        self.play(self.draw(circle_A))

        # drawing intersections
        theta1 = line1.get_angle()
        B = Dot([radius*np.cos(theta1), radius*np.sin(theta1), 0] + A.get_center(), color=self.default_color)
        self.play(self.draw(B))

        theta2 = line2.get_angle()
        C = Dot([radius*np.cos(theta2), radius*np.sin(theta2), 0] + A.get_center(), color=self.default_color)
        self.play(self.draw(C))

        # bisecting the two points
        line_BC = Line(B.get_center(), C.get_center(), color=self.default_color, z_index=B.z_index-1)
        solution, background = self.bisect_segment(line_BC, draw_solution=False, draw_endpoints=False)

        D, E, *_ = solution
        #self.play(self.draw(D))        # unnecessary to draw this point
        self.play(self.draw(E))

        # we extend the bisector a bit
        c1, c2 = self.extended_coordinates(A, E, 0, 1)
        F = Dot(c2, color=self.default_color)

        # drawing solution
        line_AE = Line(A.get_center(), E.get_center(), color=solution_color, z_index=A.z_index-1)
        line_AF = Line(A.get_center(), F.get_center(), color=solution_color, z_index=A.z_index-1)
        if draw_solution:
            self.play(self.draw(line_AF))
        
        # returning solution and background objects
        _, _, circle1, circle2 = background
        solution = (line_AE, line_AF)
        background = (A, B, C, D, E, circle_A, circle1, circle2)
        return solution, background
    
    # TODO: is this even worth?
    def drop_perpendicular(self, line, dot, solution_color=None, draw_solution=True):
        if solution_color is None:
            solution_color = self.default_color
        
        # the givens
        A, B = Dot(line.start, color=self.default_color), Dot(line.end, color=self.default_color)
        line_AB = line
        C = dot
    
    # TODO: is this even worth?
    def raise_perpendicular(self, line, dot, solution_color=None, draw_solution=True):
        if solution_color is None:
            solution_color = self.default_color

        # the givens
        A, B = Dot(line.start, color=self.default_color), Dot(line.end, color=self.default_color)
        line_AB = line
        C = dot

        # TODO: check if C is on line_AB



""" Class to test above functions while I create them """
class Tester(GreekConstructionScene):
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
        C = Dot([0, np.sqrt(3), 0], color=ORANGE)
        D = Dot([0, -np.sqrt(3), 0], color=ORANGE)
        self.play(self.draw(C))
        self.play(self.draw(D))


""" Demos to display behavior of above functions """
class CompassDemo(GreekConstructionScene):
    def construct(self):
        d1 = Dot([0, 1, 0], color=ORANGE)
        d2 = Dot([1, 0, 0], color=RED)
        d3 = Dot([-2, -2, 0], color=BLUE)
        self.add(d1, d2, d3)

        compass = self.create_compass()
        self.add(compass)

        self.draw_circle_with_compass(compass, d1.get_center(), d2.get_center(), z_index=d1.z_index-1, run_time=1)
        self.draw_circle_with_compass(compass, d2.get_center(), d3.get_center(), z_index=d1.z_index-1, run_time=1)
        self.draw_circle_with_compass(compass, d3.get_center(), d1.get_center(), z_index=d1.z_index-1, run_time=1)

        self.wait()

class CopySegmentDemo(GreekConstructionScene):
    def construct(self):
        line = Line([0, -0.5, 0], [-3, 0, 0], color=self.given_color)
        dot = Dot([1, 1, 0], color=self.given_color)
        self.add(line, dot)
        self.wait()
        self.copy_segment(line, dot, solution_color=self.solution_color)
        self.wait()

class DoubleSegmentDemo(GreekConstructionScene):
    def construct(self):
        dot1 = Dot([-1, -1, 0], color=BLUE)
        dot2 = Dot([1, 0, 0])
        line = Line(dot1.get_center(), dot2.get_center(), z_index=dot1.z_index-1)
        self.add(dot1, line)
        self.wait()
        self.double_segment(line)
        self.wait()

class DoubleAngleDemo(GreekConstructionScene):
    def construct(self):
        #line1 = Line([-2, 0, 0], [1, -3, 0], color=self.given_color)
        #line2 = Line([-2, 0, 0], [3, 2, 0], color=self.given_color)
        line1 = Line([2, 0, 0], [-1, 3, 0], color=self.given_color)
        line2 = Line([2, 0, 0], [-3, -2, 0], color=self.given_color)
        self.add(line1, line2)
        self.wait()
        solution, background = self.double_angle(line1, line2, solution_color=self.solution_color)
        self.wait()

        self.make_background_object(*background)

class BisectSegmentDemo(GreekConstructionScene):
    def construct(self):
        line = Line([-2, 0, 0], [1, 1, 0], color=self.given_color)
        #line = Line([0, 1, 0], [3, 0, 0], color=self.given_color)
        self.add(line)
        self.wait()
        solution, background = self.bisect_segment(line, solution_color=self.solution_color)
        self.wait()

class BisectAngleDemo(GreekConstructionScene):
    def construct(self):
        #line1 = Line([-2, 0, 0], [1, -3, 0], color=self.given_color)
        #line2 = Line([-2, 0, 0], [3, 2, 0], color=self.given_color)
        line1 = Line([2, 0, 0], [-1, 3, 0], color=self.given_color)
        line2 = Line([2, 0, 0], [-3, -2, 0], color=self.given_color)
        self.add(line1, line2)
        self.wait()
        solution, background = self.bisect_angle(line1, line2, solution_color=self.solution_color)
        self.wait()

        self.make_background_object(*background)

class DropPerpendicularDemo(GreekConstructionScene):
    def construct(self):
        line = Line([2, 0, 0], [-1, 3, 0], color=self.given_color)
        dot = Dot([-2, -1, 0], color=self.given_color)
        self.add(line, dot)

