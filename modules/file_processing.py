"""Process a file to extract documentation"""


import sys
from re import sub
from pygments import highlight

from .parsing import get_blocks
from .html_templates import ROW_TEMPLATE, HEADER_TEMPLATE


def lineno_align(m):
    """Properly align line numbers"""

    return f'<span class="lineno">{int(m.group(1)): 4d} <'


def process_blocks(blocks, lexer, formatter):
    """Highlight text in blocks"""

    processed = []

    ln_tot = 1

    for b in blocks:

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
    """Get a file blocks and process them"""

    blocks = get_blocks(content)
    blocks = process_blocks(blocks, lexer, formatter)

    out = ""

    i = 0
    while i < len(blocks):

        b1 = blocks[i]
        b2 = blocks[i + 1] if i != len(blocks) - 1 else (None, None)

        t1, v1 = b1
        t2, v2 = b2

        assert t1 != t2

        if t1 == "code":
            out += ROW_TEMPLATE.format(v1, "")
            i += 1
            continue

        if t1 == "explanation":
            if t2 == "code":
                out += ROW_TEMPLATE.format(v2, v1)
            elif t2 == "header":
                out += ROW_TEMPLATE.format("", v1)
                out += HEADER_TEMPLATE.format(v2)
            elif t2 is None:
                out += ROW_TEMPLATE.format("", v1)
            else:
                sys.exit("Not sure 1")

        elif t1 == "header":
            out += HEADER_TEMPLATE.format(v1)
            i += 1
            continue

        i += 2

    out = sub('<span class="lineno"> *([0-9]+) <', lineno_align, out)

    return out
