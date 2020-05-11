from pygments import highlight
from re import sub

from .parsing import get_blocks
from .html_templates import row_template, header_template


def lineno_align(m):

    return f'<span class="lineno">{int(m.group(1)): 4d} <'


def process_blocks(blocks, lexer, formatter):

    processed = []

    ln_tot = 1

    for i, b in enumerate(blocks):

        t, v, ln = b

        if t == "code":
            formatter.linenostart = ln_tot
            v = highlight(v, lexer, formatter).decode()
        else:
            if "NOTE" in v:
                v = v.replace("NOTE", '<span class="note">NOTE</span>')
            if "TODO" in v:
                v = v.replace("TODO", '<span class="todo">TODO</span>')
            if "BUG" in v:
                v = v.replace("BUG", '<span class="bug">BUG</span>')

        processed.append((t, v))

        ln_tot += ln

    return processed


def process_file(content, lexer, formatter):

    blocks = get_blocks(content)
    blocks = process_blocks(blocks, lexer, formatter)

    out = ""

    i = 0
    while i < len(blocks):

        b1 = blocks[i]
        b2 = blocks[i + 1] if i != len(blocks) - 1 else (None, None)

        t1, v1 = b1
        t2, v2 = b2

        assert(t1 != t2)

        if t1 == "code":
            out += row_template.format(v1, "")
            i += 1
            continue

        if t1 == "explanation":
            if t2 == "code":
                out += row_template.format(v2, v1)
            elif t2 == "header":
                out += row_template.format("", v1)
                out += header_template.format(v2)
            elif t2 is None:
                out += row_template.format("", v1)
            else:
                exit("Not sure 1")

        elif t1 == "header":
            out += header_template.format(v1)
            i += 1
            continue

        i += 2

    out = sub('<span class="lineno"> *([0-9]+) <', lineno_align, out)

    return out
