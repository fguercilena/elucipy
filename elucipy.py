from html_template import DOCUMENT_TEMPLATE, ROW_TEMPLATE_RIGHT, ROW_TEMPLATE_LEFT
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CppLexer
from pygments.styles import get_all_styles
from pygments.token import Comment, Text
import argparse
import itertools
import os.path
import re
import sys
import time


EPILOG = """Federico Maria Guercilena
(guercilena.federico@gmail.com, 2026)"""
DESCRIPTION = """Generate an .html document showing the source code of the
input files, with a parallel explanation running along it,
generated from the comments in the code."""


# Function to be passed to itertools.groupby to separate single line comments,
# multi line comments and everything else
def token_classifier(token):
    if token[1] is Comment.Single:
        return 1
    if token[1] is Comment.Multiline:
        return 2
    return 0


# Process a bunch of code (as a single string) and dive it up in blocks of code
# and blocks of comments
def get_blocks(code, lexer):

    # Get the tokens using Pygments's lexer
    tokens = list(lexer.get_tokens_unprocessed(code))

    # Transform tuples into lists so they can be modified
    for i in range(len(tokens)):
        tokens[i] = list(tokens[i])

    # Single line comments are sometimes interlaced with whitespace, that the
    # lexer does not flag as comments. If that happens, force them to be seen as
    # comments, so that on output we get a comment block (instead of a bunch of
    # individual lines of alternating comments and whitespace)
    # TODO: is there a more elegant solution?
    for i, token in enumerate(tokens):
        if token[1] is Text.Whitespace:
            if i > 0 and tokens[i - 1][1] is Comment.Single:
                if i < len(tokens) - 1 and tokens[i + 1][1] is Comment.Single:
                    token[1] = Comment.Single

    # Group tokens using groupby
    groups = [(t, list(v)) for t, v in itertools.groupby(tokens, token_classifier)]

    # Merge a group of adjacent tokens of a same type into a string (a 'block')
    blocks = []
    line_number = 1
    for t, group in groups:

        # TODO: These two do not seem to be needed
        start = group[0][0]
        end = group[-1][0] + len(group[-1][2])

        content = ""
        count_linebreaks = 0
        for _, _, token in group:

            count_linebreaks += token.count("\n")

            # Remove comment markers from comment lines. These line are specific
            # to C++
            # TODO: Remove them
            if t == 1:
                token = re.sub(r"//", "", token, count=1).lstrip()
            elif t == 2:
                token = re.sub(r"/\*|\*|\*/", "", token, count=1).lstrip()

            content += token

        blocks.append((start, end, line_number, content))

        # TODO: the line numbers are necessary because later they get passed to
        # the formatter to show them ion the HTML output. However the present
        # calculation seem to lead wrong numbers in some instances
        line_number += count_linebreaks

    # If the first block is a code one, prepend an empty comment block to
    # everything. This simplifies the logic later.
    if groups[0][0] == 0:
        blocks = [(0, 0, 0, "")] + blocks

    return blocks


# Format the code blocks and put them into an HTM table
def process_blocks(blocks, lexer, formatter):

    out = ""

    # Process blocks in pairs, essentially assuming they always come interlaced:
    # first a comment block, then a code one, and so on
    for tmp in itertools.batched(blocks, 2):

        # Extract the strings and line numbers, handling the case in which there
        # is an odd number of blocks
        if len(tmp) == 2:
            explanation, code = tmp

            _, _, line_number, code = code
            formatter.linenostart = line_number
            code = highlight(code, lexer, formatter).decode("utf-8")
        else:
            explanation = tmp[0]

        _, _, line_number, explanation = explanation

        # Put the text into the HTML table template
        out += ROW_TEMPLATE_RIGHT.format(code, explanation)

    return out


def main():

    # Parse command line arguments
    cl_parsr = argparse.ArgumentParser(
        add_help=True,
        epilog=EPILOG,
        description=DESCRIPTION,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    cl_parsr.add_argument("filenames", nargs="+", help="input file(s) path")
    # cl_parsr.add_argument("-l", "--language", default=None, dest="lang",
    #   choices=list(LANGUAGES),
    #   help="programming language of the input files")
    cl_parsr.add_argument(
        "-s",
        "--style",
        default="nord-darker",
        dest="style",
        choices=list(get_all_styles()),
        help="syntax highlight style",
    )
    # TODO: this option is ingored at the moment
    cl_parsr.add_argument(
        "--ignore-linebreaks",
        default=False,
        action="store_true",
        dest="ignore_lb",
        help="ignore linebreaks in explanations",
    )
    # TODO: this option is ingored at the moment
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

    # TODO: let Pygment guess the correct lexer
    lexer = CppLexer(stripnl=True, stripall=False, ensurenl=True, tabsize=4)

    # Get the HTML formatter from Pygments
    formatter = HtmlFormatter(
        full=False,
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

    # Get the CSS definitions from Pygments (the 'full' option )
    style_css = formatter.get_style_defs("body")

    if not args.quiet:
        start = time.time()

    # Main loop over the input files
    for filename in args.filenames:

        # Read the file
        with open(filename, "r") as f:
            text = f.read()

        _, filename = os.path.split(filename)

        if not args.quiet:
            print(f"Processing {filename:s}... ", end="")

        # Process the content
        out = process_blocks(get_blocks(text, lexer), lexer, formatter)
        out = DOCUMENT_TEMPLATE.format(filename, style_css, out)

        # Write the output HTML file
        outfile_path = os.path.join(args.outdir, f"{filename:s}.html")
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
