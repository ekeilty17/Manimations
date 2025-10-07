from manim import *
import re

def parse_statement(statement_short_hand):
    if isinstance(statement_short_hand, tuple) or isinstance(statement_short_hand, list):
        return [x for substatement in statement_short_hand for x in parse_statement(substatement)]
    
    character_map = {
        "~": r"\sim",
        "~=": r"\cong",
        "=": r"\equiv",
        "c=": r"\text{ coincides with }",
        ",": r", \ ",
        "<": r"<",
        ">": r">",
        "!~": r"\not \cong",
        "!=": r"\not \equiv",
        "right": r"\text{right}",
        "perp": r"\perp",
        "->": r"\rightarrow",
        "<-": r"\leftarrow",
        "<->": r"\leftrightarrow",
        "=>": r"\Rightarrow",
        "<=": r"\Leftarrow",
        "<=>": r"\Leftrightarrow",
        r"\ ": r"\ ",
        "+": r"+",
        "-": r"-",
    }

    statement = []
    for term in statement_short_hand.split(" "):
        if term in character_map:
            statement.append(character_map[term])
            continue
        
        if term[0] == "|":
            statement.append(f"\\overline{{{term[1:]}}}")
            continue
        if term[0] == "<":
            statement.append(f"\\angle {term[1:]}")
            continue
        if term[0] == "^":
            statement.append(f"\\triangle {term[1:]}")
            continue
        if term[0:2] == "()":
            statement.append(f"\\text{{Circle}} \\ {term[2:]}")
            continue
        
        if all([c.isalpha() or c == "'" for c in term]):
            statement.append(term)
            continue

        # If we get a term that doesn't match, then we assume it's hardcoded
        return [statement_short_hand]

    return list(statement)

def format_and_prepare_proof(lines, tex_to_color_map=None, scale=1, z_index=None):
        statements = [line[0] for line in lines]
        justifications = [line[1] for line in lines]
        line_number_colors = [line[2] if len(line) >= 2 else None for line in lines]
        
        STATEMENT_SCALE = 0.75
        JUSTIFICATION_SCALE = 0.5
        LINE_NUMBER_SCALE = 0.55

        statements = [parse_statement(statement) for statement in statements]
        justifications = [[justification] if isinstance(justification, str) else justification for justification in justifications]

        tex_to_color_map = None if tex_to_color_map is None else {parse_statement(key)[0]: value for key, value in tex_to_color_map.items()}
        statements_vgroup = VGroup([
            MathTex(*statement).scale(STATEMENT_SCALE).set_color_by_tex_to_color_map(tex_to_color_map).set_z_index(z_index)
            for statement in statements
        ])
        statements_vgroup = statements_vgroup.arrange(DOWN, aligned_edge=LEFT)

        justifications_vgroup = VGroup([Text(*justification).scale(JUSTIFICATION_SCALE).set_z_index(z_index) for justification in justifications])
        justifications_vgroup = justifications_vgroup.arrange(DOWN, aligned_edge=LEFT)

        # align justifications vertically relative to the statements
        for justification_mob, statement_mob in zip(justifications_vgroup, statements_vgroup):
            y_shift = statement_mob.get_center()[1] - justification_mob.get_center()[1]
            justification_mob.shift(y_shift * UP)

        # move the left edge of the justifications VGroup on the right edge of the statements VGroup
        x_shift = (statements_vgroup.get_right()[0] + MED_LARGE_BUFF) - justifications_vgroup.get_left()[0]
        justifications_vgroup.shift(RIGHT * x_shift)

        line_numbers = [Text(f"{i+1}.").scale(LINE_NUMBER_SCALE).set_z_index(z_index) for i in range(len(statements))]
        line_number_indicators = [
            # BackgroundRectangle(
            #     line_number,  
            #     stroke_color=line_number_colors[i], 
            #     stroke_width=2,
            #     stroke_opacity=1, 
            #     fill_opacity=0, 
            #     buff=0.1
            # ).set_z_index(z_index-1) 
            Underline(
                line_number,
                stroke_color=line_number_colors[i],
            ).set_z_index(z_index-1) 
            for i, line_number in enumerate(line_numbers)
        ]
        line_numbers_vgroup = VGroup([VGroup(line_number_indicator, line_number) for line_number_indicator, line_number in zip(line_numbers, line_number_indicators)])
        line_numbers_vgroup = line_numbers_vgroup.arrange(DOWN, aligned_edge=LEFT)

        # align line numbers vertically relative to the statements
        for line_number_mob, statement_mob in zip(line_numbers_vgroup, statements_vgroup):
            y_shift = statement_mob.get_center()[1] - line_number_mob.get_center()[1]
            line_number_mob.shift(y_shift * UP)

        # move the right edge of the line numbers VGroup on the left edge of the statements VGroup
        x_shift = (statements_vgroup.get_left()[0] - MED_SMALL_BUFF) - line_numbers_vgroup.get_right()[0]
        line_numbers_vgroup.shift(RIGHT * x_shift)
        
        proof = VGroup([VGroup(line_number, statement, justification) for line_number, statement, justification in zip(line_numbers_vgroup, statements_vgroup, justifications_vgroup)])
        proof.scale(scale)

        return proof


def format_and_parse_footnotes(footnotes, tex_to_color_map=None, scale=1):
    tex_to_color_map = None if tex_to_color_map is None else {parse_statement(key)[0]: value for key, value in tex_to_color_map.items()}
    
    formatted_footnotes = []
    for footnote_text in footnotes:
        footnote_lines = [line.strip() for line in footnote_text.split("\n") if line.strip()]
        formatted_footnote_lines = []
        for line in footnote_lines:
            pattern = r'(\\text+\{.*?\})'
            substrings = re.split(pattern, line)

            parsed_substrings = []
            for substring in substrings:
                substring = substring.strip()
                if not substring:
                    continue
                if r"\text" in substring:
                    parsed_substrings.append(substring)
                    continue
                for x in substring.split(" "):
                    parsed_substrings.extend(parse_statement(x))
            
            formatted_footnote_lines.append(
                MathTex(*parsed_substrings).set_color_by_tex_to_color_map(tex_to_color_map)
            )
        
        formatted_footnote_lines = VGroup(formatted_footnote_lines).arrange(DOWN, aligned_edge=LEFT)
        
        formatted_footnotes.append(formatted_footnote_lines)
    
    formatted_footnotes = VGroup(formatted_footnotes).scale(scale)
    return formatted_footnotes