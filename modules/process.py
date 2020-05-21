from re import sub
from pygments import highlight

from .html_templates import ROW_TEMPLATE, HEADER_TEMPLATE


def preprocess_file(content, filename, language):

    match = language.elucipy_regex.search(content)

    if match is None:
        return False, None, None, None

    if match[2] == "":
        title = filename
    else:
        title = match[2]

    content = language.elucipy_regex.sub("", content)

    intro = language.elucipy_trash.sub("", match[3])

    intro = intro.replace("NOTE", '<span class="note">NOTE</span>')
    intro = intro.replace("TODO", '<span class="todo">TODO</span>')
    intro = intro.replace("BUG", '<span class="bug">BUG</span>')

    return True, content, title, intro


def lineno_align(match):

    return f'<span class="lineno">{int(match[1]): 4d} <'


def process_header(header, trash):

    header = trash.sub("", header)

    header = header.replace("NOTE", '<span class="note">NOTE</span>')
    header = header.replace("TODO", '<span class="todo">TODO</span>')
    header = header.replace("BUG", '<span class="bug">BUG</span>')

    return header


def process_explanation(explanation, trash):

    explanation = trash.sub("", explanation)

    explanation = explanation.replace("#", "")
    explanation = explanation.replace("\n", "<br>")

    explanation = explanation.replace("NOTE", '<span class="note">NOTE</span>')
    explanation = explanation.replace("TODO", '<span class="todo">TODO</span>')
    explanation = explanation.replace("BUG", '<span class="bug">BUG</span>')

    return explanation


def process_code(code, lexer, formatter, line):

    formatter.linenostart = line
    return highlight(code, lexer, formatter).decode("utf-8")


def process_file(content, language, lexer, formatter):

    tmp_sections = language.header.split(content)

    sections = []
    for i, tmp_section in enumerate(tmp_sections):
        ind = i % 4
        if ind in (0, 1):
            sections.append(tmp_section)
    del tmp_sections

    line = 1
    out = ""
    for i, section in enumerate(sections):

        if i % 2 == 1:
            header = process_header(section, language.header_trash)
            out += HEADER_TEMPLATE.format(header)

            line += section.count("\n")
        else:
            blocks = language.explanation.split(section)

            if blocks[0] != "":
                code = process_code(blocks[0], lexer, formatter, line)
                out += ROW_TEMPLATE.format(code, "")

                line += blocks[0].count("\n")

            j = 1
            while j < len(blocks):

                explanation_block = blocks[j]
                code_block = blocks[j + 1] if j < len(blocks) - 1 else ""

                line += explanation_block.count("\n")

                code = process_code(code_block, lexer, formatter, line)
                explanation = process_explanation(explanation_block,
                                                  language.explanation_trash)
                out += ROW_TEMPLATE.format(code, explanation)

                line += code_block.count("\n")

                j += 2

    out = sub('<span class="lineno"> *([0-9]+) <', lineno_align, out)

    return out
