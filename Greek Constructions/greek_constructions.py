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
    PBC_INTERMEDIARY = "proof by contradiction intermediary"
    CONTRADICTION = "constradition"
    DEFAULT = "default"
    IMPOSSIBLE = "impossible"

    LHS = "LHS"
    RHS = "RHS"

    LABEL = "label"
    DOT =  "dot"
    LINE = "line"
    ANGLE = "angle"
    CIRCLE = "circle"

    TITLE = "title"
    PARAGRAPH = "paragraph"
    TEXT_PARAGRAPH = "Text paragraph"
    MATH_TEX_PARAGRAPH = "MathTex paragraph"
    FOOTNOTE = "footnote"
    PROOF = "proof"
    QED = "QED"
    STATEMENT = "statement"
    JUSTIFICATION = "justification"
    LINE_NUMBER = "line number"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

        self.add_and_remove_only = False

        self.tex_template = TexTemplate()
        self.tex_template.add_to_preamble(r"\usepackage{stix}")
        self.tex_template.add_to_preamble(r"\usepackage{relsize}")
        # self.tex_template.add_to_preamble(r"\usepackage{graphicx}")

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
            self.ASSUMPTION: BLUE_B,#ManimColor("#cc0000"),
            self.CONTRADICTION: RED_A,#ManimColor("#cc0000"),
            self.DEFAULT: self.camera.background_color,
            self.IMPOSSIBLE: ManimColor("#cc0000")
        }

        self.z_index_map = {
            self.GIVEN: 0,
            self.INTERMEDIARY: 0,
            self.ASSUMPTION: 0,
            self.CONTRADICTION: 0,
            self.DEFAULT: 0,
            self.SOLUTION: 10,
            
            self.ANGLE: -200,
            self.LINE: 0,
            self.CIRCLE: 0,
            self.LABEL: 200,
            self.DOT: 200,
            
            self.RHS: 0,
            self.LHS: 1000,

            self.TITLE: 1100,
            self.PARAGRAPH: 1100,
            self.FOOTNOTE: 1100,

            self.PROOF: 1100,
            self.STATEMENT: 1100,
            self.JUSTIFICATION: 1100,
            self.LINE_NUMBER: 1100,

            self.QED: 1100,
        }

        self.scale_map = {
            self.LABEL: 0.5,

            self.TITLE: 0.8,
            self.TEXT_PARAGRAPH: 0.5,
            self.MATH_TEX_PARAGRAPH: 0.75,
            self.FOOTNOTE: 0.75,
            
            self.PROOF: 1,
            self.STATEMENT: 0.75,
            self.JUSTIFICATION: 0.5,
            self.LINE_NUMBER: 0.55,

            self.QED: 1.2,
        }
    
    def setup(self):
        # Set the background color to a light beige
        theme = "Monokai Pro Light" # select a theme from https://iterm2colorschemes.com
        apply_theme(manim_scene=self, theme_name=theme, light_theme=True) # use the theme

    def render_without_animations(self):
        self.add_and_remove_only = True

    """ Abstract Methods to be Implemented """
    def write_givens(self):
        raise NotImplementedError("'write_givens' not implemented by child class.")
    def write_solution(self, givens, given_intermediaries):
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
    def get_solution(self, givens, given_intermediaries):
        return self.write_solution(givens, given_intermediaries)
    def get_proof_spec(self):
        # Normalize proof spec so it's  -->  [(statement, justification, color, is_intented), ...]
        default_color = self.color_map[self.DEFAULT]
        return [
            (
                t[0],
                t[1], 
                (self.color_map.get(t[2], default_color) if len(t) > 2 else default_color),
                (t[2] in [self.ASSUMPTION, self.PBC_INTERMEDIARY, self.CONTRADICTION] if len(t) > 2 else False)
            ) 
            for t in self.write_proof_spec()
        ]
    def get_footnotes(self):
        return self.write_footnotes()
    def get_tex_to_color_map(self):
        default_color = self.color_map[self.DEFAULT]
        return {
            parse_shorthand(key)[0]:                            # replacing the shorthand keys with the actual latex
            self.color_map.get(value, default_color)            # replacing the value labels with the actual colors
            for key, value in self.write_tex_to_color_map().items()
        }

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
        # It's very important that this does not write to 
        # self.givens, self.given_intermediaries, self.solution_intermediaries, and self.solution
        # We want to keep the original variable references
        # Later in `_add_mobject_updater`, the old_mob becomes the new_mob, which allows us to keep the same reference
        givens, given_intermediaries = self.get_givens()
        solution_intermediaries, solution = self.get_solution(givens, given_intermediaries)
        self.format_givens(*givens)
        self.format_solution(*solution)
        return givens, given_intermediaries, solution_intermediaries, solution

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
        # This is the one and only time that we instantiate these variables
        self.givens, self.given_intermediaries, self.solution_intermediaries, self.solution = self._compute_construction()
        if add_updaters:
            self.add_updaters()

    def initialize_introduction(self):
        title, description = self.Text(self.description, title=self.title)
        return title, description

    def initialize_proof(self, scale=None, shift=ORIGIN, center_horizontally=False):
        if scale is None:
            scale = self.scale_map[self.PROOF]
        
        proof_spec = self.get_proof_spec()
        tex_to_color_map = self.get_tex_to_color_map()

        line_numbers = VGroup([
            Text(f"{i+1}.")
                .scale(self.scale_map[self.LINE_NUMBER])
                .set_z_index(self.z_index_map[self.LINE_NUMBER]) 
            for i in range(len(proof_spec))
        ])
        
        statements = VGroup([
            #MathTex(*parse_shorthand(line[0]))
            self.MathTex(*(line[0].split(r"\\")), paragraph_spacing=1, scale=1)
                .scale(self.scale_map[self.STATEMENT])
                .set_color_by_tex_to_color_map(tex_to_color_map)
                .set_z_index(self.z_index_map[self.STATEMENT])
            for line in proof_spec
        ])
        justifications = VGroup([
            Text(line[1])   # TODO: maybe split on "\n" or something
                .scale(self.scale_map[self.JUSTIFICATION])
                .set_z_index(self.z_index_map[self.JUSTIFICATION]) 
            for line in proof_spec
        ])
        is_lines_indented = [line[3] for line in proof_spec]
        
        line_numbers, statements, justifications = format_proof(line_numbers, statements, justifications, is_lines_indented)

        # Add the indicators only after the formatting (so it doesn't affect the centering of line_numbers)
        line_number_indicators =  VGroup([
            Underline(line_number_mob, stroke_color=line[2]).set_z_index(line_number_mob.z_index) 
            for line, line_number_mob in zip(proof_spec, line_numbers)
        ])

        # Group things in the way they will be animated
        proof_line_numbers = VGroup(*[VGroup(line_number_mob, indocator_mob) for line_number_mob, indocator_mob in zip(line_numbers, line_number_indicators)])
        proof_lines = VGroup(*[VGroup(statement, justification) for statement, justification in zip(statements, justifications)])
        
        # Left justify everything
        proof = VGroup(proof_line_numbers, proof_lines)
        proof.set_z_index(self.z_index_map[self.PROOF]).scale(scale)
        
        proof.move_to(self.LEFT_CENTER)
        if not center_horizontally:
            proof.to_edge(LEFT)
        proof.shift(shift)

        # Good for debugging orientation
        # for line_number, statement, justification in zip(line_numbers, statements, justifications):
        #     self.add(Dot(line_number.get_center(), z_index=10000, color=BLUE))
        #     self.add(Dot(statement.get_center(), z_index=10000, color=RED))
        #     self.add(Dot(justification.get_center(), z_index=10000, color=YELLOW))

        return proof_line_numbers, proof_lines

    def initialize_footnotes(self, shift=ORIGIN):
        footnotes = self.get_footnotes()
        if len(footnotes) == 0:
            return [], []

        formatted_footnotes = []
        for footnote in footnotes:
            formatted_footnote = self.MathTex(*footnote.split(r"\\"))
            formatted_footnote.set_z_index(self.z_index_map[self.FOOTNOTE])#.scale(self.scale_map[self.FOOTNOTE])
            formatted_footnotes.append(formatted_footnote)
        
        formatted_footnotes = VGroup(*formatted_footnotes).set_z_index(self.z_index_map[self.FOOTNOTE])#.scale(self.scale_map[self.FOOTNOTE])
        formatted_footnotes.shift(shift)
        
        footnote_animations = [
            Write(formatted_footnotes[0]),
            *[ReplacementTransform(formatted_footnotes[i], formatted_footnotes[i+1]) for i in range(len(formatted_footnotes)-1)],
            FadeOut(formatted_footnotes[-1])
        ]
        return formatted_footnotes, footnote_animations

    """ Custom Text / MathTex """
    def MathTex(self, *paragraphs, line_spacing=0.6, paragraph_spacing=2, scale=None, z_index=None):
        if scale is None:
            scale = self.scale_map[self.MATH_TEX_PARAGRAPH]
        if z_index is None:
            z_index = self.z_index_map[self.PARAGRAPH]

        tex_to_color_map = self.get_tex_to_color_map()

        paragraph_mobjects = []
        for paragraph in paragraphs:
            paragraph = VGroup([
                MathTex(*line, tex_template=self.tex_template)
                    .set_color_by_tex_to_color_map(tex_to_color_map)
                    .scale(scale)
                    .set_z_index(z_index)
                for line in parse_math_tex_paragraph(paragraph)
            ])
            paragraph.arrange(line_spacing*DOWN, aligned_edge=LEFT)
            paragraph_mobjects.append(paragraph)
        
        paragraphs_vgroup = VGroup(*paragraph_mobjects).set_z_index(z_index).scale(scale)
        paragraphs_vgroup.arrange(paragraph_spacing*DOWN, aligned_edge=LEFT)
        paragraphs_vgroup.to_edge(DOWN).shift(self.RIGHT_CENTER[0] * RIGHT)
        return paragraphs_vgroup

    def Text(self, *paragraphs, line_spacing=0.5, title=None, z_index=None):
        if z_index is None:
            z_index = self.z_index_map[self.PARAGRAPH]

        if title is not None:
            title = Text(title).scale(self.scale_map[self.TITLE]).set_z_index(z_index)
            title.move_to(self.LEFT_CENTER)
        
        paragraphs = [
            "\n".join([line.strip() for line in paragraph.split("\n")])
            for paragraph in paragraphs
        ]
        paragraphs = VGroup([
            Text(paragraph, line_spacing=line_spacing).scale(self.scale_map[self.TEXT_PARAGRAPH]).set_z_index(z_index)
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

        if play and not self.add_and_remove_only:
            self.play(*animations)
        return animations
    
    def clear_emphasize(self, play=False, add=False):
        if add or self.add_and_remove_only:
            for mobject in self.mobjects_currently_deemphasized:
                self._custom_set_opacity(mobject, 1, animate=False)
            self.mobjects_currently_deemphasized = []
        
        animations = [self._custom_set_opacity(mobject, 1, animate=True) for mobject in self.mobjects_currently_deemphasized]
        self.mobjects_currently_deemphasized = []
        if play and not self.add_and_remove_only:
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
                mobjects_to_remove.append(anim.mobject)
                continue

            if isinstance(anim, ReplacementTransform):
                # mobjects_to_remove.append(anim.mobject)
                # mobjects_to_add.append(anim.target_mobject)
                continue

            if isinstance(anim, (Create, Write, FadeIn, GrowFromCenter, Rotate)):
                mobjects_to_add.append(anim.mobject)
                anim.mobject = anim.mobject.copy().clear_updaters()
                mobjects_to_remove.append(anim.mobject)
                continue
            
            if isinstance(anim, Transform):
                raise NotImplementedError("Have not implemented Transform, ReplacementTransform is usually easier to use.")

        if not self.add_and_remove_only:
            self.play(*animations, run_time=run_time, **kwargs)
        self.remove(*mobjects_to_remove)
        self.add(*mobjects_to_add)

    def animate_proof_line_numbers(self, proof_line_numbers):
        if len(proof_line_numbers) == 0:
            print("Warning: `proof_line_numbers` is empty")
            return
        self.custom_play(*Animate(*[anim for proof_line_number in proof_line_numbers for anim in proof_line_number]))

    def animate_proof_line(self, *proof_lines, source_mobjects=None, **kwargs):
        if source_mobjects is None:
            # If a mobject is not on t
            source_mobjects = [
                mobject for mobject in self.get_all_construction_mobjects()
                # mobject is on the screen
                if any([mobject is mob for mob in self.mobjects])
                # and the mobject is not deemphasized
                and not any([mobject is deemphasized_mobject for deemphasized_mobject in self.mobjects_currently_deemphasized]) 
            ]

        proof_line_vgroup = VGroup(proof_lines).copy().set_z_index(self.z_index_map[self.PROOF])
        if len(source_mobjects) == 0:
            proof_animation = Write(proof_line_vgroup)
        else:

            source_mobjects = VGroup([
                mob.copy().set_z_index(mob.z_index + self.z_index_map[self.PROOF]) 
                for mob in source_mobjects
            ]).set_z_index(self.z_index_map[self.PROOF])
            
            # proof_animation = Transform(source_mobjects, proof_line_vgroup, replace_mobject_with_target_in_scene=True)
            proof_animation = ReplacementTransform(source_mobjects, proof_line_vgroup)
        
        if not self.add_and_remove_only:
            self.custom_play(proof_animation, **kwargs)
        self.remove(proof_line_vgroup)
        self.add(*proof_lines)

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
        
        if self.add_and_remove_only:
            self.add(QED_bg, QED_text)
        else:
            self.play(FadeIn(QED_bg), Write(QED_text))

    """ Custom ReplacementTransform """
    def ReplacementTransformN2M(self, source_mobjects, target_mobjects, copy_source=False):
        if not isinstance(source_mobjects, (list, tuple)):
            source_mobjects = [source_mobjects]
        if not isinstance(target_mobjects, (list, tuple)):
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

    def ReplacementTransformN2M_cleanup(self):
        self.remove(*self.replace_transform_mobjects_to_remove)
        self.add(*self.replace_transform_mobjects_to_add)
        self.replace_transform_mobjects_to_remove = []
        self.replace_transform_mobjects_to_add = []