from re import sub, MULTILINE, DOTALL
from re import compile as compile_re

from modules.print_utils import pERROR


class Parser:

    def __init__(self, language):

        if language == "python":

            tmp = r"# elucipy{([^\n]*)}{(.*)}"
            self.elucipy_regex = compile_re(tmp, DOTALL)

            self.intro_c = r"^\s*# "

            tmp = r"(^[ \t\f\v]*# .*\n)+\n*"
            self.explanation_regex = compile_re(tmp, MULTILINE)

            tmp = r"((^[ \t\f\v]*)#{2,}\n)\2# (.*\n)\1\n*"
            self.header_regex = compile_re(tmp, MULTILINE)

            self.code_regexes = []
            tmp = r"(^[ \t\f\v]*[^# \t\f\v\n].*\n)+\n*"
            self.code_regexes.append(compile_re(tmp, MULTILINE))
            # triple_quote_regex = compile_re(r"\"\"\".*\"\"\"", DOTALL)
            # double_quote_regex = compile_re(r"\".*\"")
            # single_quote_regex = compile_re(r"\'.*\'")

        elif language == "fortran":

            tmp = r"! elucipy{([^\n]*)}{(.*)}"
            self.elucipy_regex = compile_re(tmp, DOTALL)

            self.intro_c = r"^\s*! "

            tmp = r"(^[ \t\f\v]*! .*\n)+\n*"
            self.explanation_regex = compile_re(tmp, MULTILINE)

            tmp = r"((^[ \t\f\v]*)!{2,}\n)\2! (.*\n)\1\n*"
            self.header_regex = compile_re(tmp, MULTILINE)

            self.code_regexes = []
            tmp = r"(^[ \t\f\v]*[^! \t\f\v\n].*\n)+\n*"
            self.code_regexes.append(compile_re(tmp, MULTILINE))

    def check_file(self, content, filename):

        match = self.elucipy_regex.search(content)

        if match is None:
            return False, None, None, None

        if match.group(1) == "":
            title = filename
        else:
            title = match.group(1)

        content = sub(self.elucipy_regex, "", content)

        intro = sub(self.intro_c, "", match.group(2), flags=MULTILINE)
        if "NOTE" in intro:
            intro = intro.replace("NOTE", '<span class="note">NOTE</span>')
        if "TODO" in intro:
            intro = intro.replace("TODO", '<span class="todo">TODO</span>')
        if "BUG" in intro:
            intro = intro.replace("BUG", '<span class="bug">BUG</span>')

        return True, content, title, intro

    def consume_block(self, text, pos):

        m = self.header_regex.match(text, pos)
        if m:
            return "header", m[3], m.end(0), m[0].count("\n")

        m = self.explanation_regex.match(text, pos)
        if m:
            text = sub(r"^[ \t\f\v]*# ", "", m[0], flags=MULTILINE)
            return "explanation", text, m.end(0), m[0].count("\n")

        for regex in self.code_regexes:
            m = regex.match(text, pos)
            if m:
                return "code", m[0], m.end(0), m[0].count("\n")

        pERROR("Cannot identify block!")

    def merge_blocks(self, blocks):

        merged = []

        for b in blocks:

            t, v, ln = b

            if t == "header":
                if len(merged) == 0:
                    merged.append((t, v, ln))
                elif merged[-1][0] == "header":
                    pERROR("there appear to be consecutive"
                           " headers in this file.")
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

    def get_blocks(self, content):

        blocks = []

        pos = 0
        while pos < len(content):

            t, v, p, ln = self.consume_block(content, pos)

            blocks.append((t, v, ln))

            pos = p

        return self.merge_blocks(blocks)
