from itertools import groupby, batched
from html_templates import DOCUMENT_TEMPLATE, ROW_TEMPLATE_RIGHT, ROW_TEMPLATE_LEFT
from os.path import split, join, dirname, realpath
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CppLexer
from pygments.token import Comment, Text
from pygments.styles import get_all_styles
import argparse
import numpy as np
import re
import sys
import time


VERSION = "elucipy -- version 1.0 (September 2026)"
EPILOG = """Federico Maria Guercilena
(guercilena.federico@gmail.com"""
DESCRIPTION = """Generate an .html document showing the source code of the
input files, with a parallel explanation running along it,
generated from the comments in the code."""


def token_classifier(token):
    if token[1] is Comment.Single:
        return 1
    if token[1] is Comment.Multiline:
        return 2

    return 0


def get_blocks(code, lexer):

    tokens = list(lexer.get_tokens_unprocessed(code))


    for i in range(len(tokens)):
        tokens[i] = list(tokens[i])

    tmp = []
    for i, token in enumerate(tokens):
        if token[1] is Text.Whitespace:
            if i > 0 and tokens[i - 1][1] is Comment.Single:
                if i < len(tokens) - 1 and tokens[i + 1][1] is Comment.Single:
                    token[1] = Comment.Single
                    # tmp.append(i)
    # mask = np.ones(len(tokens), np.bool)
    # mask[tmp] = 0
    # tokens = np.array(tokens, dtype=object)[mask]

    groups = [(t, list(v)) for t, v in groupby(tokens, token_classifier)]

    blocks = []
    line_number = 1
    for t, group in groups:

        start = group[0][0]
        end = group[-1][0] + len(group[-1][2])

        content = ""
        count_linebreaks = 0
        for _, _, token in group:

            count_linebreaks += token.count("\n")

            if t == 1:
                token = re.sub(r"//", "", token, count=1).lstrip()
            elif t == 2:
                token = re.sub(r"/\*|\*|\*/", "", token, count=1).lstrip()

            content += token

        blocks.append((start, end, line_number, content))

        line_number += count_linebreaks

    if groups[0][0] == 0:
        blocks = [(0, 0, 0, "")] + blocks

    return blocks


def process_blocks(blocks, lexer, formatter):

    out = ""

    for tmp in batched(blocks, 2):

        if len(tmp) == 2:
            explanation, code = tmp

            _, _, line_number, code = code
            formatter.linenostart = line_number
            code = highlight(code, lexer, formatter).decode("utf-8")
        else:
            explanation = tmp[0]

        _, _, line_number, explanation = explanation

        out += ROW_TEMPLATE_RIGHT.format(code, explanation)

    return out


def main():

    # Parse command line arguments
    cl_parsr = argparse.ArgumentParser(
        add_help=True, epilog=EPILOG, description=DESCRIPTION
    )

    cl_parsr.add_argument(
        "--version",
        action="version",
        version=VERSION,
        help="print version information and exit",
    )

    cl_parsr.add_argument("filenames", nargs="+", help="input file(s) path")
    # cl_parsr.add_argument("-l", "--language", default=None, dest="lang",
    #   choices=list(LANGUAGES),
    #   help="programming language of the input files")
    cl_parsr.add_argument(
        "-s",
        "--style",
        default="nord",
        dest="style",
        choices=list(get_all_styles()),
        help="syntax highlight style",
    )
    cl_parsr.add_argument(
        "--ignore-linebreaks",
        default=False,
        action="store_true",
        dest="ignore_lb",
        help="ignore linebreaks in explanations",
    )
    cl_parsr.add_argument(
        "--invert-layout",
        default=False,
        action="store_true",
        dest="invert",
        help="put explanations on the left of code",
    )
    cl_parsr.add_argument(
        "-o", "--out-directory", default=".", dest="outdir", help="output directory"
    )
    cl_parsr.add_argument(
        "-q",
        "--quiet",
        default=False,
        action="store_true",
        dest="quiet",
        help="quiet mode",
    )

    args = cl_parsr.parse_args()

    lexer = CppLexer(stripnl=True, stripall=False, ensurenl=True, tabsize=4)

    formatter = HtmlFormatter(
        full=True,
        encoding="utf-8",
        outencoding="utf-8",
        linenos="inline",
        linenostart=1,
        linenostep=1,
        lineanchors="line",
        anchorlinenos=True,
        lineseparator="<br>",
        style=args.style,
    )

    style_css = formatter.get_style_defs("body")

    formatter.full = False

    if not args.quiet:
        start = time.time()

    # Main loop over the input files
    for filename in args.filenames:

        with open(filename, "r") as f:
            text = f.read()

        _, filename = split(filename)

        if not args.quiet:
            print(f"Processing {filename:s}... ", end="")

        out = process_blocks(get_blocks(text, lexer), lexer, formatter)
        out = DOCUMENT_TEMPLATE.format(filename, style_css, out)

        outfile_path = join(args.outdir, f"{filename:s}.html")
        with open(outfile_path, "w") as output_file:
            output_file.write(out)

        if not args.quiet:
            print("Done.")

    if not args.quiet:
        stop = time.time()

        total = stop - start

        print("")
        print("All done!")
        print("")

        tmsg = f"Processed {len(args.filenames):d} files in {total:f} seconds"
        print("-" * len(tmsg))
        print(tmsg)


if __name__ == "__main__":
    main()
else:
    print_error("elucipy is not meant to be imported!")
