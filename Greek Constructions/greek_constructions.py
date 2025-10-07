from manim import *
from manim.mobject.mobject import _AnimationBuilder

from utils import *

# https://manim-themes.readthedocs.io/en/latest/index.html
from manim_themes.manim_theme import apply_theme

class GreekConstructionScenes(Scene):

    # Types
    GIVEN = "given"
    SOLUTION = "solution"
    INTERMEDIARY = "intermediary"
    ASSUMPTION = "assumption"
    CONTRADICTION = "constradition"
    DEFAULT = "default"

    LHS = "LHS"
    RHS = "RHS"

    LABEL = "label"
    DOT =  "dot"
    LINE = "line"
    ANGLE = "angle"
    CIRCLE = "circle"

    TITLE = "title"
    PARAGRAPH = "paragraph"
    FOOTNOTE = "footnote"
    PROOF = "proof"
    QED = "QED"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

        self.LEFT_CENTER = LEFT * (config.frame_width / 4)
        self.RIGHT_CENTER = RIGHT * (config.frame_width / 4)
        self.vertical_line_x_offset = 0
        self.default_run_time = 0.75
        
        self.mobjects_currently_deemphasized = []
        self.replace_transform_mobjects_to_add = []
        self.replace_transform_mobjects_to_remove = []

        self.color_map = {
            self.GIVEN: BLUE_D,
            self.SOLUTION: RED_E, 
            self.INTERMEDIARY: BLACK,
            self.ASSUMPTION: ManimColor("#cc0000"),
            self.CONTRADICTION: ManimColor("#cc0000"),
            self.DEFAULT: self.camera.background_color,
        }

        self.z_index_map = {
            self.GIVEN: 0,
            self.SOLUTION: 10, 
            self.INTERMEDIARY: 0,
            self.ASSUMPTION: 0,
            self.CONTRADICTION: 0,
            self.DEFAULT: 0,
            
            self.LHS: 1000,
            self.RHS: 0,

            self.LABEL: 200,
            self.DOT: 200,
            self.LINE: 0,
            self.ANGLE: -2,
            self.CIRCLE: 0,
            
            self.PROOF: 1100,
            self.TITLE: 1100,
            self.PARAGRAPH: 1100,
            self.FOOTNOTE: 1100,
            self.QED: 1100,
        }

        self.scale_map = {
            self.LABEL: 0.5,
            self.TITLE: 0.8,
            self.PARAGRAPH: 0.5, 
            self.QED: 1.2,
        }

        # self.left_bg_z_index = 400
        # self.given_z_index = 0
        # self.solution_z_index = 10
        # self.proof_z_index = 500

        # self.line_z_index = 0
        # self.circle_z_index = 0
        # self.dot_z_index = 200
        # self.angle_z_index = -2

        # self.DOT_LABEL_SCALE = 0.5
        # self.TITLE_SCALE = 0.8
        # self.PARAGRAPH_SCALE = 0.5
    
    def setup(self):
        # Set the background color to a light beige
        theme = "Monokai Pro Light" # select a theme from https://iterm2colorschemes.com
        apply_theme(manim_scene=self, theme_name=theme, light_theme=True) # use the theme

    """ Abstract Methods to be Implemented """
    def write_givens(self):
        raise NotImplementedError("'write_givens' not implemented by child class.")
    def write_solution(self, *givens):
        raise NotImplementedError("'write_solution' not implemented by child class.")
    def write_proof_spec(self):
        raise NotImplementedError("'write_proof_spec' not implemented by child class.")
    def write_footnotes(self):
        return []
    def write_tex_to_color_map(self):
        return {}

    """ Getters for the Abstract Methods Above """
    def get_givens(self):
        return self.write_givens()
    def get_solution(self, *givens):
        return self.write_solution(*givens)
    def get_proof_spec(self):
        # Normalize proof spec so it's  -->  [(statement, justification, color), ...]
        return [(t[0], t[1], (t[2] if len(t) > 2 else self.DEFAULT)) for t in self.write_proof_spec()]
    def get_footnotes(self):
        return self.write_footnotes()
    def get_tex_to_color_map(self):
        # replacing the labels with the actual colors
        return {key: self.color_map[value] for key, value in self.write_tex_to_color_map().items()}

    """ Construction Mobjects """
    def format_givens(self, *mobjects):
        for mob in mobjects:
            mob.set_color(self.color_map[self.GIVEN])
            mob.set_z_index(self.z_index_map[self.GIVEN])
            if isinstance(mob, Dot):
                mob.set_z_index(mob.z_index + self.z_index_map[self.DOT])
            elif isinstance(mob, Circle):
                mob.set_z_index(mob.z_index + self.z_index_map[self.CIRCLE])
            elif isinstance(mob, Line):
                mob.set_z_index(mob.z_index + self.z_index_map[self.LINE])
            elif isinstance(mob, Angle):
                mob.set_z_index(self.z_index_map[self.ANGLE])
            elif isinstance(mob, VGroup):
                for m in mob:
                    self.format_givens(m)
                mob.set_z_index(max([m.z_index for m in mob]))
    def format_solution(self, *mobjects):
        for mob in mobjects:
            mob.set_color(self.color_map[self.SOLUTION])
            mob.set_z_index(self.z_index_map[self.SOLUTION])
            if isinstance(mob, Dot):
                mob.set_z_index(mob.z_index + self.z_index_map[self.DOT])
            elif isinstance(mob, Circle):
                mob.set_z_index(mob.z_index + self.z_index_map[self.CIRCLE])
            elif isinstance(mob, Line):
                mob.set_z_index(mob.z_index + self.z_index_map[self.LINE])
            elif isinstance(mob, Angle):
                mob.set_z_index(self.z_index_map[self.ANGLE])
            elif isinstance(mob, VGroup):
                for m in mob:
                    self.format_solution(m)
                mob.set_z_index(max([m.z_index for m in mob]))

    def _compute_construction(self):
        self.givens, self.given_intermediaries = self.get_givens()
        self.solution_intermediaries, self.solution = self.get_solution(*self.givens, *self.given_intermediaries)
        self.format_givens(*self.givens)
        self.format_solution(*self.solution)
        return self.givens, self.given_intermediaries, self.solution_intermediaries, self.solution

    def get_all_construction_mobjects(self):
        return *self.givens, *self.given_intermediaries, *self.solution_intermediaries, *self.solution

    def add_updaters(self):
        all_construction_mobjects = self.get_all_construction_mobjects()
        for mob in all_construction_mobjects:
            mob.add_updater(lambda _, mob=mob: self._add_mobject_updater(*all_construction_mobjects))
        return all_construction_mobjects
    def clear_updater(self):
        all_construction_mobjects = self.get_all_construction_mobjects()
        for mob in all_construction_mobjects:
            mob.clear_updaters()
        return all_construction_mobjects

    def _add_mobject_updater(self, *all_old_construction_mobjects):
        #all_old_construction_mobjects = *old_givens, *old_given_intermediaries, *old_solution_intermediaries, *old_solution
        
        new_givens, new_given_intermediaries, new_solution_intermediaries, new_solution = self._compute_construction()
        all_new_construction_mobjects = *new_givens, *new_given_intermediaries, *new_solution_intermediaries, *new_solution
        
        for old_mob, new_mob in zip(all_old_construction_mobjects, all_new_construction_mobjects):
            new_mob.set_fill(opacity=old_mob.get_fill_opacity())
            new_mob.set_stroke(opacity=old_mob.get_stroke_opacity())
            old_mob.become(new_mob)

    """ Initialize Aspects of the Scene """
    def initialize_canvas(self):
        x_offset = self.vertical_line_x_offset
        stroke_width = 4

        # Create background rectangle
        LHS_bg = Rectangle(
            width=config.frame_width / 2 + x_offset,
            height=config.frame_height,
            fill_color=self.camera.background_color,
            fill_opacity=1,
            stroke_width=0
        ).move_to(self.LEFT_CENTER)
        LHS_bg.set_z_index(self.z_index_map[self.LHS])
        
        # Create center line
        top = UP * config.frame_height / 2 + x_offset * RIGHT
        bottom = DOWN * config.frame_height / 2 + x_offset * RIGHT        
        center_line = Line(start=top, end=bottom, stroke_width=stroke_width)
        center_line.set_z_index(self.z_index_map[self.LHS])
        
        self.add(LHS_bg, center_line)

    def initialize_construction(self, add_updaters=False):
        self._compute_construction()        # instantiates (self.givens, self.given_intermediaries, self.solution_intermediaries, self.solution)
        if add_updaters:
            self.add_updaters()

    def initialize_introduction(self):
        title, description = self.get_explanation(self.description, title=self.title)
        return title, description

    def initialize_proof(self, scale=1):
        proof_spec = self.get_proof_spec()
        tex_to_color_map = self.get_tex_to_color_map()

        default_color = self.color_map[self.DEFAULT]
        proof_spec = [
            (
                statement, 
                justification, 
                self.color_map.get(line_type, default_color)
            ) for statement, justification, line_type in proof_spec
        ]
        proof = format_and_prepare_proof(proof_spec, tex_to_color_map, scale=scale, z_index=self.z_index_map[self.PROOF])
        proof.to_edge(LEFT)#.set_z_index(self.z_index_map[self.PROOF])

        proof_line_numbers = VGroup([line_number for line_number, _, _ in proof])
        proof_lines = VGroup([VGroup(statement, justification) for _, statement, justification in proof])

        return proof_line_numbers, proof_lines

    def initialize_footnotes(self, scale=0.6):
        footnotes = self.get_footnotes()
        if len(footnotes) == 0:
            return None, None, None, None

        tex_to_color_map = self.get_tex_to_color_map()
        formatted_footnotes = format_and_parse_footnotes(footnotes, tex_to_color_map, scale=scale)

        formatted_footnotes.to_edge(DOWN).shift(self.RIGHT_CENTER[0] * RIGHT)
        for footnote in formatted_footnotes:
            footnote.set_z_index(self.z_index_map[self.PROOF])
        
        first_footnote_animation = Write(formatted_footnotes[0])
        next_footnote_animations = [ReplacementTransform(formatted_footnotes[i], formatted_footnotes[i+1]) for i in range(len(formatted_footnotes)-1)]
        last_footnote_animation = FadeOut(formatted_footnotes[-1])
        return formatted_footnotes, first_footnote_animation, next_footnote_animations, last_footnote_animation

    """ Emphasize and De-emphasize Methods """
    def emphasize(self, *mobjects_to_emphasize, play=False):
        all_construction_mobjects = list(self.get_all_construction_mobjects()) + list(mobjects_to_emphasize)
        
        animations = []
        self.mobjects_currently_deemphasized = []
        for mobject in self.mobjects:
            if not any([mobject is mob for mob in all_construction_mobjects]):
                continue
            if any([mobject is mob for mob in mobjects_to_emphasize]):
                animations.append(self._custom_set_opacity(mobject, 1))
            else:
                self.mobjects_currently_deemphasized.append(mobject)
                animations.append(self._custom_set_opacity(mobject, 0.2))

        if play:
            self.play(*animations)
        return animations
    
    def clear_emphasize(self, play=False, add=False):
        if add:
            for mobject in self.mobjects_currently_deemphasized:
                self._custom_set_opacity(mobject, 1, animate=False)
            self.mobjects_currently_deemphasized = []
        
        animations = [self._custom_set_opacity(mobject, 1, animate=True) for mobject in self.mobjects_currently_deemphasized]
        self.mobjects_currently_deemphasized = []
        if play:
            self.play(*animations)
        return animations

    def _custom_set_opacity(self, mobject, opacity, animate=True):
        return_mob = mobject.animate if animate else mobject

        if isinstance(mobject, Dot):
            return return_mob.set_opacity(opacity)

        if any([isinstance(mobject, mob_type) for mob_type in [Line, Circle, Angle]]):
            return return_mob.set_stroke(opacity=opacity)

        if isinstance(mobject, VGroup):
            if any([
                all([isinstance(mob, mob_type) for mob in mobject])
                for mob_type in [Line, Circle, Angle]
            ]):
                return return_mob.set_stroke(opacity=opacity)

        return return_mob.set_opacity(opacity)

    """ Custom Animation or Mobject Creation Script """
    def get_dot_and_label(self, label_text, dot_center, label_direction=None, buff=None, color=None, z_index=None):
        dot = Dot(dot_center)
        label = Text(label_text).scale(self.scale_map[self.LABEL])
        if color:
            dot.set_color(color)
            label.set_color(color)
        if z_index is None:
            z_index = self.z_index_map[self.DOT]
        dot.set_z_index(self.z_index_map[self.DOT])
        label.set_z_index(self.z_index_map[self.LABEL])
        
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

    def get_center_shift(self, *mobjects):
        mobjects_vgroup = VGroup(*mobjects)
        mobjects_vgroup_centered = mobjects_vgroup.copy().move_to(self.RIGHT_CENTER)
        return mobjects_vgroup_centered.get_center() - mobjects_vgroup.get_center()

    def custom_play(self, *animations, run_time=None, **kwargs):
        if run_time is None:
            run_time = self.default_run_time
        
        mobjects_to_add = []
        mobjects_to_remove = []
        for anim in animations:
            if isinstance(anim, _AnimationBuilder):
                continue
            if not isinstance(anim, Animation):
                raise TypeError(f"Expected Animation, got {type(anim)}")
            
            if isinstance(anim, (Uncreate, Unwrite, FadeOut, ShrinkToCenter)):
                continue

            if isinstance(anim, ReplacementTransform):
                continue

            if isinstance(anim, (Create, Write, FadeIn, GrowFromCenter)):
                mobjects_to_add.append(anim.mobject)
                anim.mobject = anim.mobject.copy().clear_updaters()
                mobjects_to_remove.append(anim.mobject)
                continue
            
            if isinstance(anim, Transform):
                raise NotImplementedError("Have not implemented Transform, ReplacementTransform is usually easier to use.")

        self.play(*animations, run_time=run_time, **kwargs)
        self.remove(*mobjects_to_remove)
        self.add(*mobjects_to_add)

    def animate_proof_line_numbers(self, proof_line_numbers):
        self.custom_play(*Animate(*[anim for proof_line_number in proof_line_numbers for anim in proof_line_number]))

    def animate_proof_line(self, *proof_lines, source_mobjects=None, **kwargs):
        if source_mobjects is None:
            source_mobjects = [
                mobject for mobject in self.mobjects 
                if all([mobject is not deemphasized_mobject for deemphasized_mobject in self.mobjects_currently_deemphasized]) \
                and any([mobject is mob for mob in self.get_all_construction_mobjects()])
            ]
        
        source_mobjects = [
            mob for mob in source_mobjects \
                if any([isinstance(mob, mob_type) for mob_type in [Text, MathTex, Dot, Line, Circle, Angle, RightAngle]])
        ]
        source_mobjects = VGroup(source_mobjects).copy()
        for mob_copy in source_mobjects:
            mob_copy.set_z_index(self.z_index_map[self.PROOF])

        proof_line_vgroup = VGroup(proof_lines)
        self.play(Transform(source_mobjects, proof_line_vgroup, replace_mobject_with_target_in_scene=True), **kwargs)
        self.remove(proof_line_vgroup)
        self.add(*proof_lines)

    def get_explanation(self, *paragraphs, title=None):
        if title is not None:
            title = Text(title).scale(self.scale_map[self.TITLE]).set_z_index(self.z_index_map[self.PROOF])
            title.move_to(self.LEFT_CENTER)
        
        paragraphs = [
            "\n".join([line.strip() for line in paragraph.split("\n")])
            for paragraph in paragraphs
        ]
        paragraphs = VGroup([
            Text(paragraph).scale(self.scale_map[self.PARAGRAPH]).set_z_index(self.z_index_map[self.PROOF])
            for paragraph in paragraphs
        ])
        paragraphs = paragraphs.arrange(DOWN, aligned_edge=LEFT)
        
        if title is None:
            paragraphs.move_to(self.LEFT_CENTER)
            return paragraphs
        else:
            paragraphs.next_to(title, 2*DOWN)
            explanation = VGroup(title, *paragraphs)
            explanation.move_to(self.LEFT_CENTER)
            return explanation

    def write_QED(self, position=None, position_func=None):
        QED_text = MathTex(r"\text{Q.E.D.}").scale(self.scale_map[self.QED]).set_z_index(self.z_index_map[self.QED])
        QED_bg = BackgroundRectangle(QED_text, color=self.camera.background_color, fill_opacity=1, buff=0.1).set_z_index(self.z_index_map[self.QED])
        QED = VGroup(QED_text, QED_bg)
        if position is None and position_func is None:
            QED.to_edge(DOWN)
        elif position is not None:
            QED.move_to(position)
        elif position_func is not None:
            QED = position_func(QED)
        self.play(FadeIn(QED_bg), Write(QED_text))

    """ Custom ReplaceTransform """
    def ReplaceTransformN2M(self, source_mobjects, target_mobjects, copy_source=False):
        if not isinstance(source_mobjects, list) and not isinstance(source_mobjects, tuple):
            source_mobjects = [source_mobjects]
        if not isinstance(target_mobjects, list) and not isinstance(target_mobjects, tuple):
            target_mobjects = [target_mobjects]
        if copy_source:
            source_mobjects = [mob.copy() for mob in source_mobjects]
        target_mobject_copies = [mob.copy() for mob in target_mobjects]

        animations = [
            ReplacementTransform(source_mob, target_mob)
            for source_mob in source_mobjects
            for target_mob in target_mobject_copies
        ]

        self.replace_transform_mobjects_to_remove.extend(target_mobject_copies)
        self.replace_transform_mobjects_to_add.extend(target_mobjects)
        return animations

    def ReplaceTransformN2M_cleanup(self):
        self.remove(*self.replace_transform_mobjects_to_remove)
        self.add(*self.replace_transform_mobjects_to_add)
        self.replace_transform_mobjects_to_remove = []
        self.replace_transform_mobjects_to_add = []