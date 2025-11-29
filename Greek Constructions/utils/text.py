from manim import *
import re

def parse_shorthand(shorthand_text):
    if isinstance(shorthand_text, tuple) or isinstance(shorthand_text, list):
        return [x for substatement in shorthand_text for x in parse_shorthand(substatement)]
    
    character_map = {
        "~": r"\sim",
        "~=": r"\cong",
        "=": r"=",
        "==": r"\equiv",
        "c=": r"\text{ coincides with }",
        ",": r", \ ",
        "<": r"<",
        ">": r">",
        "!c=": r"\text{ does not coincide with }",
        "right": r"\text{right}",
        "perp": r"\perp",
        "||": r"\parallel",
        "!||": r"\nparallel",
        "->": r"\rightarrow",
        "<-": r"\leftarrow",
        "<->": r"\leftrightarrow",
        "=>": r"\Rightarrow",
        "<=": r"\Leftarrow",
        "<=>": r"\Leftrightarrow",
        r"\ ": r"\ ",
        "+": r"+",
        "-": r"-",
        r"\\": r"\\",
        r"\rightanglesqr": r"\mathlarger{\mathlarger{\rightanglesqr}}",
    }

    statement = []
    for term in shorthand_text.split(" "):
        if term in character_map:
            statement.append(character_map[term])
            continue
        if term[0] == "!":
            if term[1:] in character_map:
                statement.append(fr"\not {character_map[term[1:]]}")
                continue
        
        if term[0] == "|":
            statement.append(fr"\overline{{{term[1:]}}}")
            continue
        if term[0] == "<":
            statement.append(fr"\angle {term[1:]}")
            continue
        if term[0] == "^":
            statement.append(f"\\triangle {term[1:]}")
            continue
        if term[0:2] == "()":
            statement.append(fr"\text{{Circle}} \ {term[2:]}")
            continue

        if all([c.isalpha() or c in ["'", "{", "}"] for c in term]):
            statement.append(term)
            continue

        # If we get a term that doesn't match, then we assume it's hardcoded
        return [shorthand_text]

    return list(statement)


def format_proof(line_numbers, statements, justifications, is_lines_indented):
    # Left align all groups
    line_numbers = line_numbers.arrange(DOWN, aligned_edge=LEFT)
    statements = statements.arrange(DOWN, aligned_edge=LEFT)
    justifications = justifications.arrange(DOWN, aligned_edge=LEFT)

    # the `statements` object act as the anchor to everything else

    # align line numbers vertically relative to the statements
    for line_number_mob, statement_mob in zip(line_numbers, statements):
        # statement_mob is a VGroup of proof lines, so we take [0] to line up with the top
        y_shift = statement_mob[0].get_center()[1] - line_number_mob.get_center()[1]
        line_number_mob.shift(y_shift * UP)
   
    # move the right edge of the line numbers VGroup on the left edge of the statements VGroup
    x_shift = (statements.get_left()[0] - MED_SMALL_BUFF) - line_numbers.get_right()[0]
    line_numbers.shift(RIGHT * x_shift)

    # Intend lines
    for line_number, statement, is_indented in zip(line_numbers, statements, is_lines_indented):
        if is_indented:
            line_number.shift(MED_SMALL_BUFF * RIGHT)
            statement.shift(MED_SMALL_BUFF * RIGHT)
    
    # align justifications vertically relative to the statements
    for statement_mob, justification_mob in zip(statements, justifications):
        # statement_mob is a VGroup of proof lines, so we take [0] to line up with the top
        y_shift = statement_mob[0].get_center()[1] - justification_mob.get_center()[1]
        justification_mob.shift(y_shift * UP)
    
    # move the left edge of the justifications VGroup on the right edge of the statements VGroup
    x_shift = (statements.get_right()[0] + MED_LARGE_BUFF) - justifications.get_left()[0]
    justifications.shift(x_shift * RIGHT)
    
    return line_numbers, statements, justifications


def parse_math_tex_paragraph(paragraph):
    parsed_paragraph = []
    for line in paragraph.split("\n"):
        line = line.strip()
        if line == "":
            continue

        pattern = r'(\\text\{.*?\}|\\textbf\{.*?\}|\\textit\{.*?\})'
        substrings = re.split(pattern, line)

        parsed_substrings = []
        for substring in substrings:
            substring = substring.strip()
            if not substring:
                continue
            if any([text in substring for text in [r"\text", r"\textbf", r"\textit"]]):
                parsed_substrings.append(substring)
                continue
            for x in substring.split(" "):
                parsed_substrings.extend(parse_shorthand(x))
        
        parsed_paragraph.append(parsed_substrings)
    return parsed_paragraph