from manim import *
from utils import *

# https://manim-themes.readthedocs.io/en/latest/index.html
from manim_themes.manim_theme import apply_theme

class GreekConstructionScenes(Scene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()
        
        self.non_construction_mobjects = []
        self.mobjects_to_deemphasize = []

        self.GIVEN = "given"
        self.SOLUTION = "solution"
        self.INTERMEDIARY = "intermediary"
        self.ASSUMPTION = "assumption"
        self.CONTRADICTION = "constradition"
        
        self.draw_color = BLACK
        self.given_color = BLUE_D
        self.solution_color = RED_E
        self.assumption_color = ManimColor("#cc0000")
        self.contradiction_color = ManimColor("#cc0000")

        self.type_to_color_map = {
            self.GIVEN: self.given_color,
            self.SOLUTION: self.solution_color, 
            self.INTERMEDIARY: self.draw_color,
            self.ASSUMPTION: self.assumption_color,
            self.CONTRADICTION: self.contradiction_color
        }

        self.default_run_time = 0.75

        self.left_bg_z_index = 400
        self.given_z_index = 0
        self.solution_z_index = 10
        self.proof_z_index = 500

        self.line_z_index = 0
        self.circle_z_index = 0
        self.dot_z_index = 200
        self.angle_z_index = -2

        self.DOT_LABEL_SCALE = 0.5
        self.TITLE_SCALE = 0.8
        self.DESCRIPTION_SCALE = 0.5

        self.LEFT_CENTER = LEFT * (config.frame_width / 4)
        self.RIGHT_CENTER = RIGHT * (config.frame_width / 4)

        self._initialize_canvas()
    
    def setup(self):
        # Set the background color to a light beige
        theme = "Monokai Pro Light" # select a theme from https://iterm2colorschemes.com
        apply_theme(manim_scene=self, theme_name=theme, light_theme=True) # use the theme

    # """ Wrapper Methods """
    # def play(self, *args, run_time=None, **kwargs):
    #     if run_time is None:
    #         run_time = self.default_run_time
    #     super().play(*args, run_time=run_time, **kwargs)

    """ Initialize Stuff """
    def _initialize_canvas(self):
        LHS_bg = Rectangle(
            width=config.frame_width / 2,
            height=config.frame_height,
            fill_color=self.camera.background_color,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * (config.frame_width / 4)).set_z_index(self.left_bg_z_index-1)
        self.add(LHS_bg)
        self.non_construction_mobjects.append(LHS_bg)

        center_line = self.get_vertical_center_line()
        center_line.set_z_index(self.left_bg_z_index+1)
        self.add(center_line)
        self.non_construction_mobjects.append(center_line)

    def initialize_construction(self, add_updaters=False):
        givens, given_intermediaries, solution_intermediaries, solution = self._compute_construction()
        all_construction_mobjects = *givens, *given_intermediaries, *solution_intermediaries, *solution
        
        # Having every object constantly re-computing every other object is obviously not efficient at all
        # So we only want to enable this if we have to
        if add_updaters:
            for mob in all_construction_mobjects:
                mob.add_updater(lambda _, mob=mob: self._all_construction_mobject_updater(givens, given_intermediaries, solution_intermediaries, solution))

        return givens, given_intermediaries, solution_intermediaries, solution

    def initialize_introduction(self, title_text, description_text):
        description_text = description_text.replace("\t", "")
        title = Text(title_text).scale(self.TITLE_SCALE).set_z_index(self.proof_z_index)
        description = Text(description_text).scale(self.DESCRIPTION_SCALE).set_z_index(self.proof_z_index)
        description.next_to(title, 2*DOWN)

        title_and_description = VGroup(title, description)
        title_and_description.move_to([self.LEFT_CENTER[0], 0, 0])

        title, description = title_and_description
        return title, description

    def initialize_proof(self, scale=1):
        proof_spec = self.get_proof_spec()
        proof_color_map = self.get_proof_color_map()
        
        proof_spec = [(t[0], t[1], (t[2] if len(t) > 2 else None)) for t in proof_spec]
        proof_spec = [
            (
                statement, 
                justification, 
                self.type_to_color_map.get(line_type)
            ) for statement, justification, line_type in proof_spec
        ]
        proof = format_and_prepare_proof(proof_spec, proof_color_map, scale=scale)
        proof.to_edge(LEFT).set_z_index(self.proof_z_index)

        proof_line_numbers = VGroup([line_number for line_number, _, _ in proof])
        proof_lines = VGroup([VGroup(statement, justification) for _, statement, justification in proof])

        self.non_construction_mobjects.append(proof_line_numbers)
        for proof_line in proof_lines:
            self.non_construction_mobjects.append(proof_line)

        return proof_line_numbers, proof_lines

    def write_QED(self, position=None):
        QED_text = MathTex(r"\text{Q.E.D.}").scale(1.2).set_z_index(self.proof_z_index+3)
        QED_bg = BackgroundRectangle(QED_text, color=self.camera.background_color, fill_opacity=1, buff=0.1).set_z_index(self.proof_z_index+2)
        QED = VGroup(QED_text, QED_bg)
        if position is None:
            QED.to_edge(DOWN)
        else:
            QED.move_to(position)
        self.play(Write(QED_text), FadeIn(QED_bg))

    """ Abtract Methods """
    def get_proof_spec(self):
        raise NotImplementedError("'get_proof_spec' not implemented by child class.")
    def get_proof_color_map(self):
        raise NotImplementedError("'get_proof_color_map' not implemented by child class.")
    def get_givens(self):
        raise NotImplementedError("'get_givens' not implemented by child class.")
    def get_solution(self, *givens):
        raise NotImplementedError("'get_solution' not implemented by child class.")

    """Formatting Givens and Solutions"""
    def format_givens(self, *mobjects):
        for mob in mobjects:
            mob.set_color(self.given_color)
            mob.set_z_index(self.given_z_index)
            if isinstance(mob, Dot):
                mob.set_z_index(mob.z_index + self.dot_z_index)
            elif isinstance(mob, Circle):
                mob.set_z_index(mob.z_index + self.circle_z_index)
            elif isinstance(mob, Line):
                mob.set_z_index(mob.z_index + self.line_z_index)
            elif isinstance(mob, Angle):
                mob.set_z_index(self.angle_z_index)
            elif isinstance(mob, VGroup):
                for m in mob:
                    self.format_givens(m)
                mob.set_z_index(max([m.z_index for m in mob]))

    def format_solution(self, *mobjects):
        for mob in mobjects:
            mob.set_color(self.solution_color)
            mob.set_z_index(self.solution_z_index)
            if isinstance(mob, Dot):
                mob.set_z_index(mob.z_index + self.dot_z_index)
            elif isinstance(mob, Circle):
                mob.set_z_index(mob.z_index + self.circle_z_index)
            elif isinstance(mob, Line):
                mob.set_z_index(mob.z_index + self.line_z_index)
            elif isinstance(mob, Angle):
                mob.set_z_index(self.angle_z_index)
            elif isinstance(mob, VGroup):
                for m in mob:
                    self.format_solution(m)
                mob.set_z_index(max([m.z_index for m in mob]))

    """ Emphasize and De-emphasize Methods """
    def emphasize(self, *mobjects_to_emphasize):
        self.mobjects_to_deemphasize.extend([
            mobject for mobject in self.mobjects 
            if all([mobject is not emphasized_mobject for emphasized_mobject in mobjects_to_emphasize]) \
            and not any([mobject is non_construction_mobject for non_construction_mobject in self.non_construction_mobjects])
        ])
        self.play(*[
            self._custom_set_opacity(mobject, 0.2) for mobject in self.mobjects_to_deemphasize
        ])
    
    def undo_emphasize(self):
        self.play(*[
            self._custom_set_opacity(mobject, 1) for mobject in self.mobjects_to_deemphasize
        ])
        self.mobjects_to_deemphasize = []

    """ Miscellaneous Methods """
    def get_vertical_center_line(self, offset=0, stroke_width=4):
        top = UP * config.frame_height / 2 + offset * RIGHT
        bottom = DOWN * config.frame_height / 2 + offset * RIGHT

        center_line = Line(start=top, end=bottom, stroke_width=stroke_width)
        return center_line

    def get_dot_and_label(self, label_text, dot_center, label_direction=None, buff=None, color=None, z_index=None):
        dot = Dot(dot_center)
        label = Text(label_text).scale(self.DOT_LABEL_SCALE)
        if color:
            dot.set_color(color)
            label.set_color(color)
        if z_index is None:
            z_index = self.dot_z_index
        dot.set_z_index(self.dot_z_index)
        label.set_z_index(self.dot_z_index)
        
        if label_direction is None:
            label_direction = RIGHT
        
        if buff is None:
            buff = MED_SMALL_BUFF
            if np.allclose(label_direction, DL) \
                or np.allclose(label_direction, DR) \
                or np.allclose(label_direction, UL) \
                or np.allclose(label_direction, UR):
                buff = SMALL_BUFF
        
        label.next_to(dot.get_center(), label_direction, buff=buff)

        return dot, label

    def custom_play(self, *mobjects, run_time=None, **kwargs):
        if run_time is None:
            run_time = self.default_run_time
        mobject_copies = [mobject.copy().clear_updaters() for mobject in mobjects]
        self.play(Animate(*mobject_copies), run_time=run_time, **kwargs)
        self.remove(*mobject_copies)
        self.add(*mobjects)
    
    def custom_unplay(self, *mobjects, run_time=None, **kwargs):
        if run_time is None:
            run_time = self.default_run_time
        self.play(Unanimate(*mobjects), run_time=run_time, **kwargs)

    def play_proof_line(self, *proof_lines, constructable_mobjects=None, **kwargs):
        if constructable_mobjects is None:
            constructable_mobjects = [
                mobject for mobject in self.mobjects 
                if all([mobject is not deemphasized_mobject for deemphasized_mobject in self.mobjects_to_deemphasize]) \
                and not any([mobject is non_construction_mobject for non_construction_mobject in self.non_construction_mobjects])
            ]
        
        constructable_mobjects = [
            mob for mob in constructable_mobjects \
                if any([isinstance(mob, mob_type) for mob_type in [Text, MathTex, Dot, Line, Circle, Angle, RightAngle]])
        ]
        constructable_mobjects = VGroup(constructable_mobjects).copy()
        for mob_copy in constructable_mobjects:
            mob_copy.set_z_index(self.proof_z_index)

        proof_line_vgroup = VGroup(proof_lines)
        self.play(Transform(constructable_mobjects, proof_line_vgroup, replace_mobject_with_target_in_scene=True), **kwargs)
        self.remove(proof_line_vgroup)
        self.add(*proof_lines)

    """ Helper Methods """
    # Used in `emphasize` and `undo_emphasize`
    def _custom_set_opacity(self, mobject, opacity):
        if isinstance(mobject, Dot):
            return mobject.animate.set_opacity(opacity)

        if any([isinstance(mobject, mob_type) for mob_type in [Line, Circle, Angle]]):
            return mobject.animate.set_stroke(opacity=opacity)

        if isinstance(mobject, VGroup):
            if any([
                all([isinstance(mob, mob_type) for mob in mobject])
                for mob_type in [Line, Circle, Angle]
            ]):
                return mobject.animate.set_stroke(opacity=opacity)

        return mobject.animate.set_opacity(opacity)

    # Used in `initialize_construction` and `_mobject_updater`
    def _compute_construction(self):
        givens, given_intermediaries = self.get_givens()
        solution_intermediaries, solution = self.get_solution(*givens, *given_intermediaries)
        self.format_givens(*givens)
        self.format_solution(*solution)
        return givens, given_intermediaries, solution_intermediaries, solution
    
    # Used in `initialize_construction`
    def _all_construction_mobject_updater(self, old_givens, old_given_intermediaries, old_solution_intermediaries, old_solution):
        all_old_construction_mobjects = *old_givens, *old_given_intermediaries, *old_solution_intermediaries, *old_solution
        
        new_givens, new_given_intermediaries, new_solution_intermediaries, new_solution = self._compute_construction()
        all_new_construction_mobjects = *new_givens, *new_given_intermediaries, *new_solution_intermediaries, *new_solution
        
        for old_mob, new_mob in zip(all_old_construction_mobjects, all_new_construction_mobjects):
            new_mob.set_fill(opacity=old_mob.get_fill_opacity())
            new_mob.set_stroke(opacity=old_mob.get_stroke_opacity())
            old_mob.become(new_mob)