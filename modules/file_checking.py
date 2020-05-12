"""Check if a file should be processed, retrieve its title and description"""

from re import sub, DOTALL, MULTILINE
from re import compile as compile_re


def check_file(content, filename):
    """Check if a file should be processed with elucipy"""

    elucipy_regex = compile_re("# elucipy{([^\n]*)}{(.*)}", DOTALL)

    match = elucipy_regex.search(content)

    if match is None:
        return False, None, None, None

    if match.group(1) == '':
        title = filename
    else:
        title = match.group(1)

    content = sub(elucipy_regex, "", content)

    intro = sub(r"^\s*# ", "", match.group(2), flags=MULTILINE)
    if "NOTE" in intro:
        intro = intro.replace("NOTE", '<span class="note">NOTE</span>')
    if "TODO" in intro:
        intro = intro.replace("TODO", '<span class="todo">TODO</span>')
    if "BUG" in intro:
        intro = intro.replace("BUG", '<span class="bug">BUG</span>')

    return True, content, title, intro
