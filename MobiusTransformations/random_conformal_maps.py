from mobius_transformation import MobiusTransformation
from conformal_map_scenes import ConformalMapScenes

class UnitDisc2HalfPlane(ConformalMapScenes):
    
    def construct(self):
        T = MobiusTransformation(1, complex(0, -1), 1, complex(0, 1)).inverse()
        arcs, rays = self.get_polar_net(
            arc_num=50, 
            radius=1, 
            ray_num=50
        )
        self.create_and_animate_net(arcs + rays, T)

class HalfPlane2UnitDisc(ConformalMapScenes):
    
    def construct(self):
        T = MobiusTransformation(1, complex(0, -1), 1, complex(0, 1))

        arcs, rays = self.get_polar_net(
            start_radius=0, radius=50, num_arc=100, 
            angle=PI, num_ray=20
        )
        self.create_and_animate_net(arcs + rays, T)
    
class HalfDisc2Disc(ConformalMapScenes):
    
    def construct(self):
        T = lambda z: z**2

        arcs, rays = self.get_polar_net(
            start_radius=0, radius=5, num_arc=10,
            angle=PI, num_ray=10,
        )
        self.create_and_animate_net(arcs + rays, T)

class Disc2HalfDisc(ConformalMapScenes):
    
    def construct(self):
        T = lambda z: complex(0, 1) * z**0.5

        arcs, rays = self.get_polar_net(
            start_radius=0, radius=5, num_arc=10,
            angle=2*PI, num_ray=10,
        )
        self.create_and_animate_net(arcs + rays, T)


class LineSegment2Disc(ConformalMapScenes):
    
    # Doesn't really work probably for numerical stability reasons

    def construct(self):
        T = lambda z: 1_000_000 if z == 0 else (z + 1/z)/2

        arcs, rays = self.get_polar_net(
            start_radius=0, radius=5, num_arc=10,
            angle=2*PI, num_ray=10,
        )
        self.create_and_animate_net(arcs + rays, T)
