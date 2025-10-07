import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from greek_constructions import GreekConstructionScenes

from manim import *
from utils import *

class BookNPropM(GreekConstructionScenes):

    title = "Book N Proposition M"
    description = """
        <Copy from Euclid's Elements>
    """

    def get_givens(self):
        raise NotImplementedError("TODO")
        A, label_A = self.get_dot_and_label("A", self.Ax.get_value() * RIGHT + self.Ay.get_value() * UP, DL)
        B, label_B = self.get_dot_and_label("B", self.Bx.get_value() * RIGHT + self.By.get_value() * UP, DR)
        givens = ()
        intermediaries = ()
        return givens, intermediaries

    def get_solution(self, *givens):
        raise NotImplementedError("TODO")
        intermediaries = ()
        solution = ()
        return intermediaries, solution

    def get_proof_spec(self):
        raise NotImplementedError("TODO")
    def get_footnotes(self):
        return []
    def get_proof_color_map(self):
        raise {}

    def construct(self):
        
        """ Value Trackers """
        self.Ax, self.Ay, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.5*LEFT)
        self.Bx, self.By, _ = get_value_tracker_of_point(self.RIGHT_CENTER + DOWN + 1.5*RIGHT)

        """ Variable Initialization """
        title, description = self.initialize_introduction()
        footnotes, first_footnote_animation, next_footnote_animations, last_footnote_animation = self.initialize_footnotes()
        proof_line_numbers, proof_lines = self.initialize_proof()

        givens, given_intermediaries, solution_intermediaries, solution = self.initialize_construction(add_updaters=False)
        self.add(*givens, *given_intermediaries)

        # self.add(*solution_intermediaries, *solution)
        # return

        # A, B, C = givens
        # D, E, F = given_intermediaries
        # G, H, I = solution_intermediaries
        # J, K, L = solution

        """ Animate Introduction """
        self.wait()

        self.custom_play(*Animate(title, description))
        self.wait(2)
        self.custom_play(*Unanimate(title, description))
        self.wait()
        
        """ Proof Initialization """
        proof_line_numbers, proof_lines = self.initialize_proof()
        self.play(Write(proof_line_numbers))
        self.wait()
        
        """ Start of animation """
        self.add(*solution_intermediaries, *solution)
        self.play(Write(proof_lines))