from manim import *
from greek_construction_scene import GreekConstructionScene
import numpy as np

class Rules(GreekConstructionScene):
    
    def construct(self):

        text = Text("Greek Geometry utilizes two tools", color=self.default_color)
        text1 = Text("Straight Edge", color=self.default_color)
        text2 = Text("Compass", color=self.default_color)

        self.play(Write(text))
        self.wait()
        self.play(Unwrite(text))


        straight_edge = self.create_straight_edge()
        straight_edge.move_to([-10, -10, 0])

        self.play(Write(text1))
        self.wait()
        self.position_straight_edge(straight_edge, [-4, 1, 0], [-2, -1, 0])
        self.play(Unwrite(text1))


        compass = self.create_compass()
        hinge, arm, needle, *_ = compass
        annulus, *_ = hinge
        holder, pencil = arm
        center = annulus.get_center()
        for obj in [hinge, needle, holder, pencil]:
            obj.shift(np.array([10, 10, 0]) - center) 
        self.add(compass)

        self.play(Write(text2))
        self.wait()
        self.position_compass(compass, [3, 2, 0], [4, 0, 0])
        self.play(Unwrite(text2))

        self.wait()