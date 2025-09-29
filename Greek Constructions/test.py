
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class Test(GreekConstructionScenes):

    def construct(self):

        # Create value trackers for A and B
        tracker_a = ValueTracker(0)
        tracker_b = ValueTracker(4)

        # Create points A and B
        A = Dot().move_to(LEFT * tracker_a.get_value())
        A.add_updater(lambda m: m.move_to(LEFT * tracker_a.get_value()))
        B = Dot().move_to(RIGHT * tracker_b.get_value())
        B.add_updater(lambda m: m.move_to(RIGHT * tracker_b.get_value()))

        # LineAB
        line_AB = Line(A.get_center(), B.get_center())
        line_AB.add_updater(lambda l: l.become(Line(A.get_center(), B.get_center())))

        # LineAC (this needs an updater because it depends on A)
        line_AC = Line(A.get_center(), LEFT * 3)  # Fixed offset from A
        line_AC.add_updater(lambda l: l.become(Line(A.get_center(), LEFT * 3)))

        # C depends on the midpoint of LineAB
        C = Dot(color=GREEN)
        C.add_updater(lambda m: m.move_to((A.get_center() + B.get_center()) / 2))  # Midpoint of A and B

        # Add everything to the scene
        self.add(A, B, line_AB, C, line_AC)

        # Animate the trackers to move A and B, which will update the lines and C automatically
        self.play(tracker_a.animate.set_value(2), tracker_b.animate.set_value(6))
        self.wait(1)

        # Move A and B to new positions
        self.play(tracker_a.animate.set_value(-3), tracker_b.animate.set_value(10))
        self.wait(1)