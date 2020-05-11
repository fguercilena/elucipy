from re import sub, compile, MULTILINE
from sys import exit


explanation_regex = compile(r"(^[ \t\f\v]*# .*\n)+\n*", MULTILINE)
header_regex = compile(r"((^[ \t\f\v]*)#{2,}\n)\2# (.*\n)\1\n*", MULTILINE)
code_regex = compile(r"(^[ \t\f\v]*[^# \t\f\v\n].*\n)+\n*", MULTILINE)
# triple_quote_regex = compile(r"\"\"\".*\"\"\"", DOTALL)
# double_quote_regex = compile(r"\".*\"")
# single_quote_regex = compile(r"\'.*\'")


def parse_block(text, pos):

    m = header_regex.match(text, pos)
    if m:
        return "header", m[3], m.end(0), m[0].count("\n")

    m = explanation_regex.match(text, pos)
    if m:
        text = sub(r"^[ \t\f\v]*# ", "", m[0], flags=MULTILINE)
        return "explanation", text, m.end(0), m[0].count("\n")

    m = code_regex.match(text, pos)
    if m:
        return "code", m[0], m.end(0), m[0].count("\n")

    else:
        print("\nWarning: couldn't identify the following code:\n",
              text[pos:pos + 200] + " [truncated]",
              "Assuming the rest of the file contains only code "
              "and continuing...")
        return "code", text[pos:], len(text), text[pos:].count("\n")


def merge_blocks(blocks):

    merged = []

    for b in blocks:

        t, v, ln = b

        if t == "header":
            if len(merged) == 0:
                merged.append((t, v, ln))
            elif merged[-1][0] == "header":
                exit("Error: found consecutive headers. Aborting.")
            else:
                merged.append((t, v, ln))
        elif t == "explanation":
            if len(merged) == 0:
                merged.append((t, v, ln))
            elif merged[-1][0] != "explanation":
                merged.append((t, v, ln))
            else:
                merged[-1] = (t, merged[-1][1] + v, merged[-1][2] + ln)
        elif t == "code":
            if len(merged) == 0:
                merged.append((t, v, ln))
            elif merged[-1][0] != "code":
                merged.append((t, v, ln))
            else:
                merged[-1] = (t, merged[-1][1] + v, merged[-1][2] + ln)

    return merged


def get_blocks(content):

    blocks = []

    pos = 0
    while pos < len(content):

        t, v, p, ln = parse_block(content, pos)

        blocks.append((t, v, ln))

        pos = p

    return merge_blocks(blocks)
